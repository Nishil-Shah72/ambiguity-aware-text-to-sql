import re

from app.intent import UserIntent


class IntentParser:

    def parse(self, question):
        question_lower = question.lower()

        action = None
        entities = []
        filters = []
        conditions = []
        ranking = None
        aggregation = None
        time_range = None

        # Detect ranking
        if "best" in question_lower or "top" in question_lower:
            action = "ranking"
            ranking = "best"

        # Detect aggregation
        if "average" in question_lower:
            aggregation = "average"
            action = "aggregation"

        elif "total" in question_lower:
            aggregation = "total"
            action = "aggregation"

        # Detect basic conditions
        if "above" in question_lower:
            conditions.append("greater_than")

        elif "below" in question_lower:
            conditions.append("less_than")

        elif "more than" in question_lower:
            conditions.append("greater_than")

        elif "less than" in question_lower:
            conditions.append("less_than")

        # Detect basic filters
        if "from" in question_lower:
            filters.append("from")

        if "in" in question_lower:
            filters.append("in")

        # Detect relative time ranges
        if "today" in question_lower:
            time_range = "today"

        elif "yesterday" in question_lower:
            time_range = "yesterday"

        elif "this week" in question_lower:
            time_range = "this_week"

        elif "last week" in question_lower:
            time_range = "last_week"

        elif "this month" in question_lower:
            time_range = "this_month"

        elif "last month" in question_lower:
            time_range = "last_month"

        elif "this year" in question_lower:
            time_range = "this_year"

        elif "last year" in question_lower:
            time_range = "last_year"

        elif "recent" in question_lower:
            time_range = "ambiguous"

        # Detect specific four-digit years
        year_match = re.search(r"\b(19|20)\d{2}\b", question_lower)

        if year_match:
            time_range = year_match.group()

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
            filters=filters,
            conditions=conditions,
            ranking=ranking,
            aggregation=aggregation,
            time_range=time_range
        )