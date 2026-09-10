class ResultAnalyzer:

    def analyze(self, data):
        """
        Analyze SQL execution results and create
        basic information for the final answer.
        """

        if data is None:
            return {
                "row_count": 0,
                "columns": [],
                "data": [],
                "summary": "No result was returned."
            }

        if len(data) == 0:
            return {
                "row_count": 0,
                "columns": [],
                "data": [],
                "summary": "The query returned no results."
            }

        columns = list(data[0].keys())

        return {
            "row_count": len(data),
            "columns": columns,
            "data": data,
            "summary": f"The query returned {len(data)} result(s)."
        }