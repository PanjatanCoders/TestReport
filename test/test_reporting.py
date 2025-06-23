import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SADDAM;"
        "DATABASE=MyAPP;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
)

query = "SELECT * FROM test_cases"
df = pd.read_sql(query, conn)
print(df.shape)
print(df.head())
conn.close()
