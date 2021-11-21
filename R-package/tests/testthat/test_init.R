test_that("AmericanSoccerAnalysis class initializes successfully", {

    # API version in base url --------------------------------------------
    base_url_api_version <- gsub("^.*/", "", asa_client$base_url) %>% as.character()
    expect_equal(base_url_api_version, asa_client$API_VERSION)

    # Entity tables exist ------------------------------------------------
    for (type in ENTITY_TYPES) {
        expect_s3_class(asa_client[[type]], "data.frame")
    }

    # Entity tables populated with data from all leagues -----------------
    .exp <- length(asa_client$LEAGUES)

    for (type in ENTITY_TYPES) {
        .obj <- asa_client[[type]] %>%
            tidyr::unnest(.data$competitions) %>%
            dplyr::distinct(competitions) %>%
            nrow()

        expect_equal(.obj, .exp)
    }

})
