# Import the different divisions here

from database import initialize_database, db_register_team, is_team_name_unique
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

    def register_team(self, division_type, team_name, *members):
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

                    # Turn all members into a string for the database
                    members_string = create_members_string(*members)

                    # Add team to the database with the given arguments
                    db_register_team(division_type, team_name, members_string)

                    # Create and return confirmation message
                    register_team_success = f"Team {team_name} has been registered in the {division_type} division with the following members: {', '.join([member.display_name for member in members])}"
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
