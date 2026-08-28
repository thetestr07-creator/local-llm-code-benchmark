import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pkg.core import flatten

assert flatten([1, 2, 3]) == [1, 2, 3]
assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]
assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]   # a one-level flatten fails here
print("visible OK")
