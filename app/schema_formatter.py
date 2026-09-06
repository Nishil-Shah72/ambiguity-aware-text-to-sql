from app.schema_reader import get_database_schema


def format_schema():
    schema = get_database_schema()

    formatted_schema = ""

    for table_name, table_data in schema.items():
        formatted_schema += f"Table: {table_name}\n"

        formatted_schema += "Columns:\n"

        for column in table_data["columns"]:
            formatted_schema += (
                f"  - {column['name']} ({column['type']})\n"
            )

        if table_data["foreign_keys"]:
            formatted_schema += "Relationships:\n"

            for foreign_key in table_data["foreign_keys"]:
                formatted_schema += (
                    f"  - {foreign_key['column']} → "
                    f"{foreign_key['references_table']}."
                    f"{foreign_key['references_column']}\n"
                )

        formatted_schema += "\n"

    return formatted_schema