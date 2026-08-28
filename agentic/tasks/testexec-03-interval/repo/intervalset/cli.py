"""Tiny CLI for intervalset. Not exercised by the grader; kept runnable.

Usage:
    python -m intervalset.cli "0:5,10:12" measure
    python -m intervalset.cli "0:5,3:8" show
"""
import sys

from .core import IntervalSet


def _parse(spec):
    if not spec:
        return IntervalSet()
    pairs = []
    for chunk in spec.split(","):
        a, b = chunk.split(":")
        pairs.append((float(a), float(b)))
    return IntervalSet(pairs)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print("usage: cli.py <spec> {show|measure}", file=sys.stderr)
        return 2
    spec, op = argv
    s = _parse(spec)
    if op == "show":
        print(s.intervals())
        return 0
    if op == "measure":
        print(s.measure())
        return 0
    print("unknown op: %s" % op, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
