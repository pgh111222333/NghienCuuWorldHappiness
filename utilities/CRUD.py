import pandas as pd
import tkinter as tk
from tkinter import ttk
from data.data_processor import load_data
from data.data_processor import edit_data
from data.data_processor import create_data

# Hàm thêm dữ liệu mới
def Add_Data():
    entries = {}

    # Tạo cửa sổ nhập liệu
    add = tk.Tk()
    add.geometry("700x500")
    add.title("Thêm record vào bảng")

    # Tải dữ liệu từ file CSV để lấy danh sách các cột
    df = load_data()
    fields = list(df.columns)

    # Tạo form nhập liệu
    form_frame = ttk.Frame(add, padding="10")
    form_frame.pack(fill=tk.BOTH, expand=True)

    # Tạo các trường nhập liệu cho từng cột
    for i, field in enumerate(fields):
        label = ttk.Label(form_frame, text=field + ":")
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
        
        input_inf = ttk.Entry(form_frame, width=30)
        input_inf.grid(row=i, column=1, padx=5, pady=5)
        entries[field] = input_inf

    # Nút Submit để thêm dữ liệu
    submit_btn = ttk.Button(form_frame, text="Thêm record", command=lambda: submit_data_add(entries))
    submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

    add.mainloop

# Hàm xử lý khi nhấn nút Submit trong Add_Data
def submit_data_add(e):
    # Lấy dữ liệu từ các trường nhập liệu
    data = {idx_col: input_field.get() for idx_col, input_field in e.items()}
    create_data(data)  # Gọi hàm thêm dữ liệu vào file CSV
    return data

# Hàm chỉnh sửa dữ liệu
def Edit_Data(inp_data):
    entries = {}

    # Tạo cửa sổ nhập liệu
    edit = tk.Tk()
    edit.geometry("700x500")
    edit.title("Chỉnh sửa record trong bảng")

    # Tải dữ liệu từ file CSV để lấy danh sách các cột
    df = load_data()
    fields = list(df.columns)

    # Tạo form nhập liệu
    form_frame = ttk.Frame(edit, padding="10")
    form_frame.pack(fill=tk.BOTH, expand=True)

    # Lấy giá trị cũ của 'Country name' và 'year' để xác định record cần chỉnh sửa
    old_country = inp_data.get("Country name", "")
    old_year = inp_data.get("year", "")

    # Tạo các trường nhập liệu cho từng cột
    for i, field in enumerate(fields):
        label = ttk.Label(form_frame, text=field + ":")
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
        
        input_inf = ttk.Entry(form_frame, width=30)
        input_inf.grid(row=i, column=1, padx=5, pady=5)

        # Điền giá trị cũ vào các trường nhập liệu
        if field in inp_data:
            input_inf.insert(0, inp_data[field])

        entries[field] = input_inf

    # Nút Submit để chỉnh sửa dữ liệu
    submit_btn = ttk.Button(form_frame, text="Edit record", command=lambda: submit_data_edit(entries, old_country, old_year))
    submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

    edit.mainloop

# Hàm xử lý khi nhấn nút Submit trong Edit_Data
def submit_data_edit(e, o_c, o_y):
    # Lấy dữ liệu từ các trường nhập liệu
    data = {idx_col: input_field.get() for idx_col, input_field in e.items()}
    # Gọi hàm chỉnh sửa dữ liệu trong file CSV
    edit_data(data, o_c, o_y) 