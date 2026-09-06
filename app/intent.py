class UserIntent:
    def __init__(
        self,
        question,
        action=None,
        entities=None,
        filters=None,
        conditions=None,
        aggregation=None,
        ranking=None,
        time_range=None,
        comparisons=None,
        references=None,
        scope=None
    ):
        self.question = question
        self.action = action
        self.entities = entities or []
        self.filters = filters or []
        self.conditions = conditions or []
        self.aggregation = aggregation
        self.ranking = ranking
        self.time_range = time_range
        self.comparisons = comparisons or []
        self.references = references or []
        self.scope = scope

    def to_dict(self):
        return {
            "question": self.question,
            "action": self.action,
            "entities": self.entities,
            "filters": self.filters,
            "conditions": self.conditions,
            "aggregation": self.aggregation,
            "ranking": self.ranking,
            "time_range": self.time_range,
            "comparisons": self.comparisons,
            "references": self.references,
            "scope": self.scope
        }