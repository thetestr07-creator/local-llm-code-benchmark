"""Project's own smoke test (passes today; does NOT exercise the fractional-cent edge cases)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from invoicelib.invoice import Invoice
from invoicelib.money import to_cents, cents_to_str

inv = Invoice()
inv.add("widget", 2, 1.00)
assert inv.total_cents() == 200
assert to_cents(1.00) == 100
assert cents_to_str(200) == "$2.00"
print("smoke OK")
