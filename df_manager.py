import sqlite3
import pandas as pd

def insert_marks(d, p, c, m, test_type):
    total = p + c + m
    print(f"Inserting marks - Date: {d}, Type: {test_type}, P: {p}, C: {c}, M: {m}, Total: {total}")

    conn = None
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO marks (date, test_type, physics, chemistry, maths, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (d, test_type, p, c, m, total))

        conn.commit()
        print("Successfully inserted marks into database")
    except Exception as e:
        print(f"Error inserting marks: {str(e)}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
            
def get_marks_df(test_type):
    conn = sqlite3.connect("data.db")
    try:
        # First, verify the table exists and has data
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='marks'")
        if not cursor.fetchone():
            return pd.DataFrame()  # Return empty DataFrame if table doesn't exist

        # Now try to get the data
        df = pd.read_sql_query(
            """SELECT date, physics, chemistry, maths, total 
               FROM marks 
               WHERE test_type=? 
               ORDER BY date""",
            conn,
            params=(test_type,)
        )
        return df
    except Exception as e:
        print(f"Error in get_marks_df: {str(e)}")
        return pd.DataFrame()
    finally:
        conn.close()