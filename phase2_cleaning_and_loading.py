import pandas as pd
import duckdb
import os

def clean_load_data():
    raw_path = 'data/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    db_path = 'telco_churn.duckdb'
    #Load our data:
    df = pd.read_csv(raw_path)
    #Cleaning "totalcharges"
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'],errors = 'coerce')
    missing_charges = df['TotalCharges'].isnull().sum()
    df['TotalCharges'] = df['TotalCharges'].fillna(0.0)
    #Standardizing using lowercasing:
    df.columns = df.columns.str.lower()
    #Load into DuckDB:
    conn = duckdb.connect(db_path)
    conn.execute("CREATE OR REPLACE TABLE customers AS SELECT * FROM df")
    #Verify:
    row_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    print(f"Loaded {row_count} rows into customers table in DDB")
    conn.close()
if __name__ == '__main__':
    clean_load_data()