import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def transform(data, *args, **kwargs):
    data = data.drop_duplicates()
    data = data.dropna(subset=['movie_id'])
    print(f"Đã kiểm tra chất lượng. Số dòng Credits hợp lệ nạp vào Stage: {len(data)}")
    return data