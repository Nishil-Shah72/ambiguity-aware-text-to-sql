from app.intent_parser import IntentParser


parser = IntentParser()

questions = [
    "Who is the best customer?",
    "What is the total sales?",
    "What is the average order?"
]

for question in questions:
    intent = parser.parse(question)

    print("\nQuestion:")
    print(question)

    print("Intent:")
    print(intent.to_dict())