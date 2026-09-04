import sys

from pythonnet import load


TOM_PATH = (
    r"C:\Users\Матвей\.nuget\packages"
    r"\microsoft.analysisservices"
    r"\19.114.12"
    r"\lib\net8.0"
)


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
        database = None

        for candidate in server.Databases:
            if (
                str(candidate.Name) == database_name
                or str(candidate.ID) == database_name
            ):
                database = candidate
                break

        if database is None:
            available = [
                f"{db.Name} ({db.ID})"
                for db in server.Databases
            ]

            raise RuntimeError(
                "Не удалось найти semantic model. "
                f"Доступные базы: {available}"
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