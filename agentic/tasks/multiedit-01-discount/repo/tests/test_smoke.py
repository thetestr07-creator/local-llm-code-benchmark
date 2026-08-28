import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from invoicelib.invoice import Invoice

inv = Invoice()
inv.add("widget", 2, 5.00)
assert inv.total_cents() == 1000
print("smoke OK")
