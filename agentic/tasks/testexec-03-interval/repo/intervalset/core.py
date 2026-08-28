"""IntervalSet — a normalized collection of half-open [start, end) intervals.

This class is a stub. Implement every method marked ``raise NotImplementedError``
so the tests pass. See prompt.md for the full specification (merging, adjacency,
splitting on remove, measure, overlaps, ordering, and the dunder methods).

You may use the helpers in ``intervalset.util`` (or implement it yourself).
"""


class IntervalSet:
    def __init__(self, intervals=None):
        # Internal representation: a list of [start, end] pairs kept normalized
        # (sorted, non-overlapping, non-adjacent). You decide how to fill it.
        self._items = []
        if intervals is not None:
            for pair in intervals:
                start, end = pair
                self.add(start, end)

    def add(self, start, end):
        """Add [start, end); merge/bridge overlapping or adjacent intervals."""
        raise NotImplementedError

    def remove(self, start, end):
        """Subtract [start, end); may shrink, delete, or split intervals."""
        raise NotImplementedError

    def contains(self, x):
        """True iff point x lies in some stored interval."""
        raise NotImplementedError

    def measure(self):
        """Total length: sum of (end - start) over stored intervals."""
        raise NotImplementedError

    def overlaps(self, start, end):
        """True iff [start, end) shares a point with the set."""
        raise NotImplementedError

    def intervals(self):
        """Return a NEW sorted list of (start, end) tuples."""
        raise NotImplementedError

    # --- dunder conveniences (implement using the methods above) ---

    def __contains__(self, x):
        return self.contains(x)

    def __len__(self):
        raise NotImplementedError

    def __bool__(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __repr__(self):
        return "IntervalSet(%r)" % (self.intervals(),)
