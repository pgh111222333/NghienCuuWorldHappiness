import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from utilities.CRUD import Add_Data
from utilities.CRUD import Edit_Data
from data.data_processor import load_data_cleaned
from data.data_processor import load_data
from data.data_processor import search_data
from data.data_processor import del_data
from data.data_processor import add_delta_happiness
from plots.plot import show_plots_on_new_window

df = None
columns = None
rows_per_page = 20
current_page = 0
total_pages = 0
view = None
search_bar = None
page_label = None
prev_btn = None
next_btn = None
root = None

# Hàm xác nhận thêm dữ liệu
def del_confirm():
    selected_row = view.selection()
    if not selected_row:
        messagebox.showwarning("Thông báo", "Bạn chưa chọn hàng nào cả")
        return

    item_id = selected_row[0]
    values = view.item(item_id, "values")

    columns = list(view["columns"])
    inp_data = {columns[i]: values[i] for i in range(len(columns))}

    del_data(inp_data)
#Load và lọc dữ liệu vào file CSV _Cleaned

    
# Hàm xác nhận sửa dữ liệu
def edit_confirm():
    selected_row = view.selection()
    if not selected_row:
        messagebox.showwarning("Thông báo", "Bạn chưa chọn hàng nào cả")
        return

    item_id = selected_row[0]
    values = view.item(item_id, "values")

    columns = list(view["columns"])
    inp_data = {columns[i]: values[i] for i in range(len(columns))}

    Edit_Data(inp_data)

# Hàm chọn hàng trong Treeview
def select_row(view):
    selected_row = view.selection()
    if not selected_row:
        messagebox.showwarning("Thông báo", "Bạn chưa chọn hàng nào cả")
        return None
    
    item_id = selected_row[0]
    values = view.item(item_id, "values")
    return values

# Hàm tải dữ liệu từ file CSV
def load_page():
    global current_page, rows_per_page, df, view, page_label, prev_btn, next_btn
    

    # Xóa dữ liệu hiện tại trong Treeview
    for item in view.get_children():
        view.delete(item)

    # Tính chỉ số hàng bắt đầu và kết thúc cho trang hiện tại
    start_idx = current_page * rows_per_page
    end_idx = min(start_idx + rows_per_page, len(df))

    # Thêm dữ liệu của trang hiện tại vào Treeview
    for idx in range(start_idx, end_idx):
        row = df.iloc[idx]
        view.insert("", "end", values=list(row))

    # Cập nhật label trang
    page_label.config(text=get_page_info())

    # Vô hiệu hóa nút Previous/Next nếu ở trang đầu/cuối
    prev_btn.config(state="disabled" if current_page == 0 else "normal")
    next_btn.config(state="disabled" if current_page == total_pages - 1 else "normal")

def create_gui(root):
    global df, columns, rows_per_page, current_page, total_pages, view, search_bar, page_label, prev_btn, next_btn

    # Tải dữ liệu
    df = load_data()
    columns = list(df.columns)
    total_pages = (len(df) + rows_per_page - 1) // rows_per_page

    # Tạo Frame để chứa Treeview
    table_frame = ttk.Frame(root, width=400, height=300)
    table_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    table_frame.grid_propagate(False)

    # Tạo Treeview trong table_frame
    view = ttk.Treeview(
        table_frame,
        columns=columns,
        show='headings',
        height=20,  # Hiển thị tối đa 20 hàng (đủ cho 1 trang)
        
    )
    view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Đặt tiêu đề và độ rộng cho các cột
    for col in columns:
        view.heading(col, text=col)
        view.column(col, width=120, anchor="center")  # Độ rộng cột để kích hoạt cuộn ngang

    # Thanh tìm kiếm
    search_bar = ttk.Entry(root, width=30)
    search_bar.grid(row=0, column=0, padx=5, pady=5)

    # Nút tìm kiếm
    search_btn = ttk.Button(root, text="Tìm kiếm", command=search_and_load)
    search_btn.grid(row=0, column=1, padx=5, pady=5)

    # CRUD Buttons
    create_btn = ttk.Button(root, text="Thêm record mới", command=Add_Data)
    create_btn.grid(row=2, column=0, padx=5, pady=5)

    delete_btn = ttk.Button(root, text="Xóa dữ liệu", command=del_confirm)
    delete_btn.grid(row=2, column=1, padx=5, pady=5)

    edit_btn = ttk.Button(root, text="Sửa dữ liệu", command=edit_confirm)
    edit_btn.grid(row=3, column=0, padx=5, pady=5)

    reload_btn = ttk.Button(root, text="Reload lại trang dữ liệu", command=reload_data)
    reload_btn.grid(row=3, column=1, padx=5, pady=5)
    
    add_col_btn = ttk.Button(root, text="Thêm cột deltal_happiness", command=add_delta_happiness)
    load_cleaned_btn =ttk.Button(root,text="Lọc và load dữ liệu vào file Cleaned",command=load_data_cleaned)
    load_cleaned_btn.grid(row=4,column=1,pady=5)
    add_col_btn = ttk.Button(root, text="Thêm cột deltal_happiness", command=add_delta_happiness)
    add_col_btn.grid(row=5,column=1,pady=5)
    show_plots_btn = ttk.Button(root, text="Trình diễn các biểu đồ", command=open_plot_window)
    show_plots_btn.grid(row=6,column=1, pady=5)

    # Frame cho các nút phân trang
    pagination_frame = ttk.Frame(root)
    pagination_frame.grid(row=4, column=0, columnspan=2, pady=5)

    # Nút Previous
    prev_btn = ttk.Button(pagination_frame, text="Previous", command=prev_page)
    prev_btn.grid(row=0, column=0, padx=5)

    # Nút Next
    next_btn = ttk.Button(pagination_frame, text="Next", command=next_page)
    next_btn.grid(row=0, column=1, padx=5)

    # Hiển thị trang hiện tại
    page_label = ttk.Label(pagination_frame, text=get_page_info())
    page_label.grid(row=0, column=2, padx=5)
    

    # Tải dữ liệu 
    load_page()

    root.mainloop()    
def open_plot_window():
    show_plots_on_new_window(root)

# Hàm tìm và load lại trang dữ liệu
def search_and_load():
    global df, total_pages, current_page, search_bar
    keyword = search_bar.get()
    df = search_data(keyword)
    total_pages = (len(df) + rows_per_page - 1) // rows_per_page
    current_page = 0
    load_page()

# Hàm trở về trang trước
def prev_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        load_page()

# Hàm trở đến trang tiếp theo
def next_page():
    global current_page, total_pages
    if current_page < total_pages - 1:
        current_page += 1
        load_page()

# Hàm tải lại dữ liệu từ file CSV
def reload_data():
    global df, total_pages, current_page
    df = load_data()
    total_pages = (len(df) + rows_per_page - 1) // rows_per_page
    current_page = 0
    load_page()

# Hàm lấy thông tin trang hiện tại
def get_page_info():
    global current_page, total_pages
    return f"Page {current_page + 1} of {total_pages}"


def Create_Main_GUI():
    global df
    root = tk.Tk()
    root.title("World Happiness")
    root.geometry("1500x700")

    # Tạo giao diện chính
    create_gui(root)
    root.mainloop()

if __name__ == "__main__":
    Create_Main_GUI()