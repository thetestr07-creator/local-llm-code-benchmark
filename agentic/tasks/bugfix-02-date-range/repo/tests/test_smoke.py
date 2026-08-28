"""Project smoke test. Passes on the current code. Checks structural properties
of ranges and the parse/format helpers, but does not pin down the exact number
of days for a known span (that stricter check lives elsewhere)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daterange.core import parse_date, date_range, days_in_range
from daterange.billing import BillingPeriod
from daterange.format import describe_range, iso
from daterange.weekdays import weekdays_in_range

# parse round-trips
d = parse_date("2024-03-01")
assert iso(d) == "2024-03-01"
assert parse_date(d) is d  # already-a-date passes through

# range starts at the start date and is sorted & consecutive
r = date_range("2024-03-01", "2024-03-10")
assert r[0] == parse_date("2024-03-01")
for i in range(1, len(r)):
    assert (r[i] - r[i - 1]).days == 1, "range must be consecutive days"

# reversed range is empty
assert date_range("2024-03-10", "2024-03-01") == []

# weekdays are a subset of the full range
wd = weekdays_in_range("2024-03-01", "2024-03-10")
assert set(wd).issubset(set(r))
for day in wd:
    assert day.weekday() < 5

# billing contains() is inclusive on both ends
bp = BillingPeriod("2024-03-01", "2024-03-31")
assert bp.contains("2024-03-01")
assert bp.contains("2024-03-31")
assert not bp.contains("2024-04-01")

# formatting
assert describe_range([]) == "(empty range)"

print("smoke OK")
