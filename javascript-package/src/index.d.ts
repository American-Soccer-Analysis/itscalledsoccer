import { LEAGUES, ENTITY_TYPES } from "./constants";

type ValidLeagues = keyof typeof LEAGUES;
type GeneralPositions = "GK" | "CB" | "FB" | "DM" | "CM" | "AM" | "W" | "ST";

type LeagueArgs = { leagues?: ValidLeagues[] };
type IdArgs = { ids?: string[] };
type NameArgs = { names?: string[] };
type EntityArgs = LeagueArgs & IdArgs;
type EntityByNameArgs = LeagueArgs & NameArgs;
type StatArgs<T extends string[]> = LeagueArgs & {
  [Key in T[number]]?: string | number | string[] | boolean;
};

type EntityReference<FieldName extends string> = {
  league: string;
} & {
  [key in FieldName]: string[];
};

export default class Client {
  #fuses: Map<unknown, unknown>;
  #minimumFuseScore: number;
  constructor(args?: { minimumFuseScores?: number });
  // #convertNameToId(args: { name: string, entityType: string, league: string }): Promise<unknown>
  // #getEntityIdsByName
  // #fetchEntity
  // #getStats

  /**
   * Get entities by ID
   */
  getPlayers(args: EntityArgs): Promise<Array<Player>>;
  getStadia(args: EntityArgs): Promise<Array<Stadia>>;
  getManagers(args: EntityArgs): Promise<Array<Manager>>;
  getReferees(args: EntityArgs): Promise<Array<Referee>>;
  getTeams(args: EntityArgs): Promise<Array<Team>>;

  /**
   * Get IDs by name
   */
  getPlayersByName(
    args: EntityByNameArgs
  ): Promise<Array<EntityReference<"players">>>;
  getManagersByName(
    args: EntityByNameArgs
  ): Promise<Array<EntityReference<"managers">>>;
  getStadiaByName(
    args: EntityByNameArgs
  ): Promise<Array<EntityReference<"stadia">>>;
  getRefereesByName(
    args: EntityByNameArgs
  ): Promise<Array<EntityReference<"referees">>>;
  getTeamsByName(
    args: EntityByNameArgs
  ): Promise<Array<EntityReference<"teams">>>;

  getPlayersXgoals(
    args: StatArgs<PlayersXGoalParameters>
  ): Promise<PlayerXGoals[]>;
  getPlayersXpass(
    args: StatArgs<PlayerXPassParameters>
  ): Promise<PlayerXPass[]>;
  getPlayersGoalsAdded(
    args: StatArgs<PlayersGoalsAddedParameters>
  ): Promise<PlayerGoalsAdded[]>;
  getPlayersSalaries(
    args: StatArgs<PlayersSalariesParameters>
  ): Promise<PlayerSalaries[]>;
  getGoalkeepersXgoals(
    args: StatArgs<GoalkeepersXgoalsParameters>
  ): Promise<GoalkeeperXGoals[]>;
  getGoalkeepersGoalsAdded(
    args: StatArgs<GoalkeepersGoalsAddedParameters>
  ): Promise<GoalkeeperGoalsAdded[]>;
  getTeamsXgoals(args: StatArgs<TeamsXgoalsParameters>): Promise<TeamXPass[]>;
  getTeamsXpass(args: StatArgs<TeamsXpassParameters>): Promise<TeamXPass[]>;
  getTeamsGoalsAdded(
    args: StatArgs<TeamsGoalsAddedParameters>
  ): Promise<TeamGoalsAdded[]>;
  getTeamsSalaries(
    args: StatArgs<TeamsSalariesParameters>
  ): Promise<TeamSalaries[]>;
  getGamesXgoals(args: StatArgs<GamesXgoalsParameters>): Promise<GamesXGoals[]>;
}

/**
 * Parameters
 */
type PlayersXGoalParameters = [
  "minimumMinutes",
  "minimumShots",
  "minimumKeyPasses",
  "playerId",
  "teamId",
  "seasonName",
  "startDate",
  "endDate",
  "shotPattern",
  "splitByTeams",
  "splitBySeasons",
  "splitByGames",
  "stageName",
  "generalPosition"
];

type PlayerXPassParameters = [
  "minimumMinutes",
  "minimumPasses",
  "playerId",
  "teamId",
  "seasonName",
  "startDate",
  "endDate",
  "passOriginThird",
  "splitByTeams",
  "splitBySeasons",
  "splitByGames",
  "stageName",
  "generalPosition"
];

type PlayersGoalsAddedParameters = [
  "minimumMinutes",
  "playerId",
  "teamId",
  "seasonName",
  "startDate",
  "endDate",
  "splitByTeams",
  "splitBySeasons",
  "splitByGames",
  "stageName",
  "generalPosition",
  "actionType",
  "aboveReplacement"
];

type PlayersSalariesParameters = [
  "playerId",
  "teamId",
  "position",
  "seasonName",
  "startDate",
  "endDate"
];

type GoalkeepersXgoalsParameters = [
  "minimumMinutes",
  "minimumShotsFaced",
  "playerId",
  "teamId",
  "seasonName",
  "startDate",
  "endDate",
  "shotPattern",
  "splitByTeams",
  "splitBySeasons",
  "splitByGames",
  "stageName"
];

type GoalkeepersGoalsAddedParameters = [
  "minimumMinutes",
  "playerId",
  "teamId",
  "seasonName",
  "startDate",
  "endDate",
  "splitByTeams",
  "splitBySeasons",
  "splitByGames",
  "stageName",
  "actionType",
  "aboveReplacement"
];

type TeamsXgoalsParameters = [
  "teamId",
  "seasonName",
  "startDate",
  "endDate",
  "shotPattern",
  "splitByTeams",
  "splitBySeasons",
  "splitByGames",
  "homeOnly",
  "awayOnly",
  "homeAdjusted",
  "evenGameState",
  "stageName"
];

type TeamsXpassParameters = [
  "teamId",
  "seasonName",
  "startDate",
  "endDate",
  "passOriginThird",
  "splitByTeams",
  "splitBySeasons",
  "splitByGames",
  "homeOnly",
  "awayOnly",
  "stageName"
];

type TeamsGoalsAddedParameters = [
  "teamId",
  "seasonName",
  "splitBySeasons",
  "stageName",
  "actionType",
  "zone",
  "gamestateTrunc"
];

type TeamsSalariesParameters = [
  "teamId",
  "seasonName",
  "splitByTeams",
  "splitBySeasons",
  "splitByGames"
];

type GamesParameters = ["gameId", "teamId", "seasonName", "stageName"];

type GamesXgoalsParameters = [
  "gameId",
  "seasonName",
  "startDate",
  "endDate",
  "stageName"
];

/**
 * Returned types
 */

export type Player = {
  player_id: string;
  player_name: string;
  birth_date: string;
  height_ft: number;
  height_in: number;
  weight_lb: number;
  nationality: string;
  primary_broad_position: string;
  primary_general_position: string;
  season_name: string[];
};

export type Manager = {
  manager_id: string;
  manager_name: string;
  nationality: string;
};
export type Team = {
  team_id: string;
  team_name: string;
  team_short_name: string;
  team_abbreviation: string;
};

export type Stadia = {
  stadium_id: string;
  stadium_name: string;
  capacity: number;
  year_built: number;
  roof: boolean;
  turf: boolean;
  street: string;
  city: string;
  province: string;
  country: string;
  postal_code: string;
  latitude: number;
  longitude: number;
  field_x: number;
  field_y: number;
};

export type Referee = {
  referee_id: string;
  referee_name: string;
  birth_date: string;
  nationality: string;
};

export type PlayerXGoals = {
  player_id: string;
  general_position: GeneralPositions;
  minutes_played: number;
  shots: number;
  shots_on_target: number;
  goals: number;
  xgoals: number;
  xplace: number;
  goals_minus_xgoals: number;
  key_passes: number;
  primary_assists: number;
  xassists: number;
  primary_assists_minus_xassists: number;
  xgoals_plus_xassists: number;
  points_added: number;
  xpoints_added: number;

  team_id?: string | string[];
  game_id?: string;
  season_name?: string;
};
export type PlayerXPass = {
  attempted_passes_for: number;
  pass_completion_percentage_for: number;
  xpass_completion_percentage_for: number;
  passes_completed_over_expected_for: number;
  passes_completed_over_expected_p100_for: number;
  avg_vertical_distance_for: number;
  attempted_passes_against: number;
  pass_completion_percentage_against: number;
  xpass_completion_percentage_against: number;
  passes_completed_over_expected_against: number;
  passes_completed_over_expected_p100_against: number;
  avg_vertical_distance_against: number;
  passes_completed_over_expected_difference: number;
  avg_vertical_distance_difference: number;

  count_games?: number;
  team_id?: string | string[];
  game_id?: string;
  season_name?: string;
};
export type PlayerGoalsAdded = {
  player_id: string;
  team_id: string | string[];
  general_position: GeneralPositions;
  minutes_played: number;
  data?: {
    action_type:
      | "Dribbling"
      | "Fouling"
      | "Interrupting"
      | "Passing"
      | "Receiving"
      | "Shooting";
    goals_added_raw: number;
    goals_added_above_avg: number;
    count_actions: number;
  }[];

  goals_added_raw?: number;
  goals_added_above_replacement?: number;

  count_actions?: number;
  count_games?: number;
  game_id?: string;
  season_name?: string;
};

export type PlayerSalaries = {
  player_id: string;
  team_id: string;
  season_name: number;
  position: string;
  base_salary: number;
  guaranteed_compensation: number;
  mlspa_release: string;
};

export type GoalkeeperXGoals = {
  player_id: string;
  team_id: string;
  minutes_played: number;
  shots_faced: number;
  goals_conceded: number;
  saves: number;
  share_headed_shots: number;
  xgoals_gk_faced: number;
  goals_minus_xgoals_gk: number;
  goals_divided_by_xgoals_gk: number;

  game_id?: string;
  season_name?: string;
};
export type GoalkeeperGoalsAdded = {
  player_id: "0Oq6woOxQ6";
  team_id: "mKAqBBmqbg";
  minutes_played: number;

  data?: {
    action_type:
      | "Claiming"
      | "Fielding"
      | "Handling"
      | "Passing"
      | "Shotstopping"
      | "Sweeping";
    goals_added_raw: number;
    goals_added_above_avg: number;
    count_actions: number;
  }[];

  goals_added_raw?: number;
  goals_added_above_replacement?: number;
  count_actions?: number;

  game_id?: string;
  season_name?: string;
};
export type GamesXGoals = {
  game_id: string;
  date_time_utc: string;
  home_team_id: string;
  home_goals: number;
  home_team_xgoals: number;
  home_player_xgoals: number;
  away_team_id: string;
  away_goals: number;
  away_team_xgoals: number;
  away_player_xgoals: number;
  goal_difference: number;
  team_xgoal_difference: number;
  player_xgoal_difference: number;
  final_score_difference: number;
  home_xpoints: number;
  away_xpoints: number;
};
export type TeamXGoals = {
  team_id: string;
  shots_for: number;
  shots_against: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  xgoals_for: number;
  xgoals_against: number;
  xgoal_difference: number;
  goal_difference_minus_xgoal_difference: number;
  points: number;
  xpoints: number;

  count_games?: number;
  game_id?: string;
  season_name?: string;
};
export type TeamXPass = {
  attempted_passes_for: number;
  pass_completion_percentage_for: number;
  xpass_completion_percentage_for: number;
  passes_completed_over_expected_for: number;
  passes_completed_over_expected_p100_for: number;
  avg_vertical_distance_for: number;
  attempted_passes_against: number;
  pass_completion_percentage_against: number;
  xpass_completion_percentage_against: number;
  passes_completed_over_expected_against: number;
  passes_completed_over_expected_p100_against: number;
  avg_vertical_distance_against: number;
  passes_completed_over_expected_difference: number;
  avg_vertical_distance_difference: number;

  count_games?: number;
  team_id: string | string[];
  game_id?: string;
  season_name?: string;
};
export type TeamGoalsAdded = {
  minutes?: 32074;

  player_id: string;
  team_id: string | string[];
  general_position: GeneralPositions;
  minutes_played: number;
  data?: {
    action_type:
      | "Dribbling"
      | "Fouling"
      | "Interrupting"
      | "Passing"
      | "Receiving"
      | "Shooting";
    goals_added_raw: number;
    goals_added_above_avg: number;
    count_actions: number;
  }[];

  goals_added_raw?: number;
  goals_added_above_replacement?: number;

  count_actions?: number;
  count_games?: number;
  game_id?: string;
  season_name?: string;
};
export type TeamSalaries = unknown;
