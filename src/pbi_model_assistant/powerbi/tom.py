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
) -> list[str]:
    """
    Подключается к модели, открытой в Power BI Desktop,
    и возвращает имена таблиц.
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

        return [
            str(table.Name)
            for table in database.Model.Tables
        ]

    finally:
        server.Disconnect()