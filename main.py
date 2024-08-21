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
    async def remove_team(self, ctx, team_name, division_type):
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
    async def challenge(self, ctx, challenger_team, challenged_team):
        """
        This challenge function will be usable by everyone
        and users will not need to specify which division
        since team names are set to be unique across
        all divisions (Cant have a Team Alpha in 1v1 and Team Alpha in 2v2)
        """
        result_message = self.ladder_manager.challenge(challenger_team, challenged_team)
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