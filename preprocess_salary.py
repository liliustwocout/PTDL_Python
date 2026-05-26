import pandas as pd

INPUT_FILE = "global_tech_salary.txt"
OUTPUT_FILE = "global_tech_salary_clean.csv"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Trim whitespace for text columns
    text_columns = [col for col in df.columns if df[col].dtype == object]
    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    # Convert numeric columns
    numeric_columns = ["work_year", "salary", "salary_in_usd", "remote_ratio"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop duplicate rows and rows with missing required numeric values
    df = df.drop_duplicates()
    df = df.dropna(subset=["work_year", "salary", "salary_in_usd", "remote_ratio"])

    # Convert to integer if possible
    df["work_year"] = df["work_year"].astype(int)
    df["salary"] = df["salary"].astype(int)
    df["salary_in_usd"] = df["salary_in_usd"].astype(int)
    df["remote_ratio"] = df["remote_ratio"].astype(int)

    return df


def main() -> None:
    print(f"Loading data from {INPUT_FILE}...")
    df = load_data(INPUT_FILE)

    print("Initial data overview:")
    print(df.head(5).to_string(index=False))
    print()
    print(df.info())
    print()

    df_clean = clean_data(df)

    print("Cleaned data overview:")
    print(df_clean.head(5).to_string(index=False))
    print()
    print(df_clean.info())
    print()

    print(f"Saving cleaned data to {OUTPUT_FILE}...")
    df_clean.to_csv(OUTPUT_FILE, index=False)
    print("Done.")


if __name__ == "__main__":
    main()