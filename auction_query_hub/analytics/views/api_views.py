from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from users.services import (
    count_users,
    count_buyers,
    count_sellers,
    get_user_count_by_role,
)
from auctions.services import (
    count_auctions,
    count_active_auctions,
    count_inactive_auctions,
    get_total_auction_value,
    get_auction_count_per_seller,
    get_sellers_with_more_than_one_auction,
    get_seller_with_most_auctions,
    get_seller_with_highest_auction,
    get_latest_auction_with_seller,
    get_active_auctions,
    get_total_auction_value_per_seller,
    get_sellers_with_total_value_above,
    get_sellers_without_auctions,
    get_auctions_between_prices,
    get_auctions_by_seller_username_prefix,
    get_auctions_with_title_containing,
)


@api_view(["GET"])
def analytics_api(request: Request) -> Response:
    data: dict = {
        "users": {
            "total": count_users(),
            "buyers": count_buyers(),
            "sellers": count_sellers(),
            "by_role": get_user_count_by_role(),
        },
        "auctions": {
            "total": count_auctions(),
            "active": count_active_auctions(),
            "inactive": count_inactive_auctions(),
            "total_value": get_total_auction_value(),
        },
        "seller_analytics": {
            "auction_count_per_seller": get_auction_count_per_seller(),
            "multiple_auction_sellers": get_sellers_with_more_than_one_auction(),
            "top_seller": get_seller_with_most_auctions(),
            "auction_value_per_seller": get_total_auction_value_per_seller(),
            "high_value_sellers": get_sellers_with_total_value_above(Decimal("100000")),
            "inactive_sellers": get_sellers_without_auctions(),
        },
        "auction_analytics": {
            "highest_auction": get_seller_with_highest_auction(),
            "latest_auction": get_latest_auction_with_seller(),
            "active_auctions": get_active_auctions(),
        },
    }

    return Response({
            "status": "success",
            "message": "Analytics retrieved successfully.",
            "data": data,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def users_by_role_api(request: Request) -> Response:
    results = get_user_count_by_role()
    return Response({
            "status": "success",
            "message": "User role statistics retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def auction_count_per_seller_api(request: Request) -> Response:
    results = get_auction_count_per_seller()
    return Response({
            "status": "success",
            "message": "Auction count per seller retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def multiple_auction_sellers_api(request: Request) -> Response:
    results = get_sellers_with_more_than_one_auction()
    return Response({
            "status": "success",
            "message": "Sellers with multiple auctions retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def top_seller_api(request: Request) -> Response:
    results = get_seller_with_most_auctions()
    return Response({
            "status": "success",
            "message": "Top seller retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def auction_value_per_seller_api(request: Request) -> Response:
    results = get_total_auction_value_per_seller()
    return Response({
            "status": "success",
            "message": "Auction value per seller retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def high_value_sellers_api(request: Request) -> Response:
    minimum_value = Decimal("100000")
    results = get_sellers_with_total_value_above(minimum_value)
    return Response({
            "status": "success",
            "message": "High-value sellers retrieved successfully.",
            "minimum_value": minimum_value,
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def inactive_sellers_api(request: Request) -> Response:
    results = get_sellers_without_auctions()
    return Response({
            "status": "success",
            "message": "Inactive sellers retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def highest_auction_api(request: Request) -> Response:
    results = get_seller_with_highest_auction()
    return Response({
            "status": "success",
            "message": "Highest auction retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def latest_auction_api(request: Request) -> Response:
    results = get_latest_auction_with_seller()
    return Response({
            "status": "success",
            "message": "Latest auction retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def active_auctions_api(request: Request) -> Response:
    results = get_active_auctions()

    return Response({
            "status": "success",
            "message": "Active auctions retrieved successfully.",
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def price_range_api(request: Request) -> Response:
    minimum_price = request.query_params.get("minimum_price")
    maximum_price = request.query_params.get("maximum_price")
    if minimum_price is None or maximum_price is None:
        return Response({
                "status": "error",
                "message": "Both minimum_price and maximum_price query parameters are required."
            }, status=status.HTTP_400_BAD_REQUEST)

    try:
        minimum_price = Decimal(minimum_price)
        maximum_price = Decimal(maximum_price)
    except Exception:
        return Response({
                "status": "error",
                "message": "Prices must be valid numeric values.",
            }, status=status.HTTP_400_BAD_REQUEST)

    if minimum_price < 0 or maximum_price < 0:
        return Response({
                "status": "error",
                "message": "Prices cannot be negative.",
            }, status=status.HTTP_400_BAD_REQUEST)

    if minimum_price > maximum_price:
        return Response({
                "status": "error",
                "message": "minimum_price cannot be greater than maximum_price."
            }, status=status.HTTP_400_BAD_REQUEST)

    results: list[dict] = get_auctions_between_prices(minimum_price, maximum_price)

    return Response({
            "status": "success",
            "message": "Auctions retrieved successfully.",
            "filters": {
                "minimum_price": minimum_price,
                "maximum_price": maximum_price,
            },
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def seller_search_api(request: Request) -> Response:
    prefix = request.query_params.get("prefix")
    if not prefix:
        return Response({
                "status": "error",
                "message": "The prefix query parameter is required.",
            }, status=status.HTTP_400_BAD_REQUEST)

    results = get_auctions_by_seller_username_prefix(prefix)
    return Response({
            "status": "success",
            "message": "Seller search completed successfully.",
            "prefix": prefix,
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)


@api_view(["GET"])
def auction_title_search_api(request: Request) -> Response:
    keyword = request.query_params.get("keyword")
    if not keyword:
        return Response({
                "status": "error",
                "message": "The keyword query parameter is required.",
            }, status=status.HTTP_400_BAD_REQUEST)

    results = get_auctions_with_title_containing(keyword)
    return Response({
            "status": "success",
            "message": "Auction title search completed successfully.",
            "keyword": keyword,
            "count": len(results),
            "data": results,
        }, status=status.HTTP_200_OK)