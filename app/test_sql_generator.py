from app.sql_generator import SQLGenerator
from app.schema_reader import get_database_schema
from app.intent_parser import IntentParser


schema = get_database_schema()

generator = SQLGenerator(schema)
parser = IntentParser(schema)


questions = [
    "Who is the best customer?",
    "What is the average order?",
    "What is the total sales?",
    "Show all products",
    "Show all orders",
]


for question in questions:

    intent = parser.parse(question)
    sql = generator.generate(intent)

    print("\nQuestion:", question)
    print("Intent:", intent.to_dict())
    print("SQL:", sql)