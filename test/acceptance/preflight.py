"""Read-only readiness checks. Never starts containers, loads data or builds DDS."""
import argparse, importlib.util, json, os, subprocess, sys
from pathlib import Path
from core import ROOT, HERE, Blocked, connect_readonly, dbt_executable,load_connection_env


def check(mode):
    checks=[]
    def add(name,ready,detail):
        checks.append({'check':name,'status':'READY' if ready else 'BLOCKED','detail':detail})
    for module in ('pytest','psycopg','yaml','pandas'):
        add(module,importlib.util.find_spec(module) is not None,'Python: '+sys.executable)
    add('dbt',bool(dbt_executable()),'Cài dbt-core/dbt-postgres trong cùng môi trường Python')
    for name in ('tmdb_5000_movies.csv','tmdb_5000_credits.csv','tmdb_new_batch.csv'):
        p=ROOT/'data/raw'/name
        add(name,p.is_file() and p.stat().st_size>0,'data/raw/'+name)
    try:
        proc=subprocess.run(['docker','info','--format','{{.ServerVersion}}'],capture_output=True,text=True,timeout=15)
        add('Docker Engine',proc.returncode==0,'Mở Docker Desktop; quyền truy cập Docker Engine cần hoạt động')
    except (OSError,subprocess.TimeoutExpired):
        add('Docker Engine',False,'Không gọi được Docker CLI/Engine hoặc quá 15 giây')
    saved=dict(os.environ)
    try:
        os.environ['TMDB_TEST_MODE']=mode
        if mode=='integration':
            meta=HERE/'.runtime/isolated.json'
            if not meta.is_file():raise Blocked('Chạy isolation.py prepare rồi up')
            cfg=json.loads(meta.read_text(encoding='utf8'))
            if cfg.get('project')!='tmdb_test_acceptance':raise Blocked('Sai runtime project')
            os.environ.update(TMDB_TEST_APPROVED='I_UNDERSTAND_ISOLATED_WRITES',
                TMDB_TEST_DB_PASSWORD=cfg['password'],TMDB_TEST_DB_HOST='127.0.0.1',
                TMDB_TEST_DB_PORT='55432',TMDB_TEST_DB_NAME='tmdb_test_warehouse',TMDB_TEST_DB_USER='tmdb_test_user')
        conn=connect_readonly()
        try:
            add('PostgreSQL',True,'Kết nối SELECT-only thành công')
            for relation in ('stage.stg_tmdb_movies','stage.stg_tmdb_credits','control.etl_watermark','dds.fact_movie'):
                exists=conn.execute('SELECT to_regclass(%s)',(relation,)).fetchone()[0] is not None
                count=conn.execute(f'SELECT count(*) FROM {relation}').fetchone()[0] if exists else 0
                add(relation,exists and count>0,f'rows={count}; chạy Mage Full Load trước dbt build' if not count else f'rows={count}')
        finally:conn.close()
    except (Blocked,ValueError,KeyError,OSError) as e:
        add('PostgreSQL',False,str(e) if isinstance(e,Blocked) else type(e).__name__)
    except Exception as e:
        add('PostgreSQL',False,'Không đọc được schema/data ('+type(e).__name__+')')
    finally:
        os.environ.clear();os.environ.update(saved)
    add('PBIX',(ROOT/'powerbi_dashboard/TMDB_Movie_Dashboard.pbix').is_file(),'Power BI Desktop chỉ cần cho DAX/refresh/tương tác')
    return checks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('readonly','integration'),default='readonly')
    parser.add_argument('--env-file',type=Path)
    args=parser.parse_args()
    if args.env_file:
        if not args.env_file.is_file():parser.error('Không tìm thấy --env-file')
        load_connection_env(args.env_file)
    checks=check(args.mode)
    for item in checks:print(f"{item['status']:7} | {item['check']} | {item['detail']}")
    print('READY chỉ xác nhận điều kiện chạy, không phải kết quả acceptance PASS.')
    return 2 if any(x['status']=='BLOCKED' for x in checks) else 0

if __name__=='__main__':raise SystemExit(main())
