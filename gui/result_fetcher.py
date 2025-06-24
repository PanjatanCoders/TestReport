import pyodbc


def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SADDAM;"
        "DATABASE=MyAPP;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

def fetch_all_releases():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT release_name FROM releases ORDER BY release_date DESC")
        return [row.release_name for row in cursor.fetchall()]

def insert_release(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO releases (release_name) VALUES (?)", name)
        conn.commit()

def fetch_test_results_by_release(release_name):
    import pandas as pd
    with get_connection() as conn:
        query = f"""
        SELECT tr.result_id, tc.test_case_name, tc.module_name, tc.product_name, tr.status,
               tr.executed_by, tr.execution_time_seconds, tr.execution_date, r.release_name
        FROM test_results tr
        JOIN test_cases tc ON tc.test_case_id = tr.test_case_id
        JOIN releases r ON r.release_id = tr.release_id
        WHERE r.release_name = ?
        ORDER BY tc.module_name, tr.execution_date DESC
        """
        df = pd.read_sql(query, conn, params=[release_name])
        return df

