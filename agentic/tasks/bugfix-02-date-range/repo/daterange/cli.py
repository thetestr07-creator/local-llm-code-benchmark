"""Tiny CLI: print the days in an inclusive range.

    python -m daterange.cli 2024-03-01 2024-03-05
"""
import sys
from .core import date_range
from .format import describe_range, iso


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print("usage: python -m daterange.cli <start YYYY-MM-DD> <end YYYY-MM-DD>")
        return 2
    dates = date_range(argv[0], argv[1])
    for d in dates:
        print(iso(d))
    print(describe_range(dates))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
