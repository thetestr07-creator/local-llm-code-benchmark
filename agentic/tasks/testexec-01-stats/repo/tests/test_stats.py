import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from statskit.core import mean, median

assert mean([1, 2, 3, 4]) == 2.5
assert median([1, 2, 3]) == 2
assert median([1, 2, 3, 4]) == 2.5
print("tests pass")
