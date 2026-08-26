from django.urls import path
from .views import views
from .views import api_views

urlpatterns = [
    # templates
    path("", views.user_list, name="user_list"),
    path( "create/", views.create_user, name="create_user"),
    path("<int:user_id>/update/", views.update_user, name="update_user"),
    path("<int:user_id>/delete/", views.delete_user_view, name="delete_user"),

    # APIs
    path("api/", api_views.user_api_list, name="api_user_list"),
    path("api/create/", api_views.user_api_create, name="api_user_create"),
]


# DRF Serializer classes handle validation and representation and the api_views.py handles HTTP/API behavior