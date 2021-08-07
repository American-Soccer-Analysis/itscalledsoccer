get_all_ids <- function(type, self) {
    all_ids <- data.frame()

    for (league in self$LEAGUES) {
        if (type == "stadia") {
            url <- glue::glue("{self$BASE_URL}{league}/{type}")
            type <- "stadium"
        } else {
            url <- glue::glue("{self$BASE_URL}{league}/{type}s")
        }

        r <- httpcache::GET(url)
        httr::stop_for_status(r)
        response <- r %>%
            httr::content(as = "text", encoding = "UTF-8") %>%
            jsonlite::fromJSON() %>%
            dplyr::select(c(glue::glue("{type}_name"), glue::glue("{type}_id")))

        all_ids <- all_ids %>%
            dplyr::bind_rows(response) %>%
            dplyr::distinct() %>%
            dplyr::arrange(!!as.symbol(glue::glue("{type}_name")))

        if (type == "stadium") {
            type <- "stadia"
        }
    }

    return(all_ids)
}
