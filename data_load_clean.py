import pandas as pd

def load_data_cleaned():
    input_path = 'dataset/WorldHappiness.csv'
    output_path = 'dataset/WorldHappiness_clean.csv'

    # Đọc file gốc với encoding ISO-8859-1
    df = pd.read_csv(input_path, encoding='ISO-8859-1')

    print("Thông tin ban đầu:")
    df.info()

    # Chuẩn hóa tên quốc gia
    df['Country name'] = df['Country name'].str.strip().str.title()

    # Chuyển đổi dữ liệu các cột số
    for col in df.columns:
        if col != 'Country name':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    print("Số lượng giá trị không thiếu cho từng cột:")
    print(df.count())

    # Xoá các hàng có dữ liệu thiếu
    df_clean = df.dropna(how='any')
    print(f"Số lượng hàng sau khi loại bỏ: {df_clean.shape[0]}")

    # Lưu file với encoding utf-8-sig để không lỗi tiếng Việt
    df_clean.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Đã lưu file sạch tại: {output_path}")

    return df_clean
