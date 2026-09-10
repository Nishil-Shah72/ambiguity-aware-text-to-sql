import re


class SQLValidator:

    def validate(self, sql):
        """
        Validate generated SQL before execution.

        Only SELECT queries are allowed.
        """

        if not sql:
            return False, "SQL query is empty."

        # Remove leading/trailing whitespace
        sql = sql.strip()

        # Remove trailing semicolon for checking
        sql_without_semicolon = sql.rstrip(";").strip()

        # -------------------------
        # 1. Only SELECT is allowed
        # -------------------------
        if not re.match(r"^SELECT\b", sql_without_semicolon, re.IGNORECASE):
            return False, "Only SELECT queries are allowed."

        # -------------------------
        # 2. Block dangerous SQL keywords
        # -------------------------
        forbidden_keywords = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "ALTER",
            "TRUNCATE",
            "CREATE",
            "REPLACE",
            "GRANT",
            "REVOKE"
        ]

        for keyword in forbidden_keywords:
            pattern = rf"\b{keyword}\b"

            if re.search(pattern, sql_without_semicolon, re.IGNORECASE):
                return False, f"Forbidden SQL operation detected: {keyword}"

        # -------------------------
        # 3. Block multiple statements
        # -------------------------
        if ";" in sql_without_semicolon:
            return False, "Multiple SQL statements are not allowed."

        # -------------------------
        # 4. Basic SQL structure check
        # -------------------------
        if not re.search(r"\bFROM\b", sql_without_semicolon, re.IGNORECASE):
            return False, "SQL query must contain a FROM clause."

        return True, "SQL query is valid."