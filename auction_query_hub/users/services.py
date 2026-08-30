from django.db.models import Count, Q
from django.db.models.functions import Length, Upper
from .models import User


# QUERY 01 — SELECT: select_all_users
def get_all_users() -> list[dict]:
    return list(User.objects.values())


# QUERY 02 — SELECT specific columns: select_username_email
def get_user_contact_details() -> list[dict]:
    return list(User.objects.values("username", "email"))


# QUERY 03 — WHERE: select_users_by_role
def get_users_by_role(role: str) -> list[dict]:
    return list(User
                .objects
                .filter(role=role)
                .values())


# QUERY 04 — AND: select_user_by_role_and_username
def get_user_by_role_and_username(role: str, username: str) -> list[dict]:
    return list(
        User.objects
        .filter(role=role, username=username)
        .values())


# QUERY 05 — OR: select_buyers_or_admins
def get_buyers_or_admins() -> list[dict]:
    return list(
        User.objects
        .filter(Q(role="Buyer") | Q(role="Admin"))
        .values())


# QUERY 06 — NOT: select_non_buyers
def get_non_buyers() -> list[dict]:
    return list(
        User.objects
        .exclude(role="Buyer")
        .values())


# QUERY 07 — IN: select_users_by_multiple_roles
def get_buyers_and_sellers() -> list[dict]:
    return list(
        User.objects
        .filter(role__in=["Buyer", "Seller"])
        .values())


# QUERY 08 — LIKE: select_users_by_username_pattern
def search_users_by_username_prefix(prefix: str) -> list[dict]:
    return list(
        User.objects
        .filter(username__startswith=prefix)
        .values())


# QUERY 09 — COUNT: count_total_users
def count_users() -> int:
    return User.objects.count()


# QUERY 10 — COUNT + WHERE: count_total_buyers
def count_buyers() -> int:
    return User.objects.filter(role="Buyer").count()


# QUERY 11 — DISTINCT: select_distinct_roles
def get_distinct_roles() -> list[dict]:
    return list(
        User.objects
        .values("role")
        .distinct())


# QUERY 12 — ORDER BY ASC: select_users_by_username_ascending
def get_users_ordered_by_username_asc() -> list[dict]:
    return list(
        User.objects
        .order_by("username")
        .values()
    )


# QUERY 13 — ORDER BY DESC: select_users_by_username_descending
def get_users_ordered_by_username_desc() -> list[dict]:
    return list(
        User.objects
        .order_by("-username")
        .values())


# QUERY 14 — LIMIT: select_first_two_users
def get_first_two_users() -> list[dict]:
    return list(
        User.objects
        .all()
        .values()[:2])


# QUERY 15 — LIMIT + OFFSET: select_users_with_pagination
def get_users_with_pagination(limit: int, offset: int) -> list[dict]:
    return list(
        User.objects
        .order_by("id")
        .values()[offset:offset + limit])


# QUERY 16 — GROUP BY: count_users_by_role
def get_user_count_by_role() -> list[dict]:
    return list(
        User.objects
        .values("role")
        .annotate(total_users=Count("id")))


# QUERY 17 — HAVING: select_roles_with_multiple_users
def get_roles_with_multiple_users() -> list[dict]:
    return list(
        User.objects
        .values("role")
        .annotate(total_users=Count("id"))
        .filter(total_users__gt=1))


# QUERY 18 — UPDATE: update_user_role_query
def update_user_role(user_id: int, role: str) -> int:
    return User.objects.filter(id=user_id).update(role=role)


# QUERY 19 — DELETE: delete_user_by_id
def delete_user(user_id: int) -> int:
    deleted_count, _ = User.objects.filter(id=user_id).delete()

    return deleted_count


# QUERY 20 — Latest user: select_latest_created_user
def get_latest_user() -> list[dict]:
    return list(
        User.objects
        .order_by("-created_at")
        .values()[:1])


# QUERY 21 — Oldest user: select_oldest_created_user
def get_oldest_user() -> list[dict]:
    return list(
        User.objects
        .order_by("created_at")
        .values()[:1])


# QUERY 22 — ILIKE: select_users_by_username_case_insensitive
def search_users_case_insensitive(search_term: str) -> list[dict]:
    return list(
        User.objects
        .filter(username__icontains=search_term)
        .values())


# QUERY 23 — UPPER: select_usernames_uppercase
def get_usernames_uppercase() -> list[dict]:
    return list(
        User.objects
        .annotate(uppercase_username=Upper("username"))
        .values("username", "uppercase_username"))


# QUERY 24 — LENGTH: select_usernames_with_length
def get_username_lengths() -> list[dict]:
    return list(
        User.objects
        .annotate(username_length=Length("username"))
        .values("username", "username_length"))


# QUERY 25 — GROUP BY + COUNT + ORDER BY: count_users_by_role_descending
def get_roles_by_user_count() -> list[dict]:
    return list(
        User.objects
        .values("role")
        .annotate(total_users=Count("id"))
        .order_by("-total_users"))


# QUERY 26 — COUNT + WHERE: count_total_sellers
def count_sellers() -> int:
    return User.objects.filter(role="Seller").count()