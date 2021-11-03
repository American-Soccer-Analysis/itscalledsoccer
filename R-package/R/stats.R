get_stats <- function(self, type, entity, leagues, ...) {
    .check_leagues(leagues, self$LEAGUES)
    if (missing(leagues)) leagues <- self$LEAGUES

    query <- list(...)

    if (sum(grepl("player_", names(query))) > 0) {
        .check_ids_names(query[["player_ids"]], query[["player_names"]])

        if (!is.null(query[["player_names"]])) {
            player_ids_to_filter <- .convert_names_to_ids(self$players, query[["player_names"]])
        } else {
            player_ids_to_filter <- query[["player_ids"]]
        }

        query[["player_ids"]] <- NULL
        query[["player_names"]] <- NULL
    }

    if (sum(grepl("team_", names(query))) > 0) {
        .check_ids_names(query[["team_ids"]], query[["team_names"]])

        if (!is.null(query[["team_names"]])) {
            team_ids_to_filter <- .convert_names_to_ids(self$teams, query[["team_names"]])
        } else {
            team_ids_to_filter <- query[["team_ids"]]
        }

        if (entity %in% c("players", "goalkeepers")) query[["team_id"]] <- team_ids_to_filter
        query[["team_ids"]] <- NULL
        query[["team_names"]] <- NULL
    }

    if (!is.null(query[["game_ids"]])) {
        game_ids_to_filter <- query[["game_ids"]]
        query[["game_ids"]] <- NULL
    }


    stats <- data.frame()

    for (league in leagues) {
        url <- glue::glue("{self$BASE_URL}/{league}/{entity}/{type}")

        response <- .execute_query(self, url, query)

        stats <- stats %>%
            dplyr::bind_rows(response)
    }


    if (entity %in% c("players", "goalkeepers") & (exists("player_ids_to_filter") && !is.null(player_ids_to_filter))) {
        stats <- stats %>% dplyr::filter(player_id %in% player_ids_to_filter)
    } else if (entity == "teams" & (exists("team_ids_to_filter") && !is.null(team_ids_to_filter))) {
        stats <- stats %>% dplyr::filter(team_id %in% team_ids_to_filter)
    } else if (entity == "games" & (exists("game_ids_to_filter") && !is.null(game_ids_to_filter))) {
        stats <- stats %>% dplyr::filter(game_id %in% game_ids_to_filter)
    }

    return(stats)
}
