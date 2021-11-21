test_that("Querying player-level xG values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_player_xgoals() %>% nrow()
    expect_gte(.obj, 0)

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_player_xgoals(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .exp <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$player_id) %>%
        dplyr::pull(.data$player_id)

    .obj <- asa_client$get_player_xgoals(leagues = LEAGUES) %>%
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

    .obj <- asa_client$get_player_xgoals(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$player_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Minimum minutes ----------------------------------------------------
    .exp <- 1000
    .obj <- asa_client$get_player_xgoals(minimum_minutes = .exp) %>%
        dplyr::pull(.data$minutes_played) %>%
        min()

    expect_gte(.obj, .exp)

    # Minimum shots ------------------------------------------------------
    .exp <- 100
    .obj <- asa_client$get_player_xgoals(minimum_shots = .exp) %>%
        dplyr::pull(.data$shots) %>%
        min()

    expect_gte(.obj, .exp)

    # Minimum key_passes -------------------------------------------------
    .exp <- 100
    .obj <- asa_client$get_player_xgoals(minimum_key_passes = .exp) %>%
        dplyr::pull(.data$key_passes) %>%
        min()

    expect_gte(.obj, .exp)

    # Player IDs and names (invalid) -------------------------------------
    expect_error(asa_client$get_player_xgoals(player_ids = "abc", player_names = "abc"))

    # Single ID ----------------------------------------------------------
    IDS <- "vzqo8xZQap"

    .obj <- asa_client$get_player_xgoals(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple IDs -------------------------------------------------------
    IDS <- c("vzqo8xZQap", "9vQ22BR7QK")

    .obj <- asa_client$get_player_xgoals(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single player name -------------------------------------------------
    NAMES <- "Dax McCarty"

    .obj <- asa_client$get_player_xgoals(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple player names ----------------------------------------------
    NAMES <- c("Dax McCarty", "Tiffany McCarty")

    .obj <- asa_client$get_player_xgoals(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Team IDs and names (invalid) ---------------------------------------
    expect_error(asa_client$get_player_xgoals(team_ids = "abc", team_names = "abc"))

    # Single team ID -----------------------------------------------------
    IDS <- "NWMWlBK5lz"

    .obj <- asa_client$get_player_xgoals(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team IDs --------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "9Yqdwg85vJ")

    .obj <- asa_client$get_player_xgoals(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single team name ---------------------------------------------------
    NAMES <- "Red Bulls"

    .obj <- asa_client$get_player_xgoals(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team names ------------------------------------------------
    NAMES <- c("Chicago", "Seattle")

    .obj <- asa_client$get_player_xgoals(team_names = NAMES) %>%
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
    expect_error(asa_client$get_player_xgoals(start_date = "abc"))

    # Invalid date range ------------------------------------------------
    expect_error(asa_client$get_player_xgoals(start_date = "2021-01-01", end_date = "2020-01-01"))

    # Season and date range (invalid) ------------------------------------
    expect_error(asa_client$get_player_xgoals(season_name = "abc", start_date = "abc"))

    # TODO: Add tests for shot_pattern
    # TODO: Add tests for split_by_teams
    # TODO: Add tests for split_by_seasons
    # TODO: Add tests for split_by_games
    # TODO: Add tests for stage_name

    # Single position ----------------------------------------------------
    .exp <- "AM"
    .obj <- asa_client$get_player_xgoals(general_position = .exp) %>%
        dplyr::distinct(.data$general_position) %>%
        dplyr::arrange(.data$general_position) %>%
        dplyr::pull(.data$general_position)

    expect_equal(.obj, .exp)

    # Multiple positions -------------------------------------------------
    .exp <- c("AM", "DM")
    .obj <- asa_client$get_player_xgoals(general_position = .exp) %>%
        dplyr::distinct(.data$general_position) %>%
        dplyr::arrange(.data$general_position) %>%
        dplyr::pull(.data$general_position)

    expect_equal(.obj, .exp)

})

test_that("Querying goalkeeper-level xG values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_goalkeeper_xgoals() %>% nrow()
    expect_gte(.obj, 0)

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_goalkeeper_xgoals(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .exp <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$player_id) %>%
        dplyr::pull(.data$player_id)

    .obj <- asa_client$get_goalkeeper_xgoals(leagues = LEAGUES) %>%
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

    .obj <- asa_client$get_goalkeeper_xgoals(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$player_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Minimum minutes ----------------------------------------------------
    .exp <- 1000
    .obj <- asa_client$get_goalkeeper_xgoals(minimum_minutes = .exp) %>%
        dplyr::pull(.data$minutes_played) %>%
        min()

    expect_gte(.obj, .exp)

    # Minimum shots faced ------------------------------------------------
    .exp <- 100
    .obj <- asa_client$get_goalkeeper_xgoals(minimum_shots_faced = .exp) %>%
        dplyr::pull(.data$shots_faced) %>%
        min()

    expect_gte(.obj, .exp)

    # Player IDs and names (invalid) -------------------------------------
    expect_error(asa_client$get_goalkeeper_xgoals(player_ids = "abc", player_names = "abc"))

    # Single player ID ---------------------------------------------------
    IDS <- "vzqoWbkqap"

    .obj <- asa_client$get_goalkeeper_xgoals(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple player IDs ------------------------------------------------
    IDS <- c("vzqoWbkqap", "gOMn6OlmMw")

    .obj <- asa_client$get_goalkeeper_xgoals(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single player name -------------------------------------------------
    NAMES <- "Luis Robles"

    .obj <- asa_client$get_goalkeeper_xgoals(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple player names ----------------------------------------------
    NAMES <- c("Luis Robles", "Ryan Meara")

    .obj <- asa_client$get_goalkeeper_xgoals(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Team IDs and names (invalid) ---------------------------------------
    expect_error(asa_client$get_goalkeeper_xgoals(team_ids = "abc", team_names = "abc"))

    # Single team ID -----------------------------------------------------
    IDS <- "NWMWlBK5lz"

    .obj <- asa_client$get_goalkeeper_xgoals(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team IDs --------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "9Yqdwg85vJ")

    .obj <- asa_client$get_goalkeeper_xgoals(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single team name ---------------------------------------------------
    NAMES <- "Red Bulls"

    .obj <- asa_client$get_goalkeeper_xgoals(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team names ------------------------------------------------
    NAMES <- c("Chicago", "Seattle")

    .obj <- asa_client$get_goalkeeper_xgoals(team_names = NAMES) %>%
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
    expect_error(asa_client$get_goalkeeper_xgoals(start_date = "abc"))

    # Invalid date range ------------------------------------------------
    expect_error(asa_client$get_goalkeeper_xgoals(start_date = "2021-01-01", end_date = "2020-01-01"))

    # Season and date range (invalid) ------------------------------------
    expect_error(asa_client$get_goalkeeper_xgoals(season_name = "abc", start_date = "abc"))

    # TODO: Add tests for shot_pattern
    # TODO: Add tests for split_by_teams
    # TODO: Add tests for split_by_seasons
    # TODO: Add tests for split_by_games
    # TODO: Add tests for stage_name

})

test_that("Querying team-level xG values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_team_xgoals() %>% nrow()
    expect_gte(.obj, 0)

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_team_xgoals(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$team_id) %>%
        dplyr::pull(.data$team_id)

    .obj <- asa_client$get_team_xgoals(leagues = LEAGUES) %>%
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

    .obj <- asa_client$get_team_xgoals(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$team_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Team IDs and names (invalid) ---------------------------------------
    expect_error(asa_client$get_team_xgoals(team_ids = "abc", team_names = "abc"))

    # Single team ID -----------------------------------------------------
    IDS <- "NWMWlBK5lz"

    .obj <- asa_client$get_team_xgoals(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team IDs --------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "9Yqdwg85vJ")

    .obj <- asa_client$get_team_xgoals(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single team name ---------------------------------------------------
    NAMES <- "Red Bulls"

    .obj <- asa_client$get_team_xgoals(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team names ------------------------------------------------
    NAMES <- c("Chicago", "Seattle")

    .obj <- asa_client$get_team_xgoals(team_names = NAMES) %>%
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
    expect_error(asa_client$get_team_xgoals(start_date = "abc"))

    # Invalid date range ------------------------------------------------
    expect_error(asa_client$get_team_xgoals(start_date = "2021-01-01", end_date = "2020-01-01"))

    # Season and date range (invalid) ------------------------------------
    expect_error(asa_client$get_team_xgoals(season_name = "abc", start_date = "abc"))

    # TODO: Add tests for shot_pattern
    # TODO: Add tests for split_by_seasons
    # TODO: Add tests for split_by_games
    # TODO: Add tests for home_only
    # TODO: Add tests for away_only
    # TODO: Add tests for home_adjusted
    # TODO: Add tests for even_game_state
    # TODO: Add tests for stage_name

})

test_that("Querying game-level xG values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_game_xgoals() %>% nrow()
    expect_gte(.obj, 0)

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_game_xgoals(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .obj <- asa_client$get_game_xgoals(leagues = LEAGUES) %>%
        dplyr::select(.data$game_id, .data$home_team_id, .data$away_team_id) %>%
        tidyr::pivot_longer(cols = dplyr::ends_with("team_id"), values_to = "team_id") %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    .obj <- asa_client$get_game_xgoals(leagues = LEAGUES) %>%
        dplyr::select(.data$game_id, .data$home_team_id, .data$away_team_id) %>%
        tidyr::pivot_longer(cols = dplyr::ends_with("team_id"), values_to = "team_id") %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    expect_equal(.obj, .exp)

    # TODO: Add tests for season_name
    # TODO: Add tests for date range

    # Partial date range (invalid) --------------------------------------
    expect_error(asa_client$get_game_xgoals(start_date = "abc"))

    # Invalid date range ------------------------------------------------
    expect_error(asa_client$get_game_xgoals(start_date = "2021-01-01", end_date = "2020-01-01"))

    # Season and date range (invalid) ------------------------------------
    expect_error(asa_client$get_game_xgoals(season_name = "abc", start_date = "abc"))

    # TODO: Add tests for stage_name

})
