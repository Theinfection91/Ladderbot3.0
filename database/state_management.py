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

def is_standings_channel_set(division_type: str):
    """
    Checks if there is data within the given
    division's standing channel id that
    will return true or false
    """

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT standings_channel_id FROM states WHERE division = ?", (division_type,))
    result = cursor.fetchone()[0]

    conn = conn.close()

    if result is None:
        return False
    
    else:
        return True

def get_standings_channel_id(division_type: str):
    """
    Returns the integer id for the channel
    that is set for the given division type
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT standings_channel_id FROM states WHERE division = ?", (division_type,))
    result = cursor.fetchone()[0]

    conn = conn.close()

    if result is not None:
        return result
    
def is_challenges_channel_set(division_type: str):
    """
    Checks if there is data within the given
    division's challenge channel id that
    will return true or false
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT challenges_channel_id FROM states WHERE division = ?", (division_type,))
    result = cursor.fetchone()[0]

    conn = conn.close()

    if result is None:
        return False
    
    else:
        return True

def get_challenges_channel_id(division_type: str):
    """
    Returns the integer id for the channel
    that is set for the given division type
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT challenges_channel_id FROM states WHERE division = ?", (division_type,))
    result = cursor.fetchone()[0]

    conn = conn.close()

    if result is not None:
        return result

def db_set_standings_channel(division_type: str, channel_id: int):
    """
    Sets the channel ID of the 
    standings to given integer value
    and given division type
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Update table with channel id integer
    cursor.execute("UPDATE states SET standings_channel_id = ? WHERE division = ?", (channel_id, division_type))

    conn.commit()
    conn.close()

def db_clear_standings_channel(division_type: str):
    """
    Sets the standings channel id to None
    in the given division type
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE states SET standings_channel_id = ? WHERE division = ?", (None, division_type))

    conn.commit()
    conn.close()

def db_set_challenges_channel(division_type: str, channel_id: int):
    """
    Sets the channel ID of the
    challenges to the given integer
    value and given division type
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Update table with channel id integer
    cursor.execute("UPDATE states SET challenges_channel_id = ? WHERE division = ?", (channel_id, division_type))

    conn.commit()
    conn.close()

def db_clear_challenges_channel(division_type: str):
    """
    Sets the challenges channel id to None
    in the given division type
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE states SET challenges_channel_id = ? WHERE division = ?", (None, division_type))

    conn.commit()
    conn.close()