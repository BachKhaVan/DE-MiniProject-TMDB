"""SQL reference evidence for Power BI - calculated SQL != verified DAX."""
import pytest
import os,json
from pathlib import Path
from core import ROOT
from core import record,blocked
from bi_queries import QUERIES

@pytest.mark.m34
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',list(QUERIES),ids=list(QUERIES))
def test_independent_bi_sql(case_id,request,ro_db):
    name,sql=QUERIES[case_id]
    try:
        cur=ro_db.execute('SELECT * FROM ('+sql.strip().rstrip(';')+') AS x')
        cols=[x.name for x in cur.description]
        rows=cur.fetchall()
    except Exception as e:
        ro_db.rollback()
        blocked(f'Không chạy được SQL reference {case_id}: {type(e).__name__}; kiểm tra dds và cú pháp')
    samples=[dict(zip(cols,row)) for row in rows[:30]]
    evidence=None
    directory=os.environ.get('TMDB_TEST_EVIDENCE_DIR')
    if directory:
        folder=Path(directory).resolve()
        if not folder.is_relative_to((ROOT/'test'/'results').resolve()):
            blocked('Evidence path không nằm trong test/results/')
        (folder/'queries').mkdir(parents=True,exist_ok=True)
        out=folder/'queries'/(case_id+'.json')
        out.write_text(json.dumps({'id':case_id,'query':sql,'column_names':cols,
                'rows':[dict(zip(cols,row)) for row in rows]},ensure_ascii=False,indent=2,default=str),encoding='utf8')
        evidence='queries/'+case_id+'.json'
    record(request,{'total_rows':len(rows),'sample':samples},
           note='SQL reference độc lập; chưa so với giá trị DAX/screenshot/Refresh Power BI',evidence=evidence)
    assert bool(cols),f'SQL {case_id} không trả về cấu trúc kết quả'
