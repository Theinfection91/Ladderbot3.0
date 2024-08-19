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

    # Use GPT to help learn the best way to create tables
    
def initialize_database():
    """
    Init the database, creating tables if they do not exist.
    """
    conn = connect_db()
    create_tables(conn)
    conn.close()