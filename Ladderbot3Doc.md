# Ladder Bot Documentation v3.0

### Usage:

Commands are accessible through a simple prefix (`/`) and include options for both general users and administrators. The bot is initialized with specific intents to ensure proper functioning, such as handling member updates and message content.

For more detailed usage and examples of each command, please refer to the specific command documentation within this guide.

## Commands

### Registering a Team
- **Command:** `/register_team <team_name> <division_type> <@member1> <@member2> ...`
- **Description:** Registers a new team with the specified members, and member amount must match division type (ex. Two members for 2v2). If any member given is already apart of another team then the command is canceled.
- **Parameters:**
  - `<team_name>`: The name of the team to be registered.
  - `<division_type>`: The specific division you want the team registered to.
  - `<@member1>, <@member2>, etc.`: Mentions of Discord users who are members of the team.
- **Example:** `/register_team Alpha 2v2 @User1 @User2`
- **Response:** Confirms the registration and lists the team name, division type, and team members.
- **Permissions:** Admins only

### Removing a Team
- **Command:** `/remove_team <team_name>`
- **Description:** Removes a team from the ladder.
- **Parameters:**
  - `<team_name>`: The name of the team to be removed.
- **Example:** `/remove_team Alpha`
- **Response:** Confirms removal of the specified team from the division they were in.
- **Permissions:** Admin only.

### Starting the Ladder
- **Command:** `/start_ladder <division_type>`
- **Description:** Starts the ladder in the given division type, allowing teams to begin challenging each other and report wins.
- **Parameters:**
  - `<division_type>`: The specific division of ladder to start
- **Example:** `/start_ladder <division_type>`
- **Response:** Confirms that the ladder has been started in the given division type.
- **Permissions:** Admin only.

### Ending the Ladder
- **Command:** `/end_ladder <division_type>`
- **Description:** Ends the ladder, posts final standings, announces winners, and clears all team and match data.
- **Parameters:**
  - `<division_type>`: The specific divison of ladder to end
- **Example:** `/end_ladder <division_type>`
- **Response:** Ends the ladder in the given division type.
- **Permissions:** Admin only.

### Challenging a Team
- **Command:** `/challenge <challenger_team> <team_name>`
- **Description:** Initiates a challenge where the `challenger_team` challenges `team_name`. The challenger can only challenge a team up to two ranks higher.
- **Parameters:**
  - `<challenger_team>`: The name of the team initiating the challenge.
  - `<team_name>`: The name of the team being challenged.
- **Example:** `/challenge Bravo Alpha`
- **Response:** Confirms the challenge and lists the teams involved.
- **Permissions:** Any user can challenge if the ladder is running.

### ADMIN - Challenging a Team
- **Command:** `/admin_challenge <challenger_team> <team_name>`
- **Description:** An Admin forces a challenge between `challenger_team` and `team_name`, bypassing normal restrictions.
- **Parameters:**
  - `<challenger_team>`: The name of the team initiating the challenge.
  - `<team_name>`: The name of the team being challenged.
- **Example:** `/admin_challenge Bravo Alpha`
- **Response:** Confirms the challenge, lists the teams involved, and indicates the command was issued by an Admin.
- **Permissions:** Admin only.

### Cancelling a Challenge
- **Command:** `/cancel_challenge <team_name>`
- **Description:** Cancels a challenge sent out by `team_name`.
- **Parameters:**
  - `<team_name>`: The name of the team that sent out the challenge.
- **Example:** `/cancel_challenge Bravo`
- **Response:** Confirms the challenge was canceled.
- **Permissions:** Any user can cancel their own challenge.

### ADMIN - Cancelling a Challenge
- **Command:** `/admin_cancel_challenge <team_name>`
- **Description:** Cancels a challenge sent out by `team_name`, performed by an Admin.
- **Parameters:**
  - `<team_name>`: The name of the team that sent out the challenge.
- **Example:** `/admin_cancel_challenge Echo`
- **Response:** Confirms the challenge was canceled by an Admin.
- **Permissions:** Admin only.

### Post Challenges
- **Command:** `/post_challenges <division_type>`
- **Description:** Displays all challenges currently on the board.
- **Parameters:**
  - `<division_type>`: The specific division of challenges to post
- **Example:** `/post_challenges 1v1`
- **Response:** Lists all ongoing challenges in given division type.
- **Permissions:** Any user can view challenges.

### Setting the Challenges Channel
- **Command:** `/set_challenges_channel <division_type> <#channel>`
- **Description:** Sets the given division channel where challenge notifications will be periodically updated.
- **Parameters:**
  - `<#channel>`: The channel for challenge notifications.
  - `<division_type>`: The division of challenges for the channel
- **Example:** `/set_challenges_channel 2v2 #2v2-challenges`
- **Response:** Confirms the new challenges channel for given division type.
- **Permissions:** Admin only.

### Clearing the Challenges Channel
- **Command:** `/clear_challenges_channel <division_type>`
- **Description:** Clears the division type channel designated for challenge notifications.
- **Parameters:**
  - `<division_type>`: Which division channel to clear
- **Example:** `/clear_challenges_channel 3v3`
- **Response:** Confirms the challenges channel ID was cleared for given division type
- **Permissions:** Admin only.

### Reporting a Win
- **Command:** `/report_win <winning_team>`
- **Description:** Reports the result of a match, adjusting the teams' ranks accordingly.
- **Parameters:**
  - `<winning_team>`: The name of the team that won.
- **Example:** `/report_win Alpha`
- **Response:** Updates the rankings and confirms the match result.
- **Permissions:** Any member of the involved teams can report a win.

### ADMIN - Reporting a Win
- **Command:** `/admin_report_win <winning_team>`
- **Description:** Reports the result of a match, with Admin privileges.
- **Parameters:**
  - `<winning_team>`: The name of the team that won.
- **Example:** `/admin_report_win Delta`
- **Response:** Updates the rankings and confirms the result, noting that the action was performed by an Admin.
- **Permissions:** Admins only.

### Posting Standings
- **Command:** `/post_standings <division_type>`
- **Description:** Displays the current team standings for the given division type
- **Parameters:**
  - `<division_type>`: The specific division of standings to post.
- **Example:** `/post_standings 1v1`
- **Response:** Lists current rankings of given division.
- **Permissions:** Any user can view standings.

### Posting Teams
- **Command:** `/post_teams <division_type>`
- **Description:** Displays the current teams and it's members for the given division type
- **Parameters:**
  - `<division_type>`: The specific division of standings to post.
- **Example:** `/post_teams 3v3`
- **Response:** Lists current teams and it's members of given division.
- **Permissions:** Any user can view teams.

### Setting the Standings Channel
- **Command:** `/set_standings_channel <division_type> <#channel>`
- **Description:** Sets the channel where standings will be periodically updated for given division type.
- **Parameters:**
  - `<#channel>`: The channel for standings updates.
  - `<division_type>`: The specific division of standings for the channel
- **Example:** `/set_standings_channel 1v1 #1v1-standings`
- **Response:** Confirms the new standings channel and division type.
- **Permissions:** Admin only.

### Clearing the Standings Channel
- **Command:** `/clear_standings_channel <division_type>`
- **Description:** Clears the channel designated for standings updates for given division.
- **Parameters:**
  - `<division_type>`: The specific division of standings channel to clear
- **Example:** `/clear_standings_channel 3v3`
- **Response:** Confirms the standings channel ID was cleared for given division.
- **Permissions:** Admin only.

### Setting the Teams Channel
- **Command:** `/set_teams_channel <division_type> <#channel>`
- **Description:** Sets the channel where teams will be periodically updated for given division type.
- **Parameters:**
  - `<#channel>`: The channel for standings updates.
  - `<division_type>`: The specific division of standings for the channel
- **Example:** `/set_teams_channel 3v3 #3v3-teams`
- **Response:** Confirms the new teams channel and division type.
- **Permissions:** Admin only.

### Clearing the Teams Channel
- **Command:** `/clear_teams_channel <division_type>`
- **Description:** Clears the channel designated for teams updates for given division.
- **Parameters:**
  - `<division_type>`: The specific division of standings channel to clear
- **Example:** `/clear_teams_channel 3v3`
- **Response:** Confirms the teams channel ID was cleared for given division.
- **Permissions:** Admin only.

### Adjusting Team Rank
- **Command:** `/set_rank <team_name> <rank>`
- **Description:** Manually sets a team's rank, adjusting other teams' ranks as necessary.
- **Parameters:**
  - `<team_name>`: The name of the team whose rank is being adjusted.
  - `<rank>`: The new rank for the team.
- **Example:** `/set_rank Alpha 1`
- **Response:** Updates the team's rank and adjusts other teams' ranks.
- **Permissions:** Admin only.

### Adding a Win
- **Command:** `/add_win <team_name>`
- **Description:** Manually adds a win to a team's record.
- **Parameters:**
  - `<team_name>`: The name of the team to which the win is being added.
- **Example:** `/add_win Alpha`
- **Response:** Updates the team's win count.
- **Permissions:** Admin only.

### Subtracting a Win
- **Command:** `/subtract_win <team_name>`
- **Description:** Manually subtracts a win from a team's record.
- **Parameters:**
  - `<team_name>`: The name of the team from which the win is being subtracted.
- **Example:** `/subtract_win Alpha`
- **Response:** Updates the team's win count.
- **Permissions:** Admin only.

### Adding a Loss
- **Command:** `/add_loss <team_name>`
- **Description:** Manually adds a loss to a team's record.
- **Parameters:**
  - `<team_name>`: The name of the team to which the loss is being added.
- **Example:** `/add_loss Alpha`
- **Response:** Updates the team's loss count.
- **Permissions:** Admin only.

### Subtracting a Loss
- **Command:** `/subtract_loss <team_name>`
- **Description:** Manually subtracts a loss from a team's record.
- **Parameters:**
  - `<team_name>`: The name of the team from which the loss is being subtracted.
- **Example:** `/subtract_loss Alpha`
- **Response:** Updates the team's loss count.
- **Permissions:** Admin only.

### Show Documentation Link
- **Command:** `/show_help`
- **Description:** Provides a link to the Ladder Bot's documentation.
- **Parameters:** None.
- **Example:** `/show_help`
- **Response:** Provides a GitHub link to the documentation.
- **Permissions:** Anyone.
