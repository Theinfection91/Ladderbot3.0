# Import the different divisions here

from database import initialize_database, db_register_team, is_team_name_unique

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

    def register_team(self, division_type, team_name, members):
        """
        
        """
        # Check if team name is unique and no other team is named the same in ANY division
        if is_team_name_unique(team_name):
            # Check if correct divison type was entered
            if division_type == '1v1' or '2v2' or '3v3':
                return

        


        db_register_team(division_type, team_name, members)
