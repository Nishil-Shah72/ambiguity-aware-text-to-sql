class ClarificationEngine:

    def generate_questions(self, ambiguities):
        questions = []

        for ambiguity in ambiguities:

            if ambiguity == "Ranking criteria is not specified.":
                questions.append(
                    "What should the ranking be based on?"
                )

            elif ambiguity == "Comparison criteria is not specified.":
                questions.append(
                    "What should the comparison be based on?"
                )

            elif ambiguity == "Time range is not clearly specified.":
                questions.append(
                    "What time period should be considered?"
                )

            elif ambiguity == "Reference is not clearly identified.":
                questions.append(
                    "Who or what does the reference refer to?"
                )

            elif ambiguity == "Scope of the query is not clearly specified.":
                questions.append(
                    "What scope should be considered?"
                )

        return questions

    def apply_clarification(self, intent, ambiguity, answer):
        """
        Apply the user's clarification answer to the existing intent.
        """

        answer = answer.strip().lower()

        # -------------------------
        # Ranking clarification
        # -------------------------
        if ambiguity == "Ranking criteria is not specified.":

            if any(word in answer for word in [
                "spending",
                "spent",
                "amount",
                "sales",
                "revenue",
                "money"
            ]):
                intent.ranking_criteria = "total_spending"

            elif any(word in answer for word in [
                "orders",
                "number of orders",
                "order count"
            ]):
                intent.ranking_criteria = "order_count"

            elif any(word in answer for word in [
                "visits",
                "visit count"
            ]):
                intent.ranking_criteria = "visit_count"

            elif "age" in answer:
                intent.ranking_criteria = "age"

            elif any(word in answer for word in [
                "price",
                "cost"
            ]):
                intent.ranking_criteria = "price"

            elif any(word in answer for word in [
                "quantity",
                "units"
            ]):
                intent.ranking_criteria = "quantity"

            else:
                intent.ranking_criteria = answer

        # -------------------------
        # Comparison clarification
        # -------------------------
        elif ambiguity == "Comparison criteria is not specified.":

            intent.comparison_criteria = answer

        # -------------------------
        # Time clarification
        # -------------------------
        elif ambiguity == "Time range is not clearly specified.":

            if "today" in answer:
                intent.time_range = "today"

            elif "yesterday" in answer:
                intent.time_range = "yesterday"

            elif "this week" in answer:
                intent.time_range = "this_week"

            elif "last week" in answer:
                intent.time_range = "last_week"

            elif "this month" in answer:
                intent.time_range = "this_month"

            elif "last month" in answer:
                intent.time_range = "last_month"

            elif "this year" in answer:
                intent.time_range = "this_year"

            elif "last year" in answer:
                intent.time_range = "last_year"

            else:
                intent.time_range = answer

        # -------------------------
        # Reference clarification
        # -------------------------
        elif ambiguity == "Reference is not clearly identified.":

            intent.reference_target = answer

        # -------------------------
        # Scope clarification
        # -------------------------
        elif ambiguity == "Scope of the query is not clearly specified.":

            intent.scope = answer

        return intent