from app.intent import UserIntent
from app.schema_reader import get_database_schema
import re


class IntentParser:

    def __init__(self, schema=None):
        self.schema = schema or get_database_schema()

    def parse(self, question):

        question_lower = question.lower().strip()

        action = None
        entities = []
        filters = []
        conditions = []
        aggregation = None
        ranking = None
        ranking_criteria = None
        time_range = None
        comparisons = []
        comparison_criteria = None
        references = []
        reference_target = None
        scope = None

        # --------------------------------------------------
        # ACTION DETECTION
        # --------------------------------------------------

        ranking_words = [
            "best",
            "top",
            "highest",
            "lowest",
            "maximum",
            "minimum",
            "most",
            "least",
            "largest",
            "smallest"
        ]

        if any(
            re.search(rf"\b{re.escape(word)}\b", question_lower)
            for word in ranking_words
        ):
            action = "ranking"
            ranking = "best"

        elif any(
            re.search(rf"\b{re.escape(word)}\b", question_lower)
            for word in ["average", "avg", "mean"]
        ):
            action = "aggregation"
            aggregation = "average"

        elif any(
            re.search(rf"\b{re.escape(word)}\b", question_lower)
            for word in ["total", "sum"]
        ):
            action = "aggregation"
            aggregation = "total"

        elif (
            "count" in question_lower
            or "number of" in question_lower
            or "how many" in question_lower
        ):
            action = "aggregation"
            aggregation = "count"

        elif any(
            re.search(rf"\b{re.escape(word)}\b", question_lower)
            for word in [
                "compare",
                "comparison",
                "difference",
                "versus",
                "vs"
            ]
        ):
            action = "comparison"

        elif any(
            re.search(rf"\b{re.escape(word)}\b", question_lower)
            for word in [
                "show",
                "list",
                "display",
                "find",
                "get"
            ]
        ):
            action = "retrieve"

        # --------------------------------------------------
        # RANKING CRITERIA
        # --------------------------------------------------

        if ranking:

            # Sales / spending / revenue
            if any(
                word in question_lower
                for word in [
                    "sales",
                    "revenue",
                    "amount",
                    "spending",
                    "spent",
                    "purchase value",
                    "money"
                ]
            ):
                ranking_criteria = "sales"

            # Price
            elif any(
                word in question_lower
                for word in [
                    "price",
                    "expensive",
                    "cost",
                    "cheapest",
                    "costliest"
                ]
            ):
                ranking_criteria = "price"

            # Age
            elif any(
                word in question_lower
                for word in [
                    "age",
                    "oldest",
                    "youngest",
                    "older",
                    "younger"
                ]
            ):
                ranking_criteria = "age"

            # Quantity
            elif any(
                word in question_lower
                for word in [
                    "quantity",
                    "units",
                    "sold",
                    "items sold",
                    "number sold"
                ]
            ):
                ranking_criteria = "quantity"

            # Number of orders
            elif any(
                phrase in question_lower
                for phrase in [
                    "number of orders",
                    "order count",
                    "most orders",
                    "least orders"
                ]
            ):
                ranking_criteria = "order_count"

        # --------------------------------------------------
        # TIME RANGE
        # --------------------------------------------------

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

        # --------------------------------------------------
        # COMPARISON
        # --------------------------------------------------

        if action == "comparison":

            if re.search(r"\bcustomer(s)?\b", question_lower):
                comparisons.append("customers")

            if re.search(r"\bproduct(s)?\b", question_lower):
                comparisons.append("products")

            if re.search(r"\border(s)?\b", question_lower):
                comparisons.append("orders")

            if "sales" in question_lower:
                comparisons.append("sales")

            # Comparison criteria
            if any(
                word in question_lower
                for word in [
                    "sales",
                    "revenue",
                    "spending",
                    "spent",
                    "amount"
                ]
            ):
                comparison_criteria = "sales"

            elif any(
                word in question_lower
                for word in [
                    "price",
                    "cost",
                    "expensive"
                ]
            ):
                comparison_criteria = "price"

            elif any(
                word in question_lower
                for word in [
                    "age",
                    "oldest",
                    "youngest"
                ]
            ):
                comparison_criteria = "age"

            elif any(
                word in question_lower
                for word in [
                    "quantity",
                    "units",
                    "sold"
                ]
            ):
                comparison_criteria = "quantity"

        # --------------------------------------------------
        # REFERENCES
        # --------------------------------------------------

        reference_words = [
            "his",
            "her",
            "their",
            "them",
            "that",
            "this",
            "those",
            "these",
            "it"
        ]

        for word in reference_words:

            pattern = rf"\b{re.escape(word)}\b"

            if re.search(pattern, question_lower):
                references.append(word)

        # Determine possible reference target

        if references:

            if re.search(r"\bcustomer(s)?\b", question_lower):
                reference_target = "customers"

            elif re.search(r"\bproduct(s)?\b", question_lower):
                reference_target = "products"

            elif re.search(r"\border(s)?\b", question_lower):
                reference_target = "orders"

            elif "sales" in question_lower:
                reference_target = "sales"

        # --------------------------------------------------
        # SCOPE
        # --------------------------------------------------

        if "sales" in question_lower:
            scope = "sales"

        elif re.search(r"\bcustomer(s)?\b", question_lower):
            scope = "customers"

        elif re.search(r"\bproduct(s)?\b", question_lower):
            scope = "products"

        elif re.search(r"\border(s)?\b", question_lower):
            scope = "orders"

        # --------------------------------------------------
        # TABLE / ENTITY DETECTION
        # --------------------------------------------------

        for table_name in self.schema.keys():

            table_words = table_name.lower().replace("_", " ")

            # Exact table name
            if re.search(
                rf"\b{re.escape(table_words)}\b",
                question_lower
            ):
                entities.append(table_name)

            else:
                # Singular form
                if table_words.endswith("s"):
                    singular = table_words[:-1]
                else:
                    singular = table_words

                if re.search(
                    rf"\b{re.escape(singular)}\b",
                    question_lower
                ):
                    entities.append(table_name)

        # --------------------------------------------------
        # COLUMN DETECTION
        # --------------------------------------------------

        schema_columns = []

        for table_name, table_data in self.schema.items():

            for column in table_data["columns"]:

                column_name = column["name"]

                column_text = column_name.lower().replace("_", " ")

                schema_columns.append({
                    "table": table_name,
                    "column": column_name,
                    "text": column_text
                })

                if re.search(
                    rf"\b{re.escape(column_text)}\b",
                    question_lower
                ):

                    entity = f"{table_name}.{column_name}"

                    if entity not in entities:
                        entities.append(entity)

        # --------------------------------------------------
        # SALES DETECTION
        # --------------------------------------------------

        if "sales" in question_lower:

            if "orders" not in entities:
                entities.append("orders")

            if "orders.total_amount" not in entities:
                entities.append("orders.total_amount")

        # --------------------------------------------------
        # SPECIAL RANKING DETECTION
        # --------------------------------------------------

        # "most expensive product"
        if (
            ranking
            and "expensive" in question_lower
            and "products" in entities
        ):
            ranking_criteria = "price"

        # "cheapest product"
        if (
            ranking
            and "cheapest" in question_lower
            and "products" in entities
        ):
            ranking_criteria = "price"

        # "oldest customer"
        if (
            ranking
            and "oldest" in question_lower
            and "customers" in entities
        ):
            ranking_criteria = "age"

        # "youngest customer"
        if (
            ranking
            and "youngest" in question_lower
            and "customers" in entities
        ):
            ranking_criteria = "age"

        # "product sold the most"
        if (
            ranking
            and "sold" in question_lower
            and "products" in entities
        ):
            ranking_criteria = "quantity"

        # --------------------------------------------------
        # NUMERIC CONDITIONS
        # --------------------------------------------------

        for item in schema_columns:

            column_text = item["text"]

            pattern = (
                rf"\b{re.escape(column_text)}\b\s+"
                rf"(above|greater than|more than|over|"
                rf"below|less than|under|equal to|equals?)\s+"
                rf"(\d+(?:\.\d+)?)"
            )

            match = re.search(
                pattern,
                question_lower
            )

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

        # --------------------------------------------------
        # REMOVE DUPLICATES
        # --------------------------------------------------

        entities = list(dict.fromkeys(entities))
        comparisons = list(dict.fromkeys(comparisons))
        references = list(dict.fromkeys(references))

        # --------------------------------------------------
        # RETURN INTENT
        # --------------------------------------------------

        intent = UserIntent(
            question=question,
            action=action,
            entities=entities,
            filters=filters,
            conditions=conditions,
            aggregation=aggregation,
            ranking=ranking,
            ranking_criteria=ranking_criteria,
            time_range=time_range,
            comparisons=comparisons,
            comparison_criteria=comparison_criteria,
            references=references,
            reference_target=reference_target,
            scope=scope
        )

        return intent