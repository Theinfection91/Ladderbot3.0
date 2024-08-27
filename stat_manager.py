import discord

from database import get_player_stats, increment_all_teams_count, increment_participation_count, add_division_win, add_division_loss

from utils import format_my_stats_report

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
    
    def create_my_stats_report(self, discord_id: int):
        """

        """
        raw_stats_report = get_player_stats(discord_id)

        formatted_stats_report = format_my_stats_report(raw_stats_report)

        return formatted_stats_report
    
    def increment_all_teams_count(self, discord_id):
        """
        Add ONE (1) to all_teams_count stat
        Used when a player registers for a new team
        """
        increment_all_teams_count(discord_id)

    def increment_participation_count(self, discord_id):
        """
        Add ONE (1) to participation_count (match count)
        for player stat tracking
        """
        increment_participation_count(discord_id)

    def add_to_wins_count(self, discord_id, division_type):
        """
        Add ONE (1) to total_{division_type}_wins count
        for player stat tracking
        """
        add_division_win(discord_id, division_type)

    def add_to_losses_count(self, discord_id, division_type):
        """
        Add ONE (1) to total_{division_type}_wins count
        for player stat tracking
        """
        add_division_loss(discord_id, division_type)
    