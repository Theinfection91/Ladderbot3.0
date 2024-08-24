
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

def format_standings_data(division_type: str, raw_standings_data):
    """
    Formats standings data from a division
    for post_standings into something
    prettier than what comes directly from
    the database
    """
    # Prepare the standings message
    header = f"🏆 **{division_type.upper()} Division Standings** 🏆\n"
    header += "```\n"
    header += "{:<6} {:<15} {:<5} {:<5}\n".format("Rank", "Team Name", "Wins", "Losses")
    header += "-" * 36 + "\n"

    standings_lines = [
        "{:<6} {:<15} {:<5} {:<5}".format(rank, team_name, wins, losses)
        for team_name, rank, wins, losses in raw_standings_data
    ]

    standings_message = header + "\n".join(standings_lines) + "\n```"

    return standings_message

def format_challenges_data(division_type: str, raw_challenges_data):
    """
    Formats raw challenges data for
    a given division type into
    something pretty for post_challenges
    """
    # Prepare the challenges message
    header = f"⚔️ **{division_type.upper()} Division Challenges** ⚔️\n"
    header += "```\n"
    header += "{:<20} {:<20}\n".format("Challenger", "Challenged")
    header += "-" * 41 + "\n"

    challenges_lines = [
        "{:<20} {:<20}".format(challenger, challenged)
        for challenger, challenged in raw_challenges_data
    ]

    challenges_message = header + "\n".join(challenges_lines) + "\n```"

    return challenges_message
