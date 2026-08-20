from app.intent import UserIntent

intent = UserIntent(
    question="Who is the best customer?",
    action="ranking",
    entities=["customer"],
    ranking="best"
)

print(intent.to_dict())