import pandas as pd

from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    return pd.read_csv('data/raw/tmdb_new_batch.csv')
