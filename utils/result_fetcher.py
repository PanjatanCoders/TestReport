import pyodbc
import pandas as pd

def fetch_test_results():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SADDAM;"
        "DATABASE=MyAPP;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    query = """
    SELECT 
        tr.result_id,
        tc.test_case_name,
        tc.product_name,
        tc.module_name,
        tr.status,
        tr.execution_time_seconds,
        tr.executed_by,
        tr.execution_date,
        r.release_name
    FROM test_results tr
    JOIN test_cases tc ON tr.test_case_id = tc.test_case_id
    JOIN releases r ON tr.release_id = r.release_id
    ORDER BY tr.execution_date DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
