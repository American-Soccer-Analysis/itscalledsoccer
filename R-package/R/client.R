#' Class representing an active session connected to the American Soccer Analysis public API.
#'
#' Does not take any arguments to initialize.
#' @export
AmericanSoccerAnalysis <- R6::R6Class("AmericanSoccerAnalysis",
    public = list(
        #' @field API_VERSION Latest API version.
        API_VERSION = "v1",

        #' @field MAX_API_LIMIT Maximum number of requests returned by the API by default.
        MAX_API_LIMIT = 1000,

        #' @field LEAGUES List of stylized league names.
        LEAGUES = c("nwsl", "mls", "uslc", "usl1", "nasl"),

        #' @field BASE_URL API base URL.
        BASE_URL = NULL,

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

        #' @description
        #' Creates a new `AmericanSoccerAnalysis` object.
        #' @return A new `AmericanSoccerAnalysis` object.
        initialize = function() {
            self$BASE_URL <- glue::glue("https://app.americansocceranalysis.com/api/{self$API_VERSION}")
            self$players <- get_entity(self, "player")
            self$teams <- get_entity(self, "team")
            self$stadia <- get_entity(self, "stadium")
            self$managers <- get_entity(self, "manager")
            self$referees <- get_entity(self, "referee")
        },

        #' @description
        #' Retrieves a data frame containing player names, IDs, and other metadata.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Player IDs on which to filter. Accepts a character vector of length >= 1.
        #' @param names Player names on which to filter. Partial matches are accepted. Accepts a character vector of length >= 1.
        get_players = function(leagues, ids, names) {
            players <- filter_entity(self$players, self$LEAGUES, leagues, ids, names)
            return(players)
        },

        #' @description
        #' Retrieves a data frame containing team names, abbreviations, and IDs.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Team IDs on which to filter. Accepts a character vector of length >= 1.
        #' @param names Team names on which to filter. Partial matches and abbreviations are accepted. Accepts a character vector of length >= 1.
        get_teams = function(leagues, ids, names) {
            teams <- filter_entity(self$teams, self$LEAGUES, leagues, ids, names)
            return(teams)
        },

        #' @description
        #' Retrieves a data frame containing stadium names, IDs, and other metadata.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Stadium IDs on which to filter. Accepts a character vector of length >= 1.
        #' @param names Stadium names on which to filter. Partial matches are accepted. Accepts a character vector of length >= 1.
        get_stadia = function(leagues, ids, names) {
            stadia <- filter_entity(self$stadia, self$LEAGUES, leagues, ids, names)
            return(stadia)
        },

        #' @description
        #' Retrieves a data frame containing manager names and IDs.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Manager IDs on which to filter. Accepts a character vector of length >= 1.
        #' @param names Manager names on which to filter. Partial matches are accepted. Accepts a character vector of length >= 1.
        get_managers = function(leagues, ids, names) {
            managers <- filter_entity(self$managers, self$LEAGUES, leagues, ids, names)
            return(managers)
        },

        #' @description
        #' Retrieves a data frame containing referee names and IDs.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ids Referee IDs on which to filter. Accepts a character vector of length >= 1.
        #' @param names Referee names on which to filter. Partial matches are accepted. Accepts a character vector of length >= 1.
        get_referees = function(leagues, ids, names) {
            referees <- filter_entity(self$referees, self$LEAGUES, leagues, ids, names)
            return(referees)
        },

        #' @description
        #' Retrieves a data frame containing game IDs, dates, opponents, scores, and other metadata.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param game_ids Game IDs on which to filter. Accepts a character vector of length >= 1.
        #' @param team_ids Team IDs on which to filter. Accepts a character vector of length >= 1.
        #' @param team_names Team names on which to filter. Partial matches and abbreviations are accepted. Accepts a character vector of length >= 1.
        #' @param seasons Seasons on which to filter. Accepts a character or integer vector of length >= 1.
        #' @param stages Stages (e.g., regular season, playoffs, etc.) on which to filter. See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        get_games = function(leagues, game_ids, team_ids, team_names, seasons, stages) {
            games <- get_games(self, leagues, game_ids, team_ids, team_names, seasons, stages)
            return(games)
        },

        #' @description
        #' Retrieves a data frame containing player xG data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_player_xgoals = function(leagues, ...) {
            player_xgoals <- get_stats(self, type = "xgoals", entity = "players", leagues, ...)
            return(player_xgoals)
        },

        #' @description
        #' Retrieves a data frame containing team xG data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_team_xgoals = function(leagues, ...) {
            team_xgoals <- get_stats(self, type = "xgoals", entity = "teams", leagues, ...)
            return(team_xgoals)
        },

        #' @description
        #' Retrieves a data frame containing goalkeeper xG data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_goalkeeper_xgoals = function(leagues, ...) {
            goalkeeper_xgoals <- get_stats(self, type = "xgoals", entity = "goalkeepers", leagues, ...)
            return(goalkeeper_xgoals)
        },

        #' @description
        #' Retrieves a data frame containing game xG data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_game_xgoals = function(leagues, ...) {
            game_xgoals <- get_stats(self, type = "xgoals", entity = "games", leagues, ...)
            return(game_xgoals)
        },

        #' @description
        #' Retrieves a data frame containing player xPass data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_player_xpass = function(leagues, ...) {
            player_xpass <- get_stats(self, type = "xpass", entity = "players", leagues, ...)
            return(player_xpass)
        },

        #' @description
        #' Retrieves a data frame containing team xPass data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_team_xpass = function(leagues, ...) {
            team_xpass <- get_stats(self, type = "xpass", entity = "teams", leagues, ...)
            return(team_xpass)
        },

        #' @description
        #' Retrieves a data frame containing player goals added (g+) data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_player_goals_added = function(leagues, ...) {
            player_goals_added <- get_stats(self, type = "goals-added", entity = "players", leagues, ...)
            return(player_goals_added)
        },

        #' @description
        #' Retrieves a data frame containing team goals added (g+) data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_team_goals_added = function(leagues, ...) {
            team_goals_added <- get_stats(self, type = "goals-added", entity = "teams", leagues, ...)
            return(team_goals_added)
        },

        #' @description
        #' Retrieves a data frame containing goalkeeper goals added (g+) data meeting the specified conditions.
        #' @param leagues Leagues on which to filter. Accepts a character vector of length >= 1.
        #' @param ... See the \href{https://app.americansocceranalysis.com/api/v1/__docs__/}{API documentation} for possible values. All arguments accept a vector of length >= 1.
        get_goalkeeper_goals_added = function(leagues, ...) {
            goalkeeper_goals_added <- get_stats(self, type = "goals-added", entity = "goalkeepers", leagues, ...)
            return(goalkeeper_goals_added)
        }
    )
)
