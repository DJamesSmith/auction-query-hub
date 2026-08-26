from django.db import connection


# Execute a SELECT query and return the result as a list of dictionaries.
def execute_select(query: str, params: list | tuple | None = None) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]


# Execute an INSERT, UPDATE, or DELETE query and return the number of affected rows.
def execute_write(query: str, params: list | tuple | None = None) -> int:
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        return cursor.rowcount

# QUERY 01 — SELECT: select_all_users
def get_all_users() -> list[dict]:
    return execute_select("""SELECT * FROM users;""")

# QUERY 02 — SELECT specific columns: select_username_email
def get_user_contact_details() -> list[dict]:
    return execute_select("""SELECT username, email FROM users;""")

# QUERY 03 — WHERE: select_users_by_role
def get_users_by_role(role: str) -> list[dict]:
    return execute_select("""SELECT * FROM users WHERE role = %s;""", [role])

# QUERY 04 — AND: select_user_by_role_and_username
def get_user_by_role_and_username(role: str, username: str) -> list[dict]:
    return execute_select("""SELECT * FROM users WHERE role = %s AND username = %s;""", [role, username])

# QUERY 05 — OR: select_buyers_or_admins
def get_buyers_or_admins() -> list[dict]:
    return execute_select("""SELECT * FROM users WHERE role = 'Buyer' OR role = 'Admin';""")

# QUERY 06 — NOT: select_non_buyers
def get_non_buyers() -> list[dict]:
    return execute_select("""SELECT * FROM users WHERE role <> 'Buyer';""")

# QUERY 07 — IN: select_users_by_multiple_roles
def get_buyers_and_sellers() -> list[dict]:
    return execute_select("""SELECT * FROM users WHERE role IN ('Buyer', 'Seller');""")

# QUERY 08 — LIKE: select_users_by_username_pattern
def search_users_by_username_prefix( prefix: str,) -> list[dict]:
    return execute_select("""SELECT * FROM users WHERE username LIKE %s;""", [f"{prefix}%"])

# QUERY 09 — COUNT: count_total_users
def count_users() -> int:
    result = execute_select("""SELECT COUNT(*) AS total_users FROM users;""")
    return result[0]["total_users"]

# QUERY 10 — COUNT + WHERE: count_total_buyers
def count_buyers() -> int:
    result = execute_select("""SELECT COUNT(*) AS total_buyers FROM users WHERE role = 'Buyer';""")
    return result[0]["total_buyers"]

# QUERY 11 — DISTINCT: select_distinct_roles
def get_distinct_roles() -> list[dict]:
    return execute_select("""SELECT DISTINCT role FROM users;""")

# QUERY 12 — ORDER BY ASC: select_users_by_username_ascending
def get_users_ordered_by_username_asc() -> list[dict]:
    return execute_select("""SELECT * FROM users ORDER BY username ASC;""")

# QUERY 13 — ORDER BY DESC: select_users_by_username_descending
def get_users_ordered_by_username_desc() -> list[dict]:
    return execute_select("""SELECT * FROM users ORDER BY username DESC;""")

# QUERY 14 — LIMIT: select_first_two_users
def get_first_two_users() -> list[dict]:
    return execute_select("""SELECT * FROM users LIMIT 2;""")

# QUERY 15 — LIMIT + OFFSET: select_users_with_pagination
def get_users_with_pagination( limit: int, offset: int,) -> list[dict]:
    return execute_select("""SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s;""", [limit, offset])

# QUERY 16 — GROUP BY: count_users_by_role
def get_user_count_by_role() -> list[dict]:
    return execute_select("""SELECT role, COUNT(*) AS total_users FROM users GROUP BY role;""")

# QUERY 17 — HAVING: select_roles_with_multiple_users
def get_roles_with_multiple_users() -> list[dict]:
    return execute_select("""SELECT role, COUNT(*) AS total_users FROM users GROUP BY role HAVING COUNT(*) > 1;""")

# QUERY 18 — UPDATE: update_user_role_query
def update_user_role(user_id: int, role: str) -> int:
    return execute_write("""UPDATE users SET role = %s WHERE id = %s;""", [role, user_id])

# QUERY 19 — DELETE: delete_user_by_id
def delete_user(user_id: int) -> int:
    return execute_write("""DELETE FROM users WHERE id = %s;""", [user_id])

# QUERY 20 — Latest user: select_latest_created_user
def get_latest_user() -> list[dict]:
    return execute_select("""SELECT * FROM users ORDER BY created_at DESC LIMIT 1;""")

# QUERY 21 — Oldest user: select_oldest_created_user
def get_oldest_user() -> list[dict]:
    return execute_select("""SELECT * FROM users ORDER BY created_at ASC LIMIT 1;""")

# QUERY 22 — ILIKE: select_users_by_username_case_insensitive
def search_users_case_insensitive(search_term: str ) -> list[dict]:
    return execute_select("""SELECT * FROM users WHERE username ILIKE %s;""", [f"%{search_term}%"])

# QUERY 23 — UPPER: select_usernames_uppercase
def get_usernames_uppercase() -> list[dict]:
    return execute_select("""SELECT username, UPPER(username) AS uppercase_username FROM users;""")

# QUERY 24 — LENGTH: select_usernames_with_length
def get_username_lengths() -> list[dict]:
    return execute_select("""SELECT username, LENGTH(username) AS username_length FROM users;""")

# QUERY 25 — GROUP BY + COUNT + ORDER BY: count_users_by_role_descending
def get_roles_by_user_count() -> list[dict]:
    return execute_select("""SELECT role, COUNT(*) AS total_users FROM users GROUP BY role ORDER BY total_users DESC;""")

# QUERY 26 — COUNT + WHERE: count_total_sellers
def count_sellers() -> int:
    result = execute_select("""SELECT COUNT(*) AS total_sellers FROM users WHERE role = 'Seller';""")
    return result[0]["total_sellers"]