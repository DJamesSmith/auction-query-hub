from django.urls import path
from .views import views
from .views import api_views

urlpatterns = [
    path("", views.auction_list, name="auction_list"),
    path("create/", views.create_auction, name="create_auction"),

    # APIs
    path("api/", api_views.api_auction_list, name="api_auction_list"),
    path("api/create/", api_views.api_create_auction, name="api_auction_create"),
]