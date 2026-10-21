from os import path

from mage_ai.data_preparation.decorators import data_exporter
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path


@data_exporter
def update_watermark(data, **kwargs):
    if not isinstance(data, dict) or 'cet' not in data:
        raise ValueError("Expected watermark data containing a 'cet' value.")

    cet = data['cet']
    if cet is None:
        raise ValueError("The watermark 'cet' value cannot be None.")

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    query = """
        UPDATE control.etl_watermark
        SET lset = %s
        WHERE pipeline_name = 'tmdb_incremental'
    """

    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as loader:
        loader.execute(query, (cet,))
