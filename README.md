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

## Học máy & Dự đoán mức lương (Machine Learning)

Toàn bộ quy trình xây dựng, huấn luyện và đánh giá các mô hình học máy được triển khai chi tiết trong notebook `main.ipynb`.

### 1. Mục tiêu bài toán
* **Bài toán:** Hồi quy (Regression) dự đoán mức lương trong ngành công nghệ theo USD (`salary_in_usd`).
* **Đặc trưng đầu vào (Features):** Cấp bậc kinh nghiệm (`experience_level`), loại hợp đồng (`employment_type`), chức danh công việc (`job_title`), quốc gia cư trú (`employee_residence`), tỷ lệ làm từ xa (`remote_ratio`), địa điểm công ty (`company_location`), quy mô công ty (`company_size`), và năm làm việc (`work_year`).
* **Biến mục tiêu (Target):** Được biến đổi logarit $y = \log(1 + \text{salary\_in\_usd})$ để chuẩn hóa phân phối lệch phải của mức lương, giúp mô hình hội tụ tốt hơn.

### 2. Kỹ thuật tiền xử lý & Đặc trưng (Feature Engineering)
* **Xử lý dữ liệu trùng & giá trị thiếu:** Loại bỏ hoàn toàn các bản ghi trùng lặp và bản ghi thiếu giá trị quan trọng để tránh hiện tượng mô hình học vẹt (overfitting).
* **Lọc giá trị ngoại lệ (Outlier Filtering):** Lọc theo phân vị từ 1% đến 99% của `salary_in_usd` nhằm loại bỏ các điểm dữ liệu dị biệt làm lệch hàm mất mát.
* **Mã hóa One-Hot (One-Hot Encoding):** Sử dụng `OneHotEncoder(handle_unknown='ignore')` để chuyển đổi các thuộc tính định loại sang ma trận nhị phân.
* **Chuẩn hóa dữ liệu (Feature Scaling):** Áp dụng `StandardScaler` lên toàn bộ ma trận đặc trưng $X$ để đưa các biến về cùng thang đo (mean = 0, variance = 1).
* **Phân chia dữ liệu (Train/Test Split):** Tách tập theo tỷ lệ **80% Huấn luyện (Train) - 20% Kiểm thử (Test)**. Để đảm bảo tính khách quan và kiểm tra độ bền vững, mỗi mô hình được huấn luyện lặp lại **10 lần** với các random seed khác nhau.

### 3. Các mô hình học máy thực nghiệm

Dự án triển khai và thử nghiệm 5 thuật toán học máy khác nhau:

1. **Linear Regression (Hồi quy tuyến tính):**
   * Mô hình cơ sở (Baseline). Đánh giá biến thiên $R^2$ qua 10 lần chạy (dao động khoảng $0.41 - 0.48$).
   * Tích hợp tìm kiếm lưới `GridSearchCV` (`fit_intercept`, `positive`) để tối ưu hóa siêu tham số.
2. **Decision Tree Regressor (Cây quyết định):**
   * Khảo sát khả năng phân nhánh phi tuyến tính.
   * $R^2$ dao động trong khoảng $0.28 - 0.39$ (trung bình ~0.33), dễ bị ảnh hưởng bởi tính phân mảnh dữ liệu.
3. **Random Forest Regressor (Rừng ngẫu nhiên):**
   * Mô hình Ensemble kết hợp 100 cây quyết định (`n_estimators=100`).
   * Giảm phương sai rõ rệt so với Decision Tree đơn lẻ, tính ổn định qua 10 lần chạy rất cao.
4. **XGBoost Regressor (Extreme Gradient Boosting):**
   * Thuật toán Boosting tối ưu hóa theo gradient loss, thiết lập `n_estimators=100`, `learning_rate=0.1`.
   * Cho kết quả $R^2$ cao nhất trong các mô hình (~$0.480$), bắt trọn tốt các quan hệ phức tạp giữa kinh nghiệm, vị trí và mức lương.
5. **K-Nearest Neighbors Regressor (KNN):**
   * Dự đoán mức lương dựa trên $k$ láng giềng gần nhất ($k=5$).
   * Hiệu năng thấp hơn các mô hình dựa trên cây do không gian đặc trưng sau khi One-Hot Encoding có số chiều lớn (curse of dimensionality).

### 4. Đánh giá & So sánh mô hình

Notebook trực quan hóa và so sánh toàn diện 5 mô hình trên 5 thước đo hiệu năng:
* **MSE (Mean Squared Error) & RMSE (Root Mean Squared Error):** Đo lường độ lệch bình phương giữa giá trị dự đoán và thực tế.
* **$R^2$ (Hệ số xác định):** Đo lường tỷ lệ phương sai của mức lương mà mô hình giải thích được.
* **MAE (Mean Absolute Error):** Sai số tuyệt đối trung bình, trực quan và dễ diễn giải.
* **Thời gian huấn luyện (Training Time):** So sánh tốc độ xử lý giữa các mô hình (Linear Regression nhanh nhất, Random Forest và XGBoost tiêu tốn tài nguyên hơn nhưng cho độ chính xác cao hơn).

---

## Yêu cầu thư viện

- Python 3.x
- pandas
- numpy
- matplotlib
- scipy
- scikit-learn
- xgboost

Cài đặt tất cả thư viện bằng pip:

```bash
pip install pandas numpy matplotlib scipy scikit-learn xgboost
```

## Script & Notebook thực thi

1. **Tiền xử lý dữ liệu:**
   - Script: `preprocess_salary.py`
   - Chạy lệnh: `python preprocess_salary.py`

2. **Trực quan hóa dữ liệu (5 nhóm biểu đồ nâng cao):**
   - Script: `Data-visualization-matplotlib.py`
   - Chạy lệnh: `python Data-visualization-matplotlib.py`

3. **Huấn luyện mô hình Học máy & Phân tích chi tiết:**
   - Notebook: `main.ipynb`
   - Mở và chạy từng bước trên **Jupyter Notebook**, **JupyterLab** hoặc trực tiếp trên **VS Code / Google Colab**.
