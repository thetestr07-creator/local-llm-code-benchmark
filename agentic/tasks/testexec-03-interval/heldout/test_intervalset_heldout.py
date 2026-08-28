"""HELD-OUT verification for testexec-03 — strict superset covering adjacency
merging, remove-splitting, exclusive-end semantics, floats, empty intervals,
ordering, equality and idempotence. Pure stdlib, deterministic."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intervalset.core import IntervalSet

# ---- construction: overlaps merge, order-independent ----
assert IntervalSet([(0, 5), (3, 8)]).intervals() == [(0, 8)]
assert IntervalSet([(3, 8), (0, 5)]).intervals() == [(0, 8)]
assert IntervalSet([(10, 12), (0, 5)]).intervals() == [(0, 5), (10, 12)]

# ---- adjacency MUST merge (half-open) ----
assert IntervalSet([(0, 5), (5, 10)]).intervals() == [(0, 10)]
s = IntervalSet()
s.add(0, 5)
s.add(5, 10)
s.add(10, 15)
assert s.intervals() == [(0, 15)]

# ---- add that bridges a gap between two existing intervals ----
s = IntervalSet([(0, 3), (7, 10)])
s.add(2, 8)
assert s.intervals() == [(0, 10)]

# ---- add strictly inside an existing interval is a no-op ----
s = IntervalSet([(0, 10)])
s.add(3, 6)
assert s.intervals() == [(0, 10)]

# ---- empty intervals are ignored, never stored ----
s = IntervalSet([(5, 5), (2, 2), (0, 0)])
assert s.intervals() == []
assert len(s) == 0
assert bool(s) is False
s.add(4, 4)     # empty -> no-op
assert s.intervals() == []

# ---- contains: exclusive end, inclusive start ----
s = IntervalSet([(0, 5), (10, 12)])
assert s.contains(0) is True
assert s.contains(4.999) is True
assert s.contains(5) is False       # end excluded
assert s.contains(10) is True
assert s.contains(12) is False
assert s.contains(-1) is False
assert s.contains(7) is False       # in the gap
assert (3 in s) is True
assert (5 in s) is False

# ---- measure: ints and floats ----
assert IntervalSet().measure() == 0
assert IntervalSet([(0, 5), (10, 12)]).measure() == 7
assert IntervalSet([(0.0, 2.5), (3.5, 4.0)]).measure() == 3.0

# ---- overlaps: shares a point; touching at an exclusive edge does NOT ----
s = IntervalSet([(0, 5), (10, 12)])
assert s.overlaps(4, 6) is True
assert s.overlaps(5, 10) is False   # sits exactly in the gap [5,10)
assert s.overlaps(-3, 0) is False   # ends exactly at start 0 (exclusive)
assert s.overlaps(-3, 1) is True
assert s.overlaps(12, 20) is False  # starts at exclusive end 12
assert s.overlaps(11, 13) is True
assert s.overlaps(5, 5) is False    # empty query never overlaps
assert s.overlaps(7, 7) is False

# ---- remove: shrink left, shrink right, delete, split, span multiple ----
s = IntervalSet([(0, 10)])
s.remove(0, 3)
assert s.intervals() == [(3, 10)]           # shrink left
s.remove(8, 20)
assert s.intervals() == [(3, 8)]            # shrink right (overshoot ok)

s = IntervalSet([(0, 10)])
s.remove(3, 6)
assert s.intervals() == [(0, 3), (6, 10)]   # split into two

s = IntervalSet([(0, 5), (10, 15), (20, 25)])
s.remove(3, 22)
assert s.intervals() == [(0, 3), (22, 25)]  # spans/deletes across multiple

s = IntervalSet([(0, 5)])
s.remove(0, 5)
assert s.intervals() == []                  # exact delete
s.remove(0, 5)                               # remove from empty -> no-op
assert s.intervals() == []

s = IntervalSet([(0, 10)])
s.remove(4, 4)                               # empty removal -> no-op
assert s.intervals() == [(0, 10)]
s.remove(10, 20)                             # touches exclusive end -> no-op
assert s.intervals() == [(0, 10)]
s.remove(-5, 0)                              # touches inclusive start from left -> no-op
assert s.intervals() == [(0, 10)]

# ---- intervals() returns a defensive copy ----
s = IntervalSet([(0, 5)])
got = s.intervals()
got.append((100, 200))
got[0] = (999, 999)
assert s.intervals() == [(0, 5)]

# ---- len / bool / equality ----
assert len(IntervalSet([(0, 5), (10, 12)])) == 2
assert len(IntervalSet([(0, 5), (5, 12)])) == 1     # merged
assert bool(IntervalSet([(0, 1)])) is True
assert IntervalSet([(0, 5), (5, 10)]) == IntervalSet([(0, 10)])
assert IntervalSet([(0, 5)]) != IntervalSet([(0, 6)])
assert IntervalSet() == IntervalSet([(3, 3)])

# ---- idempotence / re-normalization after many ops ----
s = IntervalSet()
for a, b in [(0, 2), (4, 6), (2, 4), (8, 10), (5, 9)]:
    s.add(a, b)
# This sequence must fully coalesce to a single interval [0, 10).
assert s.intervals() == [(0, 10)]
assert s.measure() == 10

print("HELDOUT_OK")
