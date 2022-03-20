export const playersXgoalsParameters = new Set([
  "minimum_minutes",
  "minimum_shots",
  "minimum_key_passes",
  "player_id",
  "team_id",
  "season_name",
  "start_date",
  "end_date",
  "shot_pattern",
  "split_by_teams",
  "split_by_seasons",
  "split_by_games",
  "stage_name",
  "general_position",
]);

export const playersXpassParameters = new Set([
  "minimum_minutes",
  "minimum_passes",
  "player_id",
  "team_id",
  "season_name",
  "start_date",
  "end_date",
  "pass_origin_third",
  "split_by_teams",
  "split_by_seasons",
  "split_by_games",
  "stage_name",
  "general_position",
]);

export const playersGoalsAddedParameters = new Set([
  "minimum_minutes",
  "player_id",
  "team_id",
  "season_name",
  "start_date",
  "end_date",
  "split_by_teams",
  "split_by_seasons",
  "split_by_games",
  "stage_name",
  "general_position",
  "action_type",
  "above_replacement",
]);

export const playersSalariesParameters = new Set([
  "player_id",
  "team_id",
  "position",
  "season_name",
  "start_date",
  "end_date",
]);

export const goalkeepersXgoalsParameters = new Set([
  "minimum_minutes",
  "minimum_shots_faced",
  "player_id",
  "team_id",
  "season_name",
  "start_date",
  "end_date",
  "shot_pattern",
  "split_by_teams",
  "split_by_seasons",
  "split_by_games",
  "stage_name",
]);

export const goalkeepersGoalsAddedParameters = new Set([
  "minimum_minutes",
  "player_id",
  "team_id",
  "season_name",
  "start_date",
  "end_date",
  "split_by_teams",
  "split_by_seasons",
  "split_by_games",
  "stage_name",
  "action_type",
  "above_replacement",
]);

export const teamsXgoalsParameters = new Set([
  "team_id",
  "season_name",
  "start_date",
  "end_date",
  "shot_pattern",
  "split_by_teams",
  "split_by_seasons",
  "split_by_games",
  "home_only",
  "away_only",
  "home_adjusted",
  "even_game_state",
  "stage_name",
]);

export const teamsXpassParameters = new Set([
  "team_id",
  "season_name",
  "start_date",
  "end_date",
  "pass_origin_third",
  "split_by_teams",
  "split_by_seasons",
  "split_by_games",
  "home_only",
  "away_only",
  "stage_name",
]);

export const teamsGoalsAddedParameters = new Set([
  "team_id",
  "season_name",
  "split_by_seasons",
  "stage_name",
  "action_type",
  "zone",
  "gamestate_trunc",
]);

export const teamsSalariesParameters = new Set([
  "team_id",
  "season_name",
  "split_by_teams",
  "split_by_seasons",
  "split_by_games",
]);

export const gamesParameters = new Set([
  "game_id",
  "team_id",
  "season_name",
  "stage_name",
]);

export const gamesXgoalsParameters = new Set([
  "game_id",
  "season_name",
  "start_date",
  "end_date",
  "stage_name",
]);
