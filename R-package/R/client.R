#' @title American Soccer Analysis API Client
#' @description Class representing an active session connected to the American Soccer Analysis public API.
#' @details Does not take any arguments to initialize.
#' @export
AmericanSoccerAnalysis <- R6::R6Class("AmericanSoccerAnalysis",
    public = list(
        #' @field API_VERSION Latest API version.
        API_VERSION = "v1",

        #' @field MAX_API_LIMIT Maximum number of requests returned by the API by default.
        MAX_API_LIMIT = 1000,

        #' @field LEAGUES List of stylized league names.
        LEAGUES = c("nwsl", "mls", "uslc", "usl1", "nasl", "mlsnp"),

        #' @field base_url API base URL.
        base_url = NULL,

        #' @field players Data frame containing players from all leagues.
        players = NULL,

        #' @field teams Data frame containing teams from all leagues.
        teams = NULL,

        #' @field stadia Data frame containing stadia from all leagues.
        stadia = NULL,

        #' @field managers Data frame containing managers from all leagues.
        managers = NULL,

        #' @field referees Data frame containing referees from all leagues.
        referees = NULL,

        #' @field httr_configs Configs to pass on to all \code{httr} functions. See \href{https://www.rdocumentation.org/packages/httr/versions/1.4.2/topics/config}{documentation}.
        httr_configs = list(),

        #' @description Creates a new \code{AmericanSoccerAnalysis} object.
        #' @param ... Configs to pass on to all \code{httr} functions. See \href{https://www.rdocumentation.org/packages/httr/versions/1.4.2/topics/config}{documentation}.
        #' @return A new \code{AmericanSoccerAnalysis} object.
        initialize = function(...) {
            self$base_url <- glue::glue("https://app.americansocceranalysis.com/api/{self$API_VERSION}")
            self$httr_configs <- list(...)
            self$players <- get_entity(self, "player")
            self$teams <- get_entity(self, "team")
            self$stadia <- get_entity(self, "stadium")
            self$managers <- get_entity(self, "manager")
            self$referees <- get_entity(self, "referee")
        },

        #' @description Appends new \code{httr} configs to the existing class.
        #' @param ... Configs to pass on to all \code{httr} functions. See \href{https://www.rdocumentation.org/packages/httr/versions/1.4.2/topics/config}{documentation}.
        add_httr_configs = function(...) {
            self$httr_configs <- c(self$httr_configs, list(...))
        },

        #' @description Removes all \code{httr} configs from the existing class.
        reset_httr_configs = function() {
            self$httr_configs <- list()
        },

        #' @description Retrieves a data frame containing player names, IDs, and other metadata.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Player IDs on which to filter. Cannot be combined with \code{names}. Accepts a character vector of length >= 1.
        #' @param names Player names on which to filter. Partial matches are accepted. Cannot be combined with \code{ids}. Accepts a character vector of length >= 1.
        get_players = function(leagues, ids, names) {
            players <- filter_entity(self, "players", leagues, ids, names)
            return(players)
        },

        #' @description Retrieves a data frame containing team names, abbreviations, and IDs.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Team IDs on which to filter. Cannot be combined with \code{names}. Accepts a character vector of length >= 1.
        #' @param names Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{ids}. Accepts a character vector of length >= 1.
        get_teams = function(leagues, ids, names) {
            teams <- filter_entity(self, "teams", leagues, ids, names)
            return(teams)
        },

        #' @description Retrieves a data frame containing stadium names, IDs, and other metadata.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Stadium IDs on which to filter. Cannot be combined with \code{names}. Accepts a character vector of length >= 1.
        #' @param names Stadium names on which to filter. Partial matches are accepted. Cannot be combined with \code{ids}. Accepts a character vector of length >= 1.
        get_stadia = function(leagues, ids, names) {
            stadia <- filter_entity(self, "stadia", leagues, ids, names)
            return(stadia)
        },

        #' @description Retrieves a data frame containing manager names and IDs.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Manager IDs on which to filter. Cannot be combined with \code{names}. Accepts a character vector of length >= 1.
        #' @param names Manager names on which to filter. Partial matches are accepted. Cannot be combined with \code{ids}. Accepts a character vector of length >= 1.
        get_managers = function(leagues, ids, names) {
            managers <- filter_entity(self, "managers", leagues, ids, names)
            return(managers)
        },

        #' @description Retrieves a data frame containing referee names and IDs.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Referee IDs on which to filter. Cannot be combined with \code{names}. Accepts a character vector of length >= 1.
        #' @param names Referee names on which to filter. Partial matches are accepted. Cannot be combined with \code{ids}. Accepts a character vector of length >= 1.
        get_referees = function(leagues, ids, names) {
            referees <- filter_entity(self, "referees", leagues, ids, names)
            return(referees)
        },

        #' @description Retrieves a data frame containing game IDs, dates, opponents, scores, and other metadata.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param game_ids Game IDs on which to filter. Accepts a character vector of length >= 1.
        #' @param team_ids Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #' @param team_names Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #' @param seasons Name(s)/year(s) of seasons. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #' @param stages Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        get_games = function(leagues, game_ids, team_ids, team_names, seasons, stages) {
            games <- get_games(self, leagues, game_ids, team_ids, team_names, seasons, stages)
            return(games)
        },

        #' @description Retrieves a data frame containing player xG data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{minimum_minutes}: Minimum threshold for sum of minutes played.
        #'     \item \code{minimum_shots}: Minimum threshold for sum of shots taken.
        #'     \item \code{minimum_key_passes}: Minimum threshold for sum of key passes.
        #'     \item \code{player_ids}: Player IDs on which to filter. Cannot be combined with \code{player_names}. Accepts a character vector of length >= 1.
        #'     \item \code{player_names}: Player names on which to filter. Partial matches are accepted. Cannot be combined with \code{player_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{shot_pattern}: Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a character vector of length >= 1.
        #'     \item \code{split_by_teams}: Logical indicator to group results by team.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season.
        #'     \item \code{split_by_games}: Logical indicator to group results by game.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{general_position}: Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a character vector of length >= 1.
        #'   }
        get_player_xgoals = function(leagues, ...) {
            player_xgoals <- get_stats(self, type = "xgoals", entity = "players", leagues, ...)
            return(player_xgoals)
        },

        #' @description Retrieves a data frame containing player xPass data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{minimum_minutes}: Minimum threshold for sum of minutes played.
        #'     \item \code{minimum_passes}: Minimum threshold for sum of attempted passes.
        #'     \item \code{player_ids}: Player IDs on which to filter. Cannot be combined with \code{player_names}. Accepts a character vector of length >= 1.
        #'     \item \code{player_names}: Player names on which to filter. Partial matches are accepted. Cannot be combined with \code{player_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{pass_origin_third}: Describes the third of the field from which the pass originated. Valid keywords include: 'Attacking', 'Middle', and 'Defensive'. Accepts a character vector of length >= 1.
        #'     \item \code{split_by_teams}: Logical indicator to group results by team.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season.
        #'     \item \code{split_by_games}: Logical indicator to group results by game.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{general_position}: Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a character vector of length >= 1.
        #'   }
        get_player_xpass = function(leagues, ...) {
            player_xpass <- get_stats(self, type = "xpass", entity = "players", leagues, ...)
            return(player_xpass)
        },

        #' @description Retrieves a data frame containing player goals added (g+) data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{minimum_minutes}: Minimum threshold for sum of minutes played.
        #'     \item \code{player_ids}: Player IDs on which to filter. Cannot be combined with \code{player_names}. Accepts a character vector of length >= 1.
        #'     \item \code{player_names}: Player names on which to filter. Partial matches are accepted. Cannot be combined with \code{player_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{split_by_teams}: Logical indicator to group results by team.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season.
        #'     \item \code{split_by_games}: Logical indicator to group results by game.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{action_type}: Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a character vector of length >= 1.
        #'     \item \code{general_position}: Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a character vector of length >= 1.
        #'     \item \code{above_replacement}: Logical indicator to compare players against replacement-level values. This will only return aggregated g+ values, rather than disaggregated g+ values by action type.
        #'   }
        get_player_goals_added = function(leagues, ...) {
            player_goals_added <- get_stats(self, type = "goals-added", entity = "players", leagues, ...)
            return(player_goals_added)
        },

        #' @description Retrieves a data frame containing player salary data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Currently, only MLS salary data is publicly available.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{player_ids}: Player IDs on which to filter. Cannot be combined with \code{player_names}. Accepts a character vector of length >= 1.
        #'     \item \code{player_names}: Player names on which to filter. Partial matches are accepted. Cannot be combined with \code{player_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{position}: Describes the general position, as reported by the players' association. Valid keywords include: 'GK', 'D', 'M', and 'F'. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'   }
        get_player_salaries = function(leagues, ...) {
            player_salaries <- get_stats(self, type = "salaries", entity = "players", leagues, ...)
            return(player_salaries)
        },

        #' @description Retrieves a data frame containing goalkeeper xG data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{minimum_minutes}: Minimum threshold for sum of minutes played.
        #'     \item \code{minimum_shots_faced}: Minimum threshold for sum of shots faced.
        #'     \item \code{player_ids}: Player IDs on which to filter. Cannot be combined with \code{player_names}. Accepts a character vector of length >= 1.
        #'     \item \code{player_names}: Player names on which to filter. Partial matches are accepted. Cannot be combined with \code{player_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{shot_pattern}: Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a character vector of length >= 1.
        #'     \item \code{split_by_teams}: Logical indicator to group results by team.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season.
        #'     \item \code{split_by_games}: Logical indicator to group results by game.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'   }
        get_goalkeeper_xgoals = function(leagues, ...) {
            goalkeeper_xgoals <- get_stats(self, type = "xgoals", entity = "goalkeepers", leagues, ...)
            return(goalkeeper_xgoals)
        },

        #' @description Retrieves a data frame containing goalkeeper goals added (g+) data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{minimum_minutes}: Minimum threshold for sum of minutes played.
        #'     \item \code{player_ids}: Player IDs on which to filter. Cannot be combined with \code{player_names}. Accepts a character vector of length >= 1.
        #'     \item \code{player_names}: Player names on which to filter. Partial matches are accepted. Cannot be combined with \code{player_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{split_by_teams}: Logical indicator to group results by team.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season.
        #'     \item \code{split_by_games}: Logical indicator to group results by game.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{action_type}: Describes the goals added (g+) action type. Valid keywords include: 'Claiming', 'Fielding', 'Handling', 'Passing', 'Shotstopping', and 'Sweeping'. Accepts a character vector of length >= 1.
        #'     \item \code{above_replacement}: Logical indicator to compare players against replacement-level values. This will only return aggregated g+ values, rather than disaggregated g+ values by action type.
        #'   }
        get_goalkeeper_goals_added = function(leagues, ...) {
            goalkeeper_goals_added <- get_stats(self, type = "goals-added", entity = "goalkeepers", leagues, ...)
            return(goalkeeper_goals_added)
        },

        #' @description Retrieves a data frame containing team xG data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{shot_pattern}: Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a character vector of length >= 1.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season.
        #'     \item \code{split_by_games}: Logical indicator to group results by game.
        #'     \item \code{home_only}: Logical indicator to only include results from home games.
        #'     \item \code{away_only}: Logical indicator to only include results from away games.
        #'     \item \code{home_adjusted}: Logical indicator to adjust certain values based on the share of home games a team has played during the specified duration.
        #'     \item \code{even_game_state}: Logical indicator to only include shots taken when the score was level.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'   }
        get_team_xgoals = function(leagues, ...) {
            team_xgoals <- get_stats(self, type = "xgoals", entity = "teams", leagues, ...)
            return(team_xgoals)
        },

        #' @description Retrieves a data frame containing team xPass data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{pass_origin_third}: Describes the third of the field from which the pass originated. Valid keywords include: 'Attacking', 'Middle', and 'Defensive'. Accepts a character vector of length >= 1.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season.
        #'     \item \code{split_by_games}: Logical indicator to group results by game.
        #'     \item \code{home_only}: Logical indicator to only include results from home games.
        #'     \item \code{away_only}: Logical indicator to only include results from away games.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'   }
        get_team_xpass = function(leagues, ...) {
            team_xpass <- get_stats(self, type = "xpass", entity = "teams", leagues, ...)
            return(team_xpass)
        },

        #' @description Retrieves a data frame containing team goals added (g+) data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{action_type}: Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a character vector of length >= 1.
        #'     \item \code{zone}: Zone number on pitch. Zones 1-5 are the defensive-most zones, and zones 26-30 are the attacking-most zones. Accepts a character or integer vector of length >= 1.
        #'     \item \code{gamestate_trunc}: Integer (score differential) value between -2 and 2, inclusive. Gamestates more extreme than -2 and 2 have been included with -2 and 2, respectively. Accepts a character or integer vector of length >= 1.
        #'   }
        get_team_goals_added = function(leagues, ...) {
            team_goals_added <- get_stats(self, type = "goals-added", entity = "teams", leagues, ...)
            return(team_goals_added)
        },

        #' @description Retrieves a data frame containing team salary data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Currently, only MLS salary data is publicly available.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{team_ids}: Team IDs on which to filter. Cannot be combined with \code{team_names}. Accepts a character vector of length >= 1.
        #'     \item \code{team_names}: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with \code{team_ids}. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{split_by_teams}: Logical indicator to group results by team. Results must be grouped by at least one of teams, positions, or seasons. Value is TRUE by default.
        #'     \item \code{split_by_seasons}: Logical indicator to group results by season. Results must be grouped by at least one of teams, positions, or seasons.
        #'     \item \code{split_by_positions}: Logical indicator to group results by positions. Results must be grouped by at least one of teams, positions, or seasons.
        #'   }
        get_team_salaries = function(leagues, ...) {
            team_salaries <- get_stats(self, type = "salaries", entity = "teams", leagues, ...)
            return(team_salaries)
        },

        #' @description Retrieves a data frame containing game xG data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... The following arguments will be parsed:
        #'   \itemize{
        #'     \item \code{game_ids}: Game IDs on which to filter. Accepts a character vector of length >= 1.
        #'     \item \code{season_name}: Name(s)/year(s) of seasons. Cannot be combined with a date range. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'     \item \code{start_date}: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{end_date}: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with \code{season_name}.
        #'     \item \code{stage_name}: Describes the stage of competition in which a game took place. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        #'   }
        get_game_xgoals = function(leagues, ...) {
            game_xgoals <- get_stats(self, type = "xgoals", entity = "games", leagues, ...)
            return(game_xgoals)
        }
    )
)
