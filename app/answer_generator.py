class AnswerGenerator:

    def generate(self, question, analysis):
        """
        Convert query analysis into a natural language answer.
        """

        if not analysis:
            return "No result was found."

        row_count = analysis.get("row_count", 0)
        data = analysis.get("data", [])

        if row_count == 0:
            return "No matching records were found."

        question_lower = question.lower()

        # Average queries
        if "average" in question_lower:
            if data:
                value = next(iter(data[0].values()))
                return f"The average value is {value}."

        # Total queries
        if "total" in question_lower:
            if data:
                value = next(iter(data[0].values()))
                return f"The total is {value}."

        # Ranking queries
        if "best" in question_lower or "top" in question_lower:
            return f"The query found {row_count} top result(s)."

        # General queries
        if row_count == 1:
            return f"The query returned 1 result: {data[0]}"

        return f"The query returned {row_count} result(s)."