from app.intent import UserIntent
from app.ambiguity_detector import AmbiguityDetector
from app.clarification_engine import ClarificationEngine


intent = UserIntent(
    question="Who is the best customer?",
    action="ranking",
    entities=["customer"],
    ranking="best"
)

detector = AmbiguityDetector(schema={})

ambiguities = detector.detect(intent)

engine = ClarificationEngine()

questions = engine.generate_questions(ambiguities)

print("User question:")
print("-", intent.question)

print("\nDetected ambiguities:")

for ambiguity in ambiguities:
    print("-", ambiguity)

print("\nClarification questions:")

for question in questions:
    print("-", question)