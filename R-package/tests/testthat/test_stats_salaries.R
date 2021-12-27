test_that("Querying player-level salary values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_player_salaries() %>% nrow()
    expect_gte(.obj, 0)

    # Unnamed filters ---------------------------------------------------
    expect_error(asa_client$get_player_salaries("abc", "def", "ghi"))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_player_salaries(leagues = "abc"))
    expect_error(asa_client$get_player_salaries(leagues = "nasl"))
    expect_error(asa_client$get_player_salaries(leagues = c("mls", "nasl")))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .exp <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$player_id) %>%
        dplyr::pull(.data$player_id)

    .obj <- asa_client$get_player_salaries(leagues = LEAGUES) %>%
        dplyr::mutate(obj = .data$player_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Player IDs and names (invalid) -------------------------------------
    expect_error(asa_client$get_player_salaries(player_ids = "abc", player_names = "abc"))

    # Single ID ----------------------------------------------------------
    IDS <- "vzqo8xZQap"

    .obj <- asa_client$get_player_salaries(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple IDs -------------------------------------------------------
    IDS <- c("vzqo8xZQap", "9vQ22BR7QK")

    .obj <- asa_client$get_player_salaries(player_ids = IDS) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(.data$player_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single player name -------------------------------------------------
    NAMES <- "Dax McCarty"

    .obj <- asa_client$get_player_salaries(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple player names ----------------------------------------------
    NAMES <- c("Dax McCarty", "Sean Davis")

    .obj <- asa_client$get_player_salaries(player_names = NAMES) %>%
        dplyr::distinct(.data$player_id) %>%
        nrow()

    .exp <- asa_client$players %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Team IDs and names (invalid) ---------------------------------------
    expect_error(asa_client$get_player_salaries(team_ids = "abc", team_names = "abc"))

    # Single team ID -----------------------------------------------------
    IDS <- "NWMWlBK5lz"

    .obj <- asa_client$get_player_salaries(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team IDs --------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "lgpMOvnQzy")

    .obj <- asa_client$get_player_salaries(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single team name ---------------------------------------------------
    NAMES <- "Red Bulls"
    LEAGUES <- "mls"

    .obj <- asa_client$get_player_salaries(team_names = NAMES, leagues = LEAGUES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team names ------------------------------------------------
    NAMES <- c("Chicago", "Seattle")
    LEAGUES <- "mls"

    .obj <- asa_client$get_player_salaries(team_names = NAMES, leagues = LEAGUES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # TODO: Add tests for season_name
    # TODO: Add tests for date range

    # Partial date range (invalid) --------------------------------------
    expect_error(asa_client$get_player_salaries(start_date = "abc"))

    # Invalid date range ------------------------------------------------
    expect_error(asa_client$get_player_salaries(start_date = "2021-01-01", end_date = "2020-01-01"))

    # Season and date range (invalid) ------------------------------------
    expect_error(asa_client$get_player_salaries(season_name = "abc", start_date = "abc"))

    # TODO: Add tests for position

})

test_that("Querying team-level salary values works properly", {

    # No filters ---------------------------------------------------------
    .obj <- asa_client$get_team_salaries() %>% nrow()
    expect_gte(.obj, 0)

    # Unnamed filters ---------------------------------------------------
    expect_error(asa_client$get_team_salaries("abc", "def", "ghi"))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_team_salaries(leagues = "abc"))
    expect_error(asa_client$get_team_salaries(leagues = "nasl"))
    expect_error(asa_client$get_team_salaries(leagues = c("mls", "nasl")))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$team_id) %>%
        dplyr::pull(.data$team_id)

    .obj <- asa_client$get_team_salaries(leagues = LEAGUES) %>%
        dplyr::filter(!is.na(team_id)) %>%
        dplyr::mutate(obj = .data$team_id %in% .exp) %>%
        dplyr::pull(obj) %>%
        mean(na.rm = TRUE)

    expect_equal(.obj, 1)

    # Team IDs and names (invalid) ---------------------------------------
    expect_error(asa_client$get_team_salaries(team_ids = "abc", team_names = "abc"))

    # Single team ID -----------------------------------------------------
    IDS <- "NWMWlBK5lz"

    .obj <- asa_client$get_team_salaries(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(.data$team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team IDs --------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "lgpMOvnQzy")

    .obj <- asa_client$get_team_salaries(team_ids = IDS) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        dplyr::filter(.data$team_id %in% IDS) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Single team name ---------------------------------------------------
    NAMES <- "Red Bulls"
    LEAGUES <- "mls"

    .obj <- asa_client$get_team_salaries(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # Multiple team names ------------------------------------------------
    NAMES <- c("Chicago", "Seattle")
    LEAGUES <- "mls"

    .obj <- asa_client$get_team_salaries(team_names = NAMES) %>%
        tidyr::unnest(.data$team_id) %>%
        dplyr::distinct(team_id) %>%
        nrow()

    .exp <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        nrow()

    expect_equal(.obj, .exp)

    # TODO: Add tests for season_name
    # TODO: Add tests for split_by_teams
    # TODO: Add tests for split_by_seasons
    # TODO: Add tests for split_by_positions

    # Invalid split arguments --------------------------------------------
    expect_error(asa_client$get_team_salaries(split_by_teams = FALSE, split_by_seasons = FALSE, split_by_positions = FALSE))

})
