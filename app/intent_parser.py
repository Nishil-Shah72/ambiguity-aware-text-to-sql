from app.intent import UserIntent


class IntentParser:

    def parse(self, question):
        question_lower = question.lower()

        action = None
        entities = []
        ranking = None
        aggregation = None

        # Detect ranking
        if "best" in question_lower or "top" in question_lower:
            action = "ranking"
            ranking = "best"

        # Detect aggregation
        if "average" in question_lower:
            aggregation = "average"

        elif "total" in question_lower:
            aggregation = "total"

        # Basic entity detection
        possible_entities = [
            "customer",
            "customers",
            "student",
            "students",
            "order",
            "orders",
            "product",
            "products",
            "sales"
        ]

        for entity in possible_entities:
            if entity in question_lower:
                entities.append(entity)

        return UserIntent(
            question=question,
            action=action,
            entities=entities,
            ranking=ranking,
            aggregation=aggregation
        )