import pandas as pd
from tkinter import messagebox

# Đường dẫn tới file CSV chứa dữ liệu
file_path = "data/WorldHappiness_Cleaned.csv"

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