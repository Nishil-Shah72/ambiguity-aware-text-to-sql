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
        ranking_criteria=None,
        time_range=None,
        comparisons=None,
        comparison_criteria=None,
        references=None,
        reference_target=None,
        scope=None
    ):
        self.question = question
        self.action = action
        self.entities = entities or []
        self.filters = filters or []
        self.conditions = conditions or []
        self.aggregation = aggregation
        self.ranking = ranking
        self.ranking_criteria = ranking_criteria
        self.time_range = time_range
        self.comparisons = comparisons or []
        self.comparison_criteria = comparison_criteria
        self.references = references or []
        self.reference_target = reference_target
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
            "ranking_criteria": self.ranking_criteria,
            "time_range": self.time_range,
            "comparisons": self.comparisons,
            "comparison_criteria": self.comparison_criteria,
            "references": self.references,
            "reference_target": self.reference_target,
            "scope": self.scope
        }