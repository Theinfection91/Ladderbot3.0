## Overview
**Ladderbot3.0** is a versatile Discord bot designed to manage and facilitate competitive ladder systems for teams within various divisions. This bot leverages the `LadderManager` class to interact with the underlying database, enabling a range of functionalities through Discord commands. 

### Key Features:

- **Ladder Management**: Start and end ladders for specific divisions (1v1, 2v2, 3v3) with administrative commands.
- **Team Management**: Register and remove teams from the ladder
- **Challenge System**: Allow teams to challenge each other and manage these challenges. Admins have additional capabilities to manually create or cancel challenges.
- **Match Reporting**: Report match results to update standings and ranks, with both user-level and admin-level commands for reporting wins and adjusting ranks.
- **Standings and Challenges**: Post current standings and challenges in specific channels, with options to set channels for automatic updates.
- **Administrative Controls**: Admins have extended functionalities to manually adjust team ranks, wins, and losses.

**REFER TO BOT DOCUMENTATION FOR MORE IN-DEPTH INFO:** 
- https://github.com/Theinfection91/Ladderbot3.0/blob/main/Ladderbot3Doc.md

# Discord Bot Token Usage

To properly use the Discord bot token with your program, you have two options: manually entering the token directly in the code or using a separate Python file to import the token.

## Option 1: Manual Token Entry

1. **Delete the import statement:**

   If you prefer to manually enter your token, remove the following line from the top of your code:
   
   ```python
   from my_token import MY_DISCORD_TOKEN

2. **Add your token in the main() function:**

   In the main() function located at the very bottom of the code, replace the MY_DISCORD_TOKEN variable with your actual Discord bot token. Make sure to enclose the token string in single quotes:

   ```python
   await bot.start('your_discord_token_here')
   ```
   This method is straightforward but requires you to manually edit your code whenever you want to change the token.

## Option 2: Import Token from a Separate File

1. **Create a my_token.py file:**

   If you prefer to keep your token separate, create a new file called my_token.py in the same directory as main.py

2. **Add your token to my_token.py:**

   Inside my_token.py, include the following line of code, replacing 'your_long_discord_token_here' with your actual token. Again, make sure to enclose the token string in single quotes:

   ```python
   MY_DISCORD_TOKEN = 'your_discord_token_here'
   ```

3. **Keep the import statement:**

   Ensure that the following line remains at the top of your main script:

   ```python
   from my_token import MY_DISCORD_TOKEN
   ```
