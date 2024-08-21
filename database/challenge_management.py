import sqlite3
from config import LADDERBOT_DB

def connect_db():
    return sqlite3.connect(LADDERBOT_DB)

def is_team_challenged(division_type: str, team_name: str):
    """
    Searches the database in a specific division type
    to see if a specific team has already been challenged
    and therefore cannot be challenged by another team
    until their 'pending' status has resolved
    """

def has_team_challenged(division_type: str, team_name: str):
    """
    Checks the database to see if a given team within
    the given division type has already sent out a challenge
    and therefore cannot send out another until their
    'pending' challenge has resolved
    """