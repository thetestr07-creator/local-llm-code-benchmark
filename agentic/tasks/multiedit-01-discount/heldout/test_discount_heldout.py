"""HELD-OUT verification for multiedit-01. The model under test never sees this."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from invoicelib.discount import apply_discount
from invoicelib.invoice import Invoice

# rounding behaviour
assert apply_discount(1000, 15) == 850, apply_discount(1000, 15)
assert apply_discount(999, 10) == 899, apply_discount(999, 10)   # round(899.1)
assert apply_discount(1000, 0) == 1000
assert apply_discount(1000, 100) == 0

# range validation
for bad in (-1, 101, 150):
    try:
        apply_discount(1000, bad)
        raise AssertionError("apply_discount accepted invalid percent %r" % bad)
    except ValueError:
        pass

# wired into Invoice
inv = Invoice()
inv.add("widget", 2, 5.00)           # 1000 cents
assert inv.total_cents() == 1000     # no discount yet
inv.set_discount(15)
assert inv.total_cents() == 850, inv.total_cents()
inv.set_discount(0)
assert inv.total_cents() == 1000
try:
    inv.set_discount(200)
    raise AssertionError("set_discount accepted 200")
except ValueError:
    pass
print("HELDOUT_OK")
