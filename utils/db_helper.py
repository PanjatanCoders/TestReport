import pyodbc

def get_db_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SADDAM;"
        "DATABASE=MyAPP;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

def fetch_all_releases():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT release_name FROM releases ORDER BY release_date DESC")
    releases = [row.release_name for row in cursor.fetchall()]
    conn.close()
    return releases
