"""Boolean predicates over a normalized interval list. Fully implemented.

Assumes the input list is normalized (sorted, disjoint, non-adjacent).
"""


def point_in(pairs, x):
    """True iff x is covered by some [start, end) in pairs."""
    for s, e in pairs:
        if s <= x < e:
            return True
        if x < s:
            break
    return False


def covers(pairs, start, end):
    """True iff [start, end) is fully contained in the union of pairs.

    An empty query ([start, end) with start >= end) is trivially covered.
    """
    if start >= end:
        return True
    for s, e in pairs:
        if s <= start and end <= e:
            return True
    return False
