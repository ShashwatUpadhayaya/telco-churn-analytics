import pandas as pd
import sys

def run_quality_checks(file_path):
    print(f"data validation for {file_path}")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Data set not found")
        sys.exit(1)
    #Shape giving to data:
    print(f"\n[1] Dataset shape: {df.shape[0]} rows and {df.shape[1]} columns")
    #Data type:
    print("\n[2] Data types:")
    print(df.dtypes)
    #Checking for missing vals:
    print("\n[3] Nulls:")
    null_counts = df.isnull().sum()
    print(null_counts[null_counts>0] if null_counts.sum()>0 else "No null values here")
    #Checking for duplicate rows:
    duplicates = df.duplicated().sum()
    print(f"\n[4] Number of duplicate rows: {duplicates}")
    #Apparently TotalCharges loads in as an obj/string:
    print("\n[5] checking the column format:")
    print(df['TotalCharges'].head())
if __name__ == "__main__":
    raw_data_path = "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    run_quality_checks(raw_data_path)
