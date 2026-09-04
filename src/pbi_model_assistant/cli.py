import argparse
from pbi_model_assistant.powerbi.tom import list_tables

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Power BI Model Assistant"
    )

    parser.add_argument(
        "--server",
        required=True,
        help="Power BI local Analysis Services server address",
    )

    parser.add_argument(
        "--database",
        required=True,
        help="Power BI semantic model database name",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    print("=" * 50)
    print("Power BI Model Assistant")
    print("=" * 50)

    print(f"Server:   {args.server}")
    print(f"Database: {args.database}")

    print()
    print("Connecting to Power BI...")

    tables = list_tables(
        server_address=args.server,
        database_name=args.database,
    )

    print()
    print(f"Tables: {len(tables)}")
    print("-" * 50)

    for table_name in tables:
        print(f"- {table_name}")

    print("=" * 50)

    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()
