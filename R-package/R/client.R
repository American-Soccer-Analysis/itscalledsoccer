#' Class representing an active session connected to the American Soccer Analysis public API.
#'
#' Does not take any arguments to initialize.
#' @export
AmericanSoccerAnalysis <- R6::R6Class("AmericanSoccerAnalysis",
    public = list(
        #' @field API_VERSION Latest API version.
        API_VERSION = "v1",

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
            self$BASE_URL <- glue::glue("https://app.americansocceranalysis.com/api/{self$API_VERSION}/")
            self$players <- get_entity("player", self)
            self$teams <- get_entity("team", self)
            self$stadia <- get_entity("stadium", self)
            self$managers <- get_entity("manager", self)
            self$referees <- get_entity("referee", self)
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
        #' @param stages Stages (e.g., regular season, playoffs, etc.) on which to filter. See the \url{https://app.americansocceranalysis.com/api/v1/__swagger__/}{API documentation} for possible values. Accepts a character vector of length >= 1.
        get_games = function(leagues, game_ids, team_ids, team_names, seasons, stages) {
            games <- get_games(self, leagues, game_ids, team_ids, team_names, seasons, stages)
            return(games)
        }
    )
)
