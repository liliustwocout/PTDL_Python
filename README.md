# Project: PTDL-Python-Salary

## Thuộc tính tiền xử lý dữ liệu

- File đầu vào: `global_tech_salary.txt`
- File đầu ra: `global_tech_salary_clean.csv`
- Dòng ban đầu: 5000
- Dòng sau xử lý: 3856

## Những gì đã làm

- Đọc dữ liệu CSV từ file `global_tech_salary.txt`
- Loại bỏ khoảng trắng thừa cho các cột text
- Chuyển `work_year`, `salary`, `salary_in_usd`, `remote_ratio` sang số nguyên
- Loại bỏ dòng trùng và dòng thiếu giá trị ở các cột số quan trọng

## Các bước cụ thể

Trong `preprocess_salary.py`, các bước cụ thể được viết như sau:

1. Đọc file CSV:

```python
import pandas as pd

df = pd.read_csv("global_tech_salary.txt")
```

2. Loại bỏ khoảng trắng thừa cho các cột text:

```python
text_columns = [col for col in df.columns if df[col].dtype == object]
for col in text_columns:
    df[col] = df[col].astype(str).str.strip()
```

3. Chuyển các cột số thành kiểu số:

```python
numeric_columns = ["work_year", "salary", "salary_in_usd", "remote_ratio"]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
```

4. Loại bỏ dòng trùng và dòng thiếu giá trị quan trọng:

```python
df = df.drop_duplicates()
df = df.dropna(subset=["work_year", "salary", "salary_in_usd", "remote_ratio"])
```

5. Chuyển giá trị về số nguyên:

```python
df["work_year"] = df["work_year"].astype(int)
df["salary"] = df["salary"].astype(int)
df["salary_in_usd"] = df["salary_in_usd"].astype(int)
df["remote_ratio"] = df["remote_ratio"].astype(int)
```

6. Lưu file đã xử lý:

```python
df.to_csv("global_tech_salary_clean.csv", index=False)
```

## Trực quan hóa dữ liệu (Data Visualization)

Các biểu đồ trực quan hóa dữ liệu được viết trong file `Data-visualization-matplotlib.py` và lưu trữ tại thư mục `charts/`. Code được nâng cấp chuyên nghiệp dưới dạng các biểu đồ đa bảng (multi-panel subplots), kết hợp phân tích nâng cao bằng thống kê toán học (Gaussian KDE) và biểu đồ hỗn hợp (Hybrid plots).

Đầy đủ 5 nhóm biểu đồ chính bao gồm:

### 1. Relationship (Mối quan hệ) - `charts/1_relationship.png`
* **Loại biểu đồ:** Biểu đồ hỗn hợp **Box Plot kết hợp Jittered Scatter Plot**.
* **Mô tả:** Thể hiện phân bố và mối quan hệ giữa **Cấp bậc kinh nghiệm (Experience Level)** và **Mức lương USD (Salary)**. Biểu đồ hộp (Box plot) màu xám nhạt nằm ẩn phía dưới giúp tóm tắt các chỉ số thống kê quan trọng (hộp IQR, trung vị, phạm vi), trong khi các điểm phân tán với độ lệch ngẫu nhiên (Jitter) giúp nhìn rõ mật độ chi tiết của từng quan sát.

### 2. Trend (Xu hướng) - `charts/2_trend.png`
* **Loại biểu đồ:** Gồm **2 phân bảng (Subplots 1x2)** dạng Line Plot.
  * **Phân bảng A:** Xu hướng lương trung bình qua các năm (2020 - 2024) chia theo 4 Cấp bậc kinh nghiệm (EN, MI, SE, EX) cùng đường trung bình chung toàn ngành để so sánh.
  * **Phân bảng B:** Xu hướng lương trung bình qua các năm của **Top 4 vị trí công việc phổ biến nhất** trong ngành (Data Scientist, Data Engineer, Data Analyst, Machine Learning Engineer).

### 3. Part of a Whole (Bộ phận cấu thành) - `charts/3_part_of_whole.png`
* **Loại biểu đồ:** Gồm **2 phân bảng (Subplots 1x2)** dạng Donut Chart (Biểu đồ tròn khoét lỗ).
  * **Phân bảng A:** Tỷ lệ phần trăm nhân sự ở từng cấp bậc kinh nghiệm, đi kèm tổng số lượng người tương ứng.
  * **Phân bảng B:** Tỷ lệ cơ cấu quy mô doanh nghiệp tuyển dụng (Small - S, Medium - M, Large - L) trong tập dữ liệu.

### 4. Distribution (Phân phối) - `charts/4_distribution.png`
* **Loại biểu đồ:** Gồm **2 phân bảng (Subplots 1x2)** kết hợp thống kê toán học.
  * **Phân bảng A:** Biểu đồ tần suất Histogram tích hợp **đường mật độ xác suất liên tục KDE (Kernel Density Estimate)** tính toán bằng scipy, đi kèm 2 đường nét đứt đánh dấu chính xác **Mean (Giá trị trung bình)** và **Median (Giá trị trung vị)**.
  * **Phân bảng B:** Biểu đồ hộp (Box Plot) phân bố mức lương chi tiết theo từng **Quy mô công ty** để so sánh khoảng biến thiên và các điểm dị biệt (outliers).

### 5. Flow (Dòng chảy / Sự dịch chuyển) - `charts/5_flow.png`
* **Loại biểu đồ:** Gồm **2 phân bảng (Subplots 1x2)** dạng Stacked Area Chart (Biểu đồ vùng chồng).
  * **Phân bảng A:** Sự dịch chuyển tỷ trọng các hình thức làm việc (Làm tại văn phòng - 0%, Hybrid - 50%, Làm từ xa - 100%) qua các năm (2020 - 2024).
  * **Phân bảng B:** Sự dịch chuyển cơ cấu tỷ trọng cấp bậc nhân sự (EN, MI, SE, EX) qua các năm, cho thấy xu hướng "dòng chảy" trình độ chuyên môn của thị trường công nghệ.

---

## Yêu cầu thư viện

- Python 3.x
- pandas
- numpy
- matplotlib

Cài đặt bằng pip:

```bash
pip install pandas numpy matplotlib
```

## Script thực thi

1. **Tiền xử lý dữ liệu:**
   - Script: `preprocess_salary.py`
   - Chạy lệnh: `python preprocess_salary.py`

2. **Trực quan hóa dữ liệu:**
   - Script: `Data-visualization-matplotlib.py`
   - Chạy lệnh: `python Data-visualization-matplotlib.py`
