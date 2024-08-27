import discord
from discord.ext import tasks

from stat_manager import StatManager
from rival_manager import RivalManager

from database import initialize_database, count_teams, db_register_team, db_remove_team, db_set_rank, db_update_rankings, is_team_name_unique, is_member_registered, is_member_on_team, check_team_division, does_team_exist, is_team_challenged, has_team_challenged, find_opponent_team, give_team_rank, db_register_challenge, db_remove_challenge, add_team_wins_losses, remove_challenge, is_ladder_running, set_ladder_running, subtract_team_wins_losses, get_wins_or_losses, get_standings_data, get_challenges_data, db_set_standings_channel, db_set_challenges_channel, is_standings_channel_set, get_standings_channel_id, is_challenges_channel_set, get_challenges_channel_id, db_clear_standings_channel, db_clear_challenges_channel, get_team_members, db_clear_all_challenges, db_clear_all_teams, get_teams_data, db_set_teams_channel, db_clear_teams_channel, is_teams_channel_set, get_teams_channel_id, is_member_in_members_table, db_register_member, add_division_win, add_division_loss

from utils import is_correct_member_size, is_valid_division_type, has_duplicate_members, create_members_string, format_standings_data, format_challenges_data, format_teams_data, add_time_stamp

from config import VALID_DIVISION_TYPES

from logs.logger import logger 

class LadderManager:
    """
    This class will handle talking to the different divisions within
    the entire program itself. There will be 1v1, 2v2, and 3v3. The
    LadderManager will also call on different helpers, validators,
    and parsing the database as well as other features.

    The LadderManager is controlled by the Ladderbot in main.py
    """
    def __init__(self, bot):
        """
        Constructs the LadderManager class

        The LadderManager will help register teams, and challenges
        for every division in the Ladder. When a team wants to be registered
        the LadderManager will do various things like checking to see if the
        team name already exists, checking if a member trying to register
        is already apart of a team in the same division, and various
        other tasks that a manager of a tournament would do.
        """
        self.bot = bot

        # Instantiate the StatManager and RivalManager
        self.stat_manager = StatManager()
        self.rival_manager = RivalManager()
        
        #Init the ladderbot.db when the LadderManager is instantiated
        initialize_database()

        # Starts the update of standings, challenges, and teams if they are set
        self.periodic_update_standings.start()
        self.periodic_update_challenges.start()
        self.periodic_update_teams.start()

    def create_test_teams(self, division_type: str) -> str:

        if not is_valid_division_type(division_type):
            logger.error(f'LadderManager: Wrong division type given for "create_test_teams". User entered: {division_type}')
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again. ❌"


        if division_type == '1v1':
            
            db_register_team('1v1', "Alpha", "TestName1")
            db_register_team('1v1', "Bravo", "TestName2")
            db_register_team('1v1', "Charlie", "TestName3")
            db_register_team('1v1', "Delta", "TestName4")
            db_register_team('1v1', "Echo", "TestName5")
            return f"Created five 1v1 test teams"
        
        if division_type == '2v2':
            db_register_team('2v2', "Apple", "TestName1, TestName10")
            db_register_team('2v2', "Butler", "TestName2, TestName1337")
            db_register_team('2v2', "Carlos", "TestName123165, TestName112312")
            db_register_team('2v2', "Dynasty", "TestName3425, TestName15234123")
            db_register_team('2v2', "Ellen", "TestName11323, TestName1123124")
            return f"Created five 2v2 test teams"
        
        if division_type == '3v3':
            db_register_team('3v3', "AngelWing", "Theinfection1991, TestName87650, TestNameLength")
            db_register_team('3v3', "Bittersweet", "TestName12435, TestName654, TestName1267544")
            db_register_team('3v3', "Corn", "TestName3242634, Ladderbot3, TestName96")
            db_register_team('3v3', "DeerDiary", "TestName323266, TestName73546, TestNamTestNameeLength")
            db_register_team('3v3', "Elephant", "TestName2632464, LadTestNameTestNamederbot3, TestName6t234652Length")
            return f"Created five 3v3 test teams"
  
    async def on_ready(self):
        """
        Logic for on_ready listener for when
        the bot starts up
        """
        # Show the bot has logged in to server showing it's username
        print(f"Logged in as {self.bot.user}")
        logger.info(f'LadderManager: "on_ready" initiated. Logged in as {self.bot.user}')

        # Check if any ladders are currently running, if so print which ones
        for division_type in VALID_DIVISION_TYPES:
        # Ladder Running Check
            if is_ladder_running(division_type):
                logger.info(f'LadderManager: "on_ready" found ladder running in {division_type} division.')
                print(f"The {division_type} division of the ladder is currently running.")

            # Challenge Channel Logic
            if is_challenges_channel_set(division_type):
                challenge_channel_id = get_challenges_channel_id(division_type)
                challenge_channel = self.bot.get_channel(challenge_channel_id)
                logger.info(f'LadderManager: "on_ready" found challenges channel ID {challenge_channel} set for {division_type} division.')

                if isinstance(challenge_channel, discord.TextChannel):
                    await self.update_challenges_message(division_type, challenge_channel)
                    logger.info(f'LadderManager: "on_ready" updating the challenges channel message in {challenge_channel} for {division_type} division.')
                    self.periodic_update_challenges.restart()
                    logger.info(f'LadderManager: "on_ready" starting the periodic update to the challenges channel in {challenge_channel} for {division_type} division.')
            else:
                logger.warning(f'LadderManager: "on_ready" no challenges channel set for {division_type} division.')

            # Standings Channel Logic
            if is_standings_channel_set(division_type):
                standings_channel_id = get_standings_channel_id(division_type)
                standings_channel = self.bot.get_channel(standings_channel_id)
                logger.info(f'LadderManager: "on_ready" found standings channel ID {standings_channel} set for {division_type} division.')

                if isinstance(standings_channel, discord.TextChannel):
                    await self.update_standings_message(division_type, standings_channel)
                    logger.info(f'LadderManager: "on_ready" updating the standings channel message in {standings_channel} for {division_type} division.')
                    self.periodic_update_standings.restart()
                    logger.info(f'LadderManager: "on_ready" starting the periodic update to the standings channel in {standings_channel} for {division_type} division.')
            else:
                logger.warning(f'LadderManager: "on_ready" no standings channel set for {division_type} division.')
            
            # Standings Channel Logic
            if is_teams_channel_set(division_type):
                teams_channel_id = get_teams_channel_id(division_type)
                teams_channel = self.bot.get_channel(teams_channel_id)
                logger.info(f'LadderManager: "on_ready" found teams channel ID {standings_channel} set for {division_type} division.')

                if isinstance(teams_channel, discord.TextChannel):
                    await self.update_teams_message(division_type, standings_channel)
                    logger.info(f'LadderManager: "on_ready" updating the teams channel message in {teams_channel} for {division_type} division.')
                    self.periodic_update_teams.restart()
                    logger.info(f'LadderManager: "on_ready" starting the periodic update to the teams channel in {teams_channel} for {division_type} division.')
            else:
                logger.warning(f'LadderManager: "on_ready" no teams channel set for {division_type} division.')
    
    def start_ladder(self, division_type: str) -> str:
        """
        Start the ladder for a given division type.
        """
        if not is_valid_division_type(division_type):
            logger.error(f'LadderManager: Wrong division type given for "start_ladder". User entered: {division_type}')
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again. ❌"
        
        if is_ladder_running(division_type):
            logger.error(f'LadderManager: The division given for "start_ladder" is already running. User entered: {division_type}')
            return f"❌ The {division_type} division of the ladder is already running... ❌"
        
        set_ladder_running(division_type, True)
        logger.info(f'LadderManager: The {division_type} division of the ladder has started using "start_ladder" {division_type}')
        return f"🔥 The {division_type} division of the ladder has started! 🔥"
    
    async def end_ladder(self, division_type):
        """
        End the ladder for a given division type.
        """
        # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            logger.error(f'LadderManager: Wrong division type given for "end_ladder". User entered: {division_type}')
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again. ❌"

        if not is_ladder_running(division_type):
            logger.error(f'LadderManager: The ladder for given division for "end_ladder" is not running. User entered: {division_type}')
            return f"❌ The {division_type} division of the ladder is not currently running... ❌"
        
        final_standings = await self.post_standings(division_type)
        
        # Set ladder running to False for given division
        set_ladder_running(division_type, False)
        logger.info(f'LadderManager: The {division_type} division of the ladder has ended using "end_ladder" {division_type}')

        # Clear challenges and teams for given division
        db_clear_all_challenges(division_type)
        logger.info(f'LadderManager: All challenges in {division_type} division of the ladder has been erased.')
        db_clear_all_teams(division_type)
        logger.info(f'LadderManager: All teams in {division_type} division of the ladder has been removed.')

        end_ladder_message = f"\t\t💥 The {division_type} division of the ladder has ended! 💥\n\n"
        end_ladder_message += final_standings
        logger.info(f'LadderManager: Generated string informing users the {division_type} ladder has ended and prints the final standings for the {division_type} division.')
        return end_ladder_message

    def register_team(self, division_type: str, team_name: str, *members: discord.Member):
        """
        Takes the input from the discord user and
        uses a series of help and validation functions
        and conditions to make sure the correct information
        has been given to make a team correctly.
        """
        # Check if team name is unique and no other team is named the same in ANY division
        if is_team_name_unique(team_name):

            # Check if correct divison type was entered
            if is_valid_division_type(division_type):

                # Check if correct amount of members was given for the division type
                if is_correct_member_size(division_type, *members):

                    # NOTE: Uncomment triple quotes to check if member is already registered on division type team
                    #-----------------------------------------------

                    # Create a list of all the members display names
                    member_display_names = [member.display_name for member in members]

                    # Checks every members display name against the database
                    for member_display_name in member_display_names:
                        
                        # If a player is already registered on a team in a given division type the process is stopped
                        if is_member_registered(division_type, member_display_name):
                            logger.error(f'LadderManager: Member already found on team in given division type. User entered: division_type={division_type} conflicting_member={member_display_name}')     
                            return f"{member_display_name} is already registered on a team in the {division_type} division. Please try again."
                        
                    # Pass *members: discord.Member object as members                  
                    if has_duplicate_members(members):
                        logger.error(f'LadderManager: The same member is trying to be registered to the same team twice: division_type={division_type} members={member_display_names}')
                        return f"❌ You are trying to register the same member twice. Please try again. Members entered: {member_display_names} ❌"
                    
                    # NOTE :----------------------------------------
                        
                    # Turn all members into a string for the database
                    members_string = create_members_string(*members)

                    # Add team to the database with the given arguments
                    db_register_team(division_type, team_name, members_string)
                    logger.info(f'LadderManager: Successfully created new team with following parameters: team_name={team_name} division_type={division_type} members={members_string}')

                    # Checks if members on team are already in the members table for stat tracking, if not they are added
                    for member in members:
                        if not is_member_in_members_table(member.id):
                            db_register_member(member.display_name, member.id)
                            logger.info(f'LadderManager: Member on team not found in members table for stat tracking. Registering: {member.display_name} {member.id} to database')
                        else:
                            self.stat_manager.increment_all_teams_count(member.id)
                            logger.info(f'LadderManager: {member.display_name} {member.id} has had 1 added to their all_teams_count for stat tracking.')

                    # Return confirmation message
                    return f"🎖️ Team {team_name} has been registered in the {division_type} division with the following members: {members_string} 🎖️"
                
                else:
                    members_list = [member.display_name for member in members]
                    logger.error(f'LadderManager: Wrong amount of members given for division type. User entered: division_type={division_type} members={members_list}')
                    return "❌ Please enter the correct amount of members depending on the division type. ❌"
                
            else:
                logger.error(f'LadderManager: Wrong division type given for "register_team". User entered: {division_type}')
                return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again. ❌"
            
        else:
            logger.error(f'LadderManager: team_name already found in database for "register_team". User entered: {team_name}')
            return f"❌ Team {team_name} is already being used. Please choose another team name. ❌"
        
    def remove_team(self, team_name):
        """
        Finds the correct team and tells
        the database to remove them completely
        """
        # See if team exists in the database
        if not does_team_exist(team_name):
            logger.error(f'LadderManager: No team with given team_name found in database for "remove_team". User entered: {team_name}')
            return f"❌ No team found by the name of {team_name}. Please try again. ❌"
        
        # If team exists grab the division they are in
        division_type = check_team_division(team_name)

        db_remove_team(division_type, team_name)
        logger.info(f'LadderManager: Successfully removed team from {division_type} division with following parameters: team_name={team_name}')
        return f"🛑 Team {team_name} from the {division_type} division has been removed from the Ladder. 🛑"

    async def get_member_id_from_display_names(self, guild: discord.Guild, members_string: str):
        """
        
        """
        display_names = [name.strip() for name in members_string.split(",")]
        member_ids = []
        
        for display_name in display_names:
            member = discord.utils.get(guild.members, display_name=display_name)
            if member:
                member_ids.append(member.id)
            else:
                print(f"Member with display name '{display_name}' not found in guild {guild.name}.")
        
        return member_ids

    async def send_challenge_notification(self, ctx, challenger_team, challenged_team):
        """
        Sends a notification to all members of the challenged team that they have been challenged.
        """
        # Grab guild object from context
        guild = ctx.guild

        # Grab division type for custom message
        division_type = check_team_division(challenged_team)

        # Retrieve the members string and ensure it's in the correct format
        members_string_tuple = get_team_members(challenged_team)
        if isinstance(members_string_tuple, tuple) and len(members_string_tuple) == 1:
            members_string = members_string_tuple[0]
        else:
            print("Unexpected format for members_string:", members_string_tuple)
            return  # Early exit if the format is unexpected

        member_ids = await self.get_member_id_from_display_names(guild, members_string)

        for member_id in member_ids:
            member = self.bot.get_user(member_id)
            if member is not None:
                try:
                    # If member is found, send a message displaying who challenged them
                    logger.info(f'LadderManager: Successfully sent challenge notification using parameters: challenger_team={challenger_team} challenged_team={challenged_team} | Sent notification to: members={members_string}')
                    await member.send(f"⚔️ Your team, Team {challenged_team}, has been challenged by Team {challenger_team} in the {division_type} division! ⚔️")
                except all as e:
                    error_message = f"Could not send a message to {member} (ID: {member_id})."
                    logger.error(error_message)
                    print(f"{error_message} Error: {str(e)}")
            else:
                error_message = f"LadderManager: Member with ID {member_id} not found."
                logger.error(error_message)
                print(error_message)

    async def challenge(self, ctx, challenger_team: str, challenged_team: str):
        """
        Checks if teams exist, checks what division
        type the teams are in, checks if either team
        are currently under a challenge, checks if
        challenger team is one or two ranks below the
        challenged team,
        """
        # Check if both teams exist
        if not does_team_exist(challenger_team):
            logger.error(f'LadderManager: No challenger team found for "challenge". User entered: challenger_team={challenger_team}')
            return f"❌ No team found by the name of {challenger_team}. Please try again. ❌"
        
        if not does_team_exist(challenged_team):
            logger.error(f'LadderManager: No challenged team found for "challenge". User entered: challenged_team={challenged_team}')
            return f"❌ No team found by the name of {challenged_team}. Please try again. ❌"
        
        # Capture the author of the command call's display name
        display_name = ctx.author.display_name

        # Check if the person calling the command is apart of the challenger team
        if not is_member_on_team(display_name, challenger_team):
            logger.error(f'LadderManager: User invoking command "challenge" is not part of challenger team. User entered: challenger_team={challenger_team} User: {display_name}')
            return f"❌ You are not a member of Team {challenger_team} and may not issue a challenge on their behalf. ❌"
        
        # Check if both teams exist within the same division and stores which divison if so
        challenger_division = check_team_division(challenger_team)
        challenged_division = check_team_division(challenged_team)
        
        if challenger_division != challenged_division:
            logger.error(f'LadderManager: User entered two teams that are not in the same division. User entered: challenger_team={challenger_team} challenger_team_division={challenger_division} | challenged_team={challenged_team} challenged_team_division={challenged_division}')
            return f"❌ Team {challenger_team} and Team {challenged_team} are not in the same division... ❌"
        
        # Set division type to use for helper functions
        division_type = challenger_division
        
        # Check if the ladder is running in the given division type
        if not is_ladder_running(division_type):
            logger.error(f'LadderManager: The ladder is not currently running on the given division_type. User entered: {division_type}')
            return f"❌ The {division_type} division of the ladder has not started yet... Please wait to send challenges. ❌"
        
        # Grab the rank of each team for comparison
        challenger_rank = give_team_rank(division_type, challenger_team)
        challenged_rank = give_team_rank(division_type, challenged_team)

        # Check if the challenging team is challenging either one or two ranks above them
        if challenged_rank > challenger_rank or challenged_rank <= challenger_rank - 3:
            logger.error(f'LadderManager: Teams can only challenge other teams up to two ranks above their current rank. Parameters used: challenger_rank={challenger_rank} challenged_rank={challenged_rank}')
            return f"❌ Teams can only challenge other teams up to two ranks above their current rank. ❌"
        
        # Check if either team has challenged or already been challenged
        if is_team_challenged(division_type, challenged_team):
            logger.error(f'LadderManager: Challenged team has already been challenged. User entered: challenged_team={challenged_team}')
            return f"❌ {challenged_team} has already been challenged by another team and must complete that match first! ❌"
        if has_team_challenged(division_type, challenged_team):
            logger.error(f'LadderManager: Challenged team has already sent out a challenge. User entered: challenged_team={challenged_team}')
            return f"❌ {challenged_team} has already sent out a challenge to a team and must complete that match first! ❌"
        
        if is_team_challenged(division_type, challenger_team):
            logger.error(f'LadderManager: Challenger team has already been challenged. User entered: challenger_team={challenger_team}')
            return f"❌ {challenger_team} has already been challenged by another team and must complete that match first! ❌"
        if has_team_challenged(division_type, challenger_team):
            logger.error(f'LadderManager: Challenger team has already sent out a challenge. User entered: challenger_team={challenger_team}')
            return f"❌ {challenger_team} has already sent out a challenge to a team and must complete that match first! ❌"
        
        # Once all checks are passed then register the challenge in the correct table
        db_register_challenge(division_type, challenger_team, challenged_team)

        try:
            await self.send_challenge_notification(ctx, challenger_team, challenged_team)
        except:
            error_message = 'Error: Most likely tried to send notification to Bot'
            logger.error(f'LadderManager: {error_message}')

        logger.info(f"LadderManager: A challenge in the {division_type} divison has been created between Team {challenger_team} with rank {challenger_rank} as the challenger and Team {challenged_team} with rank {challenged_rank} as the challenged team.")

        result = f"⚔️ Team {challenger_team} has challenged Team {challenged_team} in the {division_type} division! ⚔️"
        return result
    
    def cancel_challenge(self, ctx, challenger_team: str):
        """
        Method used by everyone to cancel a challenge
        sent by mistake or for whatever reason. Since the match ID
        is the challenger team, the only parameter needed will be
        the nane of the challenger team. This method will check
        if the team exists, if the person calling the command
        is apart of the challenger team, and if there actually is
        a challenge sent out by the team. If there is, it is deleted.
        """
        # Check if given team exists in the database
        if not does_team_exist(challenger_team):
            logger.error(f'LadderManager: No challenger team found for "cancel_challenge". User entered: challenger_team={challenger_team}')
            return f"❌ No Team found by the name of {challenger_team}. Please try again. ❌"
        
        # Capture the author of the command call's display name and team division
        display_name = ctx.author.display_name
        team_division = check_team_division(challenger_team)
        
        # Check if the person calling the command is apart of the challenger team
        if not is_member_on_team(display_name, challenger_team):
            logger.error(f'LadderManager: User invoking command "cancel_challenge" is not part of challenger team. User entered: challenger_team={challenger_team} User: {display_name}')
            return f"❌ You are not a member of Team {challenger_team}. ❌"

        # Check if the given team has sent out a challenge
        if not has_team_challenged(team_division, challenger_team):
            logger.error(f'LadderManager: Challenger team has not sent out a challenge to cancel. User entered: challenger_team={challenger_team}')
            return f"❌ No challenge was found where Team {challenger_team} was the Challenger. Please try again. ❌"
        
        # If all checks are passed, delete the specified challenge from correct challenges table
        db_remove_challenge(team_division, challenger_team)
        logger.info(f"LadderManager: Successfully canceled the challenge made by {challenger_team} in the {team_division} division by {display_name}.")
        return f"🚩 The challenge made by Team {challenger_team} in the {team_division} division has been canceled by a team member. 🚩"
    
    async def admin_challenge(self, ctx, challenger_team: str, challenged_team: str):
        """
        This works the same way as challenge but removes the
        functionality of grabbing the display name to
        check if the caller is on the challenger team.
        """
        # Check if both teams exist
        if not does_team_exist(challenger_team):
            logger.error(f'LadderManager: No challenger team found for "admin_challenge". User entered: challenger_team={challenger_team}')
            return f"❌ No team found by the name of {challenger_team}. Please try again. ❌"
        
        if not does_team_exist(challenged_team):
            logger.error(f'LadderManager: No challenged team found for "admin_challenge". User entered: challenged_team={challenged_team}')
            return f"❌ No team found by the name of {challenged_team}. Please try again. ❌"
        
        # Check if both teams exist within the same division and stores which divison if so
        challenger_division = check_team_division(challenger_team)
        challenged_division = check_team_division(challenged_team)
        
        if challenger_division != challenged_division:
            logger.error(f'LadderManager: User entered two teams that are not in the same division. User entered: challenger_team={challenger_team} challenger_team_division={challenger_division} | challenged_team={challenged_team} challenged_team_division={challenged_division}')
            return f"❌ Team {challenger_team} and Team {challenged_team} are not in the same division... ❌"
        
        # Set division type to use for helper functions
        division_type = challenger_division

        # Check if the ladder is running in the given division type
        if not is_ladder_running(division_type):
            logger.error(f'LadderManager: The ladder is not currently running on the given division_type. User entered: {division_type}')
            return f"❌ The {division_type} division of the ladder has not started yet... Please wait to send challenges. ❌"
        
        # Grab the rank of each team for comparison
        challenger_rank = give_team_rank(division_type, challenger_team)
        challenged_rank = give_team_rank(division_type, challenged_team)

        # Check if the challenging team is challenging either one or two ranks above them
        if challenged_rank > challenger_rank or challenged_rank <= challenger_rank - 3:
            logger.error(f'LadderManager: Teams can only challenge other teams up to two ranks above their current rank. Parameters used: challenger_rank={challenger_rank} challenged_rank={challenged_rank}')
            return f"❌ Teams can only challenge other teams up to two ranks above their current rank. ❌"
        
        # Check if either team has challenged or already been challenged
        if is_team_challenged(division_type, challenged_team):
            logger.error(f'LadderManager: Challenged team has already been challenged. User entered: challenged_team={challenged_team}')
            return f"❌ {challenged_team} has already been challenged by another team and must complete that match first! ❌"
        if has_team_challenged(division_type, challenged_team):
            logger.error(f'LadderManager: Challenged team has already sent out a challenge. User entered: challenged_team={challenged_team}')
            return f"❌ {challenged_team} has already sent out a challenge to a team and must complete that match first! ❌"
        
        if is_team_challenged(division_type, challenger_team):
            logger.error(f'LadderManager: Challenger team has already been challenged. User entered: challenger_team={challenger_team}')
            return f"❌ {challenger_team} has already been challenged by another team and must complete that match first! ❌"
        if has_team_challenged(division_type, challenger_team):
            logger.error(f'LadderManager: Challenger team has already sent out a challenge. User entered: challenger_team={challenger_team}')
            return f"❌ {challenger_team} has already sent out a challenge to a team and must complete that match first! ❌"
        
        # Once all checks are passed then register the challenge in the correct table
        db_register_challenge(division_type, challenger_team, challenged_team)
        logger.info(f"LadderManager: A challenge in the {division_type} divison has been created between Team {challenger_team} with rank {challenger_rank} as the challenger and Team {challenged_team} with rank {challenged_rank} as the challenged team.")

        # Send a notificaiton to members in challenged team
        try:
            await self.send_challenge_notification(ctx, challenger_team, challenged_team)
        except:
            print('Error: Most likely tried to send notification to Bot')

        return f"⚔️ Team {challenger_team} has challenged Team {challenged_team} in the {division_type} division! ⚔️ -This challenge was created by an Administrator."
    
    def admin_cancel_challenge(self, challenger_team: str):
        """
        This works the same way as cancel_challenge but removes the
        functionality of grabbing the display name to
        check if the caller is on the challenger team.
        """
        # Check if given team exists in the database
        if not does_team_exist(challenger_team):
            logger.error(f'LadderManager: No challenger team found for "admin_cancel_challenge". User entered: challenger_team={challenger_team}')
            return f"❌ No Team found by the name of {challenger_team}. Please try again. ❌"
        
        # Capture the team division of the challenger team
        team_division = check_team_division(challenger_team)

        # Check if the given team has sent out a challenge
        if not has_team_challenged(team_division, challenger_team):
            logger.error(f'LadderManager: Challenger team has not sent out a challenge to cancel. User entered: challenger_team={challenger_team}')
            return f"❌ No challenge was found where Team {challenger_team} was the Challenger. Please try again. ❌"
        
        # If all checks are passed, delete the specified challenge from correct challenges table
        db_remove_challenge(team_division, challenger_team)
        logger.info(f"LadderManager: Successfully canceled the challenge made by {challenger_team} in the {team_division} division by an Admin.")
        return f"🚩 The challenge made by Team {challenger_team} in the {team_division} division has been canceled by an Administrator. 🚩"
    
    async def report_win(self, ctx, winning_team: str):
        """
        Checks if there is a challenge involving the team name given,
        determines the losing team based on the winning team,
        updates ranks and wins/losses accordingly,
        and removes the challenge from the challenges table.
        """
        # Checks if given team exists
        if not does_team_exist(winning_team):
            logger.error(f'LadderManager: No winning_team name found for "report_win". User entered: winning_team={winning_team}')
            return f"❌ No team found by the name of {winning_team}. Please try again."
        
        # If team exists, grab its division type
        division_type = check_team_division(winning_team)

        # Check if the ladder is running in the given division type
        if not is_ladder_running(division_type):
            logger.error(f'LadderManager: The ladder is not currently running on the given division_type. Parameter used: {division_type}')
            return f"❌ The {division_type} division of the ladder has not started yet... ❌"
        
        # Check if author of command call is on the winning team
        display_name = ctx.author.display_name
        if not is_member_on_team(display_name, winning_team):
            logger.error(f'LadderManager: User not part of winning team tried to report_win. User: {display_name}')
            return f"❌ You are not a member of Team {winning_team}. ❌"
        
        # Check if the given team is the challenger
        if has_team_challenged(division_type, winning_team):
            # Find the opponent team to determine the loser
            losing_team = find_opponent_team(division_type, winning_team)
            
            # Update ranks when challenger wins
            logger.info(f"LadderManager: Challenger team has reported win over opponent challenged team. winning_challenger={winning_team} losing_challenged={losing_team}")
            
            db_update_rankings(division_type, winning_team, losing_team)
            logger.info(f"LadderManager: Winning challenger team: {winning_team} takes the losing challenged team: {losing_team} rank and challenged losing team moves down one rank. Win and loss is added to appropriate teams.")

            #Grab ID's of members to add to stat tracking logic
            winner_members = get_team_members(winning_team)
            loser_members = get_team_members(losing_team)
            guild = ctx.guild

            # Pass information to StatManager to update individual wins and losses for players
            for winner_member in winner_members:
                winner_member_id = await self.get_member_id_from_display_names(guild, winner_member)
                for win_id in winner_member_id:
                    self.stat_manager.add_to_wins_count(win_id, division_type)
                    self.stat_manager.increment_participation_count(win_id)
            
            for loser_member in loser_members:
                loser_member_id = await self.get_member_id_from_display_names(guild, loser_member)
                for loss_id in loser_member_id:
                    self.stat_manager.add_to_losses_count(loss_id, division_type)
                    self.stat_manager.increment_participation_count(loss_id)

            remove_challenge(division_type, winning_team)
            logger.info(f"LadderManager: Challenge from {division_type} division involving Team {winning_team} and Team {losing_team} removed from database.")
            
            return f"🏆 Team {winning_team} has won the match and taken the rank of Team {losing_team}! Team {losing_team} moves down one in the ranks. 🏆"
        else:
            # If the winning team was the challenged team, no rank change occurs
            losing_team = find_opponent_team(division_type, winning_team)

            #Grab ID's of members to add to stat tracking logic
            winner_members = get_team_members(winning_team)
            loser_members = get_team_members(losing_team)
            guild = ctx.guild

            # Pass information to StatManager to update individual wins and losses for players
            for winner_member in winner_members:
                winner_member_id = await self.get_member_id_from_display_names(guild, winner_member)
                for win_id in winner_member_id:
                    self.stat_manager.add_to_wins_count(win_id, division_type)
                    self.stat_manager.increment_participation_count(win_id)
            
            for loser_member in loser_members:
                loser_member_id = await self.get_member_id_from_display_names(guild, loser_member)
                for loss_id in loser_member_id:
                    self.stat_manager.add_to_losses_count(loss_id, division_type)
                    self.stat_manager.increment_participation_count(loss_id)
            
            # LadderManager adds team wins and losses
            add_team_wins_losses(division_type, winning_team, win=True)
            add_team_wins_losses(division_type, losing_team, win=False)

            logger.info(f"LadderManager: Team {winning_team} has won against Team {losing_team} in the {division_type} division, no rank change occurs since {winning_team} was the challenged team.")
            
            remove_challenge(division_type, losing_team)
            logger.info(f"LadderManager: Challenge from {division_type} division involving Team {winning_team} and Team {losing_team} removed from database.")
            
            return f"🏆 Team {winning_team} has won the match against Team {losing_team}, but no rank changes occur since Team {winning_team} was the challenged team. 🏆"
    
    async def admin_report_win(self, ctx, winning_team: str):
        """
        Admin method for reporting wins between teams
        Works just like report_win but doesnt check
        if the author is part of winning_team
        """
        # Checks if given team exists
        if not does_team_exist(winning_team):
            logger.error(f'LadderManager: No winning_team found by name given for "admin_report_win". User entered: winning_team={winning_team}')
            return f"❌ No team found by the name of {winning_team}. Please try again. ❌"
        
        # If team exists, grab its division type
        division_type = check_team_division(winning_team)

        # Check if the ladder is running in the given division type
        if not is_ladder_running(division_type):
            logger.error(f'LadderManager: The ladder is not currently running on the given division_type. Parameter used: {division_type}')
            return f"❌ The {division_type} division of the ladder has not started yet... ❌"
        
        # Check if the given team is the challenger
        if has_team_challenged(division_type, winning_team):
            # Find the opponent team to determine the loser
            losing_team = find_opponent_team(division_type, winning_team)
            logger.info(f"LadderManager: 'admin_report_win' Admn has reported challenger team {winning_team} winning over opponent challenged team {losing_team} in the {division_type} division. winning_challenger={winning_team} losing_challenged={losing_team}")

            # Update ranks when challenger wins
            db_update_rankings(division_type, winning_team, losing_team)
            logger.info(f"LadderManager: 'admin_report_win' Winning challenger team: {winning_team} takes the losing challenged team: {losing_team} rank and challenged losing team moves down one rank. Win and loss is added to appropriate teams.")
            
            #Grab ID's of members to add to stat tracking logic
            winner_members = get_team_members(winning_team)
            loser_members = get_team_members(losing_team)
            guild = ctx.guild

            # Pass information to StatManager to update individual wins and losses for players
            for winner_member in winner_members:
                winner_member_id = await self.get_member_id_from_display_names(guild, winner_member)
                for win_id in winner_member_id:
                    self.stat_manager.add_to_wins_count(win_id, division_type)
                    self.stat_manager.increment_participation_count(win_id)
            
            for loser_member in loser_members:
                loser_member_id = await self.get_member_id_from_display_names(guild, loser_member)
                for loss_id in loser_member_id:
                    self.stat_manager.add_to_losses_count(loss_id, division_type)
                    self.stat_manager.increment_participation_count(loss_id)

            # Remove the challenge
            remove_challenge(division_type, winning_team)
            logger.info(f"LadderManager: 'admin_report_win' Challenge from {division_type} division involving Team {winning_team} and Team {losing_team} removed from database.")
            
            return f"🏆 Team {winning_team} has won the match and taken the rank of Team {losing_team}! Team {losing_team} moves down one in the ranks. This report was made by an Administrator. 🏆"
        else:
            # If the winning team was the challenged team, no rank change occurs
            losing_team = find_opponent_team(division_type, winning_team)

            #Grab ID's of members to add to stat tracking logic
            winner_members = get_team_members(winning_team)
            loser_members = get_team_members(losing_team)
            guild = ctx.guild

            # Pass information to StatManager to update individual wins and losses for players
            for winner_member in winner_members:
                winner_member_id = await self.get_member_id_from_display_names(guild, winner_member)
                for win_id in winner_member_id:
                    self.stat_manager.add_to_wins_count(win_id, division_type)
                    self.stat_manager.increment_participation_count(win_id)
            
            for loser_member in loser_members:
                loser_member_id = await self.get_member_id_from_display_names(guild, loser_member)
                for loss_id in loser_member_id:
                    self.stat_manager.add_to_losses_count(loss_id, division_type)
                    self.stat_manager.increment_participation_count(loss_id)
            
            # Add win/loss to correct team, no rank change when challenged team wins
            add_team_wins_losses(division_type, winning_team, win=True)
            add_team_wins_losses(division_type, losing_team, win=False)
            logger.info(f"LadderManager: 'admin_report_win' Team {winning_team} has won against Team {losing_team} in the {division_type} division, no rank change occurs since {winning_team} was the challenged team.")

            # Remove the challenge
            remove_challenge(division_type, losing_team)
            logger.info(f"LadderManager: 'admin_report_win' Challenge from {division_type} division involving Team {winning_team} and Team {losing_team} removed from database.")
            
            return f"🏆 Team {winning_team} has won the match against Team {losing_team}, but no rank changes occur since Team {winning_team} was the challenged team. This report was made by an Administrator. 🏆"

    def set_rank(self, team_name: str, new_rank: int):
        """
        Admin method for manually changing the rank
        of a team
        """
        if not does_team_exist(team_name):
            logger.error(f'LadderManager: No team found by given team name for "set_rank". User entered: team_name={team_name}')
            return f"❌ No team found by the name of {team_name}. Please try again. ❌"

        # If team exists, find division type
        division_type = check_team_division(team_name)

        # Find the teams current rank
        current_rank = give_team_rank(division_type, team_name)

        # Find the max rank
        max_rank = count_teams(division_type)
        
        # Check if new rank is valid
        if new_rank < 1 or new_rank > max_rank:
            logger.error(f'LadderManager: Invalid rank given for "set_rank". max_rank={max_rank} min_rank=1 User entered: {new_rank}')
            return f"❌ Invalid rank. The rank should be between 1 and {max_rank}. Please try again. ❌"
        
        # Check if new rank being entered is the current rank of given team
        elif new_rank == current_rank:
            logger.error(f'LadderManager: Given team is already at the given new rank for for "set_rank". team_name={team_name} current_rank={current_rank} new_rank_given={new_rank}')
            return f"❌ {team_name} is already at rank {new_rank} in the {division_type} division. Please try again. ❌"
        
        else:
            # Update the ranks if all conditions pass
            db_set_rank(division_type, team_name, new_rank, current_rank)
            logger.info(f'LadderManager: Given team was assigned to the new rank in their division with "set_rank" and all other teams were adjusted accordingly. team_name={team_name} new_rank={new_rank} division_type={division_type}')
            return f"📈 Team {team_name} has been assigned to the rank of {new_rank} in the {division_type} division. 📈"
    
    def add_win(self, team_name: str):
        """
        Admin method to manually increment ONE
        win to a given team
        """
        if not does_team_exist(team_name):
            logger.error(f'LadderManager: No team found by given team name for "add_win". User entered: team_name={team_name}')
            return f"❌ No team found by the name of {team_name}. Please try again. ❌"
        
        # Grab division type if team is found
        division_type = check_team_division(team_name)

        # Add win to team
        add_team_wins_losses(division_type, team_name, True)
        logger.info(f'LadderManager: Successfully added 1 win to the given team with "add_win". team_name={team_name} division_type={division_type}')
        return f"📈 Team {team_name} has been given a win by an Administrator. 📈"

    def subtract_win(self, team_name: str):
        """
        Admin method to manually decrement ONE
        win to a given team
        """
        if not does_team_exist(team_name):
            logger.error(f'LadderManager: No team found by given team name for "subtract_win". User entered: team_name={team_name}')
            return f"❌ No team found by the name of {team_name}. Please try again. ❌"
        
        # Grab division type if team is found
        division_type = check_team_division(team_name)
        
        # Grab team's current amount of wins
        current_wins = get_wins_or_losses(team_name, True)

        if current_wins < 1:
            logger.error(f'LadderManager: Team found by given team name has no wins for "subtract_win" to minus from. User entered: team_name={team_name} team_name_wins={current_wins}')
            return f"❌ Team {team_name} does not have any wins to take away. ❌" 
        
        if current_wins >= 1:
            subtract_team_wins_losses(division_type, team_name, True)
            logger.info(f'LadderManager: Successfully subtracted 1 win from the given team with "subtract_win". This leaves Team {team_name} with {current_wins - 1}. team_name={team_name} division_type={division_type}')
            return f"📈 Team {team_name} has had a win taken away by an Administrator. They now have {current_wins - 1} wins. 📈"
    
    def add_loss(self, team_name: str):
        """
        Admin method to manually increment ONE
        loss to a given team
        """
        if not does_team_exist(team_name):
            logger.error(f'LadderManager: No team found by given team name for "add_loss". User entered: team_name={team_name}')
            return f"❌ No team found by the name of {team_name}. Please try again. ❌"
        
        # Grab division type if team is found
        division_type = check_team_division(team_name)

        # Add loss to the team
        add_team_wins_losses(division_type, team_name, False)
        logger.info(f'LadderManager: Successfully added 1 loss to the given team with "add_loss". team_name={team_name} division_type={division_type}')
        return f"📈 Team {team_name} has been given a loss by an Administrator. 📈"
    
    def subtract_loss(self, team_name: str):
        """
        Admin method to manually decrement ONE
        loss to a given team
        """
        if not does_team_exist(team_name):
            logger.error(f'LadderManager: No team found by given team name for "subtract_loss". User entered: team_name={team_name}')
            return f"❌ No team found by the name of {team_name}. Please try again. ❌"

        # Grab division type if team is found
        division_type = check_team_division(team_name)

        # Grab team's current amount of losses
        current_losses = get_wins_or_losses(team_name, False)

        if current_losses < 1:
            logger.error(f'LadderManager: Team found by given team name has no losses for "subtract_loss" to minus from. User entered: team_name={team_name} team_name_wins={current_losses}')
            return f"❌ Team {team_name} does not have any losses to take away. ❌"
        
        if current_losses >= 1:
            subtract_team_wins_losses(division_type, team_name, False)
            logger.info(f'LadderManager: Successfully subtracted 1 loss from the given team with "subtract_loss". This leaves Team {team_name} with {current_losses - 1}. team_name={team_name} division_type={division_type}')
            return f"📈 Team {team_name} has had a loss taken away by an Administrator. They now have {current_losses - 1} losses. 📈"
        
    async def post_standings(self, division_type: str):
        """
        Method for everyone to post the current
        standings of a given division type into
        the channel this was called from
        """
        # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            logger.error(f'LadderManager: Wrong division type given for "post_standings". User entered: {division_type}')
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again. Example: /post_standings 2v2 ❌"
        
        # Get standings data from database for given division type
        raw_standings_data = get_standings_data(division_type)

        # Format the raw standings data into something pretty
        formatted_standings_data = format_standings_data(division_type, raw_standings_data)

        return formatted_standings_data

    async def post_challenges(self, division_type: str):
        """
        Method for everyone to post the current
        challenges of a given division type into
        the channel this was called from
        """
        # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            logger.error(f'LadderManager: Wrong division type given for "post_challenges". User entered: {division_type}')
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again. Example: /post_challenges 1v1 ❌"
        
        # Get challenges data from database for given division type
        raw_challenges_data = get_challenges_data(division_type)

        # Format the raw standings data
        formatted_challenges_data = format_challenges_data(division_type ,raw_challenges_data)

        return formatted_challenges_data
    
    async def post_teams(self, division_type: str):
        """
        Method for posting division specific
        teams directly into the channel this
        is called from.
        """
        
        # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            logger.error(f'LadderManager: Wrong division type given for "post_teams". User entered: {division_type}')
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again. Example: /post_teams 3v3 ❌"
        
        # Get teams data from database for given division
        raw_teams_data = get_teams_data(division_type)

        # Format the raw teams data
        formatted_teams_data = format_teams_data(division_type, raw_teams_data)

        return formatted_teams_data
    
    async def set_standings_channel(self, division_type: str, channel: discord.TextChannel):
        """
        Method for manager to set the discord channel
        for the updating standings board for given
        division type
        """
         # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again using 1v1, 2v2, or 3v3 after /set_standings_channel\n\tExample: /set_standings_channel 2v2 #2v2-standings ❌"
            
        db_clear_standings_channel(division_type)
            
        # Grab channel's integer ID
        channel_id = channel.id

        # Tells database to add the integer to correct division type
        db_set_standings_channel(division_type, channel_id)
            
        # Initialize or update the standings message in the new channel
        await self.update_standings_message(division_type, channel)
        
        try:
            self.periodic_update_standings.restart()
        except Exception as e:
            print(f"Error starting periodic update task: {e}")

        return f"🏆 The {division_type} standings channel has been set to #{channel.mention}. 🏆"

    
    def clear_standings_channel(self, division_type: str):
        """
        Admin method to clear a division's standings
        channel that has been set
        """
         # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again."
        
        # Check if channel is actually set
        if not is_standings_channel_set(division_type):
            return f"❌ The standings channel for the {division_type} division has not been set yet. You can set it for specific division types by using /set_standings_channel division_type #channel-name ❌"
        else:
            self.periodic_update_standings.stop()
            db_clear_standings_channel(division_type)
            return f"🛑 The standings channel for the {division_type} division has been cleared. 🛑"
    
    async def set_challenges_channel(self, division_type: str, channel: discord.TextChannel):
        """
        Method for manager to set the discord channel
        for the updating challenges board for given
        division type 
        """
         # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again using 1v1, 2v2, or 3v3 after /set_challenges_channel\n\tExample: /set_challenges_channel 3v3 #3v3-challenges ❌"
        
        db_clear_challenges_channel(division_type)
        
        # Grabs channel's integer ID
        channel_id = channel.id

        # Tell database to add integer to correct division type
        db_set_challenges_channel(division_type, channel_id)

        # Init or update the challenges message in the channel
        await self.update_challenges_message(division_type, channel)

        try:
            self.periodic_update_challenges.restart()
        except Exception as e:
            print(f"Error starting periodic update task: {e}")

        return f"⚔️ The {division_type} challenges channel has been set to #{channel.mention}. ⚔️"
    
    def clear_challenges_channel(self, division_type: str):
        """
        Admin method to clear a division's challenges
        channel that has been set
        """
         # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again."
        
        # Check if channel is actually set
        if not is_challenges_channel_set(division_type):
            return f"❌ The challenges channel for the {division_type} division has not been set yet. You can set it for specific division types by using /set_challenges_channel division_type #channel-name ❌"
        else:
            self.periodic_update_challenges.stop()
            db_clear_challenges_channel(division_type)
            return f"🛑 The challenges channel for the {division_type} division has been cleared. 🛑"
    
    async def set_teams_channel(self, division_type: str, channel: discord.TextChannel):
        """
        Method for manager to set the discord channel
        for the updating challenges board for given
        division type 
        """
         # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again using 1v1, 2v2, or 3v3 after /set_teams_channel\n\tExample: /set_teams_channel 2v2 #2v2-teams ❌"
        
        # Grab channel ID
        channel_id = channel.id

        # Clear channel for safe measure
        db_clear_teams_channel(division_type)

        # Tell the db to add channel id to correct division type in table
        db_set_teams_channel(division_type, channel_id)

        # Init or update the teams message in the channel
        await self.update_teams_message(division_type, channel)

        try:
            self.periodic_update_teams.restart()
        except Exception as e:
            print(f"Error starting periodic update task: {e}")

        return f"👥 The {division_type} teams channel has been set to #{channel.mention}. 👥"
    
    def clear_teams_channel(self, division_type: str):
        """
        Admin method to clear a division's teams
        channel that has been set
        """
         # Check if correct division type was entered
        if not is_valid_division_type(division_type):
            return "❌ Please enter 1v1 2v2 or 3v3 for the division type and try again."
        
        # Check if channel is actually set
        if not is_teams_channel_set(division_type):
            return f"❌ The teams channel for the {division_type} division has not been set yet. You can set it for specific division types by using /set_teams_channel division_type #channel-name ❌"
        else:
            self.periodic_update_teams.stop()
            db_clear_teams_channel(division_type)
            return f"🛑 The teams channel for the {division_type} division has been cleared. 🛑"
    
    async def update_standings_message(self, division_type: str, channel: discord.TextChannel):
        """
        Internal method used to edit the scoreboard
        that appears in the designated division standings channel.

        If no message exists to edit, a new message is
        created in the designated division standings channel.
        """
        try:
            # Get the latest message from the channel's history
            async for message in channel.history(limit=1):
                standings_message = message
                break
            else:
                # If no messages are found, set to None
                standings_message = None

            # Generate the standings text
            standings_text = await self.post_standings(division_type)

            # Add a time stamp
            time_stamp = await add_time_stamp()
            standings_text += time_stamp

            if standings_message:
                # Update the existing message in the given division standings channel
                await standings_message.edit(content=standings_text)
            else:
                # Send a new message if none exists in the division standings channel
                await channel.send(content=standings_text)

        except Exception as e:
            # Log the exception or handle it accordingly
            print(f"An error occurred: {e}")

    async def update_challenges_message(self, division_type: str, channel: discord.TextChannel):
        """
        Internal method used to edit the challenge board
        that appears in the designated division challenges channel.

        If no message exists to edit, a new message is
        created in the designated division standings channel.
        """
        try:
            # Get latest message from channel history
            async for message in channel.history(limit=1):
                challenges_message = message
                break
            else:
                # If no message is found, set to None
                challenges_message = None

            challenges_text = await self.post_challenges(division_type)

            # Add time stamp
            time_stamp = await add_time_stamp()
            challenges_text += time_stamp

            if challenges_message:
                # Update the existing message
                await challenges_message.edit(content=challenges_text)
            else:
                # Send a new message if none exists
                await channel.send(content=challenges_text)
        
        except Exception as e:
            # Log the exception or handle it accordingly
            print(f"An error occurred: {e}")

    async def update_teams_message(self, division_type: str, channel: discord.TextChannel):
        """
        Internal method used to edit the scoreboard
        that appears in the designated division teams channel.

        If no message exists to edit, a new message is
        created in the designated division standings channel.
        """
        try:
            # Get the latest message from the channel's history
            async for message in channel.history(limit=1):
                standings_message = message
                break
            else:
                # If no messages are found, set to None
                standings_message = None

            # Generate the standings text
            teams_text = await self.post_teams(division_type)

            # Add a time stamp
            time_stamp = await add_time_stamp()
            teams_text += time_stamp

            if standings_message:
                # Update the existing message in the given division standings channel
                await standings_message.edit(content=teams_text)
            else:
                # Send a new message if none exists in the division standings channel
                await channel.send(content=teams_text)

        except Exception as e:
            # Log the exception or handle it accordingly
            print(f"An error occurred: {e}")
        
    @tasks.loop(seconds=15)
    async def periodic_update_standings(self):
        """
        Internal task method that will update
        the separate scoreboard that appears in the
        designated division standings channel every 15 seconds.
        """
        for division_type in VALID_DIVISION_TYPES:
            channel_id = get_standings_channel_id(division_type)
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                if isinstance(channel, discord.TextChannel):
                    await self.update_standings_message(division_type, channel)
    
    @tasks.loop(seconds=15)
    async def periodic_update_challenges(self):
        """
        Internal task method that will update
        the separate challenges that appears in the
        designated division standings channel every 15 seconds.
        """
        for division_type in VALID_DIVISION_TYPES:
            channel_id = get_challenges_channel_id(division_type)
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                if isinstance(channel, discord.TextChannel):
                    await self.update_challenges_message(division_type, channel)
    
    @tasks.loop(seconds=15)
    async def periodic_update_teams(self):
        """
        Internal task method that will update
        the separate scoreboard that appears in the
        designated division standings channel every 15 seconds.
        """
        for division_type in VALID_DIVISION_TYPES:
            channel_id = get_teams_channel_id(division_type)
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                if isinstance(channel, discord.TextChannel):
                    await self.update_teams_message(division_type, channel)
    
    def request_my_stats_report(self, ctx):
        """
        Tells the StatManager to send a report
        of the caller of the my_stats command which
        is then sent back to the caller of the command
        """
        discord_id = ctx.author.id
        my_stats_report = self.stat_manager.create_my_stats_report(discord_id)
        return my_stats_report