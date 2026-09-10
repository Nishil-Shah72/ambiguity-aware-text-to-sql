from sqlalchemy import inspect, create_engine
from sqlalchemy.engine import URL

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


DATABASE_URL = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

engine = create_engine(DATABASE_URL)


def get_database_schema():
    inspector = inspect(engine)

    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)

        schema[table_name] = {
            "columns": [],
            "foreign_keys": []
        }

        for column in columns:
            schema[table_name]["columns"].append({
                "name": column["name"],
                "type": str(column["type"])
            })

        for foreign_key in foreign_keys:
            schema[table_name]["foreign_keys"].append({
                "column": foreign_key["constrained_columns"],
                "references_table": foreign_key["referred_table"],
                "references_column": foreign_key["referred_columns"]
            })

    return schema