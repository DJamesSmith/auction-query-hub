from decimal import Decimal
from django.db.models import Count, F, Sum
from django.db.models.functions import Cast, Coalesce, Now
from django.db.models import TimeField
from users.models import User
from .models import AuctionItem


# 21 FOREIGN KEY SQL QUERIES

# Get all auctions: get_all_auctions_query
def get_all_auctions() -> list[dict]:
    return list(AuctionItem.objects.values())


# QUERY 01 — INNER JOIN: select_username_and_title
def get_username_and_auction_title() -> list[dict]:
    return list(
        AuctionItem.objects
        .values(username=F("seller__username"), title=F("title")))


# QUERY 02 — INNER JOIN: select_seller_name_and_auction_title
def get_seller_name_and_auction_title() -> list[dict]:
    return list(
        AuctionItem.objects
        .values(username=F("seller__username"), title=F("title")))


# QUERY 03 — JOIN + SELECT ALL: select_all_auction_details_with_seller
def get_all_auction_details_with_seller() -> list[dict]:
    return list(
        AuctionItem.objects
        .annotate(username=F("seller__username"))
        .values("id", "title", "description", "base_price", "current_price", "start_time", "end_time", "seller_id", "username"))


# QUERY 04 — JOIN + WHERE: select_auctions_by_rahul
def get_auctions_by_username(username: str) -> list[dict]:
    return list(
        AuctionItem.objects
        .filter(seller__username=username)
        .values())


# QUERY 05 — JOIN + WHERE ROLE: select_auctions_by_sellers_only
def get_auctions_by_seller_role(role: str = "Seller") -> list[dict]:
    return list(
        AuctionItem.objects
        .filter(seller__role=role)
        .values(username=F("seller__username"), title=F("title")))


# QUERY 06 — LEFT JOIN: select_all_users_with_auctions
def get_all_users_with_auctions() -> list[dict]:
    return list(
        User.objects
        .values("username", "auctions__title"))


# QUERY 07 — LEFT JOIN + IS NULL: select_users_without_auctions
def get_users_without_auctions() -> list[dict]:
    return list(
        User.objects
        .filter(auctions__isnull=True)
        .values())


# QUERY 08 — LEFT JOIN + GROUP BY: count_auctions_per_user
def get_auction_count_per_user() -> list[dict]:
    return list(
        User.objects
        .annotate(total_auctions=Count("auctions"))
        .values("username", "total_auctions"))


# QUERY 09 — JOIN + GROUP BY: count_auctions_per_seller
def get_auction_count_per_seller() -> list[dict]:
    return list(
        User.objects
        .filter(auctions__isnull=False)
        .annotate(total_auctions=Count("auctions"))
        .values("username", "total_auctions"))


# QUERY 10 — GROUP BY + HAVING: select_sellers_with_more_than_one_auction
def get_sellers_with_more_than_one_auction() -> list[dict]:
    return list(
        User.objects
        .filter(auctions__isnull=False)
        .annotate(total_auctions=Count("auctions"))
        .filter(total_auctions__gt=1)
        .values("username", "total_auctions"))


# QUERY 11 — SUM + GROUP BY: select_total_auction_value_per_seller
def get_total_auction_value_per_seller() -> list[dict]:
    return list(
        User.objects
        .filter(auctions__isnull=False)
        .annotate(total_auction_value=Sum("auctions__current_price"))
        .values("username", "total_auction_value"))


# QUERY 12 — ORDER BY + LIMIT: select_seller_with_highest_auction
def get_seller_with_highest_auction() -> list[dict]:
    return list(
        AuctionItem.objects
        .order_by("-current_price")
        .values(
            username=F("seller__username"),
            title=F("title"),
            current_price=F("current_price")
        )[:1])


# QUERY 13 — ORDER BY DATE + LIMIT: select_latest_auction_with_seller
def get_latest_auction_with_seller() -> list[dict]:
    return list(
        AuctionItem.objects
        .order_by("-start_time")
        .values(
            username=F("seller__username"),
            title=F("title"),
            start_time=F("start_time")
        )[:1])


# QUERY 14 — CURRENT_TIME: select_active_auctions
def get_active_auctions() -> list[dict]:
    return list(
        AuctionItem.objects
        .filter(
            end_time__gt=Cast(
                Now(),
                output_field=TimeField()))
        .values(
            username=F("seller__username"),
            title=F("title")))


# QUERY 15 — BETWEEN: select_auctions_between_prices
def get_auctions_between_prices(minimum_price: float, maximum_price: float) -> list[dict]:
    return list(
        AuctionItem.objects
        .filter(current_price__range=(minimum_price, maximum_price))
        .values(
            username=F("seller__username"),
            title=F("title"),
            current_price=F("current_price")))


# QUERY 16 — LIKE: select_sellers_starting_with_r
def get_auctions_by_seller_username_prefix(prefix: str) -> list[dict]:
    return list(
        AuctionItem.objects
        .filter(seller__username__startswith=prefix)
        .values(username=F("seller__username"), title=F("title")))


# QUERY 17 — LIKE: select_auction_titles_containing_phone
def get_auctions_with_title_containing(keyword: str) -> list[dict]:
    return list(
        AuctionItem.objects
        .filter(title__contains=keyword)
        .values(username=F("seller__username"), title=F("title")))


# QUERY 18 — GROUP BY + COUNT + ORDER BY: count_auctions_per_user_descending
def get_users_by_auction_count_descending() -> list[dict]:
    return list(
        User.objects
        .annotate(total_auctions=Count("auctions"))
        .values("username", "total_auctions")
        .order_by("-total_auctions"))


# QUERY 19 — LEFT JOIN + IS NULL: select_sellers_without_auctions
def get_sellers_without_auctions() -> list[dict]:
    return list(
        User.objects
        .filter(role="Seller", auctions__isnull=True)
        .values("id", "username"))


# QUERY 20 — GROUP BY + COUNT + LIMIT: select_seller_with_most_auctions
def get_seller_with_most_auctions() -> list[dict]:
    return list(
        User.objects
        .annotate(total_auctions=Count("auctions"))
        .values("username", "total_auctions")
        .order_by("-total_auctions")[:1])


# QUERY 21 — SUM + GROUP BY + HAVING: select_sellers_with_total_value_above_limit
def get_sellers_with_total_value_above(minimum_value: float) -> list[dict]:
    return list(
        User.objects
        .annotate(total_auction_value=Sum("auctions__current_price"))
        .filter(total_auction_value__gt=minimum_value)
        .values(
            "username",
            "total_auction_value"))


# EXTRAS
# QUERY 22 - COUNT: count_total_auctions
def count_auctions() -> int:
    return AuctionItem.objects.count()


# QUERY 23 - COUNT + CURRENT_TIME: count_active_auctions
def count_active_auctions() -> int:
    return AuctionItem.objects.filter(end_time__gt = Cast(Now(), output_field=TimeField())).count()


# QUERY 24 - COUNT + CURRENT_TIME: count_inactive_auctions
def count_inactive_auctions() -> int:
    return AuctionItem.objects.filter(
        end_time__lte=Cast(
            Now(),
            output_field=TimeField())).count()


# QUERY 25 - SUM: get_total_auction_value
def get_total_auction_value() -> Decimal:
    return AuctionItem.objects.aggregate(
        total_auction_value=Coalesce(
            Sum("current_price"),
            Decimal("0")))["total_auction_value"]