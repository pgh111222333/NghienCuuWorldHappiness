import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Đọc dữ liệu từ file CSV
data = pd.read_csv('WorldHappiness_clean.csv')

# Biểu đồ 1: Biểu đồ đường của Thang Hạnh Phúc qua các năm cho một số quốc gia
plt.figure(figsize=(10, 6))
cac_quoc_gia = ['Australia', 'Afghanistan', 'Brazil', 'Vietnam']
for quoc_gia in cac_quoc_gia:
    du_lieu_quoc_gia = data[data['Country name'] == quoc_gia]
    plt.plot(du_lieu_quoc_gia['year'], du_lieu_quoc_gia['Life Ladder'], label=quoc_gia, marker='o')
plt.title('Xu Hướng Thang Hạnh Phúc (2006-2023) của Một Số Quốc Gia')
plt.xlabel('Năm')
plt.ylabel('Thang Hạnh Phúc')
plt.legend()
plt.grid(True)
plt.show()

# Biểu đồ 2: Biểu đồ cột của Thang Hạnh Phúc trung bình theo năm
plt.figure(figsize=(12, 6))
years = sorted(data['year'].unique())
mean_happiness = [data[data['year'] == year]['Life Ladder'].mean() for year in years]
plt.bar(years, mean_happiness, color='skyblue', edgecolor='black')
plt.title('Thang Hạnh Phúc Trung Bình Theo Năm (2006-2023)')
plt.xlabel('Năm')
plt.ylabel('Thang Hạnh Phúc Trung Bình')
plt.xticks(years, rotation=45)
plt.grid(True, axis='y')
plt.show()

# Biểu đồ 3: Biểu đồ phân tán của Thang Hạnh Phúc và Log GDP bình quân đầu người
plt.figure(figsize=(10, 6))
years = data['year'].unique()
colors = plt.cm.viridis(np.linspace(0, 1, len(years)))
for i, year in enumerate(years):
    year_data = data[data['year'] == year]
    plt.scatter(year_data['Log GDP per capita'], year_data['Life Ladder'], 
                c=[colors[i]], s=50 + i*10, label=year, alpha=0.6)
plt.title('Thang Hạnh Phúc và Log GDP Bình Quân Đầu Người (2006-2023)')
plt.xlabel('Log GDP Bình Quân Đầu Người')
plt.ylabel('Thang Hạnh Phúc')
plt.legend(title='Năm', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
