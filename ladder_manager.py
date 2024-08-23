# Import the different divisions here

import discord
from database import initialize_database, count_teams, db_register_team, db_remove_team, db_set_rank, db_update_rankings, is_team_name_unique, is_member_registered, is_member_on_team, check_team_division, does_team_exist, is_team_challenged, has_team_challenged, find_opponent_team, give_team_rank, db_register_challenge, db_remove_challenge, update_team_wins_losses, update_team_rank, increment_rank_for_teams_below, remove_challenge
from utils import is_correct_member_size, create_members_string

class LadderManager:
    """
    This class will handle talking to the different divisions within
    the entire program itself. There will be 1v1, 2v2, and 3v3. The
    LadderManager will also call on different helpers, validators,
    and parsing the database as well as other features.

    The LadderManager is controlled by the Ladderbot in main.py
    """
    def __init__(self):
        """
        Constructs the LadderManager class

        The LadderManager will help register teams, and challenges
        for every division in the Ladder. When a team wants to be registered
        the LadderManager will do various things like checking to see if the
        team name already exists, checking if a member trying to register
        is already apart of a team in the same division, and various
        other tasks that a manager of a tournament would do.
        """
        #Init the ladderbot.db when the LadderManager is instantiated
        initialize_database()

    def create_test_teams(self, division_type):
        
        if division_type == '1v1':
            db_register_team('1v1', "Alpha", "Theinfection1991")
            db_register_team('1v1', "Bravo", "Theinfection1991")
            db_register_team('1v1', "Charlie", "Theinfection1991")
            db_register_team('1v1', "Delta", "Theinfection1991")
            db_register_team('1v1', "Echo", "Theinfection1991")
            return f"Created five 1v1 test teams"
        
        if division_type == '2v2':
            db_register_team('2v2', "Apple", "Theinfection1991")
            db_register_team('2v2', "Butler", "Theinfection1991")
            db_register_team('2v2', "Carlos", "Theinfection1991")
            db_register_team('2v2', "Dynasty", "Theinfection1991")
            db_register_team('2v2', "Ellen", "Theinfection1991")
            return f"Created five 2v2 test teams"
        
        if division_type == '3v3':
            db_register_team('3v3', "A", "Theinfection1991")
            db_register_team('3v3', "B", "Theinfection1991")
            db_register_team('3v3', "C", "Theinfection1991")
            db_register_team('3v3', "D", "Theinfection1991")
            db_register_team('3v3', "E", "Theinfection1991")
            return f"Created five 3v3 test teams"
    
    def register_team(self, division_type: str, team_name: str, *members):
        """
        Takes the input from the discord user and
        uses a series of help and validation functions
        and conditions to make sure the correct information
        has been given to make a team correctly.
        """
        # Check if team name is unique and no other team is named the same in ANY division
        if is_team_name_unique(team_name):

            # Check if correct divison type was entered
            if division_type == '1v1' or '2v2' or '3v3':

                # Check if correct amount of members was given for the division type
                if is_correct_member_size(division_type, *members):

                    # NOTE: Uncomment triple quotes to check if member is already registered on division type team
                    """# Create a list of all the members display names
                    member_display_names = [member.display_name for member in members]

                    # Checks every members display name against the database
                    for member_display_name in member_display_names:
                        
                        # If a player is already registered on a team in a given division type the process is stopped
                        if is_member_registered(division_type, member_display_name):     
                            member_registered = f"{member_display_name} is already registered on a team in the {division_type} division. Please try again."
                            return member_registered"""
                    # NOTE
                        
                    # Turn all members into a string for the database
                    members_string = create_members_string(*members)

                    # Add team to the database with the given arguments
                    db_register_team(division_type, team_name, members_string)

                    # Create and return confirmation message
                    register_team_success = f"Team {team_name} has been registered in the {division_type} division with the following members: {members_string}"
                    return register_team_success
                else:
                    incorrect_member_count = "Please enter the correct amount of members depending on the division type."
                    return incorrect_member_count
            else:
                incorrect_division = "Please enter 1v1 2v2 or 3v3 for the division type and try again."
                return incorrect_division
        else:
            duplicate_team_name = f"Team {team_name} is already being used. Please choose another team name."
            return duplicate_team_name
        
    def remove_team(self, division_type, team_name):
        """
        Finds the correct team and tells
        the database to remove them completely
        """
        if does_team_exist(team_name):
            db_remove_team(division_type, team_name)
            return f"Team {team_name} from the {division_type} division has been removed from the Ladder."
        else:
            return f"No team named Team {team_name} found for the {division_type} division. Please try again."
        
    def challenge(self, ctx, challenger_team: str, challenged_team: str):
        """
        Checks if teams exist, checks what division
        type the teams are in, checks if either team
        are currently under a challenge, checks if
        challenger team is one or two ranks below the
        challenged team,
        """
        # Capture the author of the command call's display name
        display_name = ctx.author.display_name

        # Check if the person calling the command is apart of the challenger team
        if not is_member_on_team(display_name, challenger_team):
            return f"You are not a member of Team {challenger_team} and may not issue a challenge on their behalf."
        
        # Check if both teams exist
        if not does_team_exist(challenger_team):
            return f"No team found by the name of {challenger_team}. Please try again."
        
        if not does_team_exist(challenged_team):
            return f"No team found by the name of {challenged_team}. Please try again."
        
        # Check if both teams exist within the same division and stores which divison if so
        challenger_division = check_team_division(challenger_team)
        challenged_division = check_team_division(challenged_team)
        
        if challenger_division != challenged_division:
            return f"Team {challenger_team} and Team {challenged_team} are not in the same division..."
        
        # Set division type to use for helper functions
        division_type = challenger_division
        
        # Grab the rank of each team for comparison
        challenger_rank = give_team_rank(division_type, challenger_team)
        challenged_rank = give_team_rank(division_type, challenged_team)

        # Check if the challenging team is challenging either one or two ranks above them
        if challenged_rank > challenger_rank or challenged_rank <= challenger_rank - 3:
            return f"Teams can only challenge other teams up to two ranks above their current rank."
        
        # Check if either team has challenged or already been challenged
        if is_team_challenged(division_type, challenged_team):
            return f"{challenged_team} has already been challenged by another team and must complete that match first!"
        if has_team_challenged(division_type, challenged_team):
            return f"{challenged_team} has already sent out a challenge to a team and must complete that match first!"
        
        if is_team_challenged(division_type, challenger_team):
            return f"{challenger_team} has already been challenged by another team and must complete that match first!"
        if has_team_challenged(division_type, challenger_team):
            return f"{challenger_team} has already sent out a challenge to a team and must complete that match first!"
        
        # Once all checks are passed then register the challenge in the correct table
        db_register_challenge(division_type, challenger_team, challenged_team)
        return f"Team {challenger_team} has challenged Team {challenged_team} in the {division_type} division!"
    
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
            return f"No Team found by the name of {challenger_team}. Please try again."
        
        # Capture the author of the command call's display name and team division
        display_name = ctx.author.display_name
        team_division = check_team_division(challenger_team)
        
        # Check if the person calling the command is apart of the challenger team
        if not is_member_on_team(display_name, challenger_team):
            return f"You are not a member of Team {challenger_team}."

        # Check if the given team has sent out a challenge
        if not has_team_challenged(team_division, challenger_team):
            return f"No challenge was found where Team {challenger_team} was the Challenger. Please try again."
        
        # If all checks are passed, delete the specified challenge from correct challenges table
        db_remove_challenge(team_division, challenger_team)
        return f"The challenge made by Team {challenger_team} in the {team_division} division has been canceled by a team member."
    
    def admin_challenge(self, challenger_team: str, challenged_team: str):
        """
        This works the same way as challenge but removes the
        functionality of grabbing the display name to
        check if the caller is on the challenger team.
        """
        # Check if both teams exist
        if not does_team_exist(challenger_team):
            return f"No team found by the name of {challenger_team}. Please try again."
        
        if not does_team_exist(challenged_team):
            return f"No team found by the name of {challenged_team}. Please try again."
        
        # Check if both teams exist within the same division and stores which divison if so
        challenger_division = check_team_division(challenger_team)
        challenged_division = check_team_division(challenged_team)
        
        if challenger_division != challenged_division:
            return f"Team {challenger_team} and Team {challenged_team} are not in the same division..."
        
        # Set division type to use for helper functions
        division_type = challenger_division
        
        # Grab the rank of each team for comparison
        challenger_rank = give_team_rank(division_type, challenger_team)
        challenged_rank = give_team_rank(division_type, challenged_team)

        # Check if the challenging team is challenging either one or two ranks above them
        if challenged_rank > challenger_rank or challenged_rank <= challenger_rank - 3:
            return f"Teams can only challenge other teams up to two ranks above their current rank."
        
        # Check if either team has challenged or already been challenged
        if is_team_challenged(division_type, challenged_team):
            return f"{challenged_team} has already been challenged by another team and must complete that match first!"
        if has_team_challenged(division_type, challenged_team):
            return f"{challenged_team} has already sent out a challenge to a team and must complete that match first!"
        
        if is_team_challenged(division_type, challenger_team):
            return f"{challenger_team} has already been challenged by another team and must complete that match first!"
        if has_team_challenged(division_type, challenger_team):
            return f"{challenger_team} has already sent out a challenge to a team and must complete that match first!"
        
        # Once all checks are passed then register the challenge in the correct table
        db_register_challenge(division_type, challenger_team, challenged_team)
        return f"Team {challenger_team} has challenged Team {challenged_team} in the {division_type} division! -This challenge was created by an Administrator."
    
    def admin_cancel_challenge(self, challenger_team: str):
        """
        This works the same way as cancel_challenge but removes the
        functionality of grabbing the display name to
        check if the caller is on the challenger team.
        """
        # Check if given team exists in the database
        if not does_team_exist(challenger_team):
            return f"No Team found by the name of {challenger_team}. Please try again."
        
        # Capture the team division of the challenger team
        team_division = check_team_division(challenger_team)

        # Check if the given team has sent out a challenge
        if not has_team_challenged(team_division, challenger_team):
            return f"No challenge was found where Team {challenger_team} was the Challenger. Please try again."
        
        # If all checks are passed, delete the specified challenge from correct challenges table
        db_remove_challenge(team_division, challenger_team)
        return f"The challenge made by Team {challenger_team} in the {team_division} division has been canceled by an Administrator."
    
    def report_win(self, ctx, winning_team: str):
        """
        Checks if there is a challenge involving the team name given,
        determines the losing team based on the winning team,
        updates ranks and wins/losses accordingly,
        and removes the challenge from the challenges table.
        """
        # Checks if given team exists
        if not does_team_exist(winning_team):
            return f"No team found by the name of {winning_team}. Please try again."
        
        # If team exists, grab its division type
        division_type = check_team_division(winning_team)
        
        # Check if author of command call is on the winning team
        display_name = ctx.author.display_name
        if not is_member_on_team(display_name, winning_team):
            return f"You are not a member of Team {winning_team}."
        
        # Check if the given team is the challenger
        if has_team_challenged(division_type, winning_team):
            # Find the opponent team to determine the loser
            losing_team = find_opponent_team(division_type, winning_team)
            
            # Update ranks when challenger wins
            db_update_rankings(division_type, winning_team, losing_team)
            remove_challenge(division_type, winning_team)
            return f"Team {winning_team} has won the match and taken the rank of Team {losing_team}! Team {losing_team} moves down one in the ranks."
        else:
            # If the winning team was the challenged team, no rank change occurs
            losing_team = find_opponent_team(division_type, winning_team)
            update_team_wins_losses(division_type, winning_team, win=True)
            update_team_wins_losses(division_type, losing_team, win=False)
            remove_challenge(division_type, losing_team)
            return f"Team {winning_team} has won the match against Team {losing_team}, but no rank changes occur since Team {winning_team} was the challenged team."
    
    def set_rank(self, team_name: str, new_rank: int):
        """
        Admin method for manually changing the rank
        of a team
        """
        if not does_team_exist(team_name):
            return f"No team found by the name of {team_name}. Please try again."

        # If team exists, find division type
        division_type = check_team_division(team_name)

        # Find the teams current rank
        current_rank = give_team_rank(division_type, team_name)

        # Find the max rank
        max_rank = count_teams(division_type)
        
        # Check if new rank is valid
        if new_rank < 1 or new_rank > max_rank:
            return f"Invalid rank. The rank should be between 1 and {max_rank}. Please try again."
        
        # Check if new rank being entered is the current rank of given team
        elif new_rank == current_rank:
            return f"{team_name} is already at rank {new_rank} in the {division_type} division. Please try again."
        
        else:
            # Update the ranks if all conditions pass
            db_set_rank(division_type, team_name, new_rank, current_rank)
            return f"Team {team_name} has been assigned to the rank of {new_rank} in the {division_type} division."