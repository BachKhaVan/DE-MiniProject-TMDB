import pandas as pd
from datetime import datetime
from os import path
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_postgres(*args, **kwargs):
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    
    # Truy vấn lấy LSET từ bảng control.etl_watermark
    query = "SELECT lset FROM control.etl_watermark WHERE pipeline_name = 'tmdb_incremental';"
    
    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as loader:
        df = loader.load(query)
        
    # Xử lý gán giá trị LSET và CET
    if df.empty:
        lset = '1900-01-01 00:00:00'
    else:
        lset = df['lset'].iloc[0]
        
    cet = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"✅ Đã lấy thành công Watermark!")
    print(f"LSET (Lần chạy trước): {lset}")
    print(f"CET (Lần chạy này): {cet}")
    
    return {'lset': str(lset), 'cet': cet}