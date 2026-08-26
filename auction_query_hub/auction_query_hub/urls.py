from django.contrib import admin
from django.urls import path, include
from users.views import views

urlpatterns = [
    # templates
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("users/", include("users.urls")),
    path("auctions/", include("auctions.urls")),
    path("analytics/", include("analytics.urls")),
]