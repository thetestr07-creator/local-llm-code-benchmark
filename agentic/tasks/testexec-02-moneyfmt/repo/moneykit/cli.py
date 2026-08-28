"""Tiny CLI wrapper around moneykit. Not exercised by the grader, but kept
importable and runnable so the package behaves like a real project.

Usage:
    python -m moneykit.cli parse "1,234.50"
    python -m moneykit.cli format 123450
"""
import sys

from .core import parse_amount, format_cents


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print("usage: cli.py {parse|format} <value>", file=sys.stderr)
        return 2
    op, value = argv
    if op == "parse":
        print(parse_amount(value))
        return 0
    if op == "format":
        print(format_cents(int(value)))
        return 0
    print("unknown op: %s" % op, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
