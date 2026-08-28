import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pkg.core import roman_to_int

cases = {"III": 3, "IV": 4, "IX": 9, "LVIII": 58, "MCMXCIV": 1994,
         "XL": 40, "XC": 90, "CD": 400, "CM": 900, "MMXXIV": 2024,
         "XLII": 42, "XCIX": 99, "DCCCXC": 890, "I": 1, "MMMCMXCIX": 3999}
for s, v in cases.items():
    got = roman_to_int(s)
    assert got == v, "roman_to_int(%r) -> %r, expected %d" % (s, got, v)
print("HELDOUT_OK")
