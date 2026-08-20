from app.intent import UserIntent
from app.ambiguity_detector import AmbiguityDetector


intent = UserIntent(
    question="Who is the best customer?",
    action="ranking",
    entities=["customer"],
    ranking="best"
)

detector = AmbiguityDetector(schema={})

ambiguities = detector.detect(intent)

print("Detected ambiguities:")

for ambiguity in ambiguities:
    print("-", ambiguity)