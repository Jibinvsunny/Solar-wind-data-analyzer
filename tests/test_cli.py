from swda import __version__
from swda.cli import build_parser, main


def test_version_string():
    assert __version__.count(".") == 2


def test_help_runs():
    assert main([]) == 0


def test_clean_arguments_parse():
    args = build_parser().parse_args(["clean", "file.dat", "--cadence", "5min"])
    assert args.path == "file.dat"
    assert args.cadence == "5min"
