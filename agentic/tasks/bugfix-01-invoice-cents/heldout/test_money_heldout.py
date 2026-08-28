"""HELD-OUT verification for bugfix-01. The model under test never sees this file.
Decides pass/fail deterministically."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from invoicelib.money import to_cents, cents_to_str
from invoicelib.invoice import Invoice

# exact fractional-cent conversions that float truncation gets wrong
cases = {0.70: 70, 1.15: 115, 2.30: 230, 0.10: 10, 0.29: 29, 5.55: 555, 0.07: 7, 9.99: 999}
for dollars, cents in cases.items():
    got = to_cents(dollars)
    assert got == cents, "to_cents(%r) -> %r, expected %d" % (dollars, got, cents)

# signatures preserved / library still usable
assert cents_to_str(490) == "$4.90"
inv = Invoice()
inv.add("a", 3, 0.10)   # 30
inv.add("b", 7, 0.70)   # 490 (truncation bug would give 7*69 = 483)
assert inv.total_cents() == 520, inv.total_cents()
assert inv.total_str() == "$5.20"
print("HELDOUT_OK")
