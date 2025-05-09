import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
def show_plots_on_new_window(parent):
    data = pd.read_csv('data/WorldHappiness_Cleaned.csv')
    new_win = tk.Toplevel(parent)
    new_win.title("Các biểu đồ World Happiness")

    # Tạo notebook (tab) để chuyển đổi giữa các plot
    notebook = ttk.Notebook(new_win)
    notebook.pack(fill='both', expand=True)

    # --- Plot 1 ---
    frame1 = ttk.Frame(notebook)
    notebook.add(frame1, text="Biểu đồ 1")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    cac_quoc_gia = ['Australia', 'Afghanistan', 'Brazil', 'Vietnam']
    for quoc_gia in cac_quoc_gia:
        du_lieu_quoc_gia = data[data['Country name'] == quoc_gia]
        ax1.plot(du_lieu_quoc_gia['year'], du_lieu_quoc_gia['Life Ladder'], label=quoc_gia, marker='o')
    ax1.set_title('Xu Hướng Thang Hạnh Phúc (2006-2023)')
    ax1.set_xlabel('Năm')
    ax1.set_ylabel('Thang Hạnh Phúc')
    ax1.legend()
    ax1.grid(True)
    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill='both', expand=True)

    # --- Plot 2 ---
    frame2 = ttk.Frame(notebook)
    notebook.add(frame2, text="Biểu đồ 2")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    years = sorted(data['year'].unique())
    mean_happiness = [data[data['year'] == year]['Life Ladder'].mean() for year in years]
    ax2.bar(years, mean_happiness, color='skyblue', edgecolor='black')
    ax2.set_title('Thang Hạnh Phúc Trung Bình Theo Năm (2006-2023)')
    ax2.set_xlabel('Năm')
    ax2.set_ylabel('Thang Hạnh Phúc Trung Bình')
    ax2.set_xticks(years)
    ax2.set_xticklabels(years, rotation=45)
    ax2.grid(True, axis='y')
    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill='both', expand=True)

    # --- Plot 3 (Chỉ cho Việt Nam) ---
    frame3 = ttk.Frame(notebook)
    notebook.add(frame3, text="Biểu đồ 3")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    vietnam_data = data[data['Country name'] == 'Vietnam']
    years = vietnam_data['year']
    
    # Vẽ đường Thang Hạnh Phúc
    ax3.plot(years, vietnam_data['Life Ladder'], marker='o', label='Thang Hạnh Phúc', color='blue')
    
    # Vẽ đường Log GDP bình quân đầu người
    ax3.plot(years, vietnam_data['Log GDP per capita'], marker='s', label='Log GDP Bình Quân Đầu Người', color='orange')
    
    ax3.set_title('Thang Hạnh Phúc và Log GDP Bình Quân Đầu Người của Việt Nam (2006-2023)')
    ax3.set_xlabel('Năm')
    ax3.set_ylabel('Giá trị')
    ax3.legend()
    ax3.grid(True)
    fig3.tight_layout()
    canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill='both', expand=True)

    # --- Plot 4 ---
    frame4 = ttk.Frame(notebook)
    notebook.add(frame4, text="Biểu đồ 4")
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    data_to_plot = [data[data['Country name'] == quoc_gia]['Life Ladder'] for quoc_gia in cac_quoc_gia]
    ax4.boxplot(data_to_plot, labels=cac_quoc_gia)
    ax4.set_title('Phân Phối Thang Hạnh Phúc của Một Số Quốc Gia (2006-2023)')
    ax4.set_xlabel('Quốc Gia')
    ax4.set_ylabel('Thang Hạnh Phúc')
    ax4.grid(True)
    canvas4 = FigureCanvasTkAgg(fig4, master=frame4)
    canvas4.draw()
    canvas4.get_tk_widget().pack(fill='both', expand=True)

    # --- Plot 5 ---
    frame5 = ttk.Frame(notebook)
    notebook.add(frame5, text="Biểu đồ 5")
    fig5, ax5 = plt.subplots(figsize=(14, 6))
    
    # Lọc dữ liệu cho 2019 và 2020
    data_2019 = data[data['year'] == 2019][['Country name', 'Life Ladder']]
    data_2020 = data[data['year'] == 2020][['Country name', 'Life Ladder']]
    
    # Gộp hai năm theo tên quốc gia (chỉ lấy các nước có mặt ở cả 2 năm)
    merged = pd.merge(data_2019, data_2020, on='Country name', suffixes=('_2019', '_2020'))
    
    # Sắp xếp tăng dần theo Life Ladder 2020
    merged = merged.sort_values(by='Life Ladder_2020', ascending=True).reset_index(drop=True)
    
    countries = merged['Country name']
    x = np.arange(len(countries))
    
    # Vẽ scatter cho 2019 và 2020, mỗi nước 2 chấm lệch nhẹ
    ax5.scatter(x - 0.1, merged['Life Ladder_2019'], color='blue', label='2019', alpha=0.7)
    ax5.scatter(x + 0.1, merged['Life Ladder_2020'], color='orange', label='2020', alpha=0.7)
    
    # Thêm nhãn quốc gia cho trục x
    ax5.set_xticks(x)
    ax5.set_xticklabels(countries, rotation=90, fontsize=8)
    ax5.set_ylabel('Thang Hạnh Phúc')
    ax5.set_xlabel('Quốc gia')
    ax5.set_title('So sánh Thang Hạnh Phúc các nước năm 2019 và 2020 (sắp xếp tăng dần theo 2020)')
    ax5.legend()
    ax5.grid(True, linestyle='--', alpha=0.5)
    fig5.tight_layout()
    canvas5 = FigureCanvasTkAgg(fig5, master=frame5)
    canvas5.draw()
    canvas5.get_tk_widget().pack(fill='both', expand=True)