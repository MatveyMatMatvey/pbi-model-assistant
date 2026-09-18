import sys

from pythonnet import load


TOM_PATH = (
    r"C:\Users\Матвей\.nuget\packages"
    r"\microsoft.analysisservices"
    r"\19.114.12"
    r"\lib\net8.0"
)

def get_table_details(
    server_address: str,
    database_name: str,
    table_name: str,
    ) -> dict:
    """
    Возвращает колонки и меры конкретной таблицы Power BI.
    """

    Server = _load_tom()

    server = Server()
    server.Connect(
        f"DataSource={server_address}"
    )

    try:
        database = _get_database(
            server,
            database_name,
        )

        target_table = None

        for table in database.Model.Tables:
            if str(table.Name) == table_name:
                target_table = table
                break

        if target_table is None:
            available_tables = [
                str(table.Name)
                for table in database.Model.Tables
                if not bool(table.IsHidden)
            ]

            raise RuntimeError(
                f"Таблица '{table_name}' не найдена. "
                f"Доступные таблицы: {available_tables}"
            )

        columns = []

        for column in target_table.Columns:
            columns.append(
                {
                    "name": str(column.Name),
                    "data_type": str(column.DataType),
                    "hidden": bool(column.IsHidden),
                }
            )

        measures = []

        for measure in target_table.Measures:
            measures.append(
                {
                    "name": str(measure.Name),
                    "expression": str(measure.Expression),
                    "format_string": str(
                        measure.FormatString or ""
                    ),
                    "hidden": bool(measure.IsHidden),
                }
            )

        return {
            "name": str(target_table.Name),
            "hidden": bool(target_table.IsHidden),
            "columns": columns,
            "measures": measures,
        }

    finally:
        server.Disconnect()

def _load_tom():
    """
    Загружает .NET CoreCLR и Microsoft TOM.
    """

    load("coreclr")

    if TOM_PATH not in sys.path:
        sys.path.insert(0, TOM_PATH)

    import clr

    clr.AddReference(
        TOM_PATH + r"\Microsoft.AnalysisServices.Tabular.dll"
    )

    from Microsoft.AnalysisServices.Tabular import Server

    return Server


def _get_database(server, database_name: str):
    """
    Находит semantic model внутри локального Power BI server.

    1. Сначала ищет точное совпадение Name или ID.
    2. Если база на локальном server только одна —
       использует её автоматически.
    """

    databases = list(server.Databases)

    for database in databases:
        if (
            str(database.Name) == database_name
            or str(database.ID) == database_name
        ):
            return database

    if len(databases) == 1:
        return databases[0]

    available = [
        f"{database.Name} ({database.ID})"
        for database in databases
    ]

    raise RuntimeError(
        f"Semantic model '{database_name}' не найдена. "
        f"Доступные базы: {available}"
    )


def list_tables(
    server_address: str,
    database_name: str,
    include_hidden: bool = False,
) -> list[dict]:
    """
    Возвращает краткую информацию о таблицах
    semantic model Power BI.
    """

    Server = _load_tom()

    server = Server()

    server.Connect(
        f"DataSource={server_address}"
    )

    try:
        database = _get_database(
                server,
                database_name,
            )

        result = []

        for table in database.Model.Tables:
            is_hidden = bool(table.IsHidden)

            if not include_hidden and is_hidden:
                continue

            result.append(
                {
                    "name": str(table.Name),
                    "columns": int(table.Columns.Count),
                    "measures": int(table.Measures.Count),
                    "hidden": is_hidden,
                }
            )

        return result

    finally:
        server.Disconnect()

def get_relationships(
    server_address: str,
    database_name: str,
) -> list[dict]:
    """
    Возвращает связи semantic model Power BI.
    """

    Server = _load_tom()

    server = Server()
    server.Connect(
        f"DataSource={server_address}"
    )

    try:
        database = _get_database(
            server,
            database_name,
        )

        result = []

        for relationship in database.Model.Relationships:
            result.append(
                {
                    "name": str(relationship.Name),
                    "from_table": str(relationship.FromTable.Name),
                    "from_column": str(relationship.FromColumn.Name),
                    "to_table": str(relationship.ToTable.Name),
                    "to_column": str(relationship.ToColumn.Name),
                    "from_cardinality": str(
                        relationship.FromCardinality
                    ),
                    "to_cardinality": str(
                        relationship.ToCardinality
                    ),
                    "active": bool(
                        relationship.IsActive
                    ),
                    "cross_filtering": str(
                        relationship.CrossFilteringBehavior
                    ),
                }
            )

        return result

    finally:
        server.Disconnect()


def create_measure(
    server_address: str,
    database_name: str,
    table_name: str,
    measure_name: str,
    expression: str,
    format_string: str = "",
) -> None:
    """
    Создаёт новую DAX-меру в открытой модели Power BI Desktop.
    """

    Server = _load_tom()

    server = Server()
    server.Connect(
        f"DataSource={server_address}"
    )

    try:
        database = _get_database(
            server,
            database_name,
        )

        target_table = None

        for table in database.Model.Tables:
            if str(table.Name) == table_name:
                target_table = table
                break

        if target_table is None:
            raise RuntimeError(
                f"Таблица '{table_name}' не найдена."
            )

        for measure in target_table.Measures:
            if str(measure.Name) == measure_name:
                raise RuntimeError(
                    f"Мера '{measure_name}' уже существует "
                    f"в таблице '{table_name}'."
                )

        from Microsoft.AnalysisServices.Tabular import Measure

        new_measure = Measure()
        new_measure.Name = measure_name
        new_measure.Expression = expression

        if format_string:
            new_measure.FormatString = format_string

        target_table.Measures.Add(new_measure)

        database.Model.SaveChanges()

    finally:
        server.Disconnect()