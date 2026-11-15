#!/usr/bin/env python3
"""Run pytest and materialize one evidence-rich, immutable (per run) report."""
from __future__ import annotations
import argparse,datetime,html,json,os,re,shutil,subprocess,sys,uuid,xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from core import ROOT,HERE,CASES,db_config,Blocked,connect_readonly,dbt_executable,load_connection_env
import sql_checks,bi_queries,test_31_mage,test_32_dbt,test_34_powerbi,test_31_scenarios,test_33_negative
import test_31_cleaners,test_35_ai

BASE=ROOT/'test'/'results'

def cli_version(cmd):
    if not shutil.which(cmd[0]):return 'Không có trên PATH'
    try:
        cp=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=7)
        return cp.stdout.strip().splitlines()[0][:120] if cp.returncode==0 and cp.stdout.strip() else 'Không xác định'
    except Exception:return 'Không xác định'

def gitmeta():
    try:
        def g(*args):return subprocess.run(['git','-C',str(ROOT),*args],text=True,capture_output=True,timeout=5)
        branch=g('branch','--show-current');commit=g('rev-parse','HEAD');dirty=g('status','--porcelain')
        return {'branch':branch.stdout.strip() if branch.returncode==0 else None,
          'commit':commit.stdout.strip() if commit.returncode==0 else None,
          'dirty':bool(dirty.stdout.strip()) if dirty.returncode==0 else None}
    except Exception:return {'branch':None,'commit':None,'dirty':None}

def data_source_meta():
    result={}
    import csv
    for name in ['tmdb_5000_movies.csv','tmdb_5000_credits.csv','tmdb_new_batch.csv']:
        p=ROOT/'data'/'raw'/name
        if p.is_file():
            with p.open(encoding='utf-8-sig',newline='') as f:
                result[name]={'rows':max(sum(1 for _ in csv.reader(f))-1,0),'mtime':datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()}
        else:result[name]={'available':False}
    return result

def db_snapshot_meta(testenv):
    """Read-only snapshot metadata, never infer append merely from an old baseline."""
    state={}
    old=dict(os.environ)
    try:
        os.environ.update({k:v for k,v in testenv.items() if k.startswith('TMDB_') or k=='POSTGRES_PASSWORD'})
        try:conn=connect_readonly()
        except Blocked as e:return {'status':'BLOCKED','reason':str(e)}
        try:
            state['database']=conn.execute('SELECT current_database()').fetchone()[0]
            state['postgres_version']=conn.execute('SHOW server_version').fetchone()[0]
            state['server_timestamp_utc']=str(conn.execute("SELECT now() AT TIME ZONE 'UTC'").fetchone()[0])
            state['snapshot_id']=str(conn.execute('SELECT txid_current_snapshot()').fetchone()[0])
            for key,table,pk in [('stage_movies','stage.stg_tmdb_movies','id'),
                                 ('stage_credits','stage.stg_tmdb_credits','movie_id'),
                                 ('fact','dds.fact_movie','movie_sk')]:
                if conn.execute('SELECT to_regclass(%s)',(table,)).fetchone()[0]:
                    state[key]={'rows':conn.execute(f'SELECT count(*) FROM {table}').fetchone()[0]}
                    state[key]['duplicate_keys']=conn.execute(f'SELECT count(*) FROM (SELECT {pk} FROM {table} GROUP BY {pk} HAVING count(*)>1) q').fetchone()[0]
                else:state[key]={'status':'MISSING'}
            if conn.execute("SELECT to_regclass('control.etl_watermark')").fetchone()[0]:
                row=conn.execute("SELECT lset::text FROM control.etl_watermark WHERE pipeline_name='tmdb_incremental'").fetchone()
                state['watermark_lset']=row[0] if row else None
            state['incremental_already_appended']='Không thể xác định chắc chắn nếu không có before/after snapshot Mage của cùng database'
            state['status']='READ_ONLY_SNAPSHOT'
            return state
        finally:conn.close()
    except Exception as e:
        return {'status':'BLOCKED','reason':f'Không đọc được snapshot metadata ({type(e).__name__})'}
    finally:
        os.environ.clear();os.environ.update(old)

def redactor():
    secrets=[os.environ.get(k,'') for k in ('TMDB_DB_PASSWORD','TMDB_TEST_DB_PASSWORD','POSTGRES_PASSWORD')]
    def clean(txt):
        for s in secrets:
            if s:txt=txt.replace(s,'[REDACTED]')
        txt=re.sub(r'(?i)(password\s*[:=]\s*)([^\s,;]+)',r'\1[REDACTED]',txt)
        return txt
    return clean

def read_junit(path,clean):
    if not path.exists():return []
    tree=ET.parse(path);out=[]
    for el in tree.iter('testcase'):
        name=el.get('name','');m=re.search(r'\[([A-Z]{1,3}\d{2})\]',name)
        id=m.group(1) if m else name
        bracket=re.search(r'\[([^\]]+)\]$',name)
        if bracket and bracket.group(1) in CASES:id=bracket.group(1)
        prop={x.get('name'):x.get('value') for x in el.findall('./properties/property')}
        failure=el.find('failure');error=el.find('error');skipped=el.find('skipped')
        msg=''
        if failure is not None or error is not None:
            obj=failure if failure is not None else error
            status='FAIL';msg=clean((obj.get('message') or obj.text or '')[:1400])
        elif skipped is not None:
            msg=clean((skipped.get('message') or skipped.text or '')[:1400]);status='BLOCKED' if 'BLOCKED:' in msg else 'SKIPPED'
        else: status='INFO' if CASES.get(id,{}).get('observation') else 'PASS'
        try:actual=json.loads(prop.get('actual','null'))
        except ValueError:actual=prop.get('actual')
        out.append({'id':id,'name':name,'status':status,'actual':actual,'message':msg,
          'note':clean(prop.get('note','')),'evidence':prop.get('evidence')})
    return out

def render_markdown(report):
    rows=report['checks'];count=report['counts']
    out=['# TMDB — Acceptance test report', '',
         f"- Run ID: `{report['run_id']}`",f"- UTC: `{report['timestamp_utc']}`",
         f"- Mode: **{report['mode']}**; Section: **{report['section']}**",
         f"- Branch/commit: `{report['git']['branch'] or 'n/a'}` / `{report['git']['commit'] or 'n/a'}`; dirty={report['git']['dirty']}",
         f"- **PASS {count.get('PASS',0)} / FAIL {count.get('FAIL',0)} / BLOCKED {count.get('BLOCKED',0)} / SKIPPED {count.get('SKIPPED',0)} / INFO {count.get('INFO',0)}**",'',
         'INFO là số liệu quan sát hoặc SQL tham chiếu; không tính là nghiệm thu đạt.', '',
         '## Bảng toàn bộ test (requirement → evidence → kết luận)','',
         '| Test ID | Mục | Loại | Tên | Kết quả | Bằng chứng |', '|---|---|---|---|---|---|']
    for r in rows:
        def esc(s):return str(s or '').replace('|','\\|').replace('\n',' ')
        out.append(f"| {r['id']} | {esc(r['section'])} | {esc(r['category'])} | {esc(r['name'])} | **{r['status']}** | `{r['evidence_path']}` |")
    out+=['','## Chi tiết FAIL/BLOCKED và test được chọn cho demo','']
    labels=[('id','1. Test ID'),('section','2. Mục'),('category','3. Phân loại'),('purpose','4. Mục đích'),('input','5. Đầu vào'),('steps','6. Các bước'),('expected','7. Expected'),('actual','8. Actual'),('status','9. Trạng thái'),('explanation','10. Nguyên nhân kết quả'),('impact','11. Ý nghĩa'),('evidence_path','12. Bằng chứng và loại'),('reproduce','13. Tái hiện'),('remediation','14. Hướng xử lý')]
    for r in rows:
        if r['status'] not in ('FAIL','BLOCKED') and not r.get('demo'):continue
        out+=['',f"### {r['id']} — {r['name']}"]
        for key,label in labels:
            val=r.get(key,'')
            if isinstance(val,(list,dict)):val=json.dumps(val,ensure_ascii=False,default=str)
            out.append(f'- **{label}:** {val}')
    out+=['','## Giới hạn','',
          '- Kết quả tĩnh chỉ chứng minh nội dung các file trong repository; không chứng minh runtime đã chạy.',
          '- Các hiện tượng Power BI chưa truy vấn được DAX expression / refresh trực tiếp được ghi BLOCKED.',
          '- Kết quả từ `dbt_transform/target/` là artifacts cũ, không phải lần build mới.',
          '- Đây không phải kết luận tổng thể thành công khi còn BLOCKED.',
          '- Mục 3.5 là yêu cầu của đề nhưng chưa triển khai; AI01–AI04 luôn BLOCKED cho tới khi có implementation và adapter kiểm thử.',
          '- Unit test cleaner không thay thế thực thi Mage; SQL reference INFO không chứng minh DAX đúng.', '',
          '## Môi trường và snapshot (không chứa credentials)','',
          '```json',json.dumps({'versions':report['versions'],'sources':report['sources'],'target':report['db_target'],'db_snapshot':report.get('db_snapshot')},ensure_ascii=False,indent=2),'```','']
    return '\n'.join(out)

def main(argv=None):
    ap=argparse.ArgumentParser(description='TMDB acceptance test: pytest + JSON/MD evidence')
    ap.add_argument('--section',default='all',choices=('all','31','32','33','34','35'))
    ap.add_argument('--mode',default='readonly',choices=('readonly','integration'))
    ap.add_argument('--approved',action='store_true',help='Chỉ với DB isolated ở localhost:55432')
    ap.add_argument('--snapshot',choices=('unknown','full'),default='unknown',help='full: bạn xác nhận stage là Full Load, chưa append batch')
    ap.add_argument('--env-file',type=Path,help='Đọc cấu hình readonly từ .env được chỉ định; không in mật khẩu')
    args=ap.parse_args(argv)
    if args.env_file:
        if not args.env_file.is_file():ap.error('Không tìm thấy --env-file')
        load_connection_env(args.env_file)
    if args.mode=='integration' and not args.approved:
        print('BLOCKED: integration cần --approved và DB cô lập, không dùng database chính',file=sys.stderr);return 2
    runid=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid.uuid4().hex[:6]
    run=BASE/('acceptance_'+runid);run.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy();env['TMDB_TEST_MODE']=args.mode
    env['TMDB_TEST_EVIDENCE_DIR']=str(run)
    env['TMDB_STAGE_SNAPSHOT']=args.snapshot
    if args.mode=='integration':
        env['TMDB_TEST_APPROVED']='I_UNDERSTAND_ISOLATED_WRITES'
        # Load password only from generated runtime env; never echo it.
        pwfile=HERE/'.runtime'/'isolated.json'
        if not pwfile.exists():
            print('BLOCKED: chạy `python test/acceptance/isolation.py prepare` trước',file=sys.stderr)
            return 2
        data=json.loads(pwfile.read_text(encoding='utf8'))
        env['TMDB_TEST_DB_PASSWORD']=data['password'];env['TMDB_TEST_DB_USER']='tmdb_test_user'
        env['TMDB_TEST_DB_PORT']='55432';env['TMDB_TEST_DB_NAME']='tmdb_test_warehouse';env['TMDB_TEST_DB_HOST']='127.0.0.1'
        # Freeze only evidence, never profiles/isolated.json (they contain secrets).
        evidence=run/'runtime_evidence';evidence.mkdir()
        runtime=HERE/'.runtime'
        paths=[runtime/name for name in ('dbt_build_provenance.json','dbt_build_run_results.json','dbt_rebuild_comparison.json')]
        paths += [runtime/'dbt_target'/name for name in ('manifest.json','catalog.json','index.html')]
        paths += list((runtime/'scenarios').glob('*.json'))+list((runtime/'scenarios').glob('*_mage.log'))
        for source in paths:
            if source.is_file():
                destination=evidence/source.relative_to(runtime)
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(source,destination)
        env['TMDB_RUNTIME_EVIDENCE_DIR']=str(evidence)
    selected=[str(x) for x in sorted(HERE.glob(f'test_{args.section}_*.py' if args.section!='all' else 'test_*.py'))]
    cmd=[sys.executable,'-m','pytest','-c',str(HERE/'pytest.ini'),*selected,'--junitxml',str(run/'junit.xml'),'-q']
    proc=subprocess.run(cmd,cwd=HERE,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    clean_base=redactor()
    secret=env.get('TMDB_TEST_DB_PASSWORD','')
    def clean(value):
        value=clean_base(value)
        return value.replace(secret,'[REDACTED]') if secret else value
    stdout=clean(proc.stdout)
    if (run/'junit.xml').exists():
        xmlpath=run/'junit.xml'
        xmlpath.write_text(clean(xmlpath.read_text(encoding='utf8')),encoding='utf8')
    if args.mode=='integration':
        isolated=json.loads((HERE/'.runtime'/'isolated.json').read_text())['password']
        stdout=stdout.replace(isolated,'[REDACTED]')
    (run/'pytest_output.txt').write_text(stdout,encoding='utf8')
    result=read_junit(run/'junit.xml',clean)
    results=[]
    for row in result:
        src=CASES.get(row['id'],{})
        data={**src,**row}
        data.setdefault('section','?');data.setdefault('category','?')
        data.setdefault('purpose',data.get('name','Unknown'))
        data.setdefault('input','Không xác định');data.setdefault('steps','Mở pytest output')
        data.setdefault('expected','Không xác định');data.setdefault('remediation','Đọc pytest_output.txt để xem lỗi')
        data['evidence_kind']=src.get('evidence_kind','Kết quả chạy mới')
        data['evidence_path']='junit.xml; pytest_output.txt' + (('; '+str(row['evidence'])) if row.get('evidence') else '') + (f" ({data['evidence_kind']})" if data['status']=='PASS' else '')
        data['reproduce']=f".\\test\\run_acceptance.ps1 -Section {args.section} -Mode {args.mode}"+(' -IsolatedConfirmed' if args.mode=='integration' else '')
        data['explanation']= data.get('note') or data.get('message') or ('Assertion đạt trên dữ liệu/mã hiện tại.' if data['status']=='PASS' else 'Chưa có dữ liệu để xác định nguyên nhân.')
        if data['status']=='FAIL' and not data.get('note'):
            data['explanation']='Đã quan sát vi phạm; '+(data.get('message','') or 'cần điều tra nguyên nhân')
        if data['status']=='BLOCKED':data['explanation']='Thiếu điều kiện kiểm chứng; '+data.get('message','')
        data['impact']=f"Chỉ xác nhận phạm vi {data['section']} của test này; không suy rộng sang toàn project."
        results.append(data)
    counts=dict(Counter(r['status'] for r in results))
    if proc.returncode and not counts.get('FAIL') and proc.returncode not in (0,):
        # pytest collection/runtime error - not a clean pass
        counts['FAIL']=counts.get('FAIL',0)+1
        results.append({'id':'RUN_ERR','name':'pytest collection/runtime failure','section':'Runner','category':'Kiểm tra độ bền',
          'purpose':'pytest phải khởi tạo thành công','input':'repo','steps':'python -m pytest','expected':'Exit code 0/1/5 theo test cases','actual':None,
          'status':'FAIL','evidence_kind':'Kết quả chạy mới','evidence_path':'pytest_output.txt','explanation':f'pytest exit={proc.returncode}, xem file output',
          'impact':'Không thể chứng thực đủ bộ test','reproduce':sys.executable+' -m pytest', 'remediation':'Kiểm tra dependencies và import path','demo':False})
    def target():
        try:
            cfg={k:v for k,v in db_config().items() if k!='password'}
            if args.mode=='integration': return {'host':'127.0.0.1','port':55432,'dbname':'tmdb_test_warehouse','user':'tmdb_test_user'}
            return cfg
        except (Blocked,ValueError):return 'Không xác định'
    report={'run_id':runid,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'mode':args.mode,'section':args.section,'git':gitmeta(),'counts':counts,'checks':results,
      'sources':data_source_meta(),'db_target':target(),'db_snapshot':db_snapshot_meta(env),
      'versions':{'python':sys.version.split()[0],'pytest':cli_version([sys.executable,'-m','pytest','--version']),
       'dbt':cli_version([dbt_executable() or 'dbt','--version']),'docker':cli_version(['docker','--version']),
       'compose':cli_version(['docker','compose','version']),'mage':cli_version(['mage','--version']),
       'powerbi_desktop':'Không thể kiểm tra từ môi trường CLI này'},
      'limitations':['Không có kết nối Desktop semantic model trong CLI; DAX/Refresh cần kiểm tra thủ công.',
       'Không sử dụng logs/artifacts cũ làm bằng chứng chạy mới.']}
    (run/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf8')
    (run/'REPORT.md').write_text(render_markdown(report),encoding='utf8')
    exitcode=1 if counts.get('FAIL',0) else 2 if (counts.get('BLOCKED',0) or counts.get('SKIPPED',0)) else 0
    print(f"Run: {run.relative_to(ROOT)}")
    print(' | '.join(f'{k}={counts.get(k,0)}' for k in ('PASS','FAIL','BLOCKED','SKIPPED','INFO')))
    print('Exit code',exitcode)
    return exitcode

if __name__=='__main__':raise SystemExit(main())
