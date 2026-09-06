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