"""HELD-OUT verification for testexec-01 — superset with edge cases the visible suite omits."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from statskit.core import mean, median

assert mean([1, 2, 3, 4]) == 2.5
assert mean([5]) == 5
assert mean([2, 2, 2]) == 2
assert median([1, 2, 3]) == 2
assert median([1, 2, 3, 4]) == 2.5
assert median([3, 1, 2]) == 2          # unsorted input
assert median([10, 2, 8, 4]) == 6      # unsorted, even length -> (4+8)/2
assert median([7]) == 7
print("HELDOUT_OK")
