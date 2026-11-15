"""3.2 source/dependency and docs; old artifacts are never proof of a new build."""
from pathlib import Path
import json,subprocess,shutil,os
import pytest
from core import ROOT,register,record,blocked,dbt_source_fingerprint,dbt_executable

DESCRIPTIONS={
 'DB01':('Đúng 18 dbt models SQL (6 staging + 7 dim + 4 bridge + 1 fact)','18 SQL models theo từng nhóm'),
 'DB02':('Đúng ba seed mappings được khai báo','Ba CSV seeds có header đúng và không rỗng'),
 'DB03':('Có generic/singular data tests trong schema.yml','schema.yml có các ràng buộc not_null, unique, relationships (không yêu cầu liệt kê đủ 18 models)'),
 'DB04':('Có 2 sources tmdb_stage trỏ tới stage','stg_tmdb_movies và stg_tmdb_credits được khai báo'),
 'DB05':('dbt refs/sources hình thành DAG hợp lệ','manifest hiện có đọc được, DAG không có cycle và bao phủ các SQL models'),
 'DB06':('dbt docs có manifest/catalog/index.html','Artifacts cũ hiện diện và parse được; không tính là lần chạy mới'),
 'DB07':('dbt project có schema staging/dds và post-hook','Có 6 views staging, dbt table models dds và vote_count default'),
 'DB08':('dbt executable có thể khởi tạo','Có dbt trên máy hiện tại (chưa tuyên bố debug thành công)'),
 'DB09':('dbt model test được chạy trên snapshot hiện tại','Có run_results của lần chạy này và DB quyền chỉ đọc'),
 'DB10':('dbt docs được sinh từ model hiện tại','docs generate trên máy người dùng mới là bằng chứng hiện hành'),
 'DB11':('Thực thi dbt build/rebuild trong database cô lập','Không chạy trên warehouse demo; có bằng chứng mới sau isolated build'),
 'DB12':('Surrogate key ổn định theo natural key sau rebuild','So sánh natural key và quan hệ, không giả định SK luôn cố định'),
 'DB13':('Mức độ bao phủ model trong schema.yml','Cả 18 models được mô tả riêng trong schema.yml (mức mong muốn, không phải điều kiện tối thiểu của đề)'),
}
for id,(title,expected) in DESCRIPTIONS.items():
 register(id,'3.2',title,expected,category='Kiểm tra độ bền' if id in ('DB11','DB12','DB13') else 'Yêu cầu bắt buộc',
    evidence='Phát hiện tĩnh trong code' if id in ('DB01','DB02','DB03','DB04','DB05','DB06','DB07') else 'Kết quả chạy mới',
    demo=id in ('DB05','DB09'),fix='Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới')

@pytest.mark.m32
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',['DB01','DB02','DB03','DB04','DB05','DB06','DB07','DB08','DB09','DB10','DB11','DB12','DB13'],ids=lambda x:x)
def test_dbt_structure(case_id,request):
    p=ROOT/'dbt_transform'
    if case_id=='DB01':
        names={k:sorted(x.stem for x in (p/'models'/k).glob('*.sql')) for k in ('staging','dimensions','bridge','facts')}
        counts={k:len(v) for k,v in names.items()}
        record(request,{'counts':counts,'files':names})
        assert counts==dict(staging=6,dimensions=7,bridge=4,facts=1)
    elif case_id=='DB02':
        import csv
        files=['country_region.csv','keyword_theme_mapping.csv','language_name_mapping.csv']
        stats=[]
        keys={'country_region.csv':('country_code','region'),
              'keyword_theme_mapping.csv':('keyword_name','theme_group'),
              'language_name_mapping.csv':('language_nk','language_name')}
        for f in files:
            with (p/'seeds'/f).open(encoding='utf-8-sig',newline='') as h:
                reader=csv.DictReader(h);rows=list(reader)
                assert set(keys[f]).issubset(reader.fieldnames or []),f'{f}: thiếu header mapping'
            nk,label=keys[f]
            values=[row[nk].strip().lower() for row in rows]
            assert len(values)==len(set(values)) and all(values),f'{f}: trùng/rỗng natural key'
            assert all(row[label] and row[label].strip() for row in rows),f'{f}: giá trị mapping rỗng'
            stats.append({'name':f,'rows':len(rows)})
        record(request,stats)
        assert all(x['rows']>0 for x in stats)
    elif case_id in ('DB03','DB04','DB07'):
        try: import yaml
        except ImportError:blocked('Cần PyYAML')
        source=(p/'models/staging/sources.yml').read_text(encoding='utf8')
        schema=(p/'models/schema.yml').read_text(encoding='utf8')
        cfg=(p/'dbt_project.yml').read_text(encoding='utf8')
        if case_id=='DB03':
            doc=yaml.safe_load(schema)
            models=doc.get('models',[])
            tokens=[t for t in ('not_null','unique','relationships') if t in schema]
            record(request,{'models_described':len(models),'test_families':tokens})
            assert len(models)>=14 and len(tokens)==3
        elif case_id=='DB04':
            data=yaml.safe_load(source)
            sources=data.get('sources',[])
            found=sorted(t['name'] for s in sources for t in s.get('tables',[]) if s.get('name')=='tmdb_stage')
            record(request,{'tables':found,'schema':sources[0].get('schema') if sources else None})
            assert found==['stg_tmdb_credits','stg_tmdb_movies'] and sources[0].get('schema')=='stage'
        else:
            mapping={'staging':'+materialized: view','dimensions':'+materialized: table','facts':'+post-hook:', 'staging_schema':'+schema: staging','dds_schema':'+schema: dds'}
            missing=[k for k,v in mapping.items() if v not in cfg]
            record(request,{'missing':missing})
            assert not missing
    elif case_id in ('DB05','DB06'):
        base=p/'target'; manifest=base/'manifest.json'
        if not manifest.exists():blocked('Thiếu target/manifest.json; tạo artifacts dưới test/results rồi đánh giá')
        try:
            m=json.loads(manifest.read_text(encoding='utf8'))
        except (ValueError,OSError):pytest.fail('manifest.json lỗi định dạng')
        if case_id=='DB06':
            other=[base/q for q in ('catalog.json','index.html','run_results.json')]
            availability={q.name:q.exists() for q in other}
            if availability['catalog.json']:
                try:json.loads((base/'catalog.json').read_text(encoding='utf8'))
                except ValueError:pytest.fail('catalog.json không phải JSON hợp lệ')
            record(request,{'artifacts':availability},note='Đây là bằng chứng có sẵn trong ZIP, không phải docs generate mới')
            assert all(availability.values()),f'Thiếu: {[k for k,v in availability.items() if not v]}'
        else:
            graph={key:set(v.get('depends_on',{}).get('nodes',[])) for key,v in m.get('nodes',{}).items() if key.startswith('model.')}
            state={}
            def dfs(u):
                if state.get(u)==1:raise AssertionError('Cycle tại '+u)
                if state.get(u)==2:return
                state[u]=1
                for dep in graph[u]:
                    if dep in graph:dfs(dep)
                state[u]=2
            for u in graph:dfs(u)
            record(request,{'models_in_old_manifest':len(graph),'source_node_count':len(m.get('sources',{}))},note='Đồ thị của artifact cũ, không phải build mới')
            assert len(graph)==18 and len(m.get('sources',{}))==2
    elif case_id=='DB13':
        import yaml
        documented={x['name'] for x in yaml.safe_load((p/'models/schema.yml').read_text(encoding='utf8'))['models']}
        existing={x.stem for x in (p/'models').glob('**/*.sql')}
        missing=sorted(existing-documented)
        record(request,{'models_sql':len(existing),'documented':len(documented),'missing_models':missing})
        assert not missing,'Các model chưa được mô tả riêng: '+', '.join(missing)
    elif case_id=='DB08':
        loc=dbt_executable()
        if loc is None:blocked('Không có dbt Core trên PATH môi trường đang chạy')
        record(request,{'found':True,'executable':Path(loc).name})
    elif case_id in ('DB09','DB10','DB11'):
        if os.getenv('TMDB_TEST_MODE')!='integration':
            blocked('Build evidence thuộc DB isolated; chạy --mode integration để không gán kết quả sang warehouse chính')
        runtime=Path(os.getenv('TMDB_RUNTIME_EVIDENCE_DIR',str(ROOT/'test/acceptance/.runtime')))
        result=runtime/'dbt_build_run_results.json'
        provenance=runtime/'dbt_build_provenance.json'
        if not result.is_file() or not provenance.is_file():blocked('Chưa thực hiện dbt build mới có provenance trong isolated; xem isolation.py dbt-build')
        meta=json.loads(provenance.read_text(encoding='utf8'))
        if meta.get('target')!='tmdb_test_warehouse':blocked('DBT build target không đúng database isolated')
        if meta.get('fingerprint')!=dbt_source_fingerprint():blocked('Model SQL/seed/macro/YML đã thay đổi sau isolated build; cần build lại')
        comparison=runtime/'dbt_rebuild_comparison.json'
        if not comparison.is_file():blocked('Thiếu snapshot nguồn của build/rebuild; chạy lại isolation.py dbt-build')
        from core import connect_readonly,Blocked
        from scenario import snapshot
        try:
            conn=connect_readonly()
            try:current=snapshot(conn)
            finally:conn.close()
        except Blocked as error:blocked(str(error))
        recorded=json.loads(comparison.read_text(encoding='utf8'))['after']['source']
        if any(current[table]!=recorded[table] for table in ('stg_tmdb_movies','stg_tmdb_credits')):
            blocked('Stage hiện tại khác nguồn đã build; phải build lại trước nghiệm thu')
        try:run=json.loads(result.read_text(encoding='utf8'))
        except ValueError:pytest.fail('dbt build artifact mới bị hỏng')
        statuses={str(x.get('status')):0 for x in run.get('results',[])}
        for x in run.get('results',[]):
            status=str(x.get('status'));statuses[status]=statuses.get(status,0)+1
        # Artifact from .runtime is generated by isolated command; still ensure
        # it was not copied from an older snapshot of the repository.
        if case_id=='DB09':
            tests=[x for x in run.get('results',[]) if str(x.get('unique_id','')).startswith('test.')]
            record(request,{'build_test_nodes':len(tests),'statuses':statuses},note='Dựa vào run_results của isolated build mới, không dùng target gốc')
            assert tests and all(x.get('status') in ('pass','success') for x in tests)
        elif case_id=='DB10':
            artifacts=[runtime/'dbt_target'/f for f in ('manifest.json','catalog.json','index.html')]
            missing=[str(x.name) for x in artifacts if not x.is_file()]
            buildtime=result.stat().st_mtime
            stale=[x.name for x in artifacts if x.exists() and x.stat().st_mtime+1 < buildtime]
            record(request,{'missing':missing,'older_than_build':stale})
            assert not missing and not stale
        else:
            successful=all(x.get('status') in ('pass','success') for x in run.get('results',[]))
            record(request,{'statuses':statuses,'build_completed':successful},note='Chỉ là isolated dbt build; pipeline Mage có thể cần chạy trước')
            assert run.get('results') and successful
    else:
        if os.getenv('TMDB_TEST_MODE')!='integration':blocked('DB12 chỉ kiểm chứng rebuild trên DB isolated')
        path=Path(os.getenv('TMDB_RUNTIME_EVIDENCE_DIR',str(ROOT/'test/acceptance/.runtime')))/'dbt_rebuild_comparison.json'
        if not path.is_file():blocked('Chạy isolation.py dbt-build để tạo before/after rebuild')
        data=json.loads(path.read_text(encoding='utf8'))
        if data.get('fingerprint')!=dbt_source_fingerprint():blocked('Source đã đổi sau rebuild')
        before,after=data['before'],data['after']
        for table in ('stg_tmdb_movies','stg_tmdb_credits'):
            if before['source'][table]!=after['source'][table]:blocked('Stage đổi giữa hai lần build; không thể kiểm tính lặp trên cùng nguồn')
        changes=[name for name in before['dds'] if before['dds'][name]!=after['dds'].get(name)]
        record(request,{'changed_tables':changes,'tables':len(before['dds'])},note='Chỉ chứng minh cùng snapshot; không yêu cầu SK ổn định khi thêm NK mới')
        assert before['dds'] and not changes,'DDS/SK thay đổi khi rebuild cùng dữ liệu'
