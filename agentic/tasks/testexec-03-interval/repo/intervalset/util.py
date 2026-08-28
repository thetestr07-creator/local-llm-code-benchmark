"""Low-level helpers for interval math. Fully implemented (not stubs).

These operate on plain (start, end) tuples with the half-open convention
[start, end). You may use them from core.IntervalSet or ignore them.
"""


def is_empty(start, end):
    """True if [start, end) contains no points (start >= end)."""
    return start >= end


def overlaps_or_adjacent(a, b):
    """True if intervals a and b overlap OR touch (adjacent).

    With half-open intervals, [0, 5) and [5, 10) are adjacent and should merge,
    so the condition is a.start <= b.end and b.start <= a.end.
    """
    return a[0] <= b[1] and b[0] <= a[1]


def merge_pair(a, b):
    """Return the union of two overlapping-or-adjacent intervals."""
    return (min(a[0], b[0]), max(a[1], b[1]))


def normalize(pairs):
    """Sort, drop empties, and merge overlapping/adjacent intervals.

    Returns a new list of (start, end) tuples. Adjacent intervals ARE merged.
    """
    cleaned = [(s, e) for (s, e) in pairs if s < e]
    cleaned.sort(key=lambda p: (p[0], p[1]))
    out = []
    for s, e in cleaned:
        if out and s <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out
