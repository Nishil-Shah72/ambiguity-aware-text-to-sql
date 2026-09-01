from app.intent_parser import IntentParser


parser = IntentParser()

questions = [
    "Show sales this year.",
    "Show orders last month.",
    "What were the sales in 2025?",
    "Show recent orders."
]

for question in questions:
    intent = parser.parse(question)

    print("\nQuestion:")
    print(question)

    print("Time Range:")
    print(intent.time_range)