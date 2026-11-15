#!/usr/bin/env python3
"""Read-only before/after snapshots around MANUALLY triggered real Mage pipeline runs."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,sys
from core import HERE,connect_readonly,Blocked,db_config

CASES=('full_repeat','batch_new','batch_empty','batch_replay','batch_existing','batch_invalid','export_failure','partial_full')
RESULTS=HERE/'.runtime'/'scenarios'

def snapshot(con):
    snap={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    for t,key in [('stg_tmdb_movies','id'),('stg_tmdb_credits','movie_id')]:
        h=hashlib.sha256();n=0
        for row in con.execute(f'SELECT row_to_json(t)::text FROM stage.{t} t ORDER BY {key},row_to_json(t)::text'):
            h.update(row[0].encode('utf8'));h.update(b'\n');n+=1
        duplicates=con.execute(f'SELECT count(*) FROM (SELECT {key} FROM stage.{t} GROUP BY {key} HAVING count(*)>1) q').fetchone()[0]
        snap[t]={'rows':n,'sha256':h.hexdigest(),'duplicate_keys':duplicates}
    wm=con.execute("SELECT lset::text FROM control.etl_watermark WHERE pipeline_name='tmdb_incremental'").fetchone()
    snap['watermark']=wm[0] if wm else None
    return snap

def main():
    ap=argparse.ArgumentParser();ap.add_argument('case',choices=CASES);ap.add_argument('phase',choices=('before','after'))
    ap.add_argument('--mage-run-id',default='',help='Chính xác ID của run thực tế trong Mage, bắt buộc với after')
    args=ap.parse_args()
    if args.phase=='after' and not args.mage_run_id:
        print('BLOCKED: cần --mage-run-id lấy từ Mage UI, không phỏng đoán run',file=sys.stderr);return 2
    os.environ['TMDB_TEST_MODE']='integration'
    os.environ['TMDB_TEST_APPROVED']='I_UNDERSTAND_ISOLATED_WRITES'
    local=HERE/'.runtime'/'isolated.json'
    if not local.exists():print('BLOCKED: chưa chuẩn bị isolated',file=sys.stderr);return 2
    config=json.loads(local.read_text(encoding='utf8'))
    os.environ.update({'TMDB_TEST_DB_PASSWORD':config['password'],'TMDB_TEST_DB_NAME':'tmdb_test_warehouse',
                       'TMDB_TEST_DB_PORT':'55432','TMDB_TEST_DB_HOST':'127.0.0.1','TMDB_TEST_DB_USER':'tmdb_test_user'})
    try:
        con=connect_readonly()
        try: result=snapshot(con)
        finally:con.close()
    except (Blocked,Exception) as e:
        print('BLOCKED: Không chụp được snapshot cô lập ('+type(e).__name__+')',file=sys.stderr);return 2
    result.update({'mage_run_id':args.mage_run_id or None,'scenario':args.case,'phase':args.phase})
    RESULTS.mkdir(parents=True,exist_ok=True)
    path=RESULTS/(args.case+'_'+args.phase+'.json')
    if path.exists():print('BLOCKED: file snapshot tồn tại, không ghi đè: '+str(path),file=sys.stderr);return 2
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print('Đã lưu snapshot thật',path.relative_to(HERE))
    return 0
if __name__=='__main__':raise SystemExit(main())
