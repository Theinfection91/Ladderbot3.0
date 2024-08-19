# Import the different divisions here

from database.database_setup import initialize_database

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
        """
        #Init the Ladderbot Database when the LadderManager is instantiated
        initialize_database()

        #
