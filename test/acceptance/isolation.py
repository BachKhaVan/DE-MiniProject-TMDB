#!/usr/bin/env python3
"""Prepare/launch isolated Mage/Postgres using ONLY newly generated files."""
import argparse,json,os,secrets,shutil,subprocess,sys,stat,hashlib,datetime
from pathlib import Path
from core import ROOT,HERE,db_config,connect_readonly,Blocked,dbt_source_fingerprint,dbt_executable

R=HERE/'.runtime'; META=R/'isolated.json'; COMPOSE=HERE/'compose.isolated.yaml'

def need_config():
    if not META.is_file():raise Blocked('Chưa tạo môi trường: python test/acceptance/isolation.py prepare')
    data=json.loads(META.read_text(encoding='utf8'))
    if data.get('project')!='tmdb_test_acceptance':raise Blocked('Không đúng project isolation')
    return data

def env():
    cfg=need_config();e=os.environ.copy();e['TMDB_TEST_PASSWORD']=cfg['password'];return e

def docker_args():
    return ['docker','compose','-p','tmdb_test_acceptance','-f',str(COMPOSE)]

def run_compose(*args):
    if shutil.which('docker') is None:raise Blocked('Docker CLI chưa có trên PATH')
    return subprocess.run([*docker_args(),*args],env=env()).returncode

def prepare():
    if META.exists():
        raise Blocked('Môi trường .runtime đã tồn tại: không ghi đè credentials; dùng up/down hoặc tự dọn đúng .runtime sau khi down')
    R.mkdir(exist_ok=True)
    ws=R/'workspace';(ws/'mage_data').mkdir(parents=True,exist_ok=True)
    # Actual Mage source copied unchanged, not replaced by mock pipeline.
    src=ROOT/'mage_pipeline';dst=ws/'mage_pipeline'
    if not src.is_dir():raise Blocked('Thiếu mage_pipeline')
    shutil.copytree(src,dst,ignore=shutil.ignore_patterns('io_config.yaml','.ssh_tunnel','.cache','*.db','__pycache__'))
    data_src=ROOT/'data'/'raw'; data_dst=ws/'data'/'raw';data_dst.mkdir(parents=True,exist_ok=True)
    required=['tmdb_5000_movies.csv','tmdb_5000_credits.csv','tmdb_new_batch.csv']
    copied=[]
    alternate=dst/'data'/'raw'
    alternate.mkdir(parents=True,exist_ok=True)
    for name in required:
        if (data_src/name).exists():
            shutil.copy2(data_src/name,data_dst/name)
            # Mage may resolve relative paths from /home/src or USER_CODE_PATH.
            shutil.copy2(data_src/name,alternate/name)
            copied.append(name)
    password=secrets.token_urlsafe(30)
    cfg={'project':'tmdb_test_acceptance','password':password,'copied_csv':copied,
         'database':'tmdb_test_warehouse','user':'tmdb_test_user','port':55432}
    META.write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf8')
    try:os.chmod(META,stat.S_IRUSR|stat.S_IWUSR)
    except OSError:pass
    # Runtime shadow config: same Mage blocks, different Postgres profile and ports.
    io_config=f'''version: 0.1.1\ndefault:\n  POSTGRES_CONNECT_TIMEOUT: 10\n  POSTGRES_DBNAME: tmdb_test_warehouse\n  POSTGRES_SCHEMA: stage\n  POSTGRES_USER: tmdb_test_user\n  POSTGRES_PASSWORD: {password}\n  POSTGRES_HOST: postgres\n  POSTGRES_PORT: 5432\n'''
    (dst/'io_config.yaml').write_text(io_config,encoding='utf8')
    # dbt CLI runs from host, PostgreSQL published on isolated port.
    pd=R/'dbt_profiles';pd.mkdir(exist_ok=True)
    prof=f'''tmdb_transform:\n  target: isolated\n  outputs:\n    isolated:\n      type: postgres\n      host: 127.0.0.1\n      port: 55432\n      dbname: tmdb_test_warehouse\n      user: tmdb_test_user\n      password: {password}\n      schema: dds\n      threads: 2\n'''
    (pd/'profiles.yml').write_text(prof,encoding='utf8')
    for p in (dst/'io_config.yaml',pd/'profiles.yml'):
        try:os.chmod(p,stat.S_IRUSR|stat.S_IWUSR)
        except OSError:pass
    print('Đã tạo workspace Mage độc lập (đúng block source), DB riêng: tmdb_test_warehouse, port 55432, Mage UI 16789')
    print('CSV tìm thấy:',', '.join(copied) or 'không có; cần thêm 2 CSV vào data/raw rồi tạo lại môi trường')
    print('KHÔNG in hay ghi mật khẩu vào log; .runtime bị loại khỏi Git qua .gitignore')

def dbt_build():
    need_config()
    executable=dbt_executable()
    if executable is None:raise Blocked('dbt Core chưa có trong Python hiện tại hoặc PATH')
    # Invalidate previous successful evidence BEFORE attempting a new build.
    for filename in ('dbt_build_provenance.json','dbt_build_run_results.json','dbt_rebuild_comparison.json'):
        (R/filename).unlink(missing_ok=True)
    # Safe guard from accidentally building on demo warehouse.
    envloc=os.environ.copy()
    envloc.update({'TMDB_TEST_MODE':'integration','TMDB_TEST_APPROVED':'I_UNDERSTAND_ISOLATED_WRITES',
                   'TMDB_TEST_DB_PASSWORD':need_config()['password'],
                   'TMDB_TEST_DB_NAME':'tmdb_test_warehouse','TMDB_TEST_DB_PORT':'55432',
                   'TMDB_TEST_DB_HOST':'127.0.0.1','TMDB_TEST_DB_USER':'tmdb_test_user'})
    # Verify with live connection BEFORE constructing any dbt CLI call.
    saved=dict(os.environ)
    try:
        os.environ.update({k:v for k,v in envloc.items() if k.startswith('TMDB_TEST_')})
        con=connect_readonly();con.close()
    finally:
        os.environ.clear();os.environ.update(saved)
    target=R/'dbt_target';logs=R/'dbt_logs'
    target.mkdir(exist_ok=True);logs.mkdir(exist_ok=True)
    envloc.update({'DBT_PROFILES_DIR':str(R/'dbt_profiles'),'DBT_TARGET_PATH':str(target),'DBT_LOG_PATH':str(logs)})
    # Never pass a password as a CLI flag; suppress raw output that may contain credentials.
    def capture():
        saved_env=dict(os.environ)
        try:
            os.environ.update({k:v for k,v in envloc.items() if k.startswith('TMDB_TEST_')})
            con=connect_readonly()
            try:
                from sql_checks import TABLES
                result={}
                for table in TABLES:
                    digest=hashlib.sha256();count=0
                    for row in con.execute(f'SELECT row_to_json(t)::text FROM dds.{table} t ORDER BY row_to_json(t)::text'):
                        digest.update(row[0].encode('utf8'));digest.update(b'\n');count+=1
                    result[table]={'rows':count,'sha256':digest.hexdigest()}
                from scenario import snapshot
                return {'dds':result,'source':snapshot(con)}
            finally:con.close()
        finally:os.environ.clear();os.environ.update(saved_env)
    first=None
    for label in ('build','rebuild','docs'):
        action='build' if label=='rebuild' else label
        cmd=[executable,action,*(['generate'] if action=='docs' else []),'--project-dir',str(ROOT/'dbt_transform'),'--profiles-dir',str(R/'dbt_profiles'),
             '--target','isolated','--target-path',str(target),'--log-path',str(logs)]
        p=subprocess.run(cmd,env=envloc,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        safe=p.stdout.replace(need_config()['password'],'[REDACTED]')
        (R/f'dbt_{label}.log').write_text(safe,encoding='utf8')
        print('dbt',label,'exit',p.returncode,'log trong .runtime; mật khẩu đã ẩn')
        if p.returncode:return p.returncode
        if label=='build':first=capture()
        if label=='rebuild' and (target/'run_results.json').exists():
            second=capture()
            comparison={'before':first,'after':second,'fingerprint':dbt_source_fingerprint()}
            (R/'dbt_rebuild_comparison.json').write_text(json.dumps(comparison,indent=2),encoding='utf8')
            shutil.copy2(target/'run_results.json',R/'dbt_build_run_results.json')
            provenance={'fingerprint':dbt_source_fingerprint(),
                        'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        'target':'tmdb_test_warehouse'}
            (R/'dbt_build_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf8')
    print('Đã chạy build/rebuild/docs trên database isolated; dbt build bao gồm seeds và tests')
    return 0

def failure_toggle(enable):
    # Strict guard; only run against dedicated isolated test database.
    data=need_config()
    from psycopg import sql
    saved=dict(os.environ)
    try:
        os.environ.update({'TMDB_TEST_MODE':'integration',
          'TMDB_TEST_APPROVED':'I_UNDERSTAND_ISOLATED_WRITES',
          'TMDB_TEST_DB_PASSWORD':data['password'],
          'TMDB_TEST_DB_NAME':'tmdb_test_warehouse',
          'TMDB_TEST_DB_PORT':'55432','TMDB_TEST_DB_HOST':'127.0.0.1',
          'TMDB_TEST_DB_USER':'tmdb_test_user'})
        cfg=db_config()
        import psycopg
        conn=psycopg.connect(**cfg,connect_timeout=5)
    except Exception:
        raise Blocked('Không kết nối được database isolated')
    finally:
        os.environ.clear();os.environ.update(saved)
    try:
        if conn.execute('select current_database()').fetchone()[0]!='tmdb_test_warehouse':
            raise Blocked('Không phải DB isolated')
        if enable:
            conn.execute('''CREATE OR REPLACE FUNCTION stage.tmdb_test_fail_insert()
                   RETURNS trigger LANGUAGE plpgsql AS $$
                   BEGIN RAISE EXCEPTION 'tmdb_test_injected_export_failure'; END;
                   $$''')
            conn.execute('''DROP TRIGGER IF EXISTS tmdb_test_fail_insert ON stage.stg_tmdb_movies''')
            conn.execute('''CREATE TRIGGER tmdb_test_fail_insert BEFORE INSERT
                ON stage.stg_tmdb_movies FOR EACH ROW
                EXECUTE FUNCTION stage.tmdb_test_fail_insert()''')
        else:
            conn.execute('''DROP TRIGGER IF EXISTS tmdb_test_fail_insert ON stage.stg_tmdb_movies''')
            conn.execute('''DROP FUNCTION IF EXISTS stage.tmdb_test_fail_insert()''')
        conn.commit()
        print('Bật injection trigger trên isolated' if enable else 'Đã bỏ trigger injection isolated')
    finally:conn.close()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['prepare','up','ps','down','dbt-build','failure-on','failure-off'])
    args=ap.parse_args()
    try:
        if args.action=='prepare':prepare();return 0
        if args.action=='dbt-build':return dbt_build()
        if args.action=='failure-on':failure_toggle(True);return 0
        if args.action=='failure-off':failure_toggle(False);return 0
        if args.action=='down':
            print('Chỉ down compose project tmdb_test_acceptance và volume tmdb_test_acceptance_pg_data')
            return run_compose('down','--volumes')
        return run_compose('up','-d','--wait','--wait-timeout','120') if args.action=='up' else run_compose(args.action)
    except Blocked as e:
        print('BLOCKED:',e,file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
