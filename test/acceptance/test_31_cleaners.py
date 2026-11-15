"""Execute the project's actual cleaning functions on controlled input (unit level)."""
import runpy
import pytest
from core import ROOT, register, record, blocked

CASES={
 'MC01':('Movies bỏ dòng trùng toàn bộ','movies_duplicate'),
 'MC02':('Movies bỏ ID/title NULL','movies_null'),
 'MC03':('Movies ép ngày sai thành NaT','movies_date'),
 'MC04':('Credits bỏ dòng trùng và movie_id NULL','credits_clean'),
 'MC05':('Movies xử lý batch rỗng có schema','movies_empty'),
 'MC06':('Cleaner thiếu cột bắt buộc phát sinh lỗi rõ ràng','movies_missing_column'),
}
for key,(name,_) in CASES.items():
    register(key,'3.1',name,'Hành vi hàm transformer đúng với dữ liệu kiểm soát',
             evidence='Unit test thực thi hàm transformer gốc; không thay thế Mage runtime',
             input_data='DataFrame fixture: duplicate, NULL, invalid date, empty, missing column')


@pytest.mark.m31
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',list(CASES))
def test_cleaner_behavior(case_id,request):
    try:import pandas as pd
    except ImportError:blocked('Cần pandas trong requirements.txt để chạy hàm transformer thật')
    credits=case_id=='MC04'
    filename='clean_credits_data.py' if credits else 'clean_movies_data.py'
    # Only the Mage decorator is bypassed; the function body is used unchanged.
    namespace=runpy.run_path(str(ROOT/'mage_pipeline/transformers'/filename),
                            init_globals={'transformer':lambda fn:fn})
    fn=namespace['transform']
    base={'id':1,'title':'A','release_date':'2020-01-02'}
    if case_id=='MC01':
        out=fn(pd.DataFrame([base,base,{**base,'id':2}]))
        assert out['id'].tolist()==[1,2]
    elif case_id=='MC02':
        out=fn(pd.DataFrame([base,{**base,'id':None},{**base,'title':None}]))
        assert len(out)==1 and out.iloc[0]['title']=='A'
    elif case_id=='MC03':
        out=fn(pd.DataFrame([base,{**base,'id':2,'release_date':'bad-date'}]))
        assert out.iloc[0]['release_date']==pd.Timestamp('2020-01-02')
        assert pd.isna(out.iloc[1]['release_date'])
    elif case_id=='MC04':
        row={'movie_id':1,'title':'A','cast':'[]','crew':'[]'}
        out=fn(pd.DataFrame([row,row,{**row,'movie_id':None}]))
        assert len(out)==1 and out.iloc[0]['movie_id']==1
    elif case_id=='MC05':
        out=fn(pd.DataFrame(columns=list(base)))
        assert out.empty and set(out.columns)==set(base)
    else:
        with pytest.raises(KeyError):fn(pd.DataFrame({'id':[1]}))
        record(request,{'missing_columns_rejected':True});return
    record(request,{'output_rows':len(out),'columns':list(out.columns)})
