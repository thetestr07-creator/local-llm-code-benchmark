import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pkg.core import is_balanced

cases = {"()": True, "([])": True, "([)]": False, "(()": False, "": True,
         "{[()()]}": True, "]": False, "([{}])": True, "(]": False,
         "a(b)c[d]": True, "((()))": True, "([)": False, "{": False}
for s, want in cases.items():
    got = is_balanced(s)
    assert got is want, "is_balanced(%r) -> %r, expected %r" % (s, got, want)
print("HELDOUT_OK")
