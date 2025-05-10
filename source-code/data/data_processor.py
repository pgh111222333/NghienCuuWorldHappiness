import pandas as pd
from tkinter import messagebox

# Đường dẫn tới file CSV chứa dữ liệu
file_path = "data/WorldHappiness_Cleaned.csv"
def load_data_cleaned():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    
    input_path = 'dataset/WorldHappiness.csv'

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
    print(f"Số lượng hàng sau khi loại bỏ dữ liệu trống: {df_clean.shape[0]}")
    #Xóa các hàng dữ liêu trùng quốc gia và năm
    df = df.drop_duplicates(['Country name', 'year'], keep='first')
    print(f"Số lượng hàng sau khi loại bỏ trùng lặp: {df_clean.shape[0]}")
    # Lưu file với encoding utf-8-sig để không lỗi tiếng Việt
    df_clean.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Đã lưu file sạch tại: {file_path}")
    df = df.sort_values(['Country name', 'year'])
    return df_clean

#load file chưa xử lí 
#load_data_cleaned()

def load_data():
    try:
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        # Hiển thị lỗi nếu không tìm thấy file
        messagebox.showerror("Lỗi", "Không tìm thấy file dữ liệu.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        # Hiển thị lỗi nếu file dữ liệu trống
        messagebox.showerror("Lỗi", "File dữ liệu trống.")
        return pd.DataFrame()

def create_data(inp_data):
    # Tải dữ liệu từ file CSV
    df = load_data()

    # Thêm hàng mới vào DataFrame
    new_row = pd.DataFrame([inp_data])
    df = pd.concat([df, new_row], ignore_index=True)

    # Ghi lại dữ liệu vào file CSV
    df.to_csv(file_path, index=False)

    # Hiển thị thông báo thành công
    messagebox.showinfo("Thông báo", "Thêm dữ liệu thành công!")

def edit_data(inp_data, o_c, o_y):
    df = load_data()

    # Tìm hàng cần chỉnh sửa
    inp_field = (df["Country name"] == o_c) & (df["year"] == int(o_y))
    if not inp_field.any():
        # Hiển thị cảnh báo nếu không tìm thấy hàng
        messagebox.showwarning("Thông báo", "Không tìm thấy hàng nào")
        return

    # Cập nhật dữ liệu trong DataFrame
    for col, value in inp_data.items():
        if col in df.columns:
            try:
                # Chuyển đổi kiểu dữ liệu nếu cần
                if pd.api.types.is_numeric_dtype(df[col]):
                    value = float(value) if '.' in value else int(value)
                df.loc[inp_field, col] = value
            except ValueError:
                # Hiển thị lỗi nếu giá trị không hợp lệ
                messagebox.showerror("Lỗi", f"Giá trị không hợp lệ cho cột {col}: {value}")
                return

    # Ghi lại dữ liệu vào file CSV
    df.to_csv(file_path, index=False)

    # Hiển thị thông báo thành công
    messagebox.showinfo("Thông báo", "Sửa giá trị thành công!")

def del_data(inp_data):
    # Tải dữ liệu từ file CSV
    df = load_data()

    # Lấy giá trị để xác định hàng cần xóa
    country = inp_data.get("Country name", "").strip()
    year = inp_data.get("year", "")

    # Chuyển đổi kiểu dữ liệu của `year` nếu cần
    try:
        year = int(year)
    except ValueError:
        # Hiển thị lỗi nếu giá trị 'year' không hợp lệ
        messagebox.showerror("Lỗi", f"Giá trị 'year' không hợp lệ: {year}")
        return

    # Tìm hàng cần xóa
    inp_field = (df["Country name"] == country) & (df["year"] == year)

    if not inp_field.any():
        # Hiển thị cảnh báo nếu không tìm thấy hàng
        messagebox.showwarning("Thông báo", "Không tìm thấy hàng cần xóa")
        return

    # Xóa hàng khỏi DataFrame
    df = df.drop(df[inp_field].index)

    # Ghi lại dữ liệu vào file CSV
    df.to_csv(file_path, index=False)

    # Hiển thị thông báo thành công
    messagebox.showinfo("Thông báo", "Xóa dữ liệu thành công!")

def add_delta_happiness():
    # Tải dữ liệu từ file CSV
    df = load_data()
    # Tính toán sự thay đổi của 'Life Ladder' theo từng quốc gia
    df['delta_happiness'] = df.groupby('Country name')['Life Ladder'].diff().fillna(0)
    df['delta_happiness'] = df['delta_happiness'].round(3)

    # Ghi lại dữ liệu vào file CSV
    df.to_csv(file_path, index=False)

    # Hiển thị thông báo thành công
    messagebox.showinfo("Thông báo", "Đã thêm cột 'delta_happiness'!")

def search_data(data_input):
    # Tải dữ liệu từ file CSV
    df = load_data()

    # Tìm kiếm từ khóa trong tất cả các cột
    result = df[df.apply(lambda row: row.astype(str).str.contains(data_input, case=False).any(), axis=1)]

    return result