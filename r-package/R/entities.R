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

        entity_all <- entity_all %>%
            dplyr::bind_rows(response)
    }

    entity_all <- entity_all %>%
        dplyr::group_by(dplyr::across(c(-dplyr::matches("competition"), -dplyr::starts_with("season"), -dplyr::ends_with("position")))) %>%
        dplyr::summarize(competitions = list(competition)) %>%
        dplyr::ungroup() %>%
        dplyr::arrange(!!as.symbol(glue::glue("{type}_name")))

    return(entity_all)
}

filter_entity <- function(entity_all, leagues, ids, names) {
    entity_filtered <- entity_all %>%
        tidyr::unnest(competitions)

    if (!missing(leagues)) {
        entity_filtered <- entity_filtered %>%
            dplyr::filter(competitions %in% leagues)
    }

    if (!missing(ids)) {
        entity_filtered <- entity_filtered %>%
            dplyr::filter(dplyr::if_any(dplyr::ends_with("_id"), ~ . %in% ids))
    }

    if (!missing(names)) {
        entity_filtered <- entity_filtered %>%
            dplyr::filter(dplyr::if_any(dplyr::ends_with("_name"), ~ . %in% names))
    }

    entity_filtered <- entity_filtered %>%
        dplyr::select(-competitions) %>%
        dplyr::distinct()

    return(entity_filtered)
}
