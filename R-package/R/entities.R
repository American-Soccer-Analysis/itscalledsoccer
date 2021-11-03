get_entity <- function(self, type) {
    entity_all <- data.frame()

    for (league in self$LEAGUES) {
        if (type == "stadium") {
            url <- glue::glue("{self$BASE_URL}/{league}/stadia")
        } else {
            url <- glue::glue("{self$BASE_URL}/{league}/{type}s")
        }

        response <- .execute_query(self, url)
        response <- response %>% dplyr::mutate(competition = league)

        entity_all <- entity_all %>% dplyr::bind_rows(response)
    }

    entity_all <- entity_all %>%
        dplyr::group_by(dplyr::across(c(-dplyr::matches("competition"), -dplyr::starts_with("season"), -dplyr::ends_with("position")))) %>%
        dplyr::summarize(competitions = list(competition)) %>%
        dplyr::ungroup() %>%
        dplyr::arrange(!!as.symbol(glue::glue("{type}_name")))

    return(entity_all)
}

filter_entity <- function(entity_all, league_options, leagues, ids, names) {
    .check_leagues(leagues, league_options)
    .check_ids_names(ids, names)

    entity_filtered <- entity_all %>%
        tidyr::unnest(competitions)

    if (!missing(leagues)) {
        entity_filtered <- entity_filtered %>%
            dplyr::filter(competitions %in% leagues)
    }

    if (!missing(names)) {
        ids <- .convert_names_to_ids(entity_filtered, names)
    }

    if (!missing(names) | !missing(ids)) {
        entity_filtered <- entity_filtered %>%
            dplyr::filter(dplyr::if_any(dplyr::ends_with("_id"), ~ . %in% ids))
    }

    entity_filtered <- entity_filtered %>%
        dplyr::select(-competitions) %>%
        dplyr::distinct()

    return(entity_filtered)
}

get_games <- function(self, leagues, game_ids, team_ids, team_names, seasons, stages) {
    .check_leagues(leagues, self$LEAGUES)
    .check_ids_names(team_ids, team_names)

    if (missing(leagues)) leagues <- self$LEAGUES

    query <- list()
    if (!missing(game_ids)) query$game_id <- game_ids
    if (!missing(team_ids)) query$team_id <- team_ids
    if (!missing(team_names)) query$team_id <- .convert_names_to_ids(self$teams, team_names)
    if (!missing(seasons)) query$season_name <- seasons
    if (!missing(stages)) query$stage_name <- stages

    games <- data.frame()

    for (league in leagues) {
        url <- glue::glue("{self$BASE_URL}/{league}/games")

        response <- .execute_query(self, url, query)

        games <- games %>%
            dplyr::bind_rows(response) %>%
            dplyr::arrange(date_time_utc)
    }

    return(games)
}
