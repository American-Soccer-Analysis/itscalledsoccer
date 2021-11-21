test_that("httr configs can successfully be added to and removed from AmericanSoccerAnalysis class", {

    # No configs by default ----------------------------------------------
    expect_null(asa_client$httr_configs)

    # Add httr configs ---------------------------------------------------
    SSL_VERIFYPEER <- 0L
    PROXY <- "64.251.21.73"
    PROXYPORT <- 8080

    asa_client$add_httr_configs(
        httr::config(ssl_verifypeer = SSL_VERIFYPEER),
        httr::use_proxy(PROXY, PROXYPORT)
    )

    expect_equal(asa_client$httr_configs[[1]][["options"]][["ssl_verifypeer"]], SSL_VERIFYPEER)
    expect_equal(asa_client$httr_configs[[2]][["options"]][["proxy"]], PROXY)
    expect_equal(asa_client$httr_configs[[2]][["options"]][["proxyport"]], PROXYPORT)

    # Reset httr configs -------------------------------------------------
    asa_client$reset_httr_configs()
    expect_null(asa_client$httr_configs)

})
