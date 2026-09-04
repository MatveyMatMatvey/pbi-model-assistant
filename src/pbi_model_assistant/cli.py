import argparse


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

    print("=" * 50)
    input("Press Enter to close...")


if __name__ == "__main__":
    main()
