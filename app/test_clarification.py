from app.clarification_engine import ClarificationEngine


engine = ClarificationEngine()

ambiguities = [
    "Ranking criteria is not specified.",
    "Comparison criteria is not specified.",
    "Time range is not clearly specified.",
    "Reference is not clearly identified.",
    "Scope of the query is not clearly specified."
]

questions = engine.generate_questions(ambiguities)

print("Clarification questions:")

for question in questions:
    print("-", question)