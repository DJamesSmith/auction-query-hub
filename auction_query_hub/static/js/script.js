$(document).ready(function () {
    $("#user-form").on("submit", function (event) {
        event.preventDefault()
        $("#message")
            .addClass("d-none")
            .removeClass("alert-success alert-danger")
            .text("")
        $(".text-danger").text("")
        $("#submit-button").prop("disabled", true)

        $.ajax({
            url: $("#user-form").data("url"),
            type: "POST",
            data: $(this).serialize(),
            success: function (response) {
                $("#message")
                    .removeClass("d-none")
                    .addClass("alert-success")
                    .text(response.message)
                $("#user-form")[0].reset()
            },
            error: function (xhr) {
                if (xhr.responseJSON) {
                    const response = xhr.responseJSON
                    if (response.errors) {
                        $.each(response.errors, function (field, errors) {
                            let errorMessage = errors[0].message
                            $("#" + field + "-error")
                                .text(errorMessage)
                        })
                    } else {
                        $("#message")
                            .removeClass("d-none")
                            .addClass("alert-danger")
                            .text(response.message)
                    }
                }
            },
            complete: function () {
                $("#submit-button").prop("disabled", false)
            }
        })
    })

    $("#auction-form").on("submit", function (event) {
        event.preventDefault()
        const form = $(this)

        $("#message")
            .addClass("d-none")
            .removeClass("alert-success alert-danger")
            .text("")

        $(".text-danger").text("")
        $("#auction-submit-button").prop("disabled", true)

        $.ajax({
            url: form.data("url"),
            type: "POST",
            data: form.serialize(),
            success: function (response) {
                $("#message")
                    .removeClass("d-none")
                    .addClass("alert-success")
                    .text(response.message)

                form[0].reset()
            },
            error: function (xhr) {
                if (xhr.responseJSON) {
                    const response = xhr.responseJSON

                    if (response.errors) {
                        $.each(
                            response.errors,
                            function (field, errors) {
                                const errorMessage = errors[0].message
                                $("#" + field + "-error")
                                    .text(errorMessage)
                            })
                    } else {
                        $("#message")
                            .removeClass("d-none")
                            .addClass("alert-danger")
                            .text(response.message)
                    }
                }
            },
            complete: function () {
                $("#auction-submit-button")
                    .prop("disabled", false)
            }
        })
    })


    $(".time-input").on("input", function () {
        let value = $(this).val()
        value = value.replace(/\D/g, "")               // Keep digits only
        value = value.substring(0, 4)                  // Maximum 4 digits

        if (value.length === 3) {
            value = "0" + value
        }

        if (value.length === 4) {
            const hours = parseInt(value.substring(0, 2), 10)
            const minutes = parseInt(value.substring(2, 4), 10)

            if (hours > 23) {
                value = "23" + value.substring(2, 4)
            }

            if (minutes > 59) {
                value = value.substring(0, 2) + "59"
            }

            value = value.substring(0, 2) + ":" + value.substring(2, 4)
        }

        $(this).val(value)
    })

    // ------------------------- Role Select: enable Update only on change -------------------------
    $(".role-select").each(function () {
        // Remember the role this select started with
        $(this).data("initial-role", $(this).val())
    })

    $(document).on("change", ".role-select", function () {
        const initialRole = $(this).data("initial-role")
        const currentRole = $(this).val()
        const updateButton = $(this).closest("form").find(".update-btn")
        updateButton.prop("disabled", currentRole === initialRole)
    })


    // ----------------------------- Price Range -----------------------------
    // Input validation
    $("#price-range-form").on("input", function () {
        const minimumPrice = parseFloat($(this).find("[name='minimum_price']").val())
        const maximumPrice = parseFloat($(this).find("[name='maximum_price']").val())
        const button = $("#price-range-button")
        clearMessage("#price-range-message")

        if (!Number.isNaN(minimumPrice) && !Number.isNaN(maximumPrice) &&
            minimumPrice >= 0 && maximumPrice >= 0 && minimumPrice <= maximumPrice
        ) {
            button.prop("disabled", false)
        } else {
            button.prop("disabled", true)
        }
    })

    // onSubmit Validation
    $("#price-range-form").on("submit", function (event) {
        event.preventDefault()
        const form = $(this)
        const minimumPrice = parseFloat(form.find("[name='minimum_price']").val())
        const maximumPrice = parseFloat(form.find("[name='maximum_price']").val())

        if (minimumPrice > maximumPrice) {
            showMessage("#price-range-message","Minimum price cannot be greater than maximum price.")
            return
        }
        clearMessage("#price-range-message")
        $("#price-range-button").prop("disabled", true)

        $.ajax({
            url: form.data("url"),
            type: "GET",
            data: form.serialize(),
            success: function (response) {
                showMessage("#price-range-message", response.message, response.count === 0 ? "warning" : "success")
                $("#search-results .card-body").html(response.html)
            },
            error: function (xhr) {
                const response = xhr.responseJSON
                if (response && response.message) {
                    showMessage("#price-range-message", response.message, "danger")
                }
            },
            complete: function () {
                $("#price-range-button").prop("disabled", false)
            }
        })
    })


    // ---------------------------- Seller Search ----------------------------
    // Input validation
    $("#seller-search-form").on("input", function () {
        const prefix = $(this)
            .find("[name='seller_prefix']")
            .val()
            .trim()

        $("#seller-search-button").prop("disabled", prefix.length < 3)
        clearMessage("#seller-search-message")
    })

    // onSubmit Validation
    $("#seller-search-form").on("submit", function (event) {
        event.preventDefault()
        const form = $(this)
        const prefix = form
            .find("[name='seller_prefix']")
            .val()
            .trim()

        if (prefix.length < 3) {
            showMessage("#seller-search-message", "Seller username prefix must contain at least 3 characters.")
            return
        }
        clearMessage("#seller-search-message")
        $("#seller-search-button").prop("disabled", true)

        $.ajax({
            url: form.data("url"),
            type: "GET",
            data: form.serialize(),
            success: function (response) {
                showMessage("#seller-search-message", response.message, response.count === 0 ? "warning" : "success")
                $("#search-results .card-body").html(response.html)
            },
            error: function (xhr) {
                const response = xhr.responseJSON
                showMessage(
                    "#seller-search-message",
                    response?.message || "Seller search failed."
                )
            },
            complete: function () {
                $("#seller-search-button").prop("disabled", false)
            }
        })
    })

    // ------------------------- Auction Title Search -------------------------

    // Input validation
    $("#auction-title-search-form").on("input", function () {
        const keyword = $(this)
            .find("[name='auction_keyword']")
            .val()
            .trim()

        $("#auction-title-search-button").prop("disabled", keyword.length < 3)
        clearMessage("#auction-title-message")
    })

    // onSubmit Validation
    $("#auction-title-search-form").on("submit", function (event) {
        event.preventDefault()
        const form = $(this)
        const keyword = form
            .find("[name='auction_keyword']")
            .val()
            .trim()

        if (keyword.length < 3) {
            showMessage("#auction-title-message", "Auction title keyword must contain at least 3 characters.")
            return
        }

        clearMessage("#auction-title-message")
        $("#auction-title-search-button").prop("disabled", true)

        $.ajax({
            url: form.data("url"),
            type: "GET",
            data: form.serialize(),
            success: function (response) {
                showMessage("#auction-title-message", response.message, response.count === 0 ? "warning" : "success")
                $("#search-results .card-body").html(response.html)
            },
            error: function (xhr) {
                const response = xhr.responseJSON
                showMessage("#auction-title-message", response?.message || "Auction title search failed.")
            },
            complete: function () {
                $("#auction-title-search-button").prop("disabled", false)
            }
        })
    })
})

function showMessage(selector, message, type = "danger") {
    const messageBox = $(selector)
    messageBox
        .removeClass("d-none alert-success alert-danger alert-warning")
        .addClass(`alert-${type}`)
        .text(message)
}

function clearMessage(selector) {
    $(selector)
        .addClass("d-none")
        .removeClass("alert-success alert-danger alert-warning")
        .text("")
}