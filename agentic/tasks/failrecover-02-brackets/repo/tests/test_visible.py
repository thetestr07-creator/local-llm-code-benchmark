import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pkg.core import is_balanced

assert is_balanced("()") is True
assert is_balanced("([])") is True
assert is_balanced("([)]") is False    # a naive counting approach gets this wrong
assert is_balanced("(()") is False
print("visible OK")
