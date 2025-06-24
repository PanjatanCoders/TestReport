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

def fetch_all_test_cases():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SADDAM;"
        "DATABASE=MyAPP;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    query = """
    SELECT 
        tc.test_case_id,
        tc.test_case_name,
        tc.product_name,
        tc.module_name,
        tr.status,
        tr.execution_date
    FROM test_cases tc
    LEFT JOIN (
        SELECT test_case_id, status, execution_date
        FROM test_results
        WHERE execution_date = (
            SELECT MAX(execution_date)
            FROM test_results r2
            WHERE r2.test_case_id = test_results.test_case_id
        )
    ) tr ON tc.test_case_id = tr.test_case_id
    ORDER BY tc.module_name, tc.test_case_name
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def update_test_result(test_case_id, release_id, status, executed_by="Tester"):
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SADDAM;"
        "DATABASE=MyAPP;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    cursor = conn.cursor()

    query = """
    INSERT INTO test_results (test_case_id, release_id, status, executed_by)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (test_case_id, release_id, status, executed_by))
    conn.commit()
    conn.close()
def get_release_id_by_name(release_name):
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SADDAM;"
        "DATABASE=MyAPP;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT release_id FROM releases WHERE release_name = ?", (release_name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
