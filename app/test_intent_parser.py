from app.schema_reader import get_database_schema
from app.intent_parser import IntentParser


schema = get_database_schema()
parser = IntentParser(schema)

questions = [
    "Who is the best customer?",
    "What is the total sales?",
    "What is the average order?",
    "Show customers older than 20",
    "Show customers under 21",
    "Show products above 100",
    "Show orders below 500",
    "Which product is most expensive?",
    "Which product sold the most quantity?",
    "Who spent the most?",
    "Show all orders last month"
]

for question in questions:

    intent = parser.parse(question)

    print("\nQuestion:")
    print(question)

    print("Intent:")
    print(intent.to_dict())