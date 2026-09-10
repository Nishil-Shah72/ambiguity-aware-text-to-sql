from app.pipeline import TextToSQLPipeline


pipeline = TextToSQLPipeline()


# Test 1: Clear question
question = "Show all products"

result = pipeline.process(question)

print("Test 1:")
print(result)


# Test 2: Ambiguous question
question = "Who is the best customer?"

result = pipeline.process(question)

print("\nTest 2:")
print(result)