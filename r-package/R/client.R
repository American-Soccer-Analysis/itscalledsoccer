#' @export
AmericanSoccerAnalysis <- R6::R6Class("AmericanSoccerAnalysis",
    public = list(
        API_VERSION = "v1",
        LEAGUES = c("nwsl", "mls", "uslc", "usl1", "nasl"),
        BASE_URL = NULL,
        players = NULL,
        teams = NULL,
        stadia = NULL,
        managers = NULL,
        referees = NULL,
        initialize = function() {
            self$BASE_URL <- glue::glue("https://app.americansocceranalysis.com/api/{self$API_VERSION}/")
            self$players <- get_entity("player", self)
            self$teams <- get_entity("team", self)
            self$stadia <- get_entity("stadium", self)
            self$managers <- get_entity("manager", self)
            self$referees <- get_entity("referee", self)
        },
        get_players = function(leagues, ids, names) {
            players <- filter_entity(self$players, self$LEAGUES, leagues, ids, names)
            return(players)
        },
        get_teams = function(leagues, ids, names) {
            teams <- filter_entity(self$teams, self$LEAGUES, leagues, ids, names)
            return(teams)
        },
        get_stadia = function(leagues, ids, names) {
            stadia <- filter_entity(self$stadia, self$LEAGUES, leagues, ids, names)
            return(stadia)
        },
        get_managers = function(leagues, ids, names) {
            managers <- filter_entity(self$managers, self$LEAGUES, leagues, ids, names)
            return(managers)
        },
        get_referees = function(leagues, ids, names) {
            referees <- filter_entity(self$referees, self$LEAGUES, leagues, ids, names)
            return(referees)
        },
        get_games = function(leagues, game_ids, team_ids, team_names, seasons, stages) {
            games <- get_games(self, leagues, game_ids, team_ids, team_names, seasons, stages)
            return(games)
        }
    )
)
