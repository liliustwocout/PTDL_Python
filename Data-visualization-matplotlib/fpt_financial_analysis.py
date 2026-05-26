import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cấu hình encoding utf-8 để in tiếng Việt ra console không bị lỗi trên Windows
sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình font chữ hỗ trợ tiếng Việt trên biểu đồ
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Segoe UI', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Đường dẫn file dữ liệu
dir_path = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(dir_path, "fpt_financial_data_2020_2025.txt")

print("Đang đọc dữ liệu từ file...")
# 1. Đọc và chuẩn bị dữ liệu
df = pd.read_csv(data_file)
df['Time'] = df['Quarter'] + '/' + df['Year'].astype(str)
df['Gross_Margin'] = (df['Gross_Profit_Billion_VND'] / df['Revenue_Billion_VND']) * 100
df['Net_Margin'] = (df['Net_Profit_Billion_VND'] / df['Revenue_Billion_VND']) * 100


# --- 1. TREND (Xu hướng Doanh thu & Lợi nhuận) ---
print("Đang vẽ biểu đồ xu hướng (Trend)...")
plt.figure(figsize=(10, 5))
plt.plot(df['Time'], df['Revenue_Billion_VND'], label='Doanh thu (Tỷ VND)', color='blue', marker='o')
plt.plot(df['Time'], df['Net_Profit_Billion_VND'], label='Lợi nhuận ròng (Tỷ VND)', color='red', marker='s')
plt.title('1. TREND: Xu hướng Doanh thu & Lợi nhuận ròng FPT')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(dir_path, 'fpt_trend.png'))
plt.close()


# --- 2. COMPARISON (So sánh doanh thu mảng Công nghệ vs Viễn thông) ---
print("Đang vẽ biểu đồ so sánh doanh thu mảng (Comparison)...")
plt.figure(figsize=(10, 5))
x_indices = range(len(df))
plt.bar([i - 0.2 for i in x_indices], df['Tech_Segment_Revenue'], width=0.4, label='Mảng Công nghệ', color='teal')
plt.bar([i + 0.2 for i in x_indices], df['Telecom_Segment_Revenue'], width=0.4, label='Mảng Viễn thông', color='orange')
plt.title('2. COMPARISON: Doanh thu Công nghệ vs Viễn thông')
plt.xticks(x_indices, df['Time'], rotation=45)
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(dir_path, 'fpt_segments.png'))
plt.close()


# --- 3. PERFORMANCE (Biên lợi nhuận gộp & ròng) ---
print("Đang vẽ biểu đồ tỷ suất biên lợi nhuận (Performance)...")
plt.figure(figsize=(10, 5))
plt.plot(df['Time'], df['Gross_Margin'], label='Biên LN gộp (%)', color='green', marker='o')
plt.plot(df['Time'], df['Net_Margin'], label='Biên LN ròng (%)', color='crimson', marker='d')
plt.title('3. PERFORMANCE: Tỷ suất Biên lợi nhuận FPT')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(dir_path, 'fpt_margins.png'))
plt.close()


# --- 4. ANNUAL GROWTH (Tài chính hàng năm) ---
print("Đang vẽ biểu đồ tăng trưởng tài chính hàng năm (Annual Growth)...")
df_year = df.groupby('Year')[['Revenue_Billion_VND', 'Net_Profit_Billion_VND']].sum().reset_index()
plt.figure(figsize=(10, 5))
x_year = range(len(df_year))
plt.bar([i - 0.2 for i in x_year], df_year['Revenue_Billion_VND'], width=0.4, label='Tổng Doanh thu', color='blue')
plt.bar([i + 0.2 for i in x_year], df_year['Net_Profit_Billion_VND'], width=0.4, label='Tổng Lợi nhuận ròng', color='red')
plt.title('4. ANNUAL GROWTH: Tài chính hàng năm FPT')
plt.xticks(x_year, df_year['Year'].astype(str))
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(dir_path, 'fpt_annual.png'))
plt.close()


# --- 5. PART OF A WHOLE (Cơ cấu doanh thu tổng thể) ---
print("Đang vẽ biểu đồ cơ cấu doanh thu tổng thể (Part of a Whole)...")
tech_sum = df['Tech_Segment_Revenue'].sum()
telecom_sum = df['Telecom_Segment_Revenue'].sum()
other_sum = df['Revenue_Billion_VND'].sum() - (tech_sum + telecom_sum)
plt.figure(figsize=(6, 6))
plt.pie([tech_sum, telecom_sum, other_sum], labels=['Công nghệ', 'Viễn thông', 'Khác'], autopct='%1.1f%%', colors=['teal', 'orange', 'gray'], startangle=140)
plt.title('5. PART OF A WHOLE: Cơ cấu Doanh thu FPT (2020-2025)')
plt.tight_layout()
plt.savefig(os.path.join(dir_path, 'fpt_part_of_whole.png'))
plt.close()


# --- 6. RELATIONSHIP (Mối tương quan Doanh thu & Lợi nhuận) ---
print("Đang vẽ biểu đồ tương quan Doanh thu & Lợi nhuận (Relationship)...")
plt.figure(figsize=(7, 5))
plt.scatter(df['Revenue_Billion_VND'], df['Net_Profit_Billion_VND'], color='purple', alpha=0.7, s=60)
plt.title('6. RELATIONSHIP: Tương quan Doanh thu & Lợi nhuận')
plt.xlabel('Doanh thu (Tỷ VND)')
plt.ylabel('Lợi nhuận ròng (Tỷ VND)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(dir_path, 'fpt_relationship.png'))
plt.close()


# --- 7. DISTRIBUTION (Phân phối lợi nhuận theo Quý) ---
print("Đang vẽ biểu đồ phân phối lợi nhuận theo Quý (Distribution)...")
plt.figure(figsize=(7, 5))
profits = [df[df['Quarter'] == q]['Net_Profit_Billion_VND'] for q in ['Q1', 'Q2', 'Q3', 'Q4']]
plt.boxplot(profits, tick_labels=['Quý 1', 'Quý 2', 'Quý 3', 'Quý 4'])
plt.title('7. DISTRIBUTION: Phân phối lợi nhuận ròng theo Quý')
plt.ylabel('Lợi nhuận ròng (Tỷ VND)')
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(dir_path, 'fpt_distribution.png'))
plt.close()


# --- 8. DASHBOARD (Báo cáo tổng hợp 2x2) ---
print("Đang tạo Dashboard tổng hợp...")
fig, axs = plt.subplots(2, 2, figsize=(16, 10))
# a) Trend
axs[0, 0].plot(df['Time'], df['Revenue_Billion_VND'], color='blue', label='Doanh thu')
axs[0, 0].plot(df['Time'], df['Net_Profit_Billion_VND'], color='red', label='Lợi nhuận')
axs[0, 0].set_title('a) Doanh thu & Lợi nhuận ròng theo Quý')
axs[0, 0].grid(True, linestyle='--', alpha=0.5)
axs[0, 0].legend()
# b) Comparison
axs[0, 1].bar([i - 0.2 for i in x_indices], df['Tech_Segment_Revenue'], width=0.4, label='Công nghệ', color='teal')
axs[0, 1].bar([i + 0.2 for i in x_indices], df['Telecom_Segment_Revenue'], width=0.4, label='Viễn thông', color='orange')
axs[0, 1].set_title('b) Doanh thu Công nghệ vs Viễn thông')
axs[0, 1].grid(True, axis='y', linestyle='--', alpha=0.5)
axs[0, 1].legend()
# c) Performance
axs[1, 0].plot(df['Time'], df['Gross_Margin'], color='green', label='Biên gộp')
axs[1, 0].plot(df['Time'], df['Net_Margin'], color='crimson', label='Biên ròng')
axs[1, 0].set_title('c) Biên lợi nhuận gộp & Biên lợi nhuận ròng')
axs[1, 0].grid(True, linestyle='--', alpha=0.5)
axs[1, 0].legend()
# d) Annual
axs[1, 1].bar([i - 0.2 for i in x_year], df_year['Revenue_Billion_VND'], width=0.4, label='Doanh thu', color='blue')
axs[1, 1].bar([i + 0.2 for i in x_year], df_year['Net_Profit_Billion_VND'], width=0.4, label='Lợi nhuận', color='red')
axs[1, 1].set_title('d) Tổng quan tài chính theo năm')
axs[1, 1].set_xticks(x_year)
axs[1, 1].set_xticklabels(df_year['Year'].astype(str))
axs[1, 1].grid(True, axis='y', linestyle='--', alpha=0.5)
axs[1, 1].legend()

# Thiết lập nhãn trục X cho các ô đồ thị dạng chuỗi thời gian để dễ nhìn
for ax in [axs[0, 0], axs[0, 1], axs[1, 0]]:
    ax.set_xticks(x_indices)
    ax.set_xticklabels(df['Time'], rotation=45, fontsize=8)

plt.suptitle('8. DASHBOARD: BÁO CÁO TÀI CHÍNH FPT (2020 - 2025)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(dir_path, 'fpt_financial_dashboard.png'))
plt.close()

print("Hoàn thành! Đã vẽ và lưu thành công cả 8 biểu đồ.")
