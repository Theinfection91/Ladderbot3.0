import sqlite3
from config import LADDERBOT_DB

def connect_db():
    return sqlite3.connect(LADDERBOT_DB)

def is_ladder_running(division_type):
    conn = connect_db()
    cursor = conn.cursor()

    # Query to find boolean for ladder_running in given division type
    cursor.execute("SELECT ladder_running FROM states WHERE division = ?", (division_type,))
    match = cursor.fetchone()

    conn.close()

    if match is None:
        print(f"No entry found in the database for division: {division_type}")
        return False
    return match[0] == 1
