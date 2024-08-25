from config import VALID_DIVISION_TYPES

def is_correct_member_size(division_type: str, *members):
    """
    Validates if the given number of members
    is the correct amount for the given
    division type.
    """
    total_members = len(members)
    if division_type == '1v1' and total_members == 1:
        return True
    
    if division_type == '2v2' and total_members == 2:
        return True
    
    if division_type == '3v3' and total_members == 3:
        return True
    
    else:
        return False

def is_valid_division_type(division_type: str) -> bool:
    """
    Checks if user entered valid division type
    as a parameter
    """
    if division_type not in VALID_DIVISION_TYPES:
        return False
    else:
        return True