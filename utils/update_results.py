import pyodbc


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
