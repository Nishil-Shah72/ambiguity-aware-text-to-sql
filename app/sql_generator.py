class SQLGenerator:

    def __init__(self, schema):
        self.schema = schema

    def generate(self, intent):
        """
        Convert UserIntent into SQL.

        Supports:
        - Retrieval
        - Ranking
        - Aggregation
        - Numeric conditions
        - Time ranges
        - Customer spending/order ranking
        - Product price/quantity/sales ranking
        """

        # ==================================================
        # 1. RANKING
        # ==================================================

        if intent.action == "ranking":

            # ----------------------------------------------
            # Customer ranking
            # ----------------------------------------------

            if "customers" in intent.entities:

                criteria = intent.ranking_criteria

                if criteria in ["total_spending", "sales", "revenue"]:
                    query = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    c.age,
    COALESCE(SUM(o.total_amount), 0) AS total_spending
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
""".strip()

                    query = self._apply_time_range(
                        query,
                        "o.order_date",
                        intent.time_range
                    )

                    query += """
GROUP BY
    c.customer_id,
    c.name,
    c.city,
    c.age
ORDER BY total_spending DESC
LIMIT 10;
""".rstrip()

                    return query

                if criteria == "order_count":
                    query = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    c.age,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
""".strip()

                    query = self._apply_time_range(
                        query,
                        "o.order_date",
                        intent.time_range
                    )

                    query += """
GROUP BY
    c.customer_id,
    c.name,
    c.city,
    c.age
ORDER BY order_count DESC
LIMIT 10;
""".rstrip()

                    return query

                if criteria == "age":
                    return """
SELECT
    customer_id,
    name,
    city,
    age
FROM customers
ORDER BY age DESC
LIMIT 10;
""".strip()

                # Default customer ranking
                query = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    c.age,
    COALESCE(SUM(o.total_amount), 0) AS total_spending
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
""".strip()

                query = self._apply_time_range(
                    query,
                    "o.order_date",
                    intent.time_range
                )

                query += """
GROUP BY
    c.customer_id,
    c.name,
    c.city,
    c.age
ORDER BY total_spending DESC
LIMIT 10;
""".rstrip()

                return query

            # ----------------------------------------------
            # Product ranking
            # ----------------------------------------------

            if "products" in intent.entities:

                criteria = intent.ranking_criteria

                if criteria == "price":
                    return """
SELECT
    product_id,
    product_name,
    category,
    price
FROM products
ORDER BY price DESC
LIMIT 10;
""".strip()

                if criteria == "quantity":
                    query = """
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    COALESCE(SUM(oi.quantity), 0) AS quantity_sold
FROM products p
LEFT JOIN order_items oi
    ON p.product_id = oi.product_id
LEFT JOIN orders o
    ON oi.order_id = o.order_id
""".strip()

                    query = self._apply_time_range(
                        query,
                        "o.order_date",
                        intent.time_range
                    )

                    query += """
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.price
ORDER BY quantity_sold DESC
LIMIT 10;
""".rstrip()

                    return query

                if criteria in [
                    "sales",
                    "revenue",
                    "total_spending"
                ]:
                    query = """
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    COALESCE(
        SUM(oi.quantity * p.price),
        0
    ) AS total_sales
FROM products p
LEFT JOIN order_items oi
    ON p.product_id = oi.product_id
LEFT JOIN orders o
    ON oi.order_id = o.order_id
""".strip()

                    query = self._apply_time_range(
                        query,
                        "o.order_date",
                        intent.time_range
                    )

                    query += """
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.price
ORDER BY total_sales DESC
LIMIT 10;
""".rstrip()

                    return query

                return """
SELECT
    product_id,
    product_name,
    category,
    price
FROM products
ORDER BY price DESC
LIMIT 10;
""".strip()

            # ----------------------------------------------
            # Order ranking
            # ----------------------------------------------

            if "orders" in intent.entities:

                query = """
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
""".strip()

                query = self._apply_time_range(
                    query,
                    "order_date",
                    intent.time_range
                )

                query += """
ORDER BY total_amount DESC
LIMIT 10;
""".rstrip()

                return query

        # ==================================================
        # 2. AGGREGATION
        # ==================================================

        if intent.action == "aggregation":

            # ----------------------------------------------
            # Average
            # ----------------------------------------------

            if intent.aggregation == "average":

                if "orders" in intent.entities:

                    query = """
SELECT
    AVG(total_amount) AS average_order_amount
FROM orders
""".strip()

                    query = self._apply_time_range(
                        query,
                        "order_date",
                        intent.time_range
                    )

                    query += ";"

                    return query

                if "products" in intent.entities:

                    return """
SELECT
    AVG(price) AS average_product_price
FROM products;
""".strip()

                if (
                    "customers.age" in intent.entities
                    or (
                        "customers" in intent.entities
                        and "age" in intent.question.lower()
                    )
                ):

                    return """
SELECT
    AVG(age) AS average_age
FROM customers;
""".strip()

            # ----------------------------------------------
            # Total
            # ----------------------------------------------

            if intent.aggregation == "total":

                if (
                    "orders.total_amount" in intent.entities
                    or "orders" in intent.entities
                    or intent.scope == "sales"
                ):

                    query = """
SELECT
    SUM(total_amount) AS total_sales
FROM orders
""".strip()

                    query = self._apply_time_range(
                        query,
                        "order_date",
                        intent.time_range
                    )

                    query += ";"

                    return query

            # ----------------------------------------------
            # Count
            # ----------------------------------------------

            if intent.aggregation == "count":

                if "customers" in intent.entities:

                    return """
SELECT
    COUNT(*) AS customer_count
FROM customers;
""".strip()

                if "products" in intent.entities:

                    return """
SELECT
    COUNT(*) AS product_count
FROM products;
""".strip()

                if "orders" in intent.entities:

                    query = """
SELECT
    COUNT(*) AS order_count
FROM orders
""".strip()

                    query = self._apply_time_range(
                        query,
                        "order_date",
                        intent.time_range
                    )

                    query += ";"

                    return query

        # ==================================================
        # 3. NUMERIC CONDITIONS
        # ==================================================

        if intent.conditions:

            condition_parts = []

            for condition in intent.conditions:

                column = condition["column"]
                operator = condition["operator"]
                value = condition["value"]

                condition_parts.append(
                    f"{column} {operator} {value}"
                )

            where_clause = " AND ".join(condition_parts)

            tables = set(
                condition["column"].split(".")[0]
                for condition in intent.conditions
            )

            if len(tables) == 1:

                table = list(tables)[0]

                query = f"""
SELECT *
FROM {table}
WHERE {where_clause}
""".strip()

                # Only orders have order_date in the
                # current database schema.
                if table == "orders":
                    query = self._apply_time_range(
                        query,
                        "order_date",
                        intent.time_range
                    )

                query += ";"

                return query

        # ==================================================
        # 4. ORDER RETRIEVAL
        # ==================================================

        if "orders" in intent.entities:

            query = """
SELECT *
FROM orders
""".strip()

            query = self._apply_time_range(
                query,
                "order_date",
                intent.time_range
            )

            query += ";"

            return query

        # ==================================================
        # 5. CUSTOMER RETRIEVAL
        # ==================================================

        if "customers" in intent.entities:

            return """
SELECT *
FROM customers;
""".strip()

        # ==================================================
        # 6. PRODUCT RETRIEVAL
        # ==================================================

        if "products" in intent.entities:

            return """
SELECT *
FROM products;
""".strip()

        return None

    # ======================================================
    # TIME RANGE HELPER
    # ======================================================

    def _apply_time_range(
        self,
        query,
        date_column,
        time_range
    ):
        """
        Add a time-range condition safely.

        If the query already contains WHERE,
        use AND instead of adding another WHERE.
        """

        if not time_range:
            return query

        connector = (
            " AND "
            if " WHERE " in query.upper()
            else " WHERE "
        )

        if time_range == "today":

            query += (
                f"{connector}"
                f"DATE({date_column}) = CURDATE()"
            )

        elif time_range == "yesterday":

            query += (
                f"{connector}"
                f"DATE({date_column}) = "
                f"DATE_SUB(CURDATE(), INTERVAL 1 DAY)"
            )

        elif time_range == "this_week":

            query += f"""
{connector}{date_column} >= DATE_SUB(
    CURDATE(),
    INTERVAL WEEKDAY(CURDATE()) DAY
)
AND {date_column} < DATE_ADD(
    DATE_SUB(
        CURDATE(),
        INTERVAL WEEKDAY(CURDATE()) DAY
    ),
    INTERVAL 7 DAY
)
""".rstrip()

        elif time_range == "last_week":

            query += f"""
{connector}{date_column} >= DATE_SUB(
    CURDATE(),
    INTERVAL (WEEKDAY(CURDATE()) + 7) DAY
)
AND {date_column} < DATE_SUB(
    CURDATE(),
    INTERVAL WEEKDAY(CURDATE()) DAY
)
""".rstrip()

        elif time_range == "this_month":

            query += f"""
{connector}{date_column} >= DATE_FORMAT(
    CURDATE(),
    '%Y-%m-01'
)
AND {date_column} < DATE_FORMAT(
    DATE_ADD(CURDATE(), INTERVAL 1 MONTH),
    '%Y-%m-01'
)
""".rstrip()

        elif time_range == "last_month":

            query += f"""
{connector}{date_column} >= DATE_FORMAT(
    DATE_SUB(CURDATE(), INTERVAL 1 MONTH),
    '%Y-%m-01'
)
AND {date_column} < DATE_FORMAT(
    CURDATE(),
    '%Y-%m-01'
)
""".rstrip()

        elif time_range == "this_year":

            query += f"""
{connector}{date_column} >= DATE_FORMAT(
    CURDATE(),
    '%Y-01-01'
)
AND {date_column} < DATE_FORMAT(
    DATE_ADD(CURDATE(), INTERVAL 1 YEAR),
    '%Y-01-01'
)
""".rstrip()

        elif time_range == "last_year":

            query += f"""
{connector}{date_column} >= DATE_FORMAT(
    DATE_SUB(CURDATE(), INTERVAL 1 YEAR),
    '%Y-01-01'
)
AND {date_column} < DATE_FORMAT(
    CURDATE(),
    '%Y-01-01'
)
""".rstrip()

        return query