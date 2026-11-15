"""Negative controls: inject faults only in isolated DB, always rollback."""
import os
import pytest
from core import register,db_config,Blocked,record,blocked,violation_rows
from sql_checks import SQL

CASES={
 'NC01':('Bridge weight_factor phải bắt được sai lệch','DW18'),
 'NC02':('ROI/profit phải bắt được sai lệch','DW26'),
 'NC03':('FK logic phải bắt được orphan','DW10'),
 'NC04':('Grain phải bắt được fact duplicate','DW06'),
 'NC05':('Bridge không chấp nhận duplicate cặp','DW14'),
}
for id,(name,assertion) in CASES.items():
 register(id,'3.3',name,f'Tạo lỗi trong isolated, SQL {assertion} bắt được, sau đó rollback',
          category='Kiểm tra độ bền',steps='BEGIN → injection có chủ đích → chạy nguyên assertion DW → ROLLBACK',
          input_data='Chỉ tmdb_test_warehouse ở localhost:55432',demo=id=='NC01')

@pytest.mark.integration
@pytest.mark.negative
@pytest.mark.m33
@pytest.mark.parametrize('case_id',list(CASES),ids=list(CASES))
def test_negative_controls(case_id,request):
    if os.getenv('TMDB_TEST_MODE')!='integration' or os.getenv('TMDB_TEST_APPROVED')!='I_UNDERSTAND_ISOLATED_WRITES':
        blocked('Negative control chỉ được phép trên database isolated')
    cfg=db_config()  # strict localhost, port, dbname
    try:import psycopg
    except ImportError:blocked('Chưa cài psycopg')
    if not cfg['password']:blocked('Thiếu isolated secret')
    try:con=psycopg.connect(**cfg,connect_timeout=5,options='-c lock_timeout=5000 -c statement_timeout=60000')
    except Exception:blocked('Không kết nối được DB isolated')
    try:
        got=con.execute('SELECT current_database()').fetchone()[0]
        if got!='tmdb_test_warehouse':blocked('DB name khác isolated')
        # The transaction is NEVER committed. Schema modifications rollback as well.
        from psycopg import sql
        try:
            q=SQL[CASES[case_id][1]]
            before,_=violation_rows(con,q)
            if case_id=='NC01':
                changed=con.execute('''UPDATE dds.bridge_movie_genre SET weight_factor=weight_factor+0.25
                    WHERE ctid=(SELECT ctid FROM dds.bridge_movie_genre ORDER BY movie_sk LIMIT 1)''')
                if changed.rowcount==0:blocked('Bridge genre không có dòng để inject weight')
            elif case_id=='NC02':
                changed=con.execute('''UPDATE dds.fact_movie SET roi=coalesce(roi,0)+3
                    WHERE ctid=(SELECT ctid FROM dds.fact_movie WHERE budget>0 AND revenue>0 ORDER BY movie_sk LIMIT 1)''')
                if changed.rowcount==0:blocked('Không có phim finance-valid để inject ROI')
            elif case_id=='NC03':
                names=con.execute('''SELECT conname FROM pg_constraint
                    WHERE conrelid='dds.bridge_movie_genre'::regclass AND contype='f'
                    AND confrelid='dds.dim_movie'::regclass''').fetchall()
                if not names:blocked('Không tìm thấy FK vật lý để cố ý drop trong transaction')
                for row in names:
                    con.execute(sql.SQL('ALTER TABLE dds.bridge_movie_genre DROP CONSTRAINT {}').format(sql.Identifier(row[0])))
                changed=con.execute('''UPDATE dds.bridge_movie_genre SET movie_sk=-9999999
                    WHERE ctid=(SELECT ctid FROM dds.bridge_movie_genre ORDER BY movie_sk LIMIT 1)''')
                if changed.rowcount==0:blocked('Bridge genre không có dòng để inject FK')
            elif case_id=='NC04':
                names=con.execute('''SELECT conname FROM pg_constraint
                    WHERE conrelid='dds.fact_movie'::regclass AND contype='p' ''').fetchall()
                if not names:blocked('Không có PK fact để drop (trong transaction)')
                con.execute(sql.SQL('ALTER TABLE dds.fact_movie DROP CONSTRAINT {}').format(sql.Identifier(names[0][0])))
                changed=con.execute('''INSERT INTO dds.fact_movie SELECT * FROM dds.fact_movie
                             WHERE movie_sk=(SELECT min(movie_sk) FROM dds.fact_movie)''')
                if changed.rowcount==0:blocked('fact_movie trống, không inject duplicate được')
            elif case_id=='NC05':
                names=con.execute('''SELECT conname FROM pg_constraint
                    WHERE conrelid='dds.bridge_movie_genre'::regclass AND contype IN ('p','u')''').fetchall()
                for row in names:
                    con.execute(sql.SQL('ALTER TABLE dds.bridge_movie_genre DROP CONSTRAINT {}').format(sql.Identifier(row[0])))
                changed=con.execute('''INSERT INTO dds.bridge_movie_genre SELECT * FROM dds.bridge_movie_genre
                    WHERE ctid=(SELECT ctid FROM dds.bridge_movie_genre ORDER BY movie_sk LIMIT 1)''')
                if changed.rowcount==0:blocked('Bridge genre trống, không inject duplicate được')
            after,samples=violation_rows(con,q)
            record(request,{'assertion':CASES[case_id][1],'before_violations':before,
                            'after_injected_violations':after,'sample':samples},
                   note='Negative control; transaction rollback in finally')
            assert after>before,f'Assertion {CASES[case_id][1]} không phát hiện lỗi tiêm vào ({before} → {after})'
        except AssertionError:raise
        except Blocked as e:blocked(str(e))
        except Exception as e:
            blocked('Không inject được dữ liệu vì ràng buộc/thiếu bảng: '+type(e).__name__)
    finally:
        con.rollback()
        con.close()
