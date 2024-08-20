import discord

def create_members_string(*members):
    """
    Formats all members given into a CSV string
    to store inside the database.
    """
    if len(members) == 1:
        return members[0].display_name
    
    # Join member display names with a comma separator
    display_names = ", ".join(member.display_name for member in members)
    
    return display_names
