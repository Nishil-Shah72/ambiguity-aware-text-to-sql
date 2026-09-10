class SQLGenerator:

    def __init__(self, schema):
        self.schema = schema

    def generate(self, intent):
        """
        Convert UserIntent into a SQL query.
        """

        # -------------------------
        # 1. Ranking queries
        # -------------------------
        if intent.action == "ranking":

            if "customers" in intent.entities:
                return """
SELECT customer_id, name, city, age
FROM customers
ORDER BY customer_id DESC
LIMIT 10;
""".strip()

            if "products" in intent.entities:
                return """
SELECT product_id, product_name, category, price
FROM products
ORDER BY price DESC
LIMIT 10;
""".strip()

            if "orders" in intent.entities:
                return """
SELECT order_id, customer_id, order_date, total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 10;
""".strip()

        # -------------------------
        # 2. Average queries
        # -------------------------
        if intent.action == "aggregation" and intent.aggregation == "average":

            if "orders" in intent.entities:
                return """
SELECT AVG(total_amount) AS average_order_amount
FROM orders;
""".strip()

            if "products" in intent.entities:
                return """
SELECT AVG(price) AS average_product_price
FROM products;
""".strip()

            if "customers.age" in intent.entities:
                return """
SELECT AVG(age) AS average_age
FROM customers;
""".strip()

        # -------------------------
        # 3. Total / SUM queries
        # -------------------------
        if intent.action == "aggregation" and intent.aggregation == "total":

            if "orders.total_amount" in intent.entities:
                return """
SELECT SUM(total_amount) AS total_sales
FROM orders;
""".strip()

            if "orders" in intent.entities:
                return """
SELECT SUM(total_amount) AS total_sales
FROM orders;
""".strip()

        # -------------------------
        # 4. Condition-based queries
        # -------------------------
        if intent.conditions:

            # Currently supports conditions on known columns
            condition_parts = []

            for condition in intent.conditions:
                column = condition["column"]
                operator = condition["operator"]
                value = condition["value"]

                condition_parts.append(
                    f"{column} {operator} {value}"
                )

            where_clause = " AND ".join(condition_parts)

            # Determine table
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

        # -------------------------
        # 5. Simple entity queries
        # -------------------------
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

        # -------------------------
        # 6. No suitable SQL found
        # -------------------------
        return None