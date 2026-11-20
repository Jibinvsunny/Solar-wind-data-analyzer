"""Command-line entry point: `swda`."""

import argparse

from swda import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="swda",
        description="Clean and prepare solar wind data for statistical and ML analysis.",
    )
    parser.add_argument("--version", action="version", version=f"swda {__version__}")
    sub = parser.add_subparsers(dest="command")

    clean = sub.add_parser("clean", help="Clean a raw solar wind file (coming in v0.1).")
    clean.add_argument("path", help="Raw data file, e.g. an OMNI2 hourly .dat file")
    clean.add_argument("--cadence", default="1h", help="Output cadence: 1min, 5min or 1h")
    clean.add_argument("--out", help="Output file (.csv or .parquet)")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "clean":
        print("The cleaning pipeline is under construction (planned for v0.1).")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
