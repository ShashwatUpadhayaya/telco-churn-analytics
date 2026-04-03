import duckdb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import warnings

warnings.filterwarnings("ignore")
def train_churn_model():
    db_path = 'telco_churn.duckdb'
    #Load from DuckDB:
    conn= duckdb.connect(db_path)
    df = conn.execute("SELECT * FROM customers").fetchdf()
    conn.close()
    #Prep:
    df = df.drop("customerid",axis=1)
    le = LabelEncoder()
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        df[col] = le.fit_transform(df[col])
    #Feature defining:
    X = df.drop("churn",axis=1)
    y = df["churn"]
    #Train-test:
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)
    #Model training:
    model = LogisticRegression(max_iter = 1000)
    model.fit(X_train, y_train)
    #Evaluation:
    y_pred = model.predict(X_test)
    print(classification_report(y_test,y_pred,target_names=['Retained(0)','Churned(1)']))
if __name__ == '__main__':
    train_churn_model()