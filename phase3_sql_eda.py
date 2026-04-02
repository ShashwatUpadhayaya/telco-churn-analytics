import duckdb
import pandas as pd
import os

def run_sql_eda():
    db_path = 'telco_churn.duckdb'
    export_dir= 'exports'
    #create exports for SQL aggrigations:
    os.makedirs(export_dir, exist_ok=True)
    conn =  duckdb.connect(db_path)
    #Contact type churn:
    contract_query = """
        SELECT
            contract,
            COUNT(customerid) AS total_customers,
            SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
            ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(customerid),2) AS churn_rate_pct
        FROM customers
        GROUP BY contract
        ORDER BY churn_rate_pct DESC;
    """
    df_contract = conn.execute(contract_query).fetchdf()
    df_contract.to_csv(f"{export_dir}/churn_by_contract.csv",index = False)
    print(df_contract.to_string(index = False))
    #Foing by payment methods:
    payment_query = """
    SELECT 
        paymentmethod,
        COUNT(customerid) AS total_customers,
        ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)*100/COUNT(customerid),2) AS churn_rate_pct
        FROM customers
        GROUP BY paymentmethod,
        ORDER BY churn_rate_pct DESC;
    """
    df_payment = conn.execute(payment_query).fetchdf()
    df_payment.to_csv(f"{export_dir}/churn_by_payment.csv", index=False)
    #Customers to risk based on tenure:
    tenure_query = """
    SELECT
        CASE
            WHEN tenure <= 12 THEN '0-1 Year(High risk)'
            WHEN tenure<=34 THEN '1-3 Years(Med risk)'
            ELSE '3+ Years(Low risk)'
        END AS tenure_group,
        COUNT(customerid) AS total_customers,
        ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(customerid), 2) AS churn_rate_pct
        FROM customers
        GROUP BY tenure_group
        ORDER BY churn_rate_pct DESC;
    """
    df_tenure = conn.execute(tenure_query).fetchdf()
    df_tenure.to_csv(f"{export_dir}/churn_by_tenure.csv", index=False)
    conn.close()
if __name__ == '__main__':
    run_sql_eda()