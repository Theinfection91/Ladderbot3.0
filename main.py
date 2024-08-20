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
    async def register_team(self, ctx, division_type: str, team_name: str, *members: discord.Member):
        """
        Registers a new team within a specified division.

        Args:
            ctx (discord.ext.commands.Context): The context of the command.
            division_type (str): The type of the division (1v1, 2v2, or 3v3).
            team_name (str): The name of the team.
            *members (discord.Member): The members of the team.

        Example:
            /register_team 2v2 Alpha @Ixnay @Flaw

        Output:
            Team Alpha has been registered in the 2v2 division with the following members: Ixnay, Flaw
        """
        result_message = self.ladder_manager.register_team(division_type, team_name, *members)
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