"""3.1: source, Mage pipeline implementation, and read-only stage observations."""
import ast,csv,collections,json,re,sys,os
from datetime import datetime
from pathlib import Path
import pytest
from core import ROOT,register,record,blocked,report_check,CASES

MOVIE_COLS=('budget','genres','homepage','id','keywords','original_language','original_title','overview','popularity','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','tagline','title','vote_average','vote_count')
CREDIT_COLS=('movie_id','title','cast','crew')
SOURCES={
 'MG01':('tmdb_5000_movies.csv',MOVIE_COLS,'id'),
 'MG02':('tmdb_5000_credits.csv',CREDIT_COLS,'movie_id'),
 'MG03':('tmdb_new_batch.csv',MOVIE_COLS,'id'),
}
for key,(fn,cols,_) in SOURCES.items():
 register(key,'3.1',f'CSV {fn} tồn tại và có header',f'CSV có đủ {len(cols)} cột bắt buộc, không trùng header',input_data='data/raw/'+fn,steps='csv.DictReader, đối chiếu cột thực tế',demo=key=='MG01')
for key,title in [('MG04','Movies: khóa id không null hoặc trùng trong file nguồn'),('MG05','Credits: khóa movie_id không null hoặc trùng trong file nguồn'),('MG06','Movie release_date parse được hoặc được ghi nhận coerce'),('MG07','Các trường JSON phim đúng cú pháp hoặc ghi nhận bất thường'),('MG08','Quan hệ CSV movies và credits hai chiều')]:
 register(key,'3.1',title,'Phân tích nguồn và ghi lại số liệu/bất thường; không giả định dữ liệu hoàn hảo',category='Kiểm tra độ bền',steps='Đọc CSV nguồn, thống kê và lấy tối đa 10 mẫu có thứ tự',observation=True)
STATIC={
 'MG09':('mage_pipeline/transformers/clean_movies_data.py','drop_duplicates','dropna',"to_datetime"),
 'MG10':('mage_pipeline/transformers/clean_credits_data.py','drop_duplicates','dropna'),
 'MG11':('mage_pipeline/data_exporters/export_movies_to_postgres.py','if_exists=\'replace\''),
 'MG12':('mage_pipeline/data_exporters/export_credits_to_postgres.py','if_exists=\'replace\''),
 'MG13':('mage_pipeline/data_exporters/export_incremental_stage.py','if_exists=\'append\''),
 'MG14':('mage_pipeline/data_loaders/get_watermark.py','control.etl_watermark','lset'),
 'MG15':('mage_pipeline/data_exporters/update_watermark.py','control.etl_watermark','UPDATE'),
 'MG16':('mage_pipeline/data_loaders/load_new_batch.py','tmdb_new_batch.csv','read_csv'),
}
for key, parts in STATIC.items():
 register(key,'3.1',f'Kiểm tra mã nguồn: {Path(parts[0]).name}','Các quy tắc trong source như mô tả tồn tại',steps='Đọc mã hiện tại + kiểm tra token và AST',evidence='Phát hiện tĩnh trong code')
register('MG17','3.1','Graph Full Load Movies/Credits đúng chuỗi','Mỗi loader → transformer → exporter theo quan hệ metadata',evidence='Phát hiện tĩnh trong code')
register('MG18','3.1','Watermark phụ thuộc vào thành công export incremental','update_watermark có upstream export_incremental_stage',category='Kiểm tra độ bền',evidence='Phát hiện tĩnh trong code',demo=True)
register('MG19','3.1','Loader incremental lọc batch qua LSET/CET','Batch mới được so với lset/cet trước export',category='Kiểm tra độ bền',evidence='Phát hiện tĩnh trong code')
register('MG20','3.1','Exporter incremental xử lý ID trùng khi replay','Có logic upsert/deduplicate hoặc unique key, không tạo bản ghi trùng',category='Kiểm tra độ bền',evidence='Phát hiện tĩnh trong code')
register('MG21','3.1','Full load rowcount stage so với CSV sau làm sạch','Số hàng stage bằng số hàng drop_duplicates + dropna của transformer',input_data='CSV nguồn + database stage',demo=True)
register('MG22','3.1','Quan hệ hai bảng stage và khóa null/trùng','Stage không mất tham chiếu / khóa sau load sạch',input_data='PostgreSQL stage')
register('MG23','3.1','Bảng watermark tồn tại và có dòng incremental','Có một dòng tmdb_incremental và LSET không null',input_data='PostgreSQL control')
register('MG24','3.1','Metadata Mage có log run thực và rowcount','Phải có log run mới có thể khẳng định các pipeline thực thi thành công',category='Kiểm tra độ bền',input_data='Mage runtime log',fix='Mở Mage UI, chạy trong isolated, cung cấp run ID/log block')
CASES['MG19']['observation']=True
CASES['MG19']['expected']='Quan sát source; đề cho phép batch tĩnh, không bắt buộc lọc thời gian LSET/CET'
CASES['MG24']['category']='Yêu cầu bắt buộc'


def csv_rows(name):
    p=ROOT/'data'/'raw'/name
    if not p.is_file(): blocked(f'Thiếu {p.relative_to(ROOT)} trong bản ZIP; thêm CSV TMDB của project')
    try:
        with p.open(encoding='utf-8-sig',newline='') as fh:
            r=csv.DictReader(fh)
            if r.fieldnames is None: blocked('CSV không có header')
            header=r.fieldnames
            rows=list(r)
    except (OSError,UnicodeError,csv.Error) as e: pytest.fail(f'Không đọc được CSV: {type(e).__name__}')
    return header,rows

@pytest.mark.m31
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',list(SOURCES),ids=list(SOURCES))
def test_csv_headers(case_id,request):
    fn,needed,_=SOURCES[case_id]
    header,rows=csv_rows(fn)
    missing=sorted(set(needed)-set(header))
    duplicates=sorted(x for x,n in collections.Counter(header).items() if n>1)
    record(request,{'header_count':len(header),'rows':len(rows),'missing':missing,'duplicate_headers':duplicates})
    assert not missing and not duplicates, f'Thiếu cột {missing}, trùng header {duplicates}'

@pytest.mark.m31
@pytest.mark.readonly
@pytest.mark.parametrize('case_id', ['MG04','MG05','MG06','MG07','MG08'])
def test_source_profiles(case_id,request):
    if case_id in ('MG04','MG05'):
        fn,_,key=SOURCES['MG01' if case_id=='MG04' else 'MG02']
        _,rows=csv_rows(fn)
        keys=[str(r.get(key,'')).strip() for r in rows]
        empties=[i+2 for i,k in enumerate(keys) if not k]
        dup=sorted(k for k,n in collections.Counter(k for k in keys if k).items() if n>1)
        record(request,{'rows':len(rows),'null_keys':len(empties),'duplicate_business_keys':len(dup),'samples':{'null_line':empties[:10],'duplicate_ids':dup[:10]}},note='Bất thường nguồn được thống kê; transformer chỉ drop duplicate toàn dòng')
    elif case_id=='MG06':
        _,rows=csv_rows('tmdb_5000_movies.csv');bad=[]
        for r in rows:
            date=(r.get('release_date') or '').strip()
            if date:
                try:datetime.strptime(date,'%Y-%m-%d')
                except ValueError:bad.append((r.get('id'),date))
        record(request,{'invalid_date_count':len(bad),'sample':sorted(bad)[:10]},note='Transformer dùng errors=coerce, ngày sai thành NaT')
    elif case_id=='MG07':
        _,rows=csv_rows('tmdb_5000_movies.csv');bad=[]
        for r in rows:
            for col in ('genres','keywords','production_companies','production_countries'):
                val=r.get(col)
                if val is not None and val.strip():
                    try: obj=json.loads(val); assert isinstance(obj,list)
                    except (ValueError,AssertionError):bad.append({'id':r.get('id'),'column':col})
        record(request,{'invalid_json_cells':len(bad),'sample':sorted(bad,key=str)[:10]})
    else:
        _,m=csv_rows('tmdb_5000_movies.csv');_,c=csv_rows('tmdb_5000_credits.csv')
        a=set(r['id'] for r in m);b=set(r['movie_id'] for r in c)
        record(request,{'movies_without_credits':len(a-b),'credits_without_movies':len(b-a),
                        'sample_movies':sorted(a-b)[:10],'sample_credits':sorted(b-a)[:10]})
    # Diagnostic source profiling does not automatically FAIL because sources can be dirty.

@pytest.mark.m31
@pytest.mark.readonly
@pytest.mark.parametrize('case_id', list(STATIC),ids=list(STATIC))
def test_mage_implementation(case_id,request):
    filename,*tokens=STATIC[case_id]
    p=ROOT/filename
    if not p.is_file(): blocked(f'Thiếu source: {filename}')
    code=p.read_text(encoding='utf8')
    try: tree=ast.parse(code)
    except SyntaxError as e:pytest.fail(f'Python syntax: {e.msg}')
    # Inspect actual call/string nodes; comments, quote style and whitespace are irrelevant.
    calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
    methods={n.func.attr for n in calls if isinstance(n.func,ast.Attribute)}
    strings=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
    export_specs={'MG11':('stage','stg_tmdb_movies','replace'),
                  'MG12':('stage','stg_tmdb_credits','replace'),
                  'MG13':('stage','stg_tmdb_movies','append'),
                  'MG15':('control','etl_watermark','append')}
    if case_id in export_specs:
        schema,table,mode=export_specs[case_id]
        matching=[]
        for call in calls:
            if not isinstance(call.func,ast.Attribute) or call.func.attr!='export':continue
            args=[n.value if isinstance(n,ast.Constant) else None for n in call.args]
            kws={kw.arg:kw.value.value for kw in call.keywords if isinstance(kw.value,ast.Constant)}
            if len(args)>=3 and args[1:3]==[schema,table] and kws.get('if_exists')==mode:
                matching.append(kws)
        missing=[] if matching else [f'export(df, {schema}, {table}, if_exists={mode})']
        if case_id=='MG15' and not any(x.get('unique_conflict_method')=='UPDATE' for x in matching):missing.append('unique_conflict_method=UPDATE')
    else:
        missing=[t for t in tokens if t not in methods and not any(t in s for s in strings)]
    record(request,{'source':filename,'present_tokens':[t for t in tokens if t not in missing],'missing_tokens':missing},note='Bằng chứng tĩnh, không chứng minh pipeline đã chạy')
    assert not missing, f'Mã nguồn không còn chứa quy tắc được kiểm tra: {missing}'

@pytest.mark.m31
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',['MG17','MG18','MG19','MG20'],ids=['MG17','MG18','MG19','MG20'])
def test_pipeline_risks(case_id,request):
    if case_id in ('MG17','MG18'):
        try: import yaml
        except ImportError:blocked('Chưa cài PyYAML')
        fn='tmdb_ingestion' if case_id=='MG17' else 'tmdb_incremental'
        p=ROOT/'mage_pipeline'/'pipelines'/fn/'metadata.yaml'
        if not p.is_file():blocked('Thiếu metadata '+fn)
        blocks={b['uuid']:b for b in yaml.safe_load(p.read_text(encoding='utf8'))['blocks']}
        if case_id=='MG17':
            expected={'clean_movies_data':['load_tmdb_movies'],
                'export_movies_to_postgres':['clean_movies_data'],
                'clean_credits_data':['load_tmdb_credits'],
                'export_credits_to_postgres':['clean_credits_data']}
            errors=[f'{k}: upstream={blocks.get(k,{}).get("upstream_blocks")}' for k,v in expected.items() if blocks.get(k,{}).get('upstream_blocks')!=v]
        else:
            def ancestors(uid,seen=None):
                seen=set() if seen is None else seen
                for parent in blocks.get(uid,{}).get('upstream_blocks',[]):
                    if parent not in seen:
                        seen.add(parent);ancestors(parent,seen)
                return seen
            actual=sorted(ancestors('update_watermark'))
            errors=[] if 'export_incremental_stage' in actual else [f'upstream hiện tại = {actual}, thiếu exporter']
        record(request,{'pipeline':fn,'errors':errors})
        assert not errors, '; '.join(errors)
    elif case_id=='MG19':
        t=(ROOT/'mage_pipeline/data_loaders/load_new_batch.py').read_text(encoding='utf8')
        record(request,{'loader_uses_lset_or_cet':bool(re.search(r'\b(lset|cet)\b',t,re.I))})
        # The assignment explicitly permits simulated static batches.
    else:
        t=(ROOT/'mage_pipeline/data_exporters/export_incremental_stage.py').read_text(encoding='utf8')
        tree=ast.parse(t)
        calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='export']
        configured=[]
        for call in calls:
            values={}
            for kw in call.keywords:
                try:values[kw.arg]=ast.literal_eval(kw.value)
                except (ValueError,TypeError):pass
            configured.append(values)
        record(request,{'export_options':configured},note='Cấu hình conflict không chứng minh PK/UNIQUE tồn tại; dùng MI04/MI05 để kiểm replay thật')
        blocked('Không thể kết luận chống trùng từ source; cần replay thật MI04/MI05 và unique constraint của stage')

@pytest.mark.m31
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',['MG21','MG22','MG23','MG24'])
def test_mage_stage(case_id,request,ro_db):
    if case_id=='MG24':blocked('Cần run ID và log Mage của lần chạy mới; metadata status=executed không đủ')
    if case_id=='MG23':
        report_check(request,ro_db,"SELECT pipeline_name,lset FROM control.etl_watermark WHERE pipeline_name='tmdb_incremental' AND lset IS NULL",'Watermark NULL')
        n=ro_db.execute("SELECT count(*) FROM control.etl_watermark WHERE pipeline_name='tmdb_incremental'").fetchone()[0]
        record(request,{'watermark_records':n})
        assert n==1,f'Watermark có {n} bản ghi, mong đợi 1'
    elif case_id=='MG22':
        sql="""SELECT 'movies_null' AS kind, coalesce(id::text,'NULL') AS key FROM stage.stg_tmdb_movies WHERE id IS NULL
        UNION ALL SELECT 'credits_null',coalesce(movie_id::text,'NULL') FROM stage.stg_tmdb_credits WHERE movie_id IS NULL
        UNION ALL SELECT 'movies_duplicate',id::text FROM stage.stg_tmdb_movies GROUP BY id HAVING count(*)>1
        UNION ALL SELECT 'credits_duplicate',movie_id::text FROM stage.stg_tmdb_credits GROUP BY movie_id HAVING count(*)>1
        UNION ALL SELECT 'credits_orphan',c.movie_id::text FROM stage.stg_tmdb_credits c LEFT JOIN stage.stg_tmdb_movies m ON c.movie_id=m.id WHERE m.id IS NULL"""
        report_check(request,ro_db,sql,'Các bất thường stage')
    else:
        # Only reliable for pristine full-load snapshots; if incremental has been appended,
        # do not mislabel valid altered data as a pipeline failure.
        sys.path.insert(0,str(ROOT/'test'))
        from validate_tmdb import read_csv_stats  # reuse existing unchanged validator
        target=[]
        for name,key,required,table in [
            ('tmdb_5000_movies.csv','id',['id','title'],'stg_tmdb_movies'),
            ('tmdb_5000_credits.csv','movie_id',['movie_id'],'stg_tmdb_credits')]:
            stats=read_csv_stats(ROOT/'data'/'raw'/name,key,required)
            if stats.error or stats.clean_rows is None:blocked(f'Không tính được clean_rows từ {name}: {stats.error}')
            n=ro_db.execute(f'SELECT count(*) FROM stage.{table}').fetchone()[0]
            target.append({'table':table,'cleaned_count':stats.clean_rows,'actual_count':n})
        record(request,{'comparison':target},note='Nếu stage đã append Incremental, cần đối chiếu snapshot trước khi khẳng định FAIL')
        changed=any(x['actual_count']!=x['cleaned_count'] for x in target)
        if os.getenv('TMDB_STAGE_SNAPSHOT')!='full':
            blocked('Chưa xác nhận Full Load: dùng --snapshot full sau khi chạy ingestion và chưa append incremental')
        assert not changed,'Snapshot Full Load đã xác nhận nhưng số dòng stage khác nguồn sau làm sạch'
