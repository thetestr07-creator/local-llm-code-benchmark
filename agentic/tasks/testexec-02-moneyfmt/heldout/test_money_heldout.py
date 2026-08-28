"""HELD-OUT verification for testexec-02 — superset with edge cases the visible
suite omits (signs, whitespace, grouping toggle, fractional/format boundaries,
error handling). Pure stdlib, deterministic."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from moneykit.core import parse_amount, format_cents

# ---- parse_amount: happy path (same as visible) ----
assert parse_amount("5") == 500
assert parse_amount("5.75") == 575
assert parse_amount("5.7") == 570
assert parse_amount("0") == 0
assert parse_amount("$5.00") == 500
assert parse_amount("1,234.50") == 123450

# ---- parse_amount: whitespace + signs ----
assert parse_amount("  5.00  ") == 500
assert parse_amount("-5") == -500
assert parse_amount("- 5.00") == -500          # space after sign
assert parse_amount("+5") == 500
assert parse_amount("-$5") == -500
assert parse_amount("$-5") == -500
assert parse_amount("$5") == 500

# ---- parse_amount: fractional-part boundaries ----
assert parse_amount("5.") == 500               # trailing dot -> .00
assert parse_amount(".5") == 50                # no integer part
assert parse_amount(".05") == 5
assert parse_amount("0.09") == 9
assert parse_amount("10.1") == 1010
assert parse_amount("1,000,000.00") == 100000000

# ---- parse_amount: negative-zero normalization ----
assert parse_amount("-0.00") == 0
assert parse_amount("-0") == 0
assert parse_amount("-.00") == 0

# ---- parse_amount: errors ----
for bad in ["", "   ", "-", "+", "$", "abc", "5.123", "5.6.7", "1,23", "5..0",
            "$ $5", "5 5", "1_000", "5.-", "--5"]:
    try:
        parse_amount(bad)
        raise AssertionError("expected ValueError for %r" % bad)
    except ValueError:
        pass

# ---- format_cents: signs and zero ----
assert format_cents(500) == "$5.00"
assert format_cents(0) == "$0.00"
assert format_cents(-500) == "-$5.00"
assert format_cents(5) == "$0.05"
assert format_cents(9) == "$0.09"
assert format_cents(-9) == "-$0.09"

# ---- format_cents: grouping on/off ----
assert format_cents(123450) == "$1,234.50"
assert format_cents(-123456789) == "-$1,234,567.89"
assert format_cents(123450, grouping=False) == "$1234.50"
assert format_cents(-123456789, grouping=False) == "-$1234567.89"
assert format_cents(1000000) == "$10,000.00"      # exactly 7 integer digits
assert format_cents(100000) == "$1,000.00"

# ---- format_cents: custom / empty symbol ----
assert format_cents(500, symbol="") == "5.00"
assert format_cents(-500, symbol="") == "-5.00"
assert format_cents(123450, symbol="USD ") == "USD 1,234.50"

# ---- format_cents: type checking ----
for bad in [5.0, "5", None, [500], 5.5]:
    try:
        format_cents(bad)
        raise AssertionError("expected TypeError for %r" % (bad,))
    except TypeError:
        pass

# ---- round trip ----
for s in ["0", "5.00", "1,234.50", "-9.99", "1,000,000.00"]:
    c = parse_amount(s)
    assert parse_amount(format_cents(c)) == c

print("HELDOUT_OK")
