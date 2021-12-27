#' @importFrom rlang .data
get_stats <- function(self, type, entity, leagues, ...) {
    query <- list(...)
    if (!all(rlang::have_name(query))) {
        bad <- which(!rlang::have_name(query)) + 1
        msg <- glue::glue("{.format_args(bad)} must be named.")
        stop(msg)
    }

    if (type == "salaries") {
        .check_leagues_salaries(self, leagues)
        if (missing(leagues)) leagues <- "mls"
        if (entity == "teams" &
            is.null(query[["split_by_teams"]]) &
            is.null(query[["split_by_seasons"]]) &
            is.null(query[["split_by_positions"]])) query[["split_by_teams"]] <- TRUE
    } else {
        .check_leagues(self, leagues)
        if (missing(leagues)) leagues <- self$LEAGUES
    }

    if (sum(grepl("player_", names(query))) > 0) {
        .check_ids_names(query[["player_ids"]], query[["player_names"]])

        if (!is.null(query[["player_names"]])) {
            query[["player_id"]] <- .convert_names_to_ids(self$players, query[["player_names"]])
        } else {
            query[["player_id"]] <- query[["player_ids"]]
        }

        query[["player_ids"]] <- NULL
        query[["player_names"]] <- NULL
    }

    if (sum(grepl("team_", names(query))) > 0) {
        .check_ids_names(query[["team_ids"]], query[["team_names"]])

        if (!is.null(query[["team_names"]])) {
            query[["team_id"]] <- .convert_names_to_ids(self$teams, query[["team_names"]])
        } else {
            query[["team_id"]] <- query[["team_ids"]]
        }

        query[["team_ids"]] <- NULL
        query[["team_names"]] <- NULL
    }

    if (!is.null(query[["game_ids"]])) {
        query[["game_id"]] <- query[["game_ids"]]
        query[["game_ids"]] <- NULL
    }


    stats <- list()
    i <- 1

    for (league in unique(leagues)) {
        url <- glue::glue("{self$base_url}/{league}/{entity}/{type}")

        response <- .execute_query(self, url, query) %>%
            as.data.frame() %>%
            dplyr::mutate(competition = league)

        stats[[i]] <- response
        i <- i + 1
    }

    stats <- data.table::rbindlist(stats, fill = TRUE)
    return(stats)
}
