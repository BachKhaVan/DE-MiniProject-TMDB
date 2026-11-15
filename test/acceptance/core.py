"""Shared acceptance-test catalog and conservative PostgreSQL access."""
from __future__ import annotations
import os, sys, json, re, hashlib, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

CASES: dict[str, dict] = {}

def register(case_id, section, title, expected, *, category='Yêu cầu bắt buộc', purpose=None,
             input_data=None, steps=None, evidence='Kết quả chạy mới', demo=False, fix=None):
    if case_id in CASES: raise ValueError(f'Duplicate case ID: {case_id}')
    CASES[case_id] = {'id':case_id,'section':section,'name':title,'category':category,
      'purpose':purpose or title, 'input': input_data or 'Source/DB tương ứng của project',
      'steps':steps or 'Thực hiện assertion mô tả trong mã test.', 'expected':expected,
      'evidence_kind':evidence,'demo':bool(demo),
      'remediation': fix or 'Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.'}
    return case_id

class Blocked(RuntimeError): pass

def db_config():
    mode=os.getenv('TMDB_TEST_MODE','readonly')
    if mode not in ('readonly','integration'): raise Blocked('TMDB_TEST_MODE phải là readonly hoặc integration')
    if mode=='integration':
        # Never accept database targets supplied from the normal demo environment.
        if os.getenv('TMDB_TEST_APPROVED')!='I_UNDERSTAND_ISOLATED_WRITES':
            raise Blocked('Chưa bật cờ bảo vệ TMDB_TEST_APPROVED cho isolated mode')
        host=os.getenv('TMDB_TEST_DB_HOST','127.0.0.1')
        port=int(os.getenv('TMDB_TEST_DB_PORT','55432'))
        name=os.getenv('TMDB_TEST_DB_NAME','tmdb_test_warehouse')
        if host not in ('127.0.0.1','localhost') or port!=55432 or name!='tmdb_test_warehouse':
            raise Blocked('Integration chỉ cho kết nối localhost:55432/tmdb_test_warehouse')
        return dict(host=host,port=port,dbname=name,
            user=os.getenv('TMDB_TEST_DB_USER','tmdb_test_user'),
            password=os.getenv('TMDB_TEST_DB_PASSWORD',''))
    return dict(host=os.getenv('TMDB_DB_HOST','127.0.0.1'),
        port=int(os.getenv('TMDB_DB_PORT','5432')),
        dbname=os.getenv('TMDB_DB_NAME','warehouse'),
        user=os.getenv('TMDB_DB_USER','labuser'),
        password=os.getenv('TMDB_DB_PASSWORD',''))

def connect_readonly():
    try: import psycopg
    except ImportError as e: raise Blocked('Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt') from e
    cfg=db_config()
    if not cfg['password']: raise Blocked('Thiếu mật khẩu: TMDB_DB_PASSWORD (readonly) hoặc TMDB_TEST_DB_PASSWORD (isolated)')
    try:
        conn=psycopg.connect(**cfg,connect_timeout=4,options='-c default_transaction_read_only=on')
        conn.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY')
        if conn.execute('SHOW transaction_read_only').fetchone()[0]!='on':
            conn.close();raise Blocked('Không chứng minh được session chỉ đọc')
        if os.getenv('TMDB_TEST_MODE')=='integration':
            got=conn.execute('select current_database()').fetchone()[0]
            if got!='tmdb_test_warehouse':conn.close();raise Blocked('Đích kết nối không phải database cô lập')
        return conn
    except Blocked:raise
    except Exception as e:
        # Do not echo connection exception: may contain user-controlled conn strings.
        raise Blocked(f'Không kết nối được PostgreSQL {cfg["host"]}:{cfg["port"]}/{cfg["dbname"]} ({type(e).__name__})') from None

def record(request, actual, *, note='', evidence=None):
    prop=request.node.user_properties
    prop.append(('actual',json.dumps(actual,ensure_ascii=False,default=str)))
    if note: prop.append(('note',str(note)))
    if evidence: prop.append(('evidence',str(evidence)))

def blocked(reason):
    import pytest
    pytest.skip('BLOCKED: '+reason)

def violation_rows(conn, sql):
    """Sql returns violations, never a PASS flag; counts are independent of LIMIT."""
    sql=sql.strip().rstrip(';')
    try:
        total=conn.execute(f'SELECT count(*) FROM ({sql}) AS violating_rows').fetchone()[0]
        rows=conn.execute(f'SELECT row_to_json(v) FROM ({sql}) v ORDER BY row_to_json(v)::text LIMIT 10').fetchall()
    except Exception as e:
        # SQL failures are BLOCKED (incompatible snapshot), not falsely recorded as zero violations.
        conn.rollback()
        raise Blocked(f'Không thực hiện được truy vấn SQL ({type(e).__name__}); kiểm tra bảng/cột/model có tồn tại') from None
    return total,[r[0] for r in rows]

def report_check(request, conn, sql, label):
    import pytest
    try: n,rows=violation_rows(conn,sql)
    except Blocked as e: blocked(str(e))
    record(request,{'violations':n,'samples':rows},note=label)
    assert n==0, f'{label}: {n} vi phạm; mẫu {json.dumps(rows,ensure_ascii=False,default=str)[:1200]}'


def dbt_source_fingerprint():
    """Hash source dbt models/seed/macros/YML, never profile or credentials."""
    root=ROOT/'dbt_transform'
    files=[root/'dbt_project.yml']
    for folder in ('models','seeds','macros'):
        files.extend(p for p in (root/folder).rglob('*') if p.is_file() and p.suffix in ('.sql','.yml','.yaml','.csv'))
    digest=hashlib.sha256()
    for path in sorted(files):
        digest.update(str(path.relative_to(root)).encode('utf8'))
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()
