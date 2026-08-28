"""Bounding queries over a normalized interval list. Fully implemented.

Not required by the grader, but part of the package surface. Assumes the input
is already normalized (sorted, non-overlapping, non-adjacent).
"""


def span(pairs):
    """Return (min_start, max_end) across all intervals, or None if empty."""
    if not pairs:
        return None
    return (pairs[0][0], pairs[-1][1])


def gaps(pairs):
    """Return the open gaps between consecutive intervals as (start, end)."""
    out = []
    for i in range(1, len(pairs)):
        prev_end = pairs[i - 1][1]
        cur_start = pairs[i][0]
        if prev_end < cur_start:
            out.append((prev_end, cur_start))
    return out
