"""pytest markers, shared read-only database snapshot, blocked/skip mapping."""
import os, pytest
from core import connect_readonly,Blocked

@pytest.fixture(scope='session')
def ro_db():
    try: conn=connect_readonly()
    except Blocked as e: pytest.skip('BLOCKED: '+str(e))
    try: yield conn
    finally: conn.close()

def pytest_collection_modifyitems(items):
    # Keep marker definition and nodeids visible to --collect-only.
    for item in items:
        if 'integration' in item.keywords and os.getenv('TMDB_TEST_MODE','readonly')!='integration':
            item.add_marker(pytest.mark.skip(reason='SKIPPED: Chỉ chạy với --mode integration'))
