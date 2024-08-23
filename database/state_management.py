import sqlite3
from config import LADDERBOT_DB

def is_ladder_running(division_type):
    """
    Checks the states table in the database
    to see if the ladder is currently running
    for a specified division type
    """