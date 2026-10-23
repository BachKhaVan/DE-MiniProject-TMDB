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

    query = """
        SELECT lset
        FROM control.etl_watermark
        WHERE pipeline_name = 'tmdb_incremental'
    """

    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as loader:
        watermark = loader.load(query)

    if watermark.empty:
        raise ValueError(
            "No watermark found for pipeline 'tmdb_incremental'."
        )

    return {
        'lset': watermark.iloc[0]['lset'],
        'cet': datetime.now(),
    }