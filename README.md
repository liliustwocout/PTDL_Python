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

## Yêu cầu thư viện

- Python 3.x
- pandas

Cài đặt bằng pip:

```bash
pip install pandas
```

## Script thực thi

- `preprocess_salary.py`
