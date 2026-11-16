import pandas as pd
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
from datetime import datetime

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def update_watermark_in_postgres(*args, **kwargs) -> None:
    # Lấy mốc thời gian CET từ kwargs của Mage (rất an toàn, không phụ thuộc khối trước)
    cet_time = kwargs.get('execution_date', datetime.now())
    
    # Tạo DataFrame để nạp vào bảng control
    df = pd.DataFrame([{
        'pipeline_name': 'tmdb_incremental',
        'lset': cet_time
    }])

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as loader:
        loader.export(
            df,
            'control',
            'etl_watermark',
            index=False,
            if_exists='append',
            unique_conflict_method='UPDATE',       # Ghi đè cập nhật mốc thời gian mới nhất
            unique_constraints=['pipeline_name']   # Đối chiếu bằng tên pipeline
        )