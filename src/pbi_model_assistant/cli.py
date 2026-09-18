import argparse
import json
from pbi_model_assistant.powerbi.tom import (
    create_measure,
    get_relationships,
    get_table_details,
    list_tables,
)
from pbi_model_assistant.model.snapshot import build_model_snapshot

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

    parser.add_argument(
        "--relationships",
        action="store_true",
        help="Show Power BI model relationships",
    )

    parser.add_argument(
        "--table",
        required=False,
        help="Show columns and measures for one Power BI table",
        )

    parser.add_argument(
    "--snapshot",
    action="store_true",
    help="Build Power BI model snapshot",
    )

    parser.add_argument(
        "--output",
        required=False,
        help="Path for snapshot JSON file",
    )

    parser.add_argument(
        "--create-measure",
        action="store_true",
        help="Create a DAX measure",
    )

    parser.add_argument(
        "--measure-name",
        required=False,
        help="Name of the measure",
    )

    parser.add_argument(
        "--expression",
        required=False,
        help="DAX expression",
    )
    
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    print("=" * 80)
    print("Power BI Model Assistant")
    print("=" * 80)

    print(f"Server:   {args.server}")
    print(f"Database: {args.database}")

    print()
    print("Connecting to Power BI...")
    print()

    if args.create_measure:
        if not args.table:
            raise RuntimeError(
                "--table is required with --create-measure"
            )

        if not args.measure_name:
            raise RuntimeError(
                "--measure-name is required with --create-measure"
            )

        if not args.expression:
            raise RuntimeError(
                "--expression is required with --create-measure"
            )

        create_measure(
            server_address=args.server,
            database_name=args.database,
            table_name=args.table,
            measure_name=args.measure_name,
            expression=args.expression,
        )

        print(
            f"Measure created: "
            f"{args.table}[{args.measure_name}]"
        )


    elif args.snapshot:
        snapshot = build_model_snapshot(
            server_address=args.server,
            database_name=args.database,
        )

        json_text = json.dumps(
            snapshot,
            ensure_ascii=False,
            indent=2,
        )

        if args.output:
            with open(
                args.output,
                "w",
                encoding="utf-8",
            ) as file:
                file.write(json_text)

            print(
                f"Snapshot saved to: {args.output}"
            )

        else:
            print(json_text)

    elif args.relationships:
        relationships = get_relationships(
            server_address=args.server,
            database_name=args.database,
        )

        print(f"RELATIONSHIPS: {len(relationships)}")
        print("=" * 100)

        for rel in relationships:
            active_mark = (
                "ACTIVE"
                if rel["active"]
                else "INACTIVE"
            )

            print(
                f"{rel['from_table']}[{rel['from_column']}]"
                f"  ({rel['from_cardinality']})"
            )

            print(
                f"    --> "
                f"{rel['to_table']}[{rel['to_column']}]"
                f"  ({rel['to_cardinality']})"
            )

            print(
                f"    {active_mark} | "
                f"Filter: {rel['cross_filtering']}"
            )

            print()

    elif args.table:
        details = get_table_details(
            server_address=args.server,
            database_name=args.database,
            table_name=args.table,
        )

        print(f"TABLE: {details['name']}")
        print("=" * 80)

        print()
        print(f"COLUMNS: {len(details['columns'])}")
        print("-" * 80)

        for column in details["columns"]:
            hidden_mark = " [hidden]" if column["hidden"] else ""

            print(
                f"{column['name']:<45}"
                f"{column['data_type']:<20}"
                f"{hidden_mark}"
            )

        print()
        print(f"MEASURES: {len(details['measures'])}")
        print("-" * 80)

        for measure in details["measures"]:
            hidden_mark = " [hidden]" if measure["hidden"] else ""

            print()
            print(
                f"{measure['name']}"
                f"{hidden_mark}"
            )

            if measure["format_string"]:
                print(
                    f"Format: {measure['format_string']}"
                )

            print("DAX:")
            print(measure["expression"])

    else:
        tables = list_tables(
            server_address=args.server,
            database_name=args.database,
        )

        print(f"Visible tables: {len(tables)}")
        print("-" * 80)

        print(
            f"{'TABLE':<45}"
            f"{'COLUMNS':>12}"
            f"{'MEASURES':>12}"
        )

        print("-" * 80)

        for table in tables:
            print(
                f"{table['name']:<45}"
                f"{table['columns']:>12}"
                f"{table['measures']:>12}"
            )

    print()
    print("=" * 80)

    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()
