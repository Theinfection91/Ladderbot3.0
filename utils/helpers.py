import discord

def create_members_string(*members):
    """
    Formats all members given into a string
    to store inside the database
    """
    display_names = ""
    if len(members) == 1:
        display_names += member.display_name
        return display_names
    
    for member in members:
        display_names += f"{member.display_name}, "
    return display_names
