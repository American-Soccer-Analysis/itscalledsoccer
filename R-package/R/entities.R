#' @importFrom rlang .data
get_entity <- function(self, type) {
    entity_all <- list()
    i <- 1

    for (league in self$LEAGUES) {
        if (type == "stadium") {
            url <- glue::glue("{self$base_url}/{league}/stadia")
        } else {
            url <- glue::glue("{self$base_url}/{league}/{type}s")
        }

        response <- .execute_query(self, url)
        response <- response %>% dplyr::mutate(competition = league)

        entity_all[[i]] <- response
        i <- i + 1
    }

    entity_all <- data.table::rbindlist(entity_all, fill = TRUE) %>%
        dplyr::group_by(dplyr::across(c(-dplyr::matches("competition"), -dplyr::starts_with("season"), -dplyr::ends_with("position")))) %>%
        dplyr::summarize(competitions = list(.data$competition)) %>%
        dplyr::ungroup() %>%
        dplyr::arrange(!!as.symbol(glue::glue("{type}_name")))

    return(entity_all)
}

#' @importFrom rlang .data
filter_entity <- function(self, entity, leagues, ids, names) {
    .check_leagues(self, leagues)
    .check_ids_names(ids, names)

    entity_filtered <- self[[entity]] %>%
        tidyr::unnest(.data$competitions)

    if (!missing(leagues)) {
        entity_filtered <- entity_filtered %>%
            dplyr::filter(.data$competitions %in% leagues)
    }

    if (!missing(names)) {
        ids <- .convert_names_to_ids(entity_filtered, names)
    }

    if (!missing(names) | !missing(ids)) {
        entity_filtered <- entity_filtered %>%
            dplyr::filter(dplyr::if_any(dplyr::ends_with("_id"), ~ . %in% ids))
    }

    entity_filtered <- entity_filtered %>%
        dplyr::select(-.data$competitions) %>%
        dplyr::distinct()

    return(entity_filtered)
}

#' @importFrom rlang .data
get_games <- function(self, leagues, game_ids, team_ids, team_names, seasons, stages) {
    .check_leagues(self, leagues)
    .check_ids_names(team_ids, team_names)

    if (missing(leagues)) leagues <- self$LEAGUES

    query <- list()
    if (!missing(game_ids)) query$game_id <- game_ids
    if (!missing(team_ids)) query$team_id <- team_ids
    if (!missing(team_names)) query$team_id <- .convert_names_to_ids(self$teams, team_names)
    if (!missing(seasons)) query$season_name <- seasons
    if (!missing(stages)) query$stage_name <- stages

    games <- list()
    i <- 1

    for (league in leagues) {
        url <- glue::glue("{self$base_url}/{league}/games")

        response <- .execute_query(self, url, query)

        games[[i]] <- response
        i <- i + 1
    }

    games <- data.table::rbindlist(games, fill = TRUE) %>% dplyr::arrange(.data$date_time_utc)
    return(games)
}
