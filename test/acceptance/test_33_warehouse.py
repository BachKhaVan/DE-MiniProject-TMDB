"""3.3: independent SQL constraints and numerical reconciliation, SELECT-only."""
import pytest
from core import report_check,CASES
from sql_checks import SQL

@pytest.mark.m33
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',[k for k in SQL if CASES[k]['section']=='3.3'],ids=lambda x:x)
def test_warehouse_invariant(case_id,request,ro_db):
    report_check(request,ro_db,SQL[case_id],case_id)
