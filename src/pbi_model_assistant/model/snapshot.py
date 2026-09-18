from pbi_model_assistant.powerbi.tom import (
    get_relationships,
    get_table_details,
    list_tables,
)


def build_model_snapshot(
    server_address: str,
    database_name: str,
) -> dict:
    """
    Собирает компактное описание semantic model Power BI.

    В snapshot входят:
    - таблицы;
    - колонки;
    - типы;
    - меры;
    - DAX;
    - relationships.

    Строки данных из модели не читаются.
    """

    table_summaries = list_tables(
        server_address=server_address,
        database_name=database_name,
    )

    tables = []

    for table_summary in table_summaries:
        table_name = table_summary["name"]

        details = get_table_details(
            server_address=server_address,
            database_name=database_name,
            table_name=table_name,
        )

        tables.append(details)

    relationships = get_relationships(
        server_address=server_address,
        database_name=database_name,
    )

    return {
        "database": database_name,
        "tables": tables,
        "relationships": relationships,
    }