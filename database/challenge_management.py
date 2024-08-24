import sqlite3
from config import LADDERBOT_DB

def connect_db():
    return sqlite3.connect(LADDERBOT_DB)

def find_opponent_team(division_type: str, opponent_team: str):
    """
    Finds who a team is facing in a match within
    the given division type
    """

    conn = connect_db()
    cursor = conn.cursor()

    # Variable to hold correct challenges location
    table_name = f'challenges_{division_type}'

    # Query to find the opponent
    cursor.execute(f'''
    SELECT challenger, challenged
    FROM {table_name}
    WHERE challenger = ? OR challenged = ?
    ''', (opponent_team, opponent_team))

    match = cursor.fetchone()

    conn.close()

    if match:
        # Determine the opponent team based on which team is the given team
        if match[0] == opponent_team:
            return match[1]  # Opponent team is in the "challenged" column
        else:
            return match[0]  # Opponent team is in the "challenger" column
    else:
        return None

def is_team_challenged(division_type: str, team_name: str):
    """
    Searches the database all division types
    to see if a specific team has already been challenged
    and therefore cannot be challenged by another team
    until their 'pending' status has resolved
    """
    conn = connect_db()
    cursor = conn.cursor()

    if division_type == '1v1':
        cursor.execute("SELECT COUNT(*) FROM challenges_1v1 WHERE challenged = ?", (team_name,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    if division_type == '2v2':
        cursor.execute("SELECT COUNT(*) FROM challenges_2v2 WHERE challenged = ?", (team_name,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    if division_type == '3v3':
        cursor.execute("SELECT COUNT(*) FROM challenges_3v3 WHERE challenged = ?", (team_name,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

def has_team_challenged(division_type: str, team_name: str):
    """
    Checks the database to see if a given team within
    the given division type has already sent out a challenge
    and therefore cannot send out another until their
    'pending' challenge has resolved
    """
    conn = connect_db()
    cursor = conn.cursor()

    if division_type == '1v1':
        cursor.execute("SELECT COUNT(*) FROM challenges_1v1 WHERE challenger = ?", (team_name,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    if division_type == '2v2':
        cursor.execute("SELECT COUNT(*) FROM challenges_2v2 WHERE challenger = ?", (team_name,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    if division_type == '3v3':
        cursor.execute("SELECT COUNT(*) FROM challenges_3v3 WHERE challenger = ?", (team_name,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

def get_challenges_data(division_type: str):
    """
    Used to grab challenges data for
    division type to then format for
    post_challenges method
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Pick correct challenges table
    table_name = f"challenges_{division_type}"

    # Fetch the current challenges for division type
    cursor.execute(f"SELECT challenger, challenged FROM {table_name} ORDER BY id ASC")
    challenges = cursor.fetchall()
    conn.close()

    # Return raw data to be used in helper function to format neatly
    return challenges

def db_register_challenge(division_type: str, challenger_team: str, challenged_team: str):
    """
    INSERT's given data into the correct division table and also
    uses the challenger's team name as the match_id
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Status string to add to row
    status = 'pending'

    # If challenge is a 1v1
    if division_type == '1v1':
        cursor.execute('''
        INSERT INTO challenges_1v1 (match_id, challenger, challenged, status)
        VALUES (?, ?, ?, ?)
''', (challenger_team, challenger_team, challenged_team, status))
        
        conn.commit()
        conn.close()
    
    # If challenge is a 2v2
    if division_type == '2v2':
        cursor.execute('''
        INSERT INTO challenges_2v2 (match_id, challenger, challenged, status)
        VALUES (?, ?, ?, ?)
''', (challenger_team, challenger_team, challenged_team, status))
        
        conn.commit()
        conn.close()
    
    # If challenge is a 3v3
    if division_type == '3v3':
        cursor.execute('''
        INSERT INTO challenges_3v3 (match_id, challenger, challenged, status)
        VALUES (?, ?, ?, ?)
''', (challenger_team, challenger_team, challenged_team, status))
        
        conn.commit()
        conn.close()

def db_remove_challenge(division_type: str, challenger_team: str):
    """
    Removes a challenge some specific team
    in a specific division
    """

    conn = connect_db()
    cursor = conn.cursor()

    # If division type is 1v1
    if division_type == '1v1':
        cursor.execute("DELETE FROM challenges_1v1 WHERE match_id = ?", (challenger_team,))

        conn.commit()
        conn.close()
    
    # If division type is 2v2
    if division_type == '2v2':
        cursor.execute("DELETE FROM challenges_2v2 WHERE match_id = ?", (challenger_team,))

        conn.commit()
        conn.close()

    # If division type is 3v3
    if division_type == '3v3':
        cursor.execute("DELETE FROM challenges_3v3 WHERE match_id = ?", (challenger_team,))

        conn.commit()
        conn.close()

def remove_challenge(division_type: str, team_name: str):
    """
    Removes a challenge for a specific team.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    if division_type == '1v1':
        cursor.execute("DELETE FROM challenges_1v1 WHERE challenger = ? OR challenged = ?", (team_name, team_name))
    elif division_type == '2v2':
        cursor.execute("DELETE FROM challenges_2v2 WHERE challenger = ? OR challenged = ?", (team_name, team_name))
    elif division_type == '3v3':
        cursor.execute("DELETE FROM challenges_3v3 WHERE challenger = ? OR challenged = ?", (team_name, team_name))
    
    conn.commit()
    conn.close()

def db_clear_all_challenges(division_type: str):
    """
    Clears all challenges from the table corresponding to the given division type.
    """
    table_name = f"challenges_{division_type}"
    
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table_name}")

    conn.commit()
    conn.close()
