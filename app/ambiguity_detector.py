class AmbiguityDetector:

    def __init__(self, schema):
        self.schema = schema

    def detect(self, intent):
        ambiguities = []

        # Ranking ambiguity
        if intent.ranking and not intent.ranking_criteria:
            ambiguities.append(
                "Ranking criteria is not specified."
            )

        # Comparison ambiguity
        if intent.comparisons and not getattr(
            intent, "comparison_criteria", None
        ):
            ambiguities.append(
                "Comparison criteria is not specified."
            )

        # Time ambiguity
        if intent.time_range == "ambiguous":
            ambiguities.append(
                "Time range is not clearly specified."
            )

        # Reference ambiguity
        if intent.references and not getattr(
            intent, "reference_target", None
        ):
            ambiguities.append(
                "Reference is not clearly identified."
            )

        # Scope ambiguity
        if intent.scope == "ambiguous":
            ambiguities.append(
                "Scope of the query is not clearly specified."
            )

        return ambiguities