from app.sql_executor import SQLExecutor


executor = SQLExecutor()


sql = "SELECT * FROM products;"

data, error = executor.execute(sql)


if error:
    print("Error:", error)
else:
    print("Query executed successfully!")
    print("Results:")

    for row in data:
        print(row)