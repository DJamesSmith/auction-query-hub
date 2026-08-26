from django.urls import path
from .views import api_views
from .views import views


urlpatterns = [
    # templates
    path("", views.analytics, name="analytics"),
    path("price-range/", views.price_range_search, name="price_range_search"),
    path("sellers/", views.seller_search, name="seller_search"),
    path("auctions/search/", views.auction_title_search, name="auction_title_search"),


    # APIs
    path("api/", api_views.analytics_api, name="analytics_api"),

    # User analytics APIs
    path("api/users-by-role/", api_views.users_by_role_api, name="users_by_role_api"),                                      # users by role

    # Seller analytics APIs
    path("api/auction-count-per-seller/", api_views.auction_count_per_seller_api, name="auction_count_per_seller_api"),     # auction count per seller
    path("api/multiple-auction-sellers/", api_views.multiple_auction_sellers_api, name="multiple_auction_sellers_api"),     # sellers with multiple auctions
    path("api/top-seller/", api_views.top_seller_api, name="top_seller_api"),                                               # top seller
    path("api/auction-value-per-seller/", api_views.auction_value_per_seller_api, name="auction_value_per_seller_api"),     # auction value per seller
    path("api/high-value-sellers/", api_views.high_value_sellers_api, name="high_value_sellers_api"),                       # high-value sellers
    path("api/inactive-sellers/", api_views.inactive_sellers_api, name="inactive_sellers_api"),                             # inactive sellers

    # Auction analytics APIs
    path("api/highest-auction/", api_views.highest_auction_api, name="highest_auction_api"),                                # highest auction
    path("api/latest-auction/", api_views.latest_auction_api, name="latest_auction_api"),                                   # latest auction
    path("api/active-auctions/", api_views.active_auctions_api, name="active_auctions_api"),                                # active auctions

    # Search APIs
    path("api/price-range/", api_views.price_range_api, name="price_range_api"),                                            # price-range search
    path("api/sellers/", api_views.seller_search_api, name="seller_search_api"),                                            # seller-prefix search
    path("api/auctions/search/", api_views.auction_title_search_api, name="auction_title_search_api"),                      # auction-title search
]