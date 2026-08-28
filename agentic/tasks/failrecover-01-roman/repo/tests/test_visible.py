import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pkg.core import roman_to_int

assert roman_to_int("III") == 3
assert roman_to_int("IV") == 4        # a naive additive parser gets this wrong (6)
assert roman_to_int("IX") == 9
assert roman_to_int("LVIII") == 58
assert roman_to_int("MCMXCIV") == 1994
print("visible OK")
