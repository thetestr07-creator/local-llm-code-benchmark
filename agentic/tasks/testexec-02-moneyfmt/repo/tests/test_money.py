import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from moneykit.core import parse_amount, format_cents

# --- parse_amount: basic happy path ---
assert parse_amount("5") == 500
assert parse_amount("5.75") == 575
assert parse_amount("5.7") == 570
assert parse_amount("0") == 0
assert parse_amount("$5.00") == 500
assert parse_amount("1,234.50") == 123450

# --- format_cents: basic happy path ---
assert format_cents(500) == "$5.00"
assert format_cents(0) == "$0.00"
assert format_cents(123450) == "$1,234.50"
assert format_cents(-500) == "-$5.00"

print("tests pass")
