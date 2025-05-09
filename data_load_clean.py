import pandas as pd

# Đọc dữ liệu từ file CSV (đã có header)
df = pd.read_csv('WorldHappiness.csv', encoding='ISO-8859-1')

# Chuẩn hóa dữ liệu: loại bỏ khoảng trắng ở tên quốc gia
df['Country name'] = df['Country name'].str.strip().str.title()

# Chuyển kiểu dữ liệu cho các cột số (trừ cột tên quốc gia)
for col in df.columns:
    if col != 'Country name':
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Thống kê số lượng giá trị không thiếu cho từng cột
print("Số lượng giá trị không thiếu cho từng cột:")
print(df.count())

# Loại bỏ các hàng có giá trị thiếu
df_clean = df.dropna(axis=0)

# Thống kê số lượng hàng sau khi loại bỏ
print(f"Số lượng hàng sau khi loại bỏ các hàng thiếu dữ liệu: {df_clean.shape[0]}")

# Lưu lại file đã xử lý
df_clean.to_csv('WorldHappiness_clean.csv', index=False)