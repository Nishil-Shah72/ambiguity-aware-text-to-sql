from app.sql_validator import SQLValidator


validator = SQLValidator()


queries = [
    "SELECT * FROM customers;",
    "SELECT AVG(price) FROM products;",
    "DROP TABLE customers;",
    "DELETE FROM orders;",
    "UPDATE customers SET age = 20;",
]


for query in queries:

    is_valid, message = validator.validate(query)

    print("\nSQL:", query)
    print("Valid:", is_valid)
    print("Message:", message)