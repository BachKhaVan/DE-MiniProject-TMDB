"""Regression checks for false PASS/BLOCKED and evidence classification. No Docker/DB writes."""
import sys
from pathlib import Path
from types import SimpleNamespace
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'acceptance'))
import core
import run as runner
import test_33_negative as negative
import test_34_powerbi as powerbi
from compare_powerbi import compare


@pytest.mark.parametrize('case_id,expected',[('Q1SQL','INFO'),('BI01','INFO'),('MG04','INFO'),('MC01','PASS')])
def test_junit_preserves_id_and_observation(tmp_path,case_id,expected):
    xml=tmp_path/'junit.xml'
    xml.write_text(f'<testsuite><testcase name="test_example[{case_id}]"/></testsuite>',encoding='utf8')
    rows=runner.read_junit(xml,lambda text:text)
    assert rows[0]['id']==case_id
    assert rows[0]['status']==expected


def test_observation_failure_is_still_failure(tmp_path):
    xml=tmp_path/'junit.xml'
    xml.write_text('<testsuite><testcase name="test_example[BI01]"><failure message="bad SQL"/></testcase></testsuite>')
    assert runner.read_junit(xml,lambda text:text)[0]['status']=='FAIL'


def test_negative_control_assertion_is_not_swallowed(monkeypatch):
    import psycopg
    monkeypatch.setenv('TMDB_TEST_MODE','integration')
    monkeypatch.setenv('TMDB_TEST_APPROVED','I_UNDERSTAND_ISOLATED_WRITES')
    monkeypatch.setattr(negative,'db_config',lambda:{'password':'unit-fixture'})
    calls=[]
    class Connection:
        def execute(self,sql):return SimpleNamespace(fetchone=lambda:('tmdb_test_warehouse',),rowcount=1)
        def rollback(self):calls.append('rollback')
        def close(self):calls.append('close')
    monkeypatch.setattr(psycopg,'connect',lambda **kwargs:Connection())
    monkeypatch.setattr(negative,'violation_rows',lambda *args:(0,[]))
    request=SimpleNamespace(node=SimpleNamespace(user_properties=[]))
    with pytest.raises(AssertionError,match='không phát hiện'):
        negative.test_negative_controls('NC01',request)
    assert calls==['rollback','close']


def test_two_dashboard_pages_meet_assignment(monkeypatch):
    monkeypatch.setattr(powerbi,'load_pbir',lambda:[{'name':'Overview'},{'name':'Details'}])
    powerbi.test_powerbi_metadata_and_manual('PB02',SimpleNamespace(node=SimpleNamespace(user_properties=[])))


def test_slicer_only_page_is_not_chart(monkeypatch):
    monkeypatch.setattr(powerbi,'load_pbir',lambda:[{'name':'Empty','visuals':[{'visual':{'visualType':'slicer'}}]}])
    with pytest.raises(AssertionError):
        powerbi.test_powerbi_metadata_and_manual('PB03',SimpleNamespace(node=SimpleNamespace(user_properties=[])))


def test_integration_rejects_demo_target(monkeypatch):
    monkeypatch.setenv('TMDB_TEST_MODE','integration')
    monkeypatch.setenv('TMDB_TEST_APPROVED','I_UNDERSTAND_ISOLATED_WRITES')
    monkeypatch.setenv('TMDB_TEST_DB_NAME','warehouse')
    with pytest.raises(core.Blocked):core.db_config()


def test_sql_error_does_not_reset_outer_snapshot():
    class MissingTable(Exception):sqlstate='42P01'
    class Transaction:
        def __enter__(self):pass
        def __exit__(self,*args):return False
    class Connection:
        def transaction(self):return Transaction()
        def execute(self,sql):raise MissingTable()
        def rollback(self):raise AssertionError('Outer snapshot must survive')
    with pytest.raises(core.Blocked):core.violation_rows(Connection(),'SELECT * FROM missing')


def test_syntax_error_fails_instead_of_blocked():
    class BadSQL(Exception):sqlstate='42601'
    class Transaction:
        def __enter__(self):pass
        def __exit__(self,*args):return False
    class Connection:
        def transaction(self):return Transaction()
        def execute(self,sql):raise BadSQL()
    with pytest.raises(BadSQL):core.violation_rows(Connection(),'bad sql')


@pytest.mark.parametrize('changed,value',[('movies','4804'),('roi_median','130%'),('total_profit','NaN')])
def test_dax_comparison_rejects_wrong_or_formatted_values(changed,value):
    expected=dict(movies=4803,valid_movies=3229,valid_revenue='100.00',total_profit='60',roi_median='1.3',pct_over_budget='0.755')
    actual={key:str(val) for key,val in expected.items()};actual[changed]=value
    assert any(item['status']=='FAIL' for item in compare(expected,actual))


def test_dax_comparison_matches_raw_numbers():
    expected=dict(movies=4803,valid_movies=3229,valid_revenue='100.00',total_profit='60',roi_median='1.3',pct_over_budget='0.755')
    assert all(item['status']=='PASS' for item in compare(expected,expected))
