

def is_correct_member_size(division_type, *members):
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