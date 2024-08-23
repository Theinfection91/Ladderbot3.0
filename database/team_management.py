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

def does_team_exist(team_name: str):
    """
    Checks if a team name exists within
    a specified division type.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM teams WHERE team_name = ?", (team_name,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def is_member_registered(division_type: str, member_name: str):
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

def is_member_on_team(display_name: str, team_name: str):
    """
    Checks if a person is apart of a certain team
    Will be used for author purposes of command calls
    to make sure people are making changes to their own
    teams and cant cancel challenges or make challenges for
    a team that they are not on.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT members FROM teams WHERE team_name = ?", (team_name,))
    results = cursor.fetchall()
    
    conn.close()

    # Iterate over each member in the members strings results
    for result in results:
        members_string = result[0]

    # Split string into list for names and strip white space
        members_list = [member.strip() for member in members_string.split(",")]

        if display_name in members_list:
            return True
    
    # If display name is not found in members_list, return False
    return False


def give_team_rank(division_type: str, team_name: str):
    """
    Returns the rank of a given team in a given division type.
    If the team does not exist, returns None.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT rank FROM teams WHERE division = ? AND team_name = ?", (division_type, team_name,))
    rank_result = cursor.fetchone()
    
    conn.close()
    
    # If the team is found, return the rank (first element of the tuple)
    return rank_result[0] if rank_result else None

def update_team_rank(division_type: str, team_name: str, new_rank: int):
    """
    Updates the rank for a given team in the specified division.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''
    UPDATE teams
    SET rank = ?
    WHERE team_name = ? AND division = ?
    ''', (new_rank, team_name, division_type))
    
    conn.commit()
    conn.close()

def increment_rank_for_teams_below(division_type: str, threshold_rank: int):
    """
    Increments the rank for teams below a certain rank in the given division.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # Increment ranks for teams ranked lower than the threshold
    cursor.execute(f'''
    UPDATE teams
    SET rank = rank + 1
    WHERE rank >= ? AND division = ?
    ''', (threshold_rank, division_type))
    
    conn.commit()
    conn.close()

def update_team_wins_losses(division_type: str, team_name: str, win: bool):
    """
    Updates wins or losses for a team.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    if win:
        cursor.execute(f'''
        UPDATE teams
        SET wins = wins + 1
        WHERE team_name = ? AND division = ?
        ''', (team_name, division_type))
    else:
        cursor.execute(f'''
        UPDATE teams
        SET losses = losses + 1
        WHERE team_name = ? AND division = ?
        ''', (team_name, division_type))
    
    conn.commit()
    conn.close()

def check_team_division(team_name: str):
    """
    Checks what division a team is in
    and returns the division type back
    in a string
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT division FROM teams WHERE team_name = ?", (team_name,))
    result = cursor.fetchone()[0]

    conn.close()
    return result

def db_update_rankings(division_type: str, winning_team: str, losing_team: str):
    """
    Updates rankings and records based on the result of a match.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Step 1: Retrieve and store all teams' ranks
    cursor.execute(f'''
    SELECT team_name, rank FROM teams
    WHERE division = ?
    ORDER BY rank
    ''', (division_type,))
    teams = cursor.fetchall()

    # Create a dictionary to easily access team ranks
    team_ranks = {team[0]: team[1] for team in teams}

    # Get the current ranks for winning and losing teams
    winning_team_rank = team_ranks.get(winning_team)
    losing_team_rank = team_ranks.get(losing_team)

    if winning_team_rank is None or losing_team_rank is None:
        conn.close()
        return "Error: One or both teams not found."

    # Step 2: Update ranks for winning and losing teams
    if winning_team_rank > losing_team_rank:

        # First, shift all teams ranked between the losing team and winning team up by one
        for team, rank in team_ranks.items():
            if losing_team_rank < rank < winning_team_rank:
                team_ranks[team] = rank + 1

        # Now, set the winning team to the rank of the losing team
        team_ranks[winning_team] = losing_team_rank

        # Finally, set the losing team to the rank previously held by the winning team
        team_ranks[losing_team] = winning_team_rank

    elif winning_team_rank < losing_team_rank:
        conn.close()
        return "Error: The winning team rank is not greater than the losing team rank."

    # Step 3: Apply new ranking order
    sorted_teams = sorted(team_ranks.items(), key=lambda item: item[1])
    for index, (team_name, _) in enumerate(sorted_teams):
        cursor.execute(f'''
        UPDATE teams
        SET rank = ?
        WHERE team_name = ?
        AND division = ?
        ''', (index + 1, team_name, division_type))

    # Update wins and losses
    cursor.execute(f'''
    UPDATE teams
    SET wins = wins + 1
    WHERE team_name = ?
    AND division = ?
    ''', (winning_team, division_type))

    cursor.execute(f'''
    UPDATE teams
    SET losses = losses + 1
    WHERE team_name = ?
    AND division = ?
    ''', (losing_team, division_type))

    conn.commit()
    conn.close()

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

def db_remove_team(division_type: str, team_name: str):
    """
    DELETE's a given team from a given division
    in the ladderbot.db
    """
    # Connect to ladderbot.db and create cursor
    conn = connect_db()
    cursor = conn.cursor()

    # DELETE data with specified parameters
    cursor.execute("DELETE FROM teams WHERE team_name = ? AND division = ?", (team_name, division_type))

    # Commit and close connection
    conn.commit()
    conn.close()
