from app.intent import UserIntent
from app.ambiguity_detector import AmbiguityDetector


detector = AmbiguityDetector(schema={})


# Test 1: Ranking ambiguity
intent1 = UserIntent(
    question="Who is the best customer?",
    action="ranking",
    entities=["customer"],
    ranking="best"
)


# Test 2: Comparison ambiguity
intent2 = UserIntent(
    question="Compare the customers.",
    action="comparison",
    entities=["customer"],
    comparisons=["customer"]
)


# Test 3: Time ambiguity
intent3 = UserIntent(
    question="Show recent orders.",
    action="filter",
    entities=["orders"],
    time_range="ambiguous"
)


# Test 4: Reference ambiguity
intent4 = UserIntent(
    question="Show his orders.",
    action="show",
    entities=["orders"],
    references=["his"]
)


# Test 5: Scope ambiguity
intent5 = UserIntent(
    question="Show sales.",
    action="show",
    entities=["sales"],
    scope="ambiguous"
)


test_intents = [
    intent1,
    intent2,
    intent3,
    intent4,
    intent5
]


for number, intent in enumerate(test_intents, start=1):
    print(f"\nTest {number}: {intent.question}")

    ambiguities = detector.detect(intent)

    if ambiguities:
        for ambiguity in ambiguities:
            print("-", ambiguity)
    else:
        print("- No ambiguity detected.")