class AmbiguityDetector:
    def __init__(self, schema):
        self.schema = schema

    def detect(self, intent):
        ambiguities = []

        if intent.ranking and not intent.aggregation:
            ambiguities.append(
                "Ranking criteria is not specified."
            )

        return ambiguities