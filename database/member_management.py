import sqlite3
from config import LADDERBOT_DB

def connect_db():
    return sqlite3.connect(LADDERBOT_DB)

def is_member_in_members_table(discord_id):
    """
    Check if member has already been added
    to the members table to eliminate registering
    the same ID twice in one table.
    """

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM members WHERE discord_id = ?", (discord_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 1

def db_register_member(display_name, discord_id):
    """
    Adds new member to the members table
    using their display name and discord id then setting
    the rest of their stats to a default 0
    """
    if display_name is None or discord_id is None:
        raise ValueError("display_name and discord_id cannot be None")

    conn = connect_db()
    try:
        cursor = conn.cursor()

        default_zero = 0
        cursor.execute('''
            INSERT INTO members (display_name, discord_id, total_1v1_wins, total_1v1_losses, total_2v2_wins, total_2v2_losses, total_3v3_wins, total_3v3_losses, champion_1v1_title, champion_2v2_title, champion_3v3_title, all_teams_count, participation_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (display_name, discord_id, default_zero, default_zero, default_zero, default_zero, default_zero, default_zero, default_zero, default_zero, default_zero, default_zero, default_zero))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while trying to register a member: {e}")
        conn.rollback()
    finally:
        conn.close()
