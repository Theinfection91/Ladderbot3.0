import discord
from discord.ext import commands
import asyncio

from ladder_manager import LadderManager

from my_token import MY_DISCORD_TOKEN

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
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def start_ladder(self, ctx, division_type: str):
        """
        Method for starting the ladder in
        a given division type
        """
        result = self.ladder_manager.start_ladder(division_type)
        await ctx.send(result)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def end_ladder(self, ctx, division_type: str):
        """
        Method for ending the ladder in
        a given division type
        """
        result = self.ladder_manager.end_ladder(division_type)
        await ctx.send(result)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def register_team(self, ctx, team_name: str,  division_type: str, *members: discord.Member):
        """
        Registers a new team within a specified division.

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
        result_message = self.ladder_manager.register_team(division_type, team_name, *members)
        await ctx.send(result_message)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_team(self, ctx, team_name: str, division_type: str):
        """
        Removes a team within a specifed division

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            team_name (str): The name of the team.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).

        Example:
            /remove_team Delta 1v1

        Output:
            Team Delta from the 1v1 division has been removed from the Ladder.
        """
        result_message = self.ladder_manager.remove_team(division_type, team_name)
        await ctx.send(result_message)

    @commands.command()
    async def challenge(self, ctx, challenger_team: str, challenged_team: str):
        """
        This challenge function will be usable by everyone
        and users will not need to specify which division
        since team names are set to be unique across
        all divisions (Cant have a Team Alpha in 1v1 and Team Alpha in 2v2)
        """
        result_message = self.ladder_manager.challenge(ctx, challenger_team, challenged_team)
        await ctx.send(result_message)

    @commands.command()
    async def cancel_challenge(self, ctx, challenger_team: str):
        """
        Will cancel the challenge of a given challenger team
        """
        result_message = self.ladder_manager.cancel_challenge(ctx, challenger_team)
        await ctx.send(result_message)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_challenge(self, ctx, challenger_team: str, challenged_team: str):
        """
        Admin method for manually creating challenges
        between teams
        """
        result_message = self.ladder_manager.admin_challenge(challenger_team, challenged_team)
        await ctx.send(result_message)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_cancel_challenge(self, ctx, challenger_team: str):
        """
        Admin method for manually cancelling challenges
        between teams
        """
        result_message = self.ladder_manager.admin_cancel_challenge(challenger_team)
        await ctx.send(result_message)
    
    @commands.command()
    async def report_win(self, ctx, winning_team):
        """
        Command for all users to report who won
        their match between the challenger and challenged team.
        """
        result_message = self.ladder_manager.report_win(ctx, winning_team)
        await ctx.send(result_message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_report_win(self, ctx, winning_team):
        """
        Command for Admins only to report who won
        a match, giving the winning team just like report_win
        """
        result_message = self.ladder_manager.admin_report_win(winning_team)
        await ctx.send(result_message)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_rank(self, ctx, team_name: str, new_rank: int):
        """
        Admin method for manually changing
        the rank a given team and adjusting
        the other teams ranks accordingly.
        """
        result_message = self.ladder_manager.set_rank(team_name, new_rank)
        await ctx.send(result_message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_test_teams(self, ctx, division_type):
        """
        Create 5 test teams fast for debugging
        """
        result_message = self.ladder_manager.create_test_teams(division_type)
        await ctx.send(result_message)

# Define bot prefix and intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def main():
    ladder_manger = LadderManager()

    # Add cog (class) to the bot
    await bot.add_cog(Ladderbot(bot, ladder_manger))

    # Add Discord Token for bot received from Discord Developer Portal
    await bot.start(MY_DISCORD_TOKEN)

asyncio.run(main())