import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intervalset.core import IntervalSet

# --- construction + merging of overlaps ---
s = IntervalSet([(0, 5), (3, 8)])
assert s.intervals() == [(0, 8)]

# --- add ---
s = IntervalSet()
s.add(0, 5)
s.add(10, 12)
assert s.intervals() == [(0, 5), (10, 12)]

# --- contains ---
assert s.contains(0) is True
assert s.contains(5) is False      # end is exclusive
assert 3 in s
assert 7 not in s

# --- measure ---
assert s.measure() == 7            # 5 + 2

# --- remove (simple shrink) ---
s2 = IntervalSet([(0, 10)])
s2.remove(0, 3)
assert s2.intervals() == [(3, 10)]

# --- overlaps ---
assert s.overlaps(4, 6) is True
assert s.overlaps(5, 10) is False  # touches nothing between 5 and 10

# --- len / bool ---
assert len(s) == 2
assert bool(s) is True
assert bool(IntervalSet()) is False

print("tests pass")
