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

def set_ladder_running(division_type: str, true_or_false: bool):
    """
    Sets the ladder in a given division type
    to either true or false
    """
    conn = connect_db()
    cursor = conn.cursor()

    if true_or_false:
        cursor.execute("UPDATE states SET ladder_running = ? WHERE division = ?", (1, division_type))
    
    else:
        cursor.execute("UPDATE states SET ladder_running = ? WHERE division = ?", (0, division_type))
    
    conn.commit()
    conn.close()