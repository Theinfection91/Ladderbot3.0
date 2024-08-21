import sqlite3
from config import LADDERBOT_DB

def connect_db():
    return sqlite3.connect(LADDERBOT_DB)

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
        VALUE (?, ?, ?, ?)
''', (challenger_team, challenger_team, challenged_team, status))
        
        conn.commit()
        conn.close()
    
    # If challenge is a 2v2
    if division_type == '2v2':
        cursor.execute('''
        INSERT INTO challenges_2v2 (match_id, challenger, challenged, status)
        VALUE (?, ?, ?, ?)
''', (challenger_team, challenger_team, challenged_team, status))
        
        conn.commit()
        conn.close()
    
    # If challenge is a 3v3
    if division_type == '3v3':
        cursor.execute('''
        INSERT INTO challenges_3v3 (match_id, challenger, challenged, status)
        VALUE (?, ?, ?, ?)
''', (challenger_team, challenger_team, challenged_team, status))
        
        conn.commit()
        conn.close()