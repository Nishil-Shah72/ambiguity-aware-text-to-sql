class SQLGenerator:

    def __init__(self, schema):
        self.schema = schema

    def generate(self, intent):
        """
        Convert UserIntent into a SQL query.

        Supports:
        - Retrieval
        - Ranking
        - Aggregation
        - Numeric conditions
        - Time ranges
        - Customer spending/order ranking
        - Product price/quantity/sales ranking
        """

        # ============================================================
        # 1. RANKING QUERIES
        # ============================================================

        if intent.action == "ranking":

            # --------------------------------------------------------
            # CUSTOMER RANKING
            # --------------------------------------------------------

            if "customers" in intent.entities:

                criteria = intent.ranking_criteria

                # Customer ranking by total spending
                if criteria == "total_spending" or criteria == "sales":

                    return """
SELECT
    c.customer_id,
    c.name,
    c.city,
    c.age,
    COALESCE(SUM(o.total_amount), 0) AS total_spending
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name,
    c.city,
    c.age
ORDER BY total_spending DESC
LIMIT 10;
""".strip()

                # Customer ranking by number of orders
                if criteria == "order_count" or criteria == "quantity":

                    return """
SELECT
    c.customer_id,
    c.name,
    c.city,
    c.age,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name,
    c.city,
    c.age
ORDER BY order_count DESC
LIMIT 10;
""".strip()

                # Customer ranking by age
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
                return """
SELECT
    c.customer_id,
    c.name,
    c.city,
    c.age,
    COALESCE(SUM(o.total_amount), 0) AS total_spending
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name,
    c.city,
    c.age
ORDER BY total_spending DESC
LIMIT 10;
""".strip()

            # --------------------------------------------------------
            # PRODUCT RANKING
            # --------------------------------------------------------

            if "products" in intent.entities:

                criteria = intent.ranking_criteria

                # Product ranking by price
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

                # Product ranking by quantity sold
                if criteria == "quantity":

                    return """
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    COALESCE(SUM(oi.quantity), 0) AS quantity_sold
FROM products p
LEFT JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.price
ORDER BY quantity_sold DESC
LIMIT 10;
""".strip()

                # Product ranking by sales/revenue
                if criteria in ["sales", "revenue", "total_spending"]:

                    return """
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    COALESCE(SUM(oi.quantity * p.price), 0) AS total_sales
FROM products p
LEFT JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.price
ORDER BY total_sales DESC
LIMIT 10;
""".strip()

                # Default product ranking
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

            # --------------------------------------------------------
            # ORDER RANKING
            # --------------------------------------------------------

            if "orders" in intent.entities:

                return """
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 10;
""".strip()

        # ============================================================
        # 2. AGGREGATION QUERIES
        # ============================================================

        if intent.action == "aggregation":

            # --------------------------------------------------------
            # AVERAGE
            # --------------------------------------------------------

            if intent.aggregation == "average":

                if "orders" in intent.entities:

                    query = """
SELECT AVG(total_amount) AS average_order_amount
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
SELECT AVG(price) AS average_product_price
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
SELECT AVG(age) AS average_age
FROM customers;
""".strip()

            # --------------------------------------------------------
            # TOTAL / SUM
            # --------------------------------------------------------

            if intent.aggregation == "total":

                if (
                    "orders.total_amount" in intent.entities
                    or "orders" in intent.entities
                    or intent.scope == "sales"
                ):

                    query = """
SELECT SUM(total_amount) AS total_sales
FROM orders
""".strip()

                    query = self._apply_time_range(
                        query,
                        "order_date",
                        intent.time_range
                    )

                    query += ";"

                    return query

            # --------------------------------------------------------
            # COUNT
            # --------------------------------------------------------

            if intent.aggregation == "count":

                if "customers" in intent.entities:

                    return """
SELECT COUNT(*) AS customer_count
FROM customers;
""".strip()

                if "products" in intent.entities:

                    return """
SELECT COUNT(*) AS product_count
FROM products;
""".strip()

                if "orders" in intent.entities:

                    query = """
SELECT COUNT(*) AS order_count
FROM orders
""".strip()

                    query = self._apply_time_range(
                        query,
                        "order_date",
                        intent.time_range
                    )

                    query += ";"

                    return query

        # ============================================================
        # 3. NUMERIC CONDITION QUERIES
        # ============================================================

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

                query = self._apply_time_range(
                    query,
                    "order_date",
                    intent.time_range
                )

                query += ";"

                return query

        # ============================================================
        # 4. ORDER QUERIES WITH TIME RANGE
        # ============================================================

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

        # ============================================================
        # 5. CUSTOMER RETRIEVAL
        # ============================================================

        if "customers" in intent.entities:

            return """
SELECT *
FROM customers;
""".strip()

        # ============================================================
        # 6. PRODUCT RETRIEVAL
        # ============================================================

        if "products" in intent.entities:

            return """
SELECT *
FROM products;
""".strip()

        # ============================================================
        # 7. FALLBACK
        # ============================================================

        return None

    # ================================================================
    # TIME RANGE HELPER
    # ================================================================

    def _apply_time_range(self, query, date_column, time_range):

        if not time_range:
            return query

        # ------------------------------------------------------------
        # TODAY
        # ------------------------------------------------------------

        if time_range == "today":

            query += f"""
WHERE DATE({date_column}) = CURDATE()
""".rstrip()

        # ------------------------------------------------------------
        # YESTERDAY
        # ------------------------------------------------------------

        elif time_range == "yesterday":

            query += f"""
WHERE DATE({date_column}) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
""".rstrip()

        # ------------------------------------------------------------
        # THIS WEEK
        # ------------------------------------------------------------

        elif time_range == "this_week":

            query += f"""
WHERE {date_column} >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY)
AND {date_column} < DATE_ADD(
    DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY),
    INTERVAL 7 DAY
)
""".rstrip()

        # ------------------------------------------------------------
        # LAST WEEK
        # ------------------------------------------------------------

        elif time_range == "last_week":

            query += f"""
WHERE {date_column} >= DATE_SUB(
    CURDATE(),
    INTERVAL (WEEKDAY(CURDATE()) + 7) DAY
)
AND {date_column} < DATE_SUB(
    CURDATE(),
    INTERVAL WEEKDAY(CURDATE()) DAY
)
""".rstrip()

        # ------------------------------------------------------------
        # THIS MONTH
        # ------------------------------------------------------------

        elif time_range == "this_month":

            query += f"""
WHERE {date_column} >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
AND {date_column} < DATE_FORMAT(
    DATE_ADD(CURDATE(), INTERVAL 1 MONTH),
    '%Y-%m-01'
)
""".rstrip()

        # ------------------------------------------------------------
        # LAST MONTH
        # ------------------------------------------------------------

        elif time_range == "last_month":

            query += f"""
WHERE {date_column} >= DATE_FORMAT(
    DATE_SUB(CURDATE(), INTERVAL 1 MONTH),
    '%Y-%m-01'
)
AND {date_column} < DATE_FORMAT(
    CURDATE(),
    '%Y-%m-01'
)
""".rstrip()

        # ------------------------------------------------------------
        # THIS YEAR
        # ------------------------------------------------------------

        elif time_range == "this_year":

            query += f"""
WHERE {date_column} >= DATE_FORMAT(CURDATE(), '%Y-01-01')
AND {date_column} < DATE_FORMAT(
    DATE_ADD(CURDATE(), INTERVAL 1 YEAR),
    '%Y-01-01'
)
""".rstrip()

        # ------------------------------------------------------------
        # LAST YEAR
        # ------------------------------------------------------------

        elif time_range == "last_year":

            query += f"""
WHERE {date_column} >= DATE_FORMAT(
    DATE_SUB(CURDATE(), INTERVAL 1 YEAR),
    '%Y-01-01'
)
AND {date_column} < DATE_FORMAT(
    CURDATE(),
    '%Y-01-01'
)
""".rstrip()

        return query