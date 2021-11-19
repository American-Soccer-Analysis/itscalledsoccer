test_that("Filtering players works properly", {

    # No filters ---------------------------------------------------------
    df_a <- asa_client$players
    df_b <- asa_client$get_players()

    expect_equal(nrow(df_b), nrow(df_a))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_players(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    df_a <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES)

    df_b <- asa_client$get_players(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    df_a <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$player_id)

    df_b <- asa_client$get_players(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # IDs and names (invalid) --------------------------------------------
    expect_error(asa_client$get_players(ids = "abc", names = "abc"))

    # Single ID ----------------------------------------------------------
    IDS <- "vzqo8xZQap"

    df_a <- asa_client$players %>% dplyr::filter(.data$player_id %in% IDS)
    df_b <- asa_client$get_players(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple IDs -------------------------------------------------------
    IDS <- c("vzqo8xZQap", "9vQ22BR7QK")

    df_a <- asa_client$players %>% dplyr::filter(.data$player_id %in% IDS)
    df_b <- asa_client$get_players(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Single name --------------------------------------------------------
    NAMES <- "Dax McCarty"

    df_a <- asa_client$players %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name))
    df_b <- asa_client$get_players(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple names -----------------------------------------------------
    NAMES <- c("Dax McCarty", "Tiffany McCarty")

    df_a <- asa_client$players %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$player_name))
    df_b <- asa_client$get_players(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and IDs ----------------------------------------------------
    LEAGUES <- "mls"
    IDS <- c("p6qbedyp50", "9z5kagOjQA")

    df_a <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      .data$player_id %in% IDS) %>%
        dplyr::distinct(.data$player_id)

    df_b <- asa_client$get_players(leagues = LEAGUES, ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and names --------------------------------------------------
    LEAGUES <- "mls"
    NAMES <- "Wright-Phillips"

    df_a <- asa_client$players %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      grepl(paste0(NAMES, collapse = "|"), .data$player_name)) %>%
        dplyr::distinct(.data$player_id)

    df_b <- asa_client$get_players(leagues = LEAGUES, names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

})

test_that("Filtering teams works properly", {

    # No filters ---------------------------------------------------------
    df_a <- asa_client$teams
    df_b <- asa_client$get_teams()

    expect_equal(nrow(df_b), nrow(df_a))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_teams(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    df_a <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES)

    df_b <- asa_client$get_teams(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    df_a <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$team_id)

    df_b <- asa_client$get_teams(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # IDs and names (invalid) --------------------------------------------
    expect_error(asa_client$get_teams(ids = "abc", names = "abc"))

    # Single ID ----------------------------------------------------------
    IDS <- "NWMWlBK5lz"

    df_a <- asa_client$teams %>% dplyr::filter(.data$team_id %in% IDS)
    df_b <- asa_client$get_teams(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple IDs -------------------------------------------------------
    IDS <- c("a2lqRX2Mr0", "9Yqdwg85vJ")

    df_a <- asa_client$teams %>% dplyr::filter(.data$team_id %in% IDS)
    df_b <- asa_client$get_teams(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Single name --------------------------------------------------------
    NAMES <- "Red Bulls"

    df_a <- asa_client$teams %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name))
    df_b <- asa_client$get_teams(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple names -----------------------------------------------------
    NAMES <- c("Chicago", "Seattle")

    df_a <- asa_client$teams %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$team_name))
    df_b <- asa_client$get_teams(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and IDs ----------------------------------------------------
    LEAGUES <- "mls"
    IDS <- c("a2lqRX2Mr0", "9Yqdwg85vJ")

    df_a <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      .data$team_id %in% IDS) %>%
        dplyr::distinct(.data$team_id)

    df_b <- asa_client$get_teams(leagues = LEAGUES, ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and names --------------------------------------------------
    LEAGUES <- "mls"
    NAMES <- "Chicago"

    df_a <- asa_client$teams %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      grepl(paste0(NAMES, collapse = "|"), .data$team_name)) %>%
        dplyr::distinct(.data$team_id)

    df_b <- asa_client$get_teams(leagues = LEAGUES, names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

})

test_that("Filtering stadia works properly", {

    # No filters ---------------------------------------------------------
    df_a <- asa_client$stadia
    df_b <- asa_client$get_stadia()

    expect_equal(nrow(df_b), nrow(df_a))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_stadia(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    df_a <- asa_client$stadia %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES)

    df_b <- asa_client$get_stadia(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    df_a <- asa_client$stadia %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$stadium_id)

    df_b <- asa_client$get_stadia(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # IDs and names (invalid) --------------------------------------------
    expect_error(asa_client$get_stadia(ids = "abc", names = "abc"))

    # Single ID ----------------------------------------------------------
    IDS <- "Vj58BPwQ8n"

    df_a <- asa_client$stadia %>% dplyr::filter(.data$stadium_id %in% IDS)
    df_b <- asa_client$get_stadia(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple IDs -------------------------------------------------------
    IDS <- c("Vj58BPwQ8n", "4JMALEDQKg")

    df_a <- asa_client$stadia %>% dplyr::filter(.data$stadium_id %in% IDS)
    df_b <- asa_client$get_stadia(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Single name --------------------------------------------------------
    NAMES <- "Toyota"

    df_a <- asa_client$stadia %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$stadium_name))
    df_b <- asa_client$get_stadia(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple names -----------------------------------------------------
    NAMES <- c("Buck Shaw", "Yankee")

    df_a <- asa_client$stadia %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$stadium_name))
    df_b <- asa_client$get_stadia(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and IDs ----------------------------------------------------
    LEAGUES <- "mls"
    IDS <- c("Vj58BPwQ8n", "4JMALEDQKg")

    df_a <- asa_client$stadia %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      .data$stadium_id %in% IDS) %>%
        dplyr::distinct(.data$stadium_id)

    df_b <- asa_client$get_stadia(leagues = LEAGUES, ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and names --------------------------------------------------
    LEAGUES <- "mls"
    NAMES <- "Buck Shaw"

    df_a <- asa_client$stadia %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      grepl(paste0(NAMES, collapse = "|"), .data$stadium_name)) %>%
        dplyr::distinct(.data$stadium_id)

    df_b <- asa_client$get_stadia(leagues = LEAGUES, names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

})

test_that("Filtering managers works properly", {

    # No filters ---------------------------------------------------------
    df_a <- asa_client$managers
    df_b <- asa_client$get_managers()

    expect_equal(nrow(df_b), nrow(df_a))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_managers(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    df_a <- asa_client$managers %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES)

    df_b <- asa_client$get_managers(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    df_a <- asa_client$managers %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$manager_id)

    df_b <- asa_client$get_managers(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # IDs and names (invalid) --------------------------------------------
    expect_error(asa_client$get_managers(ids = "abc", names = "abc"))

    # Single ID ----------------------------------------------------------
    IDS <- "LeVq3j5WOJ"

    df_a <- asa_client$managers %>% dplyr::filter(.data$manager_id %in% IDS)
    df_b <- asa_client$get_managers(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple IDs -------------------------------------------------------
    IDS <- c("LeVq3j5WOJ", "0Oq6zkzq6D")

    df_a <- asa_client$managers %>% dplyr::filter(.data$manager_id %in% IDS)
    df_b <- asa_client$get_managers(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Single name --------------------------------------------------------
    NAMES <- "Bruce"

    df_a <- asa_client$managers %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$manager_name))
    df_b <- asa_client$get_managers(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple names -----------------------------------------------------
    NAMES <- c("Bruce", "Bob")

    df_a <- asa_client$managers %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$manager_name))
    df_b <- asa_client$get_managers(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and IDs ----------------------------------------------------
    LEAGUES <- "mls"
    IDS <- c("LeVq3j5WOJ", "0Oq6zkzq6D")

    df_a <- asa_client$managers %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      .data$manager_id %in% IDS) %>%
        dplyr::distinct(.data$manager_id)

    df_b <- asa_client$get_managers(leagues = LEAGUES, ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and names --------------------------------------------------
    LEAGUES <- "mls"
    NAMES <- "Bruce"

    df_a <- asa_client$managers %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      grepl(paste0(NAMES, collapse = "|"), .data$manager_name)) %>%
        dplyr::distinct(.data$manager_id)

    df_b <- asa_client$get_managers(leagues = LEAGUES, names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

})

test_that("Filtering referees works properly", {

    # No filters ---------------------------------------------------------
    df_a <- asa_client$referees
    df_b <- asa_client$get_referees()

    expect_equal(nrow(df_b), nrow(df_a))

    # Invalid league -----------------------------------------------------
    expect_error(asa_client$get_referees(leagues = "abc"))

    # Single league ------------------------------------------------------
    LEAGUES <- "mls"

    df_a <- asa_client$referees %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES)

    df_b <- asa_client$get_referees(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple leagues ---------------------------------------------------
    LEAGUES <- c("mls", "uslc")

    df_a <- asa_client$referees %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES) %>%
        dplyr::distinct(.data$referee_id)

    df_b <- asa_client$get_referees(leagues = LEAGUES)

    expect_equal(nrow(df_b), nrow(df_a))

    # IDs and names (invalid) --------------------------------------------
    expect_error(asa_client$get_referees(ids = "abc", names = "abc"))

    # Single ID ----------------------------------------------------------
    IDS <- "a35r6KG5L6"

    df_a <- asa_client$referees %>% dplyr::filter(.data$referee_id %in% IDS)
    df_b <- asa_client$get_referees(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple IDs -------------------------------------------------------
    IDS <- c("a35r6KG5L6", "0Oq6037M6D")

    df_a <- asa_client$referees %>% dplyr::filter(.data$referee_id %in% IDS)
    df_b <- asa_client$get_referees(ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Single name --------------------------------------------------------
    NAMES <- "Geiger"

    df_a <- asa_client$referees %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$referee_name))
    df_b <- asa_client$get_referees(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Multiple names -----------------------------------------------------
    NAMES <- c("Geiger", "Kelly")

    df_a <- asa_client$referees %>% dplyr::filter(grepl(paste0(NAMES, collapse = "|"), .data$referee_name))
    df_b <- asa_client$get_referees(names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and IDs ----------------------------------------------------
    LEAGUES <- "mls"
    IDS <- c("a35r6KG5L6", "0Oq6037M6D")

    df_a <- asa_client$referees %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      .data$referee_id %in% IDS) %>%
        dplyr::distinct(.data$referee_id)

    df_b <- asa_client$get_referees(leagues = LEAGUES, ids = IDS)

    expect_equal(nrow(df_b), nrow(df_a))

    # Leagues and names --------------------------------------------------
    LEAGUES <- "mls"
    NAMES <- "Geiger"

    df_a <- asa_client$referees %>%
        tidyr::unnest(.data$competitions) %>%
        dplyr::filter(.data$competitions %in% LEAGUES,
                      grepl(paste0(NAMES, collapse = "|"), .data$referee_name)) %>%
        dplyr::distinct(.data$referee_id)

    df_b <- asa_client$get_referees(leagues = LEAGUES, names = NAMES)

    expect_equal(nrow(df_b), nrow(df_a))

})
