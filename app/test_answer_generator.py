from app.answer_generator import AnswerGenerator


generator = AnswerGenerator()


# Test 1: Average query
question = "What is the average order?"

analysis = {
    "row_count": 1,
    "data": [
        {
            "average_order_amount": 2500.50
        }
    ]
}

answer = generator.generate(question, analysis)

print("Test 1:")
print(answer)


# Test 2: Total query
question = "What is the total sales?"

analysis = {
    "row_count": 1,
    "data": [
        {
            "total_sales": 15000
        }
    ]
}

answer = generator.generate(question, analysis)

print("\nTest 2:")
print(answer)


# Test 3: Ranking query
question = "Who is the best customer?"

analysis = {
    "row_count": 3,
    "data": [
        {"customer_id": 1, "name": "A", "city": "Delhi"},
        {"customer_id": 2, "name": "B", "city": "Mumbai"},
        {"customer_id": 3, "name": "C", "city": "Jaipur"}
    ]
}

answer = generator.generate(question, analysis)

print("\nTest 3:")
print(answer)


# Test 4: No results
question = "Show products"

analysis = {
    "row_count": 0,
    "data": []
}

answer = generator.generate(question, analysis)

print("\nTest 4:")
print(answer)