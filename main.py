import discord
from discord.ext import commands
import asyncio

from logs.logger import logger

from ladder_manager import LadderManager

"""
Delete 'from my_token import MY_DISCORD_TOKEN' when manually
entering a full token string at the bottom of the code

To use the my_token import correctly, please refer to the
NOTE's at the very bottom of the code in main() function
"""

from my_token import MY_DISCORD_TOKEN

"""
NOTE
"""

class Ladderbot(commands.Cog):
    """
    This class will house all the discord commands
    that will then call onto the LadderManager class
    to go through the correct database to pull/edit/update/delete
    or what have you with that specific data.
    """
    def __init__(self, bot: commands.Bot, ladder_manager: LadderManager):
        self.bot = bot
        self.ladder_manager = ladder_manager
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.ladder_manager.on_ready()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def start_ladder(self, ctx, division_type: str):
        """
        Starts the ladder in a given division type.

        This command will start the ladder in the given division type.
        The ladder will be started with the teams that are currently
        registered in the division.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /start_ladder 1v1

        Output:
            The ladder in the 1v1 division has been started.
        """
        logger.info(f'Command "start_ladder" invoked by {ctx.author} with division_type={division_type}')
        result = self.ladder_manager.start_ladder(division_type)
        await ctx.send(result)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_test_teams(self, ctx, division_type: str):
        """
        Creates 5 test teams fast for debugging purposes.

        This command will create 5 test teams in the given division type.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /create_test_teams 1v1

        Output:
            5 test teams have been created in the 1v1 division.
        """
        logger.info(f'Command "create_test_teams" invoked by {ctx.author} with division_type={division_type}')
        result = self.ladder_manager.create_test_teams(division_type)
        await ctx.send(result)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def end_ladder(self, ctx, division_type: str):
        """
        Ends the ladder in a given division type.

        This command will end the ladder in the given division type.
        The ladder will be ended with the teams that are currently
        registered in the division.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /end_ladder 2v2

        Output:
            The 2v2 division of the ladder has ended!.
        """
        logger.info(f'Command "end_ladder" invoked by {ctx.author} with division_type={division_type}')
        result = await self.ladder_manager.end_ladder(division_type)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def register_team(self, ctx, team_name: str,  division_type: str, *members: discord.Member):
        """
        Registers a new team within a specified division.
        
        NOTE: Team names are unique across the entire program,
        meaning if there is a Team Alpha in the 2v2 division then
        the program will not allow a Team Alpha to be created in the
        1v1 or 3v3 division. By having team names unique this way it 
        reduces the need for inputting division type on some commands
        like remove_team, challenges, and report_wins.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            team_name (str): The name of the team.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).
            *members (discord.Member): The members of the team.

        Example:
            /register_team Alpha 2v2 @Ixnay @Flaw

        Output:
            Team Alpha has been registered in the 2v2 division with the following members: Ixnay, Flaw
        """
        members_list = [member for member in members]
        logger.info(f'Command "register_team" invoked by {ctx.author} with team_name={team_name} division_type={division_type} members={members_list}')
        result = self.ladder_manager.register_team(division_type, team_name, *members)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_team(self, ctx, team_name: str):
        """
        Removes a team from the entire ladder

        This command will remove the team with the given name from the
        the entire ladder. Note that this command is only available to
        administrators.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            team_name (str): The name of the team.

        Example:
            /remove_team Delta

        Output:
            Team Delta from the 3v3 division has been removed from the Ladder.
        """
        logger.info(f'Command "remove_team" invoked by {ctx.author} with team_name={team_name}')
        result = self.ladder_manager.remove_team(team_name)
        await ctx.send(result)

    @commands.command()
    async def challenge(self, ctx, challenger_team: str, challenged_team: str):
        """
        This challenge function will be usable by everyone
        and users will not need to specify which division
        since team names are set to be unique across
        all divisions (Cant have a Team Charlie in 1v1 and Team Charlie in 2v2)

        A team may only challenge at most two ranks above their rank,
        and no team may challenge below their rank.

        Once a successful challenge is created, the members of the challenged
        team are sent a direct message from the bot with the details.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            challenger_team (str): The name of the team that is challenging.
            challenged_team (str): The name of the team that is being challenged.

        Example:
            /challenge Echo Delta

        Output:
            Team Echo has challenged Team Delta in the 3v3 division!
        """
        logger.info(f'Command "challenge" invoked by {ctx.author} with challenger_team={challenger_team} challenged_team={challenged_team}')
        result = await self.ladder_manager.challenge(ctx, challenger_team, challenged_team)
        await ctx.send(result)

    @commands.command()
    async def cancel_challenge(self, ctx, challenger_team: str):
        """
        Will cancel the challenge of a given challenger team,
        must be used by someone who is apart of the challenger team.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            challenger_team (str): The name of the team that is cancelling the challenge.

        Example:
            /cancel_challenge Echo

        Output:
            The challenge made by Team Echo in the 3v3 division has been canceled by a team member.
        """
        logger.info(f'Command "cancel_challenge" invoked by {ctx.author} with challenger_team={challenger_team}')
        result = self.ladder_manager.cancel_challenge(ctx, challenger_team)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_challenge(self, ctx, challenger_team: str, challenged_team: str):
        """
        Admin method for manually creating challenges
        between teams. This can be useful for when a
        challenge needs to be re-created due to a technical
        issue.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            challenger_team (str): The name of the team that is challenging.
            challenged_team (str): The name of the team that is being challenged.

        Example:
            /admin_challenge Echo Delta

        Output:
            Team Echo has challenged Team Delta in the 3v3 division!. -This challenge was created by an Administrator.
        """
        logger.info(f'Command "admin_challenge" invoked by {ctx.author} with challenger_team={challenger_team} challenged_team={challenged_team}')
        result = await self.ladder_manager.admin_challenge(ctx, challenger_team, challenged_team)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_cancel_challenge(self, ctx, challenger_team: str):
        """
        Admin method for manually cancelling challenges
        between teams

        This command can be used to cancel a challenge that has already been
        created. This can be useful for when a challenge needs to be removed
        due to a technical issue.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            challenger_team (str): The name of the team that made the challenge.

        Example:
            /admin_cancel_challenge Echo

        Output:
            The challenge made by Team Echo in the 3v3 division has been canceled by an Administrator.
        """
        logger.info(f'Command "admin_cancel_challenge" invoked by {ctx.author} with challenger_team={challenger_team}')
        result = self.ladder_manager.admin_cancel_challenge(challenger_team)
        await ctx.send(result)
    
    @commands.command()
    async def report_win(self, ctx, winning_team):
        """
        Command for all users to report who won
        their match between the challenger and challenged team.

        Rank change will occur if the winning team was the challenger
        with the challenger team moving at most two ranks up, and the 
        challenged team will always only move one spot down. 
        If the winning team was the challenged team, no rank changes will occur.
        
        Example: If Bravo Rank 5 challenges and beats Alpha Rank 3, they become Bravo 3
        and Alpha 4. A "swap" would occur if the teams are directly above and below
        each other in the standings by rank.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            winning_team (str): The name of the team that won the match.

        Example:
            /report_win Echo

        Output:
            Team Echo has won the match and taken the rank of Team Delta! Team Delta moves down one in the ranks.
            Team Delta has won the match against Team Echo, but no rank changes occur since Team Delta was the challenged team.
        """
        logger.info(f'Command "report_win" invoked by {ctx.author} with winning_team={winning_team}')
        result = await self.ladder_manager.report_win(ctx, winning_team)
        await ctx.send(result)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_report_win(self, ctx, winning_team):
        """
        This command works exactly like report_win, but is available only to
        administrators. This command is useful for when an administrator needs
        to manually edit the standings of a division for any reason.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            winning_team (str): The name of the team that won the match.

        Example:
            /admin_report_win Echo

        Output:
            Team Charlie has won the match and taken the rank of Team Alpha! Team Alpha moves down one in the ranks. This report was made by an Administrator.
            Team Alpha has won the match against Team Charlie, but no rank changes occur since Team Alpha was the challenged team. This report was made by an Administrator.
        """
        logger.info(f'Command "admin_report_win" invoked by {ctx.author} with winning_team={winning_team}')
        result = await self.ladder_manager.admin_report_win(ctx, winning_team)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_rank(self, ctx, team_name: str, new_rank: int):
        """
        Admin method for manually changing
        the rank a given team and adjusting
        the other teams ranks accordingly.

        This command is useful for when a team needs to be moved to a
        specific rank, for example, if a team needs to be moved to the top
        of the ladder.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            team_name (str): The name of the team to have its rank changed.
            new_rank (int): The new rank of the given team.

        Example:
            /set_rank Alpha 1

        Output:
            Team Alpha has been assigned to the rank of 1 in the 1v1 division.
        """
        logger.info(f'Command "set_rank" invoked by {ctx.author} with team_name={team_name} new_rank={new_rank}')
        result = self.ladder_manager.set_rank(team_name, new_rank)
        await ctx.send(result)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_win(self, ctx, team_name: str):
        """
        Admin method to manually increment
        ONE win to the given team

        This command is useful for when a team needs to be given a win
        for a match due to technical error.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            team_name (str): The name of the team to have its win count incremented.

        Example:
            /add_win Alpha

        Output:
            Team Alpha has been given a win by an Administrator.
        """
        logger.info(f'Command "add_win" invoked by {ctx.author} with team_name={team_name}')
        result = self.ladder_manager.add_win(team_name)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def subtract_win(self, ctx, team_name: str):
        """
        Admin method to manually decrement
        ONE win to the given team

        This command is useful for when a team needs to have a win
        revoked due to technical error.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            team_name (str): The name of the team to have its win count decremented.

        Example:
            /subtract_win Alpha

        Output:
            Team Bravo has had a win taken away by an Administrator. They now have 5 wins.
        """
        logger.info(f'Command "subtract_win" invoked by {ctx.author} with team_name={team_name}')
        result = self.ladder_manager.subtract_win(team_name)
        await ctx.send(result)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_loss(self, ctx, team_name: str):
        """
        Admin method to manually increment
        ONE loss to the given team

        This command is useful for when a team needs to be given a loss
        for a match due to technical error.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            team_name (str): The name of the team to have its loss count incremented.

        Example:
            /add_loss Delta

        Output:
            Team Delta has been given a loss by an Administrator.
        """
        logger.info(f'Command "add_loss" invoked by {ctx.author} with team_name={team_name}')
        result = self.ladder_manager.add_loss(team_name)
        await ctx.send(result)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def subtract_loss(self, ctx, team_name: str):
        """
        Admin method to manually decrement
        ONE loss to the given team

        This command is useful for when a team needs to have a loss
        removed due to technical error.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            team_name (str): The name of the team to have its loss count decremented.

        Example:
            /subtract_loss Delta

        Output:
            Team Charlie has had a loss taken away by an Administrator. They now have 2 losses.
        """
        logger.info(f'Command "subtract_loss" invoked by {ctx.author} with team_name={team_name}')
        result = self.ladder_manager.subtract_loss(team_name)
        await ctx.send(result)
    
    @commands.command()
    async def post_standings(self, ctx, division_type: str):
        """
        This command is useful for when a user wants to quickly
        see the current standings of a division without needing
        to go to the #standings channel.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /post_standings 1v1

        Output: Formatted table of the standings in the given division
        """
        logger.info(f'Command "post_standings" invoked by {ctx.author} with division_type={division_type}')
        result = await self.ladder_manager.post_standings(division_type)
        await ctx.send(result)

    @commands.command()
    async def post_challenges(self, ctx, division_type: str):
        """
        This command is useful for when a user wants to quickly
        see the current challenges of a division without needing
        to go to the #challenges channel.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /post_challenges 1v1

        Output: Formatted table of the current challenges in the given division
        """
        logger.info(f'Command "post_challenges" invoked by {ctx.author} with division_type={division_type}')
        result = await self.ladder_manager.post_challenges(division_type)
        await ctx.send(result)
    
    @commands.command()
    async def post_teams(self, ctx, division_type: str):
        """
        This command is useful for when a user wants to quickly
        see the current teams of a division without needing
        to go to the #teams channel.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /post_teams 3v3

        Output: Formatted table of the current teams in the given division
        """
        logger.info(f'Command "post_teams" invoked by {ctx.author} with division_type={division_type}')
        result = await self.ladder_manager.post_teams(division_type)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_standings_channel(self, ctx, division_type: str, channel: discord.TextChannel):
        """
        Admin command to set the updating
        standings board to specified channel
        for the given division type.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).
            channel (discord.TextChannel): The channel to which the standings board will be posted.

        Example:
            /set_standings_channel 1v1 #1v1-standings

        Output:
            The 1v1 standings channel has been set to #1v1-standings
        """
        logger.info(f'Command "set_standings_channel" invoked by {ctx.author} with division_type={division_type} channel={channel}')
        result = await self.ladder_manager.set_standings_channel(division_type, channel)
        await ctx.send(result)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear_standings_channel(self, ctx, division_type: str):
        """
        Admin method to clear a division's standings
        channel that has been set

        This command is useful for when an admin want to remove
        the standings channel for a division.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /clear_standings_channel 3v3

        Output:
            The standings channel for the 3v3 division has been cleared.
        """
        logger.info(f'Command "clear_standings_channel" invoked by {ctx.author} with division_type={division_type}')
        result = self.ladder_manager.clear_standings_channel(division_type)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_challenges_channel(self, ctx, division_type: str, channel: discord.TextChannel):
        """
        Admin method to set the updating
        challenges channel to specified channel
        for the given division type.

        This command is useful for when an admin want to set
        the channel that the challenges will be posted to.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).
            channel (discord.TextChannel): The channel to which the challenges board will be posted.

        Example:
            /set_challenges_channel 2v2 #2v2-challenges

        Output:
            The 2v2 challenges channel has been set to #2v2-challenges
        """
        logger.info(f'Command "set_challenges_channel" invoked by {ctx.author} with division_type={division_type} channel={channel}')
        result = await self.ladder_manager.set_challenges_channel(division_type, channel)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear_challenges_channel(self, ctx, division_type: str):
        """
        Admin method to clear a division's challenges
        channel that has been set

        This command is useful for when the challenges channel
        for a division needs to be removed.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /clear_challenges_channel 1v1

        Output:
            The challenges channel for the 1v1 division has been cleared.
        """
        logger.info(f'Command "clear_challenges_channel" invoked by {ctx.author} with division_type={division_type}')
        result = self.ladder_manager.clear_challenges_channel(division_type)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_teams_channel(self, ctx, division_type: str, channel: discord.TextChannel):
        """
        Admin method to set the updating
        teams channel to specified channel
        for the given division type.

        This command is useful for when an admin want to set
        the channel that the challenges will be posted to.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).
            channel (discord.TextChannel): The channel to which the teams board will be posted.

        Example:
            /set_teams_channel 3v3 #3v3-teams

        Output:
            The 3v3 teams channel has been set to #3v3-teams
        """
        logger.info(f'Command "set_teams_channel" invoked by {ctx.author} with division_type={division_type} channel={channel}')
        result = await self.ladder_manager.set_teams_channel(division_type, channel)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear_teams_channel(self, ctx, division_type: str):
        """
        Admin method to clear a division's teams
        channel that has been set

        This command is useful for when the challenges channel
        for a division needs to be removed.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /clear_teams_channel 1v1

        Output:
            The challenges channel for the 1v1 division has been cleared.
        """
        logger.info(f'Command "clear_teams_channel" invoked by {ctx.author} with division_type={division_type}')
        result = self.ladder_manager.clear_teams_channel(division_type)
        await ctx.send(result)
    
    # NOTE: STATS RELATED COMMANDS

    @commands.command()
    async def my_stats(self, ctx):
        """
        TODO: Command to tell LadderManager to provide all stats tracked
        for the caller of this command. The LadderManager requests a stat
        report from the StatManager, who uses their tools of parsing the database
        to compile a my_stats_report for the user based off of their Discord ID
        which is gained from the ctx on the call itself.
        """
        logger.info(f'Command "my_stats" invoked by {ctx.author}')
        result = self.ladder_manager.request_my_stats_report(ctx)
        await ctx.send(result)


    @commands.command(name='show_help', help='Provides a link to the bot documentation.')
    async def show_help(self, ctx):
        """
        Provides a link to the bot documentation.

        This command is useful for when a user wants to quickly
        access the bot's documentation.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.

        Example:
            /show_help

        Output: A link to the bot's documentation.
        """
        logger.info(f'Command "show_help" invoked by {ctx.author}')
        help_text = """
        📖 **For more detailed information, refer to the bot's documentation.**
        ** https://github.com/Theinfection91/Ladderbot3.0/blob/main/Ladderbot3Doc.md ** 📖
        """
        # Send the help text to the channel this method was called from
        await ctx.send(help_text)

# Define bot prefix and intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

async def main():
    ladder_manger = LadderManager(bot)

    # Add cog (class) to the bot
    await bot.add_cog(Ladderbot(bot, ladder_manger))

    
    """
    NOTE: IF USING A MANUAL TOKEN, GO BACK TO TOP OF CODE AND DELETE THE 'from my_token import MY_DISCORD_TOKEN' LINE
    Remove the MY_DISCORD_TOKEN variable below and enter paste your Discord Bot Token in-between a pair of single quotes and save file
        
        Example: await bot.start('long_string_that_is_your_discord_token')
        
    """
    

    """
    NOTE: ALTERNATIVELY, CREATE A FILE CALLED my_token.py IN SAME FOLDER AS main.py
    INSIDE my_token.py YOU ONLY NEED ONE LINE OF CODE WHICH IS:
    
        MY_DISCORD_TOKEN = 'long_string_that_is_your_discord_token'
    
    BY DOING THIS METHOD, DO NOT DELETE THE 'from my_token import MY_DISCORD_TOKEN' AT TOP OF THIS CODE
    
    """
    await bot.start(MY_DISCORD_TOKEN)

asyncio.run(main())