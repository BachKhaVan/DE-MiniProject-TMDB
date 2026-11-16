from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    
    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as loader:
        # THỦ THUẬT: Chạy ép lệnh SQL tạo Khóa chính trước khi nạp
        loader.execute('''
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.table_constraints 
                    WHERE table_name = 'stg_tmdb_movies' AND constraint_type = 'PRIMARY KEY'
                ) THEN
                    ALTER TABLE stage.stg_tmdb_movies ADD PRIMARY KEY (id);
                END IF;
            END $$;
        ''')
        
        # Sau khi có khóa chính thì nạp và Upsert bình thường
        loader.export(
            df,
            'stage',
            'stg_tmdb_movies',
            index=False,
            if_exists='append',
            unique_conflict_method='UPDATE',
            unique_constraints=['id']
        )