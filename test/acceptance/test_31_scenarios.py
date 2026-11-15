"""Compare real isolated before/after Mage snapshots; no mock pipelines."""
from pathlib import Path
import os,json,datetime,hashlib
import pytest
from core import HERE,register,record,blocked,CASES

DESCS={
 'MI01':('Full Load chạy lại giữ nguyên dữ liệu','full_repeat'),
 'MI02':('Incremental batch mới thêm phim không trùng','batch_new'),
 'MI03':('Incremental batch rỗng không thay đổi bảng','batch_empty'),
 'MI04':('Incremental cùng batch replay không tạo trùng','batch_replay'),
 'MI05':('Batch chứa ID đã có không tạo duplicate','batch_existing'),
 'MI06':('Batch lỗi không làm bẩn stage','batch_invalid'),
 'MI07':('Export thất bại không cập nhật watermark','export_failure'),
 'MI08':('Full Load lỗi một nhánh có snapshot mô tả','partial_full'),
}
for k,(desc,scenario) in DESCS.items():
 register(k,'3.1',desc,'Đối chiếu 2 snapshot before/after của lần Mage run thực',
 category='Kiểm tra độ bền' if k in ('MI04','MI05','MI06','MI07') else 'Yêu cầu bắt buộc',
 steps=f'scenario.py {scenario} before → Mage UI run thật → scenario.py {scenario} after --mage-run-id <ID>',
 input_data='DB isolated và log Mage của run thật',demo=k in ('MI01','MI04','MI07'))
CASES['MI08']['observation']=True
CASES['MI08']['category']='Kiểm tra độ bền'

@pytest.mark.m31
@pytest.mark.integration
@pytest.mark.parametrize('case_id',list(DESCS),ids=list(DESCS))
def test_real_pipeline_scenarios(case_id,request):
    scenario=DESCS[case_id][1]
    base=Path(os.getenv('TMDB_RUNTIME_EVIDENCE_DIR',str(HERE/'.runtime')))/'scenarios'
    before,after=(base/(scenario+'_'+t+'.json') for t in ('before','after'))
    if not before.exists() or not after.exists():
        blocked('Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md')
    b=json.loads(before.read_text());a=json.loads(after.read_text())
    if not a.get('mage_run_id'):blocked('Thiếu Mage run ID; không đủ chứng minh pipeline đã chạy')
    if b.get('scenario')!=scenario or a.get('scenario')!=scenario or b.get('phase')!='before' or a.get('phase')!='after':
        blocked('Snapshot không đúng case/phase')
    if b.get('database')!='tmdb_test_warehouse' or a.get('database')!='tmdb_test_warehouse':
        blocked('Snapshot cũ chưa ghi database; chụp lại bằng scenario.py hiện tại')
    if datetime.datetime.fromisoformat(a['timestamp_utc'])<=datetime.datetime.fromisoformat(b['timestamp_utc']):
        blocked('Thời gian after không nằm sau before')
    logpath=base/Path(a.get('log_file','missing')).name
    if not logpath.is_file():blocked('Thiếu log thực; after cần --mage-log và --run-status')
    log=logpath.read_text(encoding='utf8')
    if hashlib.sha256(log.encode('utf8')).hexdigest()!=a.get('log_sha256'):blocked('Log đã đổi sau snapshot')
    required='failed' if case_id in ('MI07','MI08') else 'success'
    if case_id!='MI06' and a.get('run_status')!=required:
        if case_id in ('MI07','MI08'):blocked('Chưa xác nhận lỗi được kích hoạt như kịch bản yêu cầu')
        pytest.fail('Pipeline thực tế không thành công; không thể PASS chỉ vì dữ liệu chưa đổi')
    if case_id=='MI06' and a.get('run_status') not in ('success','failed'):blocked('Thiếu trạng thái runtime')
    if case_id=='MI07' and 'tmdb_test_injected_export_failure' not in log:
        blocked('Log chưa chứng minh trigger export failure đã thực sự chạy')
    m=b['stg_tmdb_movies'];n=a['stg_tmdb_movies']
    c=b['stg_tmdb_credits'];d=a['stg_tmdb_credits']
    delta=n['rows']-m['rows']
    observation={'scenario':scenario,'run_id':a['mage_run_id'],'movies_delta':delta,
      'movies_duplicate_before':m['duplicate_keys'],'movies_duplicate_after':n['duplicate_keys'],
      'movies_hash_changed':m['sha256']!=n['sha256'],'credits_delta':d['rows']-c['rows'],
      'watermark_before':b['watermark'],'watermark_after':a['watermark']}
    record(request,observation,note='Runtime SQL snapshot trước/sau; run ID do người dùng điền từ Mage UI')
    if case_id=='MI01':
        assert m['sha256']==n['sha256'] and c['sha256']==d['sha256'],'Full Load replay thay đổi dữ liệu giữa 2 lần'
    elif case_id=='MI02':
        if not b.get('batch') or not a.get('batch'):blocked('Cần chụp lại snapshot có metadata batch')
        if b['batch']['sha256']!=a['batch']['sha256']:blocked('Batch đổi giữa before/after')
        expected=len(b['batch']['ids_absent'])
        if not expected:blocked('Fixture batch_new không có ID mới so với snapshot before')
        assert delta==expected and not a['batch']['ids_absent'] and n['duplicate_keys']<=m['duplicate_keys'], 'Số dòng/ID nạp không khớp batch mới hoặc tạo trùng'
    elif case_id in ('MI03','MI04','MI05'):
        assert m['sha256']==n['sha256'] and n['duplicate_keys']<=m['duplicate_keys'],'Stage thay đổi/trùng khi lặp batch hoặc batch rỗng'
    elif case_id=='MI06':
        assert m['sha256']==n['sha256'],'Batch lỗi đã thay đổi stage'
    elif case_id=='MI07':
        assert b['watermark']==a['watermark'],'Watermark tăng dù exporter được cố ý gây lỗi (cần kiểm tra log để xác nhận failure)'
    else:
        # Partial failure is not necessarily a breach of required atomicity.
        # Record observed stage deltas; never assert a non-mandatory atomic guarantee.
        pass
