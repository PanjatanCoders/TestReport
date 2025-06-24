import pyodbc
import pandas as pd

# Create DB connection
def get_db_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SADDAM;"
        "DATABASE=MyAPP;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

# Fetch all test results
def fetch_test_results():
    conn = get_db_connection()
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

# Fetch test results for a specific release
def fetch_test_results_by_release(release_name):
    conn = get_db_connection()
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
    WHERE r.release_name = ?
    ORDER BY tr.execution_date DESC
    """
    df = pd.read_sql(query, conn, params=[release_name])
    conn.close()
    return df
