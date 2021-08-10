get_entity <- function(type, self) {
    entity_all <- data.frame()

    for (league in self$LEAGUES) {
        if (type == "stadium") {
            url <- glue::glue("{self$BASE_URL}{league}/stadia")
        } else {
            url <- glue::glue("{self$BASE_URL}{league}/{type}s")
        }

        r <- httpcache::GET(url)
        httr::stop_for_status(r)
        response <- r %>%
            httr::content(as = "text", encoding = "UTF-8") %>%
            jsonlite::fromJSON() %>%
            dplyr::mutate(competition = league)

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
    if (!missing(game_ids)) query$game_id <- .collapse_query_string(game_ids)
    if (!missing(team_ids)) query$team_id <- .collapse_query_string(team_ids)
    if (!missing(team_names)) query$team_id <- .collapse_query_string(.convert_names_to_ids(self$teams, team_names))
    if (!missing(seasons)) query$season_name <- .collapse_query_string(seasons)
    if (!missing(stages)) query$stage_name <- .collapse_query_string(stages)

    games <- data.frame()

    for (league in leagues) {
        url <- glue::glue("{self$BASE_URL}{league}/games")

        r <- httpcache::GET(url, query = query)
        httr::stop_for_status(r)
        response <- r %>%
            httr::content(as = "text", encoding = "UTF-8") %>%
            jsonlite::fromJSON()

        games <- games %>%
            dplyr::bind_rows(response) %>%
            dplyr::arrange(date_time_utc)
    }

    return(games)
}

.collapse_query_string <- function(value) {
    value <- paste0(value, collapse = ",")
    return(value)
}

.check_leagues <- function(leagues, league_options) {
    if (!missing(leagues)) {
        if (any(!leagues %in% league_options)) {
            stop(glue::glue("Leagues are limited only to the following options: {paste0(league_options, collapse = ', ')}."))
        }
    }
}

.check_ids_names <- function(ids, names) {
    if (!missing(ids) & !missing(names)) {
        stop("Please specify only IDs or names, not both.")
    }

    if (!missing(ids)) {
        if (class(ids) != "character" | length(ids) < 1) {
            stop("IDs must be passed as a vector of characters with length >= 1.")
        }
    }

    if (!missing(names)) {
        if (class(names) != "character" | length(names) < 1) {
            stop("Names must be passed as a vector of characters with length >= 1.")
        }
    }
}

.convert_names_to_ids <- function(df, names) {
    names_clean <- .clean_names(names)
    names_string <- paste0(names_clean, collapse = "|")

    ids <- df %>%
        dplyr::mutate(dplyr::across(dplyr::matches("(_name|_abbreviation)$"), .fns = list(clean = ~.clean_names(.)))) %>%
        dplyr::filter(dplyr::if_any(dplyr::ends_with("_clean"), ~grepl(names_string, .))) %>%
        dplyr::select(!dplyr::ends_with("_clean")) %>%
        dplyr::pull(names(.)[which(grepl("_id$", names(.)))])

    return(ids)
}

.clean_names <- function(names) {
    names <- stringi::stri_trans_general(str = names, id = "Latin-ASCII")
    names <- tolower(names)
    return(names)
}
