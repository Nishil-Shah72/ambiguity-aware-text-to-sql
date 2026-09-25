class SQLGenerator:

    def __init__(self, schema):
        self.schema = schema

    def generate(self, intent):
        """
        Convert UserIntent into a SQL query.
        """

        # -------------------------------------------------
        # 1. Ranking queries
        # -------------------------------------------------
        if intent.action == "ranking":

            # ---------------------------------------------
            # Customer ranking
            # ---------------------------------------------
            if "customers" in intent.entities:

                # Rank customers by total spending
                if intent.ranking_criteria in ["total_spending", "sales"]:
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

                # Rank customers by number of orders
                if intent.ranking_criteria == "order_count":
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

                # Rank customers by age
                if intent.ranking_criteria == "age":
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
    customer_id,
    name,
    city,
    age
FROM customers
ORDER BY customer_id DESC
LIMIT 10;
""".strip()

            # ---------------------------------------------
            # Product ranking
            # ---------------------------------------------
            if "products" in intent.entities:

                # Most expensive products
                if intent.ranking_criteria == "price":
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

                # Best-selling products by quantity
                if intent.ranking_criteria == "quantity":
                    return """
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    COALESCE(SUM(oi.quantity), 0) AS total_quantity
FROM products p
LEFT JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.price
ORDER BY total_quantity DESC
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

            # ---------------------------------------------
            # Order ranking
            # ---------------------------------------------
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

        # -------------------------------------------------
        # 2. Average queries
        # -------------------------------------------------
        if intent.action == "aggregation" and intent.aggregation == "average":

            if "orders" in intent.entities:
                return """
SELECT
    AVG(total_amount) AS average_order_amount
FROM orders;
""".strip()

            if "products" in intent.entities:
                return """
SELECT
    AVG(price) AS average_product_price
FROM products;
""".strip()

            if "customers.age" in intent.entities:
                return """
SELECT
    AVG(age) AS average_age
FROM customers;
""".strip()

        # -------------------------------------------------
        # 3. Total / SUM queries
        # -------------------------------------------------
        if intent.action == "aggregation" and intent.aggregation == "total":

            if "orders.total_amount" in intent.entities:
                return """
SELECT
    SUM(total_amount) AS total_sales
FROM orders;
""".strip()

            if "orders" in intent.entities:
                return """
SELECT
    SUM(total_amount) AS total_sales
FROM orders;
""".strip()

        # -------------------------------------------------
        # 4. Count queries
        # -------------------------------------------------
        if intent.action == "aggregation" and intent.aggregation == "count":

            if "customers" in intent.entities:
                return """
SELECT
    COUNT(*) AS customer_count
FROM customers;
""".strip()

            if "orders" in intent.entities:
                return """
SELECT
    COUNT(*) AS order_count
FROM orders;
""".strip()

            if "products" in intent.entities:
                return """
SELECT
    COUNT(*) AS product_count
FROM products;
""".strip()

        # -------------------------------------------------
        # 5. Condition-based queries
        # -------------------------------------------------
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

                return f"""
SELECT *
FROM {table}
WHERE {where_clause};
""".strip()

        # -------------------------------------------------
        # 6. Simple entity queries
        # -------------------------------------------------
        if "customers" in intent.entities:
            return """
SELECT *
FROM customers;
""".strip()

        if "orders" in intent.entities:
            return """
SELECT *
FROM orders;
""".strip()

        if "products" in intent.entities:
            return """
SELECT *
FROM products;
""".strip()

        # -------------------------------------------------
        # 7. No suitable SQL found
        # -------------------------------------------------
        return None