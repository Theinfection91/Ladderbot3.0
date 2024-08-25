## Overview
**Ladderbot3.0** is a versatile Discord bot designed to manage and facilitate competitive ladder systems for teams within various divisions. This bot leverages the `LadderManager` class to interact with the underlying database, enabling a range of functionalities through Discord commands which the bot handles by using a variety of helper or validator functions and methods. This is still a work in progress but overall it is stable and functions even better than my previous 2.0 version. Below you will find it's current features and also a list of things to come that I am currently creating ideas for or already working on. Thank you for your time and interest in this project, I have just started learning Python and programming in general over the last year and am excited to share my work and also keep learning as much as possible in the process. You can submit issues in the issues tab or message me on Discord at `Theinfection1991`.

### **Refer to Ladderbot3.0 Documentation for more in-depth information on all commands:** 
- **https://github.com/Theinfection91/Ladderbot3.0/blob/main/Ladderbot3Doc.md**

### Key Features:

- **Ladder Management**: Start and end ladders for specific divisions (1v1, 2v2, 3v3) with administrative commands.
- **Team Management**: Register and remove teams from the ladder
- **Challenge System**: Allow teams to challenge each other and manage these challenges. Admins have additional capabilities to manually create or cancel challenges.
- **Match Reporting**: Report match results to update standings and ranks, with both user-level and admin-level commands for reporting wins and adjusting ranks.
- **Standings and Challenges**: Post current standings and challenges in specific channels, with options to set channels for automatic updates.
- **Administrative Controls**: Admins have extended functionalities to manually adjust team ranks, wins, and losses.
- **Teams Channels (INTRODUCED AND IN-PROGESS)**: You can now use /post_teams <division_type> to have the bot spit out a table similar to challenges and standings of the teams in that division and their member(s). Soon there will be a way of displaying teams and all of their members into a specific channel for a given division, like how standings and challenges channels currently work.
- **Logging System (INTRODUCED AND IN-PROGESS)**: Have access to a ladderbot.log file in the logs folder that will keep track of command invokes by every user, show what parameters were being passed through methods, and allow a way to visually see and keep track of errors. This is still being implemented through out the program, and may eventually lead to having commands in the bot to show and filter certain aspects of the log files within a certain given parameters. The log files are set to begin removing data at 5MB and will hold a maximum of 5 back up copies of the log.

### Things to Come:

- **Improved Error Handling**: More error messages when forgetting a parameter or using the wrong one. Currently some commands will not generate a response if used incorrectly, and even though nothing is happening in the backend it can worry the user that some data may have changed and they can't be sure because the bot didn't say anything.
- **Open To New Ideas**: If you have any unique and creative ideas, or even a little one or tiny tweak you think would work well with this tournament manager, then please do not hesitate to let me know. I'm very open to new ideas as I really love doing this, but sometimes I work better when being asked to create something rather than trying to figure one out on my own.

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
