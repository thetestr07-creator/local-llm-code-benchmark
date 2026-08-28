# intervalset

A normalized set of half-open `[start, end)` intervals over the reals.

```python
from intervalset import IntervalSet

s = IntervalSet([(0, 5), (3, 8)])
s.intervals()      # -> [(0, 8)]      (overlaps merged)
s.add(8, 10)
s.intervals()      # -> [(0, 10)]     (adjacent merged)
s.remove(2, 4)
s.intervals()      # -> [(0, 2), (4, 10)]  (split)
s.measure()        # -> 8
3 in s             # -> False
```

## Layout

- `intervalset/core.py` — the `IntervalSet` class (implement this)
- `intervalset/util.py` — normalize / merge helpers (implemented)
- `intervalset/bounds.py` — span / gaps queries (implemented)
- `intervalset/errors.py` — exception types
- `intervalset/cli.py` — `python -m intervalset.cli "0:5,10:12" measure`

## Tests

```
python3 tests/test_intervalset.py
```
