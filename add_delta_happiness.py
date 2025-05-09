import pandas as pd
def add_delta_happiness(df):

 # Sắp xếp dữ liệu theo quốc gia và năm
    df = df.sort_values(['Country name', 'year'])

    # Tính delta_happiness cho từng quốc gia
    df['delta_happiness'] = df.groupby('Country name')['Life Ladder'].diff().fillna(0)
    df['delta_happiness'] = df['delta_happiness'].round(3)

    # Kiểm tra kết quả
    #print(df[['Country name', 'year', 'Life Ladder', 'delta_happiness']].head(100))
    return df  # Trả về DataFrame đã thêm cột
