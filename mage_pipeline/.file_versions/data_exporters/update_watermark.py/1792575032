from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data(data, *args, **kwargs):
    # data chính là cái dictionary {'lset': ..., 'cet': ...} được truyền từ get_watermark
    cet = data['cet']
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    
    # Lệnh UPDATE SQL để ghi nhận đã nạp xong
    query = f"UPDATE control.etl_watermark SET lset = '{cet}' WHERE pipeline_name = 'tmdb_incremental';"
    
    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as loader:
        loader.execute(query)
        
    print(f"✅ Đã cập nhật thành công Watermark! LSET mới là: {cet}")