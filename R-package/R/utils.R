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
    if ((!missing(ids) & !missing(names)) && (!is.null(ids) & !is.null(names))) {
        stop("Please specify only IDs or names, not both.")
    }

    if (!missing(ids)) {
        if (!is.null(ids) & (class(ids) != "character" | length(ids) < 1)) {
            stop("IDs must be passed as a vector of characters with length >= 1.")
        }
    }

    if (!missing(names)) {
        if (!is.null(names) & (class(names) != "character" | length(names) < 1)) {
            stop("Names must be passed as a vector of characters with length >= 1.")
        }
    }
}

.convert_names_to_ids <- function(df, names) {
    . <- NULL
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

.single_request <- function(url, query) {
    for (arg_name in names(query)) {
        if (length(query[[arg_name]]) > 1) {
            query[[arg_name]] <- .collapse_query_string(query[[arg_name]])
        }
    }

    r <- httpcache::GET(url = url, query = query)
    httr::stop_for_status(r)
    response <- r %>%
        httr::content(as = "text", encoding = "UTF-8") %>%
        jsonlite::fromJSON()

    return(response)
}

.execute_query <- function(self, url, query = list()) {
    tmp_response <- .single_request(url, query)
    response <- tmp_response

    if (is.data.frame(tmp_response)) {
        offset <- self$MAX_API_LIMIT

        while (nrow(tmp_response) == self$MAX_API_LIMIT) {
            query$offset <- offset
            tmp_response <- .single_request(url, query)

            response <- response %>% dplyr::bind_rows(tmp_response)
            offset <- offset + self$MAX_API_LIMIT
        }
    }

    return(response)
}

.format_comma <- function(..., .max = 6) {
    x <- paste0(...)
    if (length(x) > .max) {
        length(x) <- .max
        x[[.max]] <- "..."
    }

    paste0(x, collapse = ", ")
}

.format_args <- function(x) {
    args <- if (length(x) == 1) "Argument" else "Arguments"
    glue::glue("{args} {.format_comma(x)}")
}
