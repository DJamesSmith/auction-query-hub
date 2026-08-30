from decimal import Decimal
from django.db import connection

# 21 FOREIGN KEY SQL QUERIES
# Execute a SELECT query and return the result as a list of dictionaries.
def execute_select(query: str, params: list | tuple | None = None) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]

# Execute an INSERT, UPDATE, or DELETE query and return the number of affected rows
def execute_write(query: str, params: list | tuple | None = None) -> int:
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        return cursor.rowcount


# Get all auctions: get_all_auctions_query
def get_all_auctions() -> list[dict]:
    return execute_select("""select * from auction_items;""")


# QUERY 01 — INNER JOIN: select_username_and_title
def get_username_and_auction_title() -> list[dict]:
    return execute_select("""
        SELECT username, title
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id;""")


# QUERY 02 — INNER JOIN: select_seller_name_and_auction_title
def get_seller_name_and_auction_title() -> list[dict]:
    return execute_select("""
        SELECT u.username, a.title
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id;""")


# QUERY 03 — JOIN + SELECT ALL: select_all_auction_details_with_seller
def get_all_auction_details_with_seller() -> list[dict]:
    return execute_select("""
        SELECT a.*, u.username
        FROM auction_items a
        JOIN users u
            ON a.seller_id = u.id;""")


# QUERY 04 — JOIN + WHERE: select_auctions_by_rahul
def get_auctions_by_username(username: str) -> list[dict]:
    return execute_select("""
            SELECT a.*
            FROM users u
            JOIN auction_items a
                ON u.id = a.seller_id
            WHERE u.username = %s;
        """, [username])


# QUERY 05 — JOIN + WHERE ROLE: select_auctions_by_sellers_only
def get_auctions_by_seller_role(role: str = "Seller") -> list[dict]:
    return execute_select("""
            SELECT u.username, a.title
            FROM users u
            JOIN auction_items a
                ON u.id = a.seller_id
            WHERE u.role = %s;
        """, [role])


# QUERY 06 — LEFT JOIN: select_all_users_with_auctions
def get_all_users_with_auctions() -> list[dict]:
    return execute_select("""
        SELECT u.username, a.title
        FROM users u
        LEFT JOIN auction_items a
            ON u.id = a.seller_id;""")


# QUERY 07 — LEFT JOIN + IS NULL: select_users_without_auctions
def get_users_without_auctions() -> list[dict]:
    return execute_select("""
        SELECT u.*
        FROM users u
        LEFT JOIN auction_items a
            ON u.id = a.seller_id
        WHERE a.id IS NULL;""")


# QUERY 08 — LEFT JOIN + GROUP BY: count_auctions_per_user
def get_auction_count_per_user() -> list[dict]:
    return execute_select("""
        SELECT u.username, COUNT(a.id) AS total_auctions
        FROM users u
        LEFT JOIN auction_items a
            ON u.id = a.seller_id
        GROUP BY u.username;""")


# QUERY 09 — JOIN + GROUP BY: count_auctions_per_seller
def get_auction_count_per_seller() -> list[dict]:
    return execute_select("""
        SELECT u.username, COUNT(a.id) AS total_auctions
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id
        GROUP BY u.username;""")


# QUERY 10 — GROUP BY + HAVING: select_sellers_with_more_than_one_auction
def get_sellers_with_more_than_one_auction() -> list[dict]:
    return execute_select("""
        SELECT u.username, COUNT(a.id) AS total_auctions
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id
        GROUP BY u.username
        HAVING COUNT(a.id) > 1;""")


# QUERY 11 — SUM + GROUP BY: select_total_auction_value_per_seller
def get_total_auction_value_per_seller() -> list[dict]:
    return execute_select("""
        SELECT u.username, SUM(a.current_price) AS total_auction_value
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id
        GROUP BY u.username;""")


# QUERY 12 — ORDER BY + LIMIT: select_seller_with_highest_auction
def get_seller_with_highest_auction() -> list[dict]:
    return execute_select("""
        SELECT u.username, a.title, a.current_price
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id
        ORDER BY a.current_price DESC
        LIMIT 1;""")


# QUERY 13 — ORDER BY DATE + LIMIT: select_latest_auction_with_seller
def get_latest_auction_with_seller() -> list[dict]:
    return execute_select("""
        SELECT u.username, a.title, a.start_time
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id
        ORDER BY a.start_time DESC
        LIMIT 1;""")


# QUERY 14 — CURRENT_TIME: select_active_auctions
def get_active_auctions() -> list[dict]:
    return execute_select("""
        SELECT u.username, a.title
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id
        WHERE a.end_time > CURRENT_TIME;""")


# QUERY 15 — BETWEEN: select_auctions_between_prices
def get_auctions_between_prices(minimum_price: float, maximum_price: float) -> list[dict]:
    return execute_select("""
        SELECT u.username, a.title, a.current_price
        FROM users u
        JOIN auction_items a
            ON u.id = a.seller_id
        WHERE a.current_price BETWEEN %s AND %s;
    """, [minimum_price, maximum_price])


# QUERY 16 — LIKE: select_sellers_starting_with_r
def get_auctions_by_seller_username_prefix(prefix: str) -> list[dict]:
    return execute_select("""
            SELECT u.username, a.title
            FROM users u
            JOIN auction_items a
                ON u.id = a.seller_id
            WHERE u.username LIKE %s;
        """, [f"{prefix}%"])


# QUERY 17 — LIKE: select_auction_titles_containing_phone
def get_auctions_with_title_containing(keyword: str) -> list[dict]:
    return execute_select("""
            SELECT u.username, a.title
            FROM users u
            JOIN auction_items a
                ON u.id = a.seller_id
            WHERE a.title LIKE %s;
        """, [f"%{keyword}%"])


# QUERY 18 — GROUP BY + COUNT + ORDER BY: count_auctions_per_user_descending
def get_users_by_auction_count_descending() -> list[dict]:
    return execute_select("""
        SELECT
            u.username,
            COUNT(a.id) AS total_auctions
        FROM users u
        LEFT JOIN auction_items a
            ON u.id = a.seller_id
        GROUP BY u.username
        ORDER BY total_auctions DESC;""")


# QUERY 19 — LEFT JOIN + IS NULL: select_sellers_without_auctions
def get_sellers_without_auctions() -> list[dict]:
    return execute_select("""
        SELECT u.id, u.username
        FROM users u
        LEFT JOIN auction_items a
            ON u.id = a.seller_id
        WHERE u.role = 'Seller'
        AND a.id IS NULL;
    """)


# QUERY 20 — GROUP BY + COUNT + LIMIT: select_seller_with_most_auctions
def get_seller_with_most_auctions() -> list[dict]:
    return execute_select("""
        SELECT
            u.username,
            COUNT(a.id) AS total_auctions
        FROM users u
        LEFT JOIN auction_items a
            ON u.id = a.seller_id
        GROUP BY u.username
        ORDER BY total_auctions DESC
        LIMIT 1;""")


# QUERY 21 — SUM + GROUP BY + HAVING: select_sellers_with_total_value_above_limit
def get_sellers_with_total_value_above(minimum_value: float) -> list[dict]:
    return execute_select("""SELECT
            u.username,
            SUM(a.current_price) AS total_auction_value
        FROM users u
        LEFT JOIN auction_items a
            ON u.id = a.seller_id
        GROUP BY u.username
        HAVING SUM(a.current_price) > %s;""", [minimum_value])

# EXTRAS
# QUERY 22 - COUNT: count_total_auctions
def count_auctions() -> int:
    result = execute_select("""SELECT COUNT(*) AS total_auctions FROM auction_items;""")
    return result[0]["total_auctions"]

# QUERY 23 - COUNT + CURRENT_TIME: count_active_auctions
def count_active_auctions() -> int:
    result = execute_select("""SELECT COUNT(*) AS total_active_auctions FROM auction_items WHERE end_time > CURRENT_TIME;""")
    return result[0]["total_active_auctions"]


# QUERY 24 - COUNT + CURRENT_TIME: count_inactive_auctions
def count_inactive_auctions() -> int:
    result = execute_select("""SELECT COUNT(*) AS total_inactive_auctions FROM auction_items WHERE end_time <= CURRENT_TIME;""")
    return result[0]["total_inactive_auctions"]


# QUERY 25 - SUM: get_total_auction_value
def get_total_auction_value() -> Decimal:
    result = execute_select("""SELECT COALESCE(SUM(current_price), 0) AS total_auction_value FROM auction_items;""")
    return result[0]["total_auction_value"]