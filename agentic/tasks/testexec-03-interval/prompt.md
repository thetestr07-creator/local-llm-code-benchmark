Implement the stubbed class `IntervalSet` in `intervalset/core.py` so that the
test suite passes. Run the tests with `python3 tests/test_intervalset.py` to
check your work.

An `IntervalSet` represents a set of real numbers as a collection of
**half-open intervals** `[start, end)` — `start` is included, `end` is
excluded. The set is always kept **normalized**: stored as a list of
non-empty, non-overlapping, **non-adjacent** intervals sorted by `start`.
(Adjacent intervals like `[0, 5)` and `[5, 10)` MUST be merged into
`[0, 10)`.)

Numbers may be `int` or `float`. Compare with `<`/`==` as usual.

## Constructor

```python
IntervalSet(intervals=None)
```

- `intervals` is an optional iterable of `(start, end)` pairs. Add each one
  (merging as needed). `None` or an empty iterable yields the empty set.
- Any pair with `start >= end` is **empty** and contributes nothing (silently
  ignored — it is not an error).

## Methods to implement

### `add(self, start, end) -> None`
Add the interval `[start, end)` to the set, merging with (and bridging across)
any intervals it overlaps or is adjacent to. Empty intervals (`start >= end`)
are ignored.

### `remove(self, start, end) -> None`
Subtract `[start, end)` from the set. This may shrink an interval, delete
intervals fully covered, or **split** one interval into two. Empty intervals
are ignored.

### `contains(self, x) -> bool`
Return `True` iff the point `x` lies in some stored interval (i.e. some
`start <= x < end`). Also usable as `x in interval_set` (`__contains__`).

### `measure(self) -> (int | float)`
Return the total length of the set: the sum of `(end - start)` over all stored
intervals. The empty set has measure `0`.

### `overlaps(self, start, end) -> bool`
Return `True` iff `[start, end)` shares at least one point with the set. An
empty query interval (`start >= end`) never overlaps (returns `False`).

### `intervals(self) -> list[tuple]`
Return the normalized intervals as a **new** list of `(start, end)` tuples,
sorted ascending by `start`. Callers must not be able to mutate internal state
through the returned list.

## Additional behavior

- `len(interval_set)` returns the **number of stored (merged) intervals**.
- `bool(interval_set)` is `False` for the empty set, `True` otherwise.
- Two `IntervalSet`s are equal (`==`) iff their normalized intervals are
  identical.

Do not change the public method names or signatures. Keep the module importable.
