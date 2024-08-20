import sqlite3
from config import LADDERBOT_DB

def connect_db():
    return sqlite3.connect(LADDERBOT_DB)

def count_teams(division_type: str):
    """
    Returns the length of the amount 
    of teams in a given division

    Will be useful to use like when assigning
    rank to newly created teams
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Query database for specific division in teams
    cursor.execute('''
        SELECT COUNT(*) FROM teams
        WHERE division = ?
''', (division_type,))
    
    count = cursor.fetchone()[0]
    conn.close()

    return count

def is_team_name_unique(team_name: str) -> bool:
    """
    Check if the team name is unique in the database.

    Args:
        team_name (str): The name of the team to check.

    Returns:
        bool: True if the team name is unique, False otherwise.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM teams WHERE team_name = ?", (team_name,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def is_member_registered(division_type, member_name):
    """
    TODO

    Checks if a given player is already registered
    to a team in a given division

    Args:
        division_type (str): The division type to check.
        member_name (str): The members name to check.

    Returns:
        bool: True if player is on team in division already, False otherwise.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT members FROM teams WHERE division = ?", (division_type,))
    results = cursor.fetchall()

    conn.close()

    # Iterate over each team's members string in the results
    for result in results:
        members_string = result[0]

        # Split string into list for names and strip white space
        members_list = [member.strip() for member in members_string.split(",")]

        # Look for member_name in the list
        if member_name in members_list:
            return True
    
    # If no match found, return False
    return False



def db_register_team(division_type: str, team_name: str, members: str):
    """
    INSERT's given data into correct table
    in ladderbot.db based on the division type given.
    """
    # Count the total teams in given division and assign team rank to bottom
    starting_rank = count_teams(division_type) + 1
    
    # Create teams with 0 wins and losses
    default_win_loss = 0

    # Connect to ladderbot.db and create cursor
    conn = connect_db()
    cursor = conn.cursor()

    # INSERT data in correct division for the team
    cursor.execute('''
        INSERT INTO teams (team_name, division, rank, wins, losses, members)
        VALUES (?, ?, ?, ?, ?, ?)
''', (team_name, division_type, starting_rank, default_win_loss, default_win_loss, members))
    
    # Commit and close the connection to the database
    conn.commit()
    conn.close()