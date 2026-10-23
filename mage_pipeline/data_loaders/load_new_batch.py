import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_file(*args, **kwargs):
    # Đã sửa lỗi dư chữ pd
    df = pd.read_csv('data/raw/tmdb_new_batch.csv')
    print(f"Đã đọc {len(df)} dòng dữ liệu mới.")
    return df