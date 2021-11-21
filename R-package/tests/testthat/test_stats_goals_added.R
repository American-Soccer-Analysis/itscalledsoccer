test_that("Querying player-level goals added (g+) values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_player_goals_added() %>% nrow()
    expect_gte(.obj, 0)

    # Unnamed filters ---------------------------------------------------
    expect_error(asa_client$get_player_goals_added("abc", "def", "ghi"))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_player_goals_added(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .exp <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$player_id) %>%
        dplyr::pull(.data$player_id)

    .obj <- asa_client$get_player_goals_added(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$player_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    .exp <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$player_id) %>%
        dplyr::pull(.data$player_id)

    .obj <- asa_client$get_player_goals_added(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$player_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Minimum minutes ----------------------------------------------------
    .exp <- 1000
    .obj <- asa_client$get_player_goals_added(minimum_minutes = .exp) %>%
        dplyr::pull(.data$minutes_played) %>%
        min()

    expect_gte(.obj, .exp)

    # Player IDs and names (invalid) -------------------------------------
    expect_error(asa_client$get_player_goals_added(player_ids = "abc", player_names = "abc"))

    # Single ID ----------------------------------------------------------
    IDS <- "vzqo8xZQap"

    .obj <- asa_client$get_player_goals_added(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple IDs -------------------------------------------------------
    IDS <- c("vzqo8xZQap", "9vQ22BR7QK")

    .obj <- asa_client$get_player_goals_added(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single player name -------------------------------------------------
    NAMES <- "Dax McCarty"

    .obj <- asa_client$get_player_goals_added(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple player names ----------------------------------------------
    NAMES <- c("Dax McCarty", "Tiffany McCarty")

    .obj <- asa_client$get_player_goals_added(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Team IDs and names (invalid) ---------------------------------------
    expect_error(asa_client$get_player_goals_added(team_ids = "abc", team_names = "abc"))

    # Single team ID -----------------------------------------------------
    IDS <- "NWMWlBK5lz"

    .obj <- asa_client$get_player_goals_added(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team IDs --------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "9Yqdwg85vJ")

    .obj <- asa_client$get_player_goals_added(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single team name ---------------------------------------------------
    NAMES <- "Red Bulls"

    .obj <- asa_client$get_player_goals_added(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team names ------------------------------------------------
    NAMES <- c("Chicago", "Seattle")

    .obj <- asa_client$get_player_goals_added(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # TODO: Add tests for season_name
    # TODO: Add tests for date range

    # Partial date range (invalid) --------------------------------------
    expect_error(asa_client$get_player_goals_added(start_date = "abc"))

    # Invalid date range ------------------------------------------------
    expect_error(asa_client$get_player_goals_added(start_date = "2021-01-01", end_date = "2020-01-01"))

    # Season and date range (invalid) ------------------------------------
    expect_error(asa_client$get_player_goals_added(season_name = "abc", start_date = "abc"))

    # TODO: Add tests for shot_pattern
    # TODO: Add tests for split_by_teams
    # TODO: Add tests for split_by_seasons
    # TODO: Add tests for split_by_games
    # TODO: Add tests for stage_name

    # Single action type -------------------------------------------------
    .exp <- "Passing"
    .obj <- asa_client$get_player_goals_added(action_type = .exp) %>%
        tidyr::unnest(.data$data) %>%
        dplyr::distinct(.data$action_type) %>%
        dplyr::arrange(.data$action_type) %>%
        dplyr::pull(.data$action_type)

    expect_equal(.obj, .exp)

    # Multiple action types ----------------------------------------------
    .exp <- c("Passing", "Shooting")
    .obj <- asa_client$get_player_goals_added(action_type = .exp) %>%
        tidyr::unnest(.data$data) %>%
        dplyr::distinct(.data$action_type) %>%
        dplyr::arrange(.data$action_type) %>%
        dplyr::pull(.data$action_type)

    expect_equal(.obj, .exp)

    # Single position ----------------------------------------------------
    .exp <- "AM"
    .obj <- asa_client$get_player_goals_added(general_position = .exp) %>%
        dplyr::distinct(.data$general_position) %>%
        dplyr::arrange(.data$general_position) %>%
        dplyr::pull(.data$general_position)

    expect_equal(.obj, .exp)

    # Multiple positions -------------------------------------------------
    .exp <- c("AM", "DM")
    .obj <- asa_client$get_player_goals_added(general_position = .exp) %>%
        dplyr::distinct(.data$general_position) %>%
        dplyr::arrange(.data$general_position) %>%
        dplyr::pull(.data$general_position)

    expect_equal(.obj, .exp)

    # Above replacement --------------------------------------------------
    .exp <- "goals_added_above_replacement"
    .obj <- asa_client$get_player_goals_added(above_replacement = TRUE) %>%
        dplyr::select(dplyr::ends_with("above_replacement")) %>%
        names()

    expect_equal(.obj, .exp)

})

test_that("Querying goalkeeper-level goals added (g+) values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_goalkeeper_goals_added() %>% nrow()
    expect_gte(.obj, 0)

    # Unnamed filters ---------------------------------------------------
    expect_error(asa_client$get_goalkeeper_goals_added("abc", "def", "ghi"))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_goalkeeper_goals_added(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .exp <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$player_id) %>%
        dplyr::pull(.data$player_id)

    .obj <- asa_client$get_goalkeeper_goals_added(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$player_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    .exp <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$player_id) %>%
        dplyr::pull(.data$player_id)

    .obj <- asa_client$get_goalkeeper_goals_added(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$player_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Minimum minutes ----------------------------------------------------
    .exp <- 1000
    .obj <- asa_client$get_goalkeeper_goals_added(minimum_minutes = .exp) %>%
        dplyr::pull(.data$minutes_played) %>%
        min()

    expect_gte(.obj, .exp)

    # Player IDs and names (invalid) -------------------------------------
    expect_error(asa_client$get_goalkeeper_goals_added(player_ids = "abc", player_names = "abc"))

    # Single player ID ---------------------------------------------------
    IDS <- "vzqoWbkqap"

    .obj <- asa_client$get_goalkeeper_goals_added(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple player IDs ------------------------------------------------
    IDS <- c("vzqoWbkqap", "gOMn6OlmMw")

    .obj <- asa_client$get_goalkeeper_goals_added(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single player name -------------------------------------------------
    NAMES <- "Luis Robles"

    .obj <- asa_client$get_goalkeeper_goals_added(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple player names ----------------------------------------------
    NAMES <- c("Luis Robles", "Ryan Meara")

    .obj <- asa_client$get_goalkeeper_goals_added(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Team IDs and names (invalid) ---------------------------------------
    expect_error(asa_client$get_goalkeeper_goals_added(team_ids = "abc", team_names = "abc"))

    # Single team ID -----------------------------------------------------
    IDS <- "NWMWlBK5lz"

    .obj <- asa_client$get_goalkeeper_goals_added(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team IDs --------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "9Yqdwg85vJ")

    .obj <- asa_client$get_goalkeeper_goals_added(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single team name ---------------------------------------------------
    NAMES <- "Red Bulls"

    .obj <- asa_client$get_goalkeeper_goals_added(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team names ------------------------------------------------
    NAMES <- c("Chicago", "Seattle")

    .obj <- asa_client$get_goalkeeper_goals_added(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # TODO: Add tests for season_name
    # TODO: Add tests for date range

    # Partial date range (invalid) --------------------------------------
    expect_error(asa_client$get_goalkeeper_goals_added(start_date = "abc"))

    # Invalid date range ------------------------------------------------
    expect_error(asa_client$get_goalkeeper_goals_added(start_date = "2021-01-01", end_date = "2020-01-01"))

    # Season and date range (invalid) ------------------------------------
    expect_error(asa_client$get_goalkeeper_goals_added(season_name = "abc", start_date = "abc"))

    # TODO: Add tests for split_by_teams
    # TODO: Add tests for split_by_seasons
    # TODO: Add tests for split_by_games
    # TODO: Add tests for stage_name

    # Single action type -------------------------------------------------
    .exp <- "Shotstopping"
    .obj <- asa_client$get_goalkeeper_goals_added(action_type = .exp) %>%
        tidyr::unnest(.data$data) %>%
        dplyr::distinct(.data$action_type) %>%
        dplyr::arrange(.data$action_type) %>%
        dplyr::pull(.data$action_type)

    expect_equal(.obj, .exp)

    # Multiple action types ----------------------------------------------
    .exp <- c("Shotstopping", "Sweeping")
    .obj <- asa_client$get_goalkeeper_goals_added(action_type = .exp) %>%
        tidyr::unnest(.data$data) %>%
        dplyr::distinct(.data$action_type) %>%
        dplyr::arrange(.data$action_type) %>%
        dplyr::pull(.data$action_type)

    expect_equal(.obj, .exp)

    # Above replacement --------------------------------------------------
    .exp <- "goals_added_above_replacement"
    .obj <- asa_client$get_goalkeeper_goals_added(above_replacement = TRUE) %>%
        dplyr::select(dplyr::ends_with("above_replacement")) %>%
        names()

    expect_equal(.obj, .exp)

})

test_that("Querying team-level goals added (g+) values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_team_goals_added() %>% nrow()
    expect_gte(.obj, 0)

    # Unnamed filters ---------------------------------------------------
    expect_error(asa_client$get_team_goals_added("abc", "def", "ghi"))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_team_goals_added(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$team_id) %>%
        dplyr::pull(.data$team_id)

    .obj <- asa_client$get_team_goals_added(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$team_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$team_id) %>%
        dplyr::pull(.data$team_id)

    .obj <- asa_client$get_team_goals_added(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$team_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Team IDs and names (invalid) ---------------------------------------
    expect_error(asa_client$get_team_goals_added(team_ids = "abc", team_names = "abc"))

    # Single team ID -----------------------------------------------------
    IDS <- "NWMWlBK5lz"

    .obj <- asa_client$get_team_goals_added(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team IDs --------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "9Yqdwg85vJ")

    .obj <- asa_client$get_team_goals_added(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single team name ---------------------------------------------------
    NAMES <- "Red Bulls"

    .obj <- asa_client$get_team_goals_added(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team names ------------------------------------------------
    NAMES <- c("Chicago", "Seattle")

    .obj <- asa_client$get_team_goals_added(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # TODO: Add tests for season_name
    # TODO: Add tests for split_by_seasons
    # TODO: Add tests for stage_name

    # Single action type -------------------------------------------------
    .exp <- "Passing"
    .obj <- asa_client$get_team_goals_added(action_type = .exp) %>%
        tidyr::unnest(.data$data) %>%
        dplyr::distinct(.data$action_type) %>%
        dplyr::arrange(.data$action_type) %>%
        dplyr::pull(.data$action_type)

    expect_equal(.obj, .exp)

    # Multiple action types ----------------------------------------------
    .exp <- c("Passing", "Shooting")
    .obj <- asa_client$get_team_goals_added(action_type = .exp) %>%
        tidyr::unnest(.data$data) %>%
        dplyr::distinct(.data$action_type) %>%
        dplyr::arrange(.data$action_type) %>%
        dplyr::pull(.data$action_type)

    expect_equal(.obj, .exp)

    # TODO: Add tests for zone
    # TODO: Add tests for gamestate_trunc

})
