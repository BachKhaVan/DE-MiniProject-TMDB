"""3.2: independent SELECT checks on dbt staging & dimension transformation logic."""
import pytest
from core import report_check,CASES
from sql_checks import SQL

@pytest.mark.m32
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',[k for k in SQL if CASES[k]['section']=='3.2'],ids=lambda x:x)
def test_transformation_invariant(case_id,request,ro_db):
    report_check(request,ro_db,SQL[case_id],case_id)
