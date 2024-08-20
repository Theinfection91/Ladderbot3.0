#database/database_setup.py

import sqlite3
from config.settings import LADDERBOT_DB

"""
All the functions needed for setting
up SQLite database and tables.
"""
def connect_db():
    """
    Connect to the SQLite database.
    """
    return sqlite3.connect(LADDERBOT_DB)

def create_tables(conn):
    """
    Create the necessary tables for
    all data needed in divisions, etc
    for the database.
    """
    # Create SQL cursor
    cursor = conn.cursor()
    
    # Create a Teams tables with team_name, division, rank, wins, losses, and members
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name TEXT NOT NULL,
        division TEXT NOT NULL,
        rank INTEGER NOT NULL,
        wins INTEGER NOT NULL,
        losses INTEGER NOT NULL,
        members TEXT NOT NULL
)
''')
    
    # Create a table for 1v1 challenges
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS challenges_1v1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT NOT NULL,
        challenger TEXT NOT NULL,
        challenged TEXT NOT NULL                   
)
''')
    
    # Create a table for 2v2 challenges
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS challenges_2v2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT NOT NULL,
        challenger TEXT NOT NULL,
        challenged TEXT NOT NULL                   
)
''')
    
    # Create a table for 3v3 challenges
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS challenges_3v3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT NOT NULL,
        challenger TEXT NOT NULL,
        challenged TEXT NOT NULL                   
)
''')
    
    # Add logic for other tables as needed

    # Commit the changes
    conn.commit()
    
def initialize_database():
    """
    Init the database, creating tables if they do not exist.
    """
    conn = connect_db()
    create_tables(conn)
    conn.close()