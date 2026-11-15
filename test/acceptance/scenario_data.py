#!/usr/bin/env python3
"""Prepare batch fixtures only inside isolated Mage shadow workspace, never source data."""
import argparse,csv,json,shutil,sys
from pathlib import Path
from core import HERE,ROOT,Blocked

DST=HERE/'.runtime'/'workspace'/'data'/'raw'/'tmdb_new_batch.csv'
ALT=HERE/'.runtime'/'workspace'/'mage_pipeline'/'data'/'raw'/'tmdb_new_batch.csv'

def run(action):
    cfg=HERE/'.runtime'/'isolated.json'
    if not cfg.exists():raise Blocked('Chưa prepare isolated runtime')
    data=json.loads(cfg.read_text(encoding='utf8'))
    if data.get('project')!='tmdb_test_acceptance':raise Blocked('Sai project name')
    source=ROOT/'data'/'raw'/'tmdb_new_batch.csv'
    movies=ROOT/'data'/'raw'/'tmdb_5000_movies.csv'
    if action in ('new','restore'):
        if not source.exists():raise Blocked('Không có source batch tmdb_new_batch.csv')
        for dest in (DST,ALT):
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,dest)
        return 'Dùng bản sao batch thật trong isolated workspace'
    if not movies.is_file():raise Blocked('Không có tmdb_5000_movies.csv')
    with movies.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames
        if not fields:raise Blocked('CSV source thiếu header')
        example=next(reader,None)
    if example is None:raise Blocked('CSV source không có dữ liệu')
    if action=='empty':rows=[]
    elif action=='existing':rows=[example]
    elif action=='invalid':
        if 'genres' not in fields:raise Blocked('Thiếu cột genres')
        example['genres']='[{malformed_json'
        rows=[example]
    else:raise Blocked('Action chưa hỗ trợ')
    for dest in (DST,ALT):
        dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    return f'Đã tạo {action} CSV chỉ trong isolated workspace, {len(rows)} rows'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['new','restore','empty','existing','invalid'])
    args=ap.parse_args()
    try:print(run(args.action));return 0
    except Blocked as e:print('BLOCKED:',e,file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
