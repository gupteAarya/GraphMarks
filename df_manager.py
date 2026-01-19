import sqlite3
import pandas as pd

def insert_marks(d, p, c, m, test_type):
    total = p + c + m

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO marks (date, test_type, physics, chemistry, maths, total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (d, test_type, p, c, m, total))

    conn.commit()
    conn.close()

def get_marks_df(test_type):
    conn = sqlite3.connect("data.db")
    df = pd.read_sql_query(
        """SELECT date, physics, chemistry, maths, total FROM marks WHERE test_type=? ORDER BY date""",
        conn,
        params=(test_type,)
    )
    conn.close()
    return df