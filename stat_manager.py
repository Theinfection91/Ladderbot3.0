import discord

from database import get_player_stats

class StatManager:
    """
    Class to hold methods for keeping up
    and processing data for player and 
    "seasonal" team stats that will eventually
    lead to player achievements.
    """

    def __init__(self):
        """
        
        """
    
    def my_stats(discord_id):
        """

        """
        player_stats = get_player_stats(discord_id)

        return player_stats