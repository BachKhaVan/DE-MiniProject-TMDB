from os import path

from datetime import datetime

from mage_ai.data_preparation.decorators import data_loader
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path


@data_loader
def load_data(*args, **kwargs):
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
