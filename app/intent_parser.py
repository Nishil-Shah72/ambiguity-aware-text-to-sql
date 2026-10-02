import re

from app.intent import UserIntent


class IntentParser:

    def __init__(self, schema):
        self.schema = schema

    def parse(self, question):

        question_lower = question.lower()

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

        # ==================================================
        # ACTION DETECTION
        # ==================================================

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
            re.search(
                rf"\b{re.escape(word)}\b",
                question_lower
            )
            for word in ranking_words
        ):
            action = "ranking"
            ranking = "best"

        elif any(
            word in question_lower
            for word in [
                "average",
                "mean"
            ]
        ):
            action = "aggregation"
            aggregation = "average"

        elif any(
            word in question_lower
            for word in [
                "total",
                "sum"
            ]
        ):
            action = "aggregation"
            aggregation = "total"

        elif any(
            word in question_lower
            for word in [
                "count",
                "number of"
            ]
        ):
            action = "aggregation"
            aggregation = "count"

        elif any(
            word in question_lower
            for word in [
                "compare",
                "comparison",
                "difference",
                "versus",
                "vs"
            ]
        ):
            action = "comparison"
            comparisons.append("comparison")

        elif any(
            word in question_lower
            for word in [
                "show",
                "list",
                "find",
                "get",
                "display"
            ]
        ):
            action = "retrieve"

        # ==================================================
        # ENTITY / TABLE DETECTION
        # ==================================================

        # schema_reader returns:
        #
        # {
        #     "customers": {...},
        #     "orders": {...},
        #     "products": {...},
        #     "order_items": {...}
        # }

        schema_tables = self.schema

        for table_name in schema_tables:

            if re.search(
                rf"\b{re.escape(table_name.lower())}\b",
                question_lower
            ):
                entities.append(table_name)

        # Singular forms

        singular_to_plural = {
            "customer": "customers",
            "order": "orders",
            "product": "products"
        }

        for singular, plural in singular_to_plural.items():

            if (
                re.search(
                    rf"\b{re.escape(singular)}\b",
                    question_lower
                )
                and plural in schema_tables
                and plural not in entities
            ):
                entities.append(plural)

        # ==================================================
        # COLUMN DETECTION
        # ==================================================

        for table_name, table_info in schema_tables.items():

            columns = table_info.get("columns", [])

            for column_info in columns:

                # schema_reader returns dictionaries
                # such as {"name": "age", "type": "INTEGER"}

                column_name = column_info.get("name")

                if not column_name:
                    continue

                if re.search(
                    rf"\b{re.escape(column_name.lower())}\b",
                    question_lower
                ):

                    qualified_column = (
                        f"{table_name}.{column_name}"
                    )

                    if qualified_column not in entities:
                        entities.append(qualified_column)

        # ==================================================
        # SCOPE DETECTION
        # ==================================================

        if "sales" in question_lower:
            scope = "sales"

        elif "customers" in entities:
            scope = "customers"

        elif "orders" in entities:
            scope = "orders"

        elif "products" in entities:
            scope = "products"

        # ==================================================
        # SALES DETECTION
        # ==================================================

        if (
            "sales" in question_lower
            and aggregation is None
            and action != "ranking"
        ):
            action = "aggregation"
            aggregation = "total"
            scope = "sales"

        # ==================================================
        # RANKING CRITERIA
        # ==================================================

        if action == "ranking":

            # Customer spending / sales

            if any(
                word in question_lower
                for word in [
                    "spending",
                    "spent",
                    "revenue",
                    "sales",
                    "money"
                ]
            ):
                ranking_criteria = "total_spending"

            # Product price

            elif (
                "most expensive" in question_lower
                or "highest price" in question_lower
                or "highest priced" in question_lower
            ):
                ranking_criteria = "price"

            elif (
                "cheapest" in question_lower
                or "lowest price" in question_lower
                or "lowest priced" in question_lower
            ):
                ranking_criteria = "price"

            # Customer age

            elif (
                "oldest customer" in question_lower
                or "oldest customers" in question_lower
            ):
                ranking_criteria = "age"

            elif (
                "youngest customer" in question_lower
                or "youngest customers" in question_lower
            ):
                ranking_criteria = "age"

            # Order count

            elif (
                "order count" in question_lower
                or "number of orders" in question_lower
                or "most orders" in question_lower
            ):
                ranking_criteria = "order_count"

            # Quantity sold

            elif (
                "quantity" in question_lower
                or "units" in question_lower
                or "sold the most" in question_lower
            ):
                ranking_criteria = "quantity"

        # ==================================================
        # TIME RANGE DETECTION
        # ==================================================

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

        elif any(
            phrase in question_lower
            for phrase in [
                "recent",
                "recently"
            ]
        ):
            time_range = "ambiguous"

        # ==================================================
        # COMPARISON CRITERIA
        # ==================================================

        if action == "comparison":

            if "sales" in question_lower:
                comparison_criteria = "sales"

            elif "price" in question_lower:
                comparison_criteria = "price"

            elif "age" in question_lower:
                comparison_criteria = "age"

            elif "quantity" in question_lower:
                comparison_criteria = "quantity"

            elif "orders" in question_lower:
                comparison_criteria = "orders"

        # ==================================================
        # REFERENCE DETECTION
        # ==================================================

        reference_words = [
            "they",
            "them",
            "their",
            "that customer",
            "that product",
            "that order",
            "this customer",
            "this product",
            "this order"
        ]

        for word in reference_words:

            if word in question_lower:

                references.append(word)

                if "customer" in word:
                    reference_target = "customer"

                elif "product" in word:
                    reference_target = "product"

                elif "order" in word:
                    reference_target = "order"

                else:
                    reference_target = "unknown"

                break

        # ==================================================
        # NUMERIC CONDITIONS
        # ==================================================

        conditions.extend(
            self._detect_numeric_conditions(
                question_lower,
                entities
            )
        )

        # ==================================================
        # RETURN INTENT
        # ==================================================

        return UserIntent(
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

    # ======================================================
    # NUMERIC CONDITION DETECTION
    # ======================================================

    def _detect_numeric_conditions(
        self,
        question_lower,
        entities
    ):

        conditions = []

        # ==================================================
        # AGE CONDITIONS
        # ==================================================

        age_patterns = [
            (
                r"\bolder than\s+(\d+)",
                ">"
            ),
            (
                r"\babove\s+(\d+)\s*(?:years?\s*old)?",
                ">"
            ),
            (
                r"\bgreater than\s+(\d+)\s*(?:years?\s*old)?",
                ">"
            ),
            (
                r"\bat least\s+(\d+)\s*(?:years?\s*old)?",
                ">="
            ),
            (
                r"\byounger than\s+(\d+)",
                "<"
            ),
            (
                r"\bunder\s+(\d+)\s*(?:years?\s*old)?",
                "<"
            ),
            (
                r"\bbelow\s+(\d+)\s*(?:years?\s*old)?",
                "<"
            ),
            (
                r"\bless than\s+(\d+)\s*(?:years?\s*old)?",
                "<"
            ),
            (
                r"\bat most\s+(\d+)\s*(?:years?\s*old)?",
                "<="
            )
        ]

        for pattern, operator in age_patterns:

            match = re.search(
                pattern,
                question_lower
            )

            if match and (
                "customers" in entities
                or "customer" in question_lower
            ):

                conditions.append(
                    {
                        "column": "customers.age",
                        "operator": operator,
                        "value": match.group(1)
                    }
                )

                break

        # ==================================================
        # PRODUCT PRICE CONDITIONS
        # ==================================================

        price_patterns = [
            (
                r"\bprice\s+(?:above|over|greater than)\s+(\d+(?:\.\d+)?)",
                ">"
            ),
            (
                r"\bprice\s+(?:below|under|less than)\s+(\d+(?:\.\d+)?)",
                "<"
            ),
            (
                r"\bprice\s+(?:at least)\s+(\d+(?:\.\d+)?)",
                ">="
            ),
            (
                r"\bprice\s+(?:at most)\s+(\d+(?:\.\d+)?)",
                "<="
            )
        ]

        for pattern, operator in price_patterns:

            match = re.search(
                pattern,
                question_lower
            )

            if match and "products" in entities:

                conditions.append(
                    {
                        "column": "products.price",
                        "operator": operator,
                        "value": match.group(1)
                    }
                )

                break

        # Handle:
        # "Show products above 100"
        # "Show products below 500"

        if "products" in entities:

            product_price_patterns = [
                (
                    r"\babove\s+(\d+(?:\.\d+)?)",
                    ">"
                ),
                (
                    r"\bover\s+(\d+(?:\.\d+)?)",
                    ">"
                ),
                (
                    r"\bbelow\s+(\d+(?:\.\d+)?)",
                    "<"
                ),
                (
                    r"\bunder\s+(\d+(?:\.\d+)?)",
                    "<"
                )
            ]

            for pattern, operator in product_price_patterns:

                match = re.search(
                    pattern,
                    question_lower
                )

                if match:

                    conditions.append(
                        {
                            "column": "products.price",
                            "operator": operator,
                            "value": match.group(1)
                        }
                    )

                    break

        # ==================================================
        # ORDER AMOUNT CONDITIONS
        # ==================================================

        amount_patterns = [
            (
                r"(?:order|orders|amount|total)\s+(?:above|over|greater than)\s+(\d+(?:\.\d+)?)",
                ">"
            ),
            (
                r"(?:order|orders|amount|total)\s+(?:below|under|less than)\s+(\d+(?:\.\d+)?)",
                "<"
            ),
            (
                r"(?:order|orders|amount|total)\s+(?:at least)\s+(\d+(?:\.\d+)?)",
                ">="
            ),
            (
                r"(?:order|orders|amount|total)\s+(?:at most)\s+(\d+(?:\.\d+)?)",
                "<="
            )
        ]

        for pattern, operator in amount_patterns:

            match = re.search(
                pattern,
                question_lower
            )

            if match and "orders" in entities:

                conditions.append(
                    {
                        "column": "orders.total_amount",
                        "operator": operator,
                        "value": match.group(1)
                    }
                )

                break

        # Handle:
        # "Show orders below 500"
        # "Show orders above 1000"

        if "orders" in entities:

            order_amount_patterns = [
                (
                    r"\babove\s+(\d+(?:\.\d+)?)",
                    ">"
                ),
                (
                    r"\bover\s+(\d+(?:\.\d+)?)",
                    ">"
                ),
                (
                    r"\bbelow\s+(\d+(?:\.\d+)?)",
                    "<"
                ),
                (
                    r"\bunder\s+(\d+(?:\.\d+)?)",
                    "<"
                )
            ]

            for pattern, operator in order_amount_patterns:

                match = re.search(
                    pattern,
                    question_lower
                )

                if match:

                    conditions.append(
                        {
                            "column": "orders.total_amount",
                            "operator": operator,
                            "value": match.group(1)
                        }
                    )

                    break

        return conditions