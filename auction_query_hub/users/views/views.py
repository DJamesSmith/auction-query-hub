from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import QuerySet
from auctions.models import AuctionItem
from ..models import User
from ..forms import UserForm
from ..services import (
    get_all_users,
    delete_user,
    get_distinct_roles,
    get_users_by_role,
    get_users_with_pagination,
    search_users_case_insensitive,
    update_user_role,
)


# def home(request: HttpRequest) -> HttpResponse:
#     users: QuerySet[User] = User.objects.all()
#     auctions: QuerySet[AuctionItem] = AuctionItem.objects.all()
#     user_auctions = User.objects.prefetch_related("auctions")

#     context: dict = {
#         "users": users,
#         "auctions": auctions,
#         "user_auctions": user_auctions,
#     }

#     return render(request, "home.html", context)

def home(request: HttpRequest) -> HttpResponse:
    users: QuerySet[User] = User.objects.prefetch_related("auctions")
    auctions: QuerySet[AuctionItem] = AuctionItem.objects.select_related("seller")
    # user_auctions = user.auctions.all()                   # returns AuctionItem objects belonging to that particular user. It does not return a single auction.

    context: dict = {
        "users": users,
        "auctions": auctions,
    }

    return render(request, "home.html", context)


def create_user(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        form: UserForm = UserForm()
        return render(request, "users/user_form.html", { "form": form })

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            # user.password = make_password(form.cleaned_data["password"])
            user.password = form.cleaned_data["password"]
            user.save()

            return JsonResponse({
                    "success": True,
                    "message": "User created successfully.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                    },
                }, status=201)
        return JsonResponse({
                "success": False,
                "errors": form.errors.get_json_data(),      # returns something structured like: { "email": [{ "message": "User with this Email already exists.", "code": "unique" }]}
            }, status=400)
    return JsonResponse({
            "success": False,
            "message": "Invalid request method.",
        }, status=405)


def user_list(request: HttpRequest) -> HttpResponse:
    search_term: str = request.GET.get("search", "").strip()
    role: str = request.GET.get("role", "").strip()

    page: int = int(request.GET.get("page", 1))
    page_size: int = 10
    offset: int = (page - 1) * page_size
    roles: list[dict] = get_distinct_roles()
    has_next: bool = False

    if search_term:
        users = search_users_case_insensitive(search_term)
    elif role:
        users: list[dict] = get_users_by_role(role)
    else:
        users = get_users_with_pagination(limit=page_size, offset=offset)
        has_next = len(users) == page_size

    context = {
        "users": users,
        "roles": roles,
        "search_term": search_term,
        "selected_role": role,
        "page": page,
        "page_size": page_size,
        "has_next": has_next,
    }

    return render(request, "users/user_list.html", context)

def update_user(request: HttpRequest, user_id: int) -> HttpResponse:
    if request.method == "POST":
        role = request.POST.get("role")
        if role:
            update_user_role(user_id=user_id, role=role)
    return redirect("user_list")

def delete_user_view(request: HttpRequest, user_id: int) -> HttpResponse:
    if request.method == "POST":
        delete_user(user_id)
    return redirect("user_list")