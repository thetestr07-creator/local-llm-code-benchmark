# Design notes

## Half-open convention

Every interval is `[start, end)` — the left endpoint is included, the right
endpoint is excluded. This makes adjacency clean: `[0, 5)` and `[5, 10)`
partition `[0, 10)` with no gap and no overlap, so they merge.

## Normalization invariant

`IntervalSet` keeps its stored intervals:

1. non-empty (`start < end`),
2. sorted ascending by `start`,
3. pairwise non-overlapping **and** non-adjacent.

Every mutating operation (`add`, `remove`, constructor) must re-establish this
invariant before returning.

## remove() and splitting

Subtracting an interval from the middle of a stored interval splits it into
two. For example removing `[3, 6)` from `[0, 10)` yields `[0, 3)` and `[6, 10)`.
Removing a range that only clips an edge shrinks the interval; removing a range
that fully covers an interval deletes it.
