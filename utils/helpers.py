import time

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
    header += "| Rank | Team Name       | Wins | Losses |\n"
    header += "|------|-----------------|------|--------|\n"

    standings_lines = [
        f"| {rank:<4} | {team_name:<15} | {wins:<4} | {losses:<6} |"
        "\n|------|-----------------|------|--------|"
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
    header += "| Challenger         | Challenged         |\n"
    header += "|--------------------|--------------------|\n"

    challenges_lines = [
        f"| {challenger:<18} | {challenged:<18} |"
        "\n|--------------------|--------------------|"
        for challenger, challenged in raw_challenges_data
    ]

    challenges_message = header + "\n".join(challenges_lines) + "\n```"

    return challenges_message

def format_teams_data(division_type: str, raw_teams_data):
    """
    Formats raw teams data for a given division type
    into something pretty for display in the teams channel.
    """

    # Prepare the teams message
    header = f"👥 **{division_type.upper()} Division Teams** 👥\n"
    header += "```\n"
    header += "| Team Name         | Members                         \n"
    header += "|-------------------|---------------------------------\n"

    # Calculate the max width for the members column
    members_col_width = 32  # Adjust this value as needed

    teams_lines = [
        f"| {team_name:<17} | {members:<{members_col_width}} "
        "\n|-------------------|---------------------------------"
        for team_name, members in raw_teams_data
    ]

    teams_message = header + "\n".join(teams_lines) + "\n```"

    return teams_message

async def add_time_stamp():
    """
    Returns a formatted time stamp of
    the time and date this function is called
    """
    # Create time stamp and format it to be readable
    time_stamp = time.time()
    readable_time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))

    # Format to include Last updated:
    formatted_time_stamp = f"\n\nLast updated: {readable_time_stamp}"

    return formatted_time_stamp