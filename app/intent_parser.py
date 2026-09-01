from app.intent import UserIntent
from app.schema_reader import get_database_schema
import re


class IntentParser:

    def __init__(self, schema=None):
        self.schema = schema or get_database_schema()

    def parse(self, question):
        question_lower = question.lower()

        action = None
        entities = []
        ranking = None
        aggregation = None
        time_range = None
        conditions = []

        # -------------------------
        # Detect ranking
        # -------------------------
        if "best" in question_lower or "top" in question_lower:
            action = "ranking"
            ranking = "best"

        # -------------------------
        # Detect aggregation
        # -------------------------
        if "average" in question_lower:
            action = "aggregation"
            aggregation = "average"

        elif "total" in question_lower:
            action = "aggregation"
            aggregation = "total"

        # -------------------------
        # Detect time range
        # -------------------------
        if "today" in question_lower:
            time_range = "today"

        elif "yesterday" in question_lower:
            time_range = "yesterday"

        elif "last month" in question_lower:
            time_range = "last_month"

        elif "this month" in question_lower:
            time_range = "this_month"

        elif "last year" in question_lower:
            time_range = "last_year"

        elif "this year" in question_lower:
            time_range = "this_year"

        elif "recent" in question_lower:
            time_range = "ambiguous"

        # -------------------------
        # Detect entities from tables
        # -------------------------
        for table_name in self.schema.keys():

            table_words = table_name.lower().replace("_", " ")

            if re.search(r"\b" + re.escape(table_words) + r"\b", question_lower):
                entities.append(table_name)

            else:
                singular = table_words.rstrip("s")

                if re.search(
                    r"\b" + re.escape(singular) + r"\b",
                    question_lower
                ):
                    entities.append(table_name)

        # -------------------------
        # Detect columns from schema
        # -------------------------
        schema_columns = []

        for table_name, table_data in self.schema.items():

            for column in table_data["columns"]:

                column_name = column["name"].lower().replace("_", " ")

                schema_columns.append({
                    "table": table_name,
                    "column": column["name"],
                    "text": column_name
                })

                # FIX:
                # Use word boundaries so "age" does not match
                # inside words such as "average".
                if re.search(
                    r"\b" + re.escape(column_name) + r"\b",
                    question_lower
                ):
                    entity = f"{table_name}.{column['name']}"

                    if entity not in entities:
                        entities.append(entity)

        # -------------------------
        # Business concept: sales
        # -------------------------
        if re.search(r"\bsales\b", question_lower):

            if "orders" not in entities:
                entities.append("orders")

            if "orders.total_amount" not in entities:
                entities.append("orders.total_amount")

        # -------------------------
        # Detect conditions
        # -------------------------
        for item in schema_columns:

            column_text = item["text"]

            # Examples:
            # price above 1000
            # age greater than 18
            # total amount below 5000

            pattern = (
                rf"\b{re.escape(column_text)}\b\s+"
                r"(above|greater than|more than|over|below|less than|"
                r"under|equal to|equals?)\s+"
                r"(\d+(?:\.\d+)?)"
            )

            match = re.search(pattern, question_lower)

            if match:

                operator_word = match.group(1)
                value = match.group(2)

                if operator_word in [
                    "above",
                    "greater than",
                    "more than",
                    "over"
                ]:
                    operator = ">"

                elif operator_word in [
                    "below",
                    "less than",
                    "under"
                ]:
                    operator = "<"

                else:
                    operator = "="

                conditions.append({
                    "column": f"{item['table']}.{item['column']}",
                    "operator": operator,
                    "value": value
                })

        # -------------------------
        # Remove duplicate entities
        # -------------------------
        entities = list(dict.fromkeys(entities))

        # -------------------------
        # Return structured intent
        # -------------------------
        return UserIntent(
            question=question,
            action=action,
            entities=entities,
            conditions=conditions,
            ranking=ranking,
            aggregation=aggregation,
            time_range=time_range
        )