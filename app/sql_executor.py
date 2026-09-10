from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


class SQLExecutor:

    def __init__(self):

        database_url = URL.create(
            drivername="mysql+mysqlconnector",
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=int(DB_PORT),
            database=DB_NAME
        )

        self.engine = create_engine(database_url)

    def execute(self, sql):
        """
        Execute a validated SQL SELECT query
        and return the results.
        """

        if not sql:
            return None, "SQL query is empty."

        # Security check
        if not sql.strip().lower().startswith("select"):
            return None, "Only SELECT queries are allowed."

        try:
            with self.engine.connect() as connection:

                result = connection.execute(text(sql))

                rows = result.fetchall()
                columns = result.keys()

                data = [
                    dict(zip(columns, row))
                    for row in rows
                ]

                return data, None

        except Exception as e:
            return None, str(e)