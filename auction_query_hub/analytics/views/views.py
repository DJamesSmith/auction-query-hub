from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from auctions.services import get_all_auctions
from django.template.loader import render_to_string
from users.services import (
    count_users,
    count_buyers,

    # Analytics
    get_user_count_by_role,
)

from auctions.services import (
    get_all_auctions,
    get_auction_count_per_seller,
    get_sellers_with_more_than_one_auction,
    get_total_auction_value_per_seller,
    get_seller_with_highest_auction,
    get_latest_auction_with_seller,
    get_active_auctions,
    get_auctions_between_prices,
    get_auctions_by_seller_username_prefix,
    get_auctions_with_title_containing,
    get_sellers_without_auctions,
    get_seller_with_most_auctions,
    get_sellers_with_total_value_above,
)

def analytics(request: HttpRequest) -> HttpResponse:
    # USER ANALYTICS
    total_users = count_users()
    total_buyers = count_buyers()
    role_statistics = get_user_count_by_role()
    total_sellers = sum(row["total_users"] for row in role_statistics if row["role"] == "Seller")

    # AUCTION ANALYTICS
    all_auctions = get_all_auctions()
    total_auctions = len(all_auctions)
    active_auctions = get_active_auctions()
    active_auctions_count = len(active_auctions)
    inactive_auctions_count = total_auctions - active_auctions_count

    # SELLER ANALYTICS
    auction_count_per_seller = get_auction_count_per_seller()
    multiple_auction_sellers = get_sellers_with_more_than_one_auction()
    auction_value_per_seller = get_total_auction_value_per_seller()
    high_value_sellers = get_sellers_with_total_value_above(10000)

    # TOP SELLER / HIGHEST / LATEST
    top_seller_result = get_seller_with_most_auctions()
    top_seller: dict = top_seller_result[0] if top_seller_result else None
    highest_auction_result = get_seller_with_highest_auction()
    highest_auction = highest_auction_result[0] if highest_auction_result else None
    latest_auction_result = get_latest_auction_with_seller()
    latest_auction = latest_auction_result[0] if latest_auction_result else None

    # INACTIVE SELLERS
    inactive_sellers = get_sellers_without_auctions()
    inactive_sellers_count = len(inactive_sellers)

    # TOTAL AUCTION VALUE
    total_auction_value = sum(seller["total_auction_value"] or 0 for seller in auction_value_per_seller)

    # TEMPLATE CONTEXT
    context = {
        # User statistics
        "total_users": total_users,
        "total_buyers": total_buyers,
        "total_sellers": total_sellers,
        "role_statistics": role_statistics,

        # Auction statistics
        "total_auctions": total_auctions,
        "active_auctions_count": active_auctions_count,
        "inactive_auctions_count": inactive_auctions_count,
        "total_auction_value": total_auction_value,

        # Seller analytics
        "auction_count_per_seller": auction_count_per_seller,
        "multiple_auction_sellers": multiple_auction_sellers,
        "auction_value_per_seller": auction_value_per_seller,
        "high_value_sellers": high_value_sellers,

        # Top seller / auctions
        "top_seller": top_seller,
        "highest_auction": highest_auction,
        "latest_auction": latest_auction,

        # Active auctions
        "active_auctions": active_auctions,

        # Inactive sellers
        "inactive_sellers": inactive_sellers,
        "inactive_sellers_count": inactive_sellers_count,
    }

    return render(request, "analytics.html", context)


def price_range_search(request: HttpRequest) -> JsonResponse:
    minimum_price = request.GET.get("minimum_price", "").strip()
    maximum_price = request.GET.get("maximum_price", "").strip()

    if not minimum_price or not maximum_price:
        return JsonResponse({
            "status": "error",
            "message": "Both minimum price and maximum price are required."
        }, status=400)

    try:
        minimum_price_value = float(minimum_price)
        maximum_price_value = float(maximum_price)
    except ValueError:
        return JsonResponse({
            "status": "error",
            "message": "Prices must be valid numbers."
        }, status=400)

    if minimum_price_value < 0 or maximum_price_value < 0:
        return JsonResponse({
            "status": "error",
            "message": "Prices cannot be negative."
        }, status=400)

    if minimum_price_value > maximum_price_value:
        return JsonResponse({
            "status": "error",
            "message": "Minimum price cannot be greater than maximum price."
        }, status=400)

    results = get_auctions_between_prices(minimum_price_value, maximum_price_value)
    context: dict = {
        "results": results,
        "search_type": "price",
        "empty_message": "No auctions found within the specified price range.",
    }
    html = render_to_string("search_results.html", context, request=request)

    return JsonResponse({
        "status": "success",
        "message": "Price range search completed successfully." if results else "No auctions found within the specified price range.",
        "count": len(results),
        "html": html,
    })


def seller_search(request: HttpRequest) -> JsonResponse:
    seller_prefix = request.GET.get("seller_prefix", "").strip()

    if not seller_prefix:
        return JsonResponse({
            "status": "error",
            "message": "Please enter a seller username prefix."
        }, status=400)

    results: list[dict] = get_auctions_by_seller_username_prefix(seller_prefix)
    context: dict = {
        "results": results,
        "search_type": "seller",
        "empty_message": "No auctions found for this seller prefix.",
    }
    html = render_to_string("search_results.html", context, request=request)

    return JsonResponse({
        "status": "success",
        "message": "Seller search completed successfully." if results else "No auctions found for this seller prefix.",
        "count": len(results),
        "html": html
    })


def auction_title_search(request: HttpRequest) -> JsonResponse:
    keyword = request.GET.get("auction_keyword", "").strip()

    if not keyword:
        return JsonResponse({
            "status": "error",
            "message": "Please enter an auction title keyword."
        }, status=400)

    results = get_auctions_with_title_containing(keyword)
    context: dict = {
        "results": results,
        "search_type": "title",
        "empty_message": "No auctions found matching the specified title.",
    }
    html = render_to_string("search_results.html", context, request=request)

    return JsonResponse({
        "status": "success",
        "message": "Auction title search completed successfully." if results else "No auctions found matching the specified title.",
        "count": len(results),
        "html": html
    })