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
            self$players <- get_all_ids("player", self)
            self$teams <- get_all_ids("team", self)
            self$stadia <- get_all_ids("stadia", self)
            self$managers <- get_all_ids("manager", self)
            self$referees <- get_all_ids("referee", self)
        }
    )
)
