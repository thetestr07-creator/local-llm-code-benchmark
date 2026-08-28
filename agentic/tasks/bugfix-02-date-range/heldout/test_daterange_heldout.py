"""HELD-OUT verification for bugfix-02. The model under test never sees this file.
Decides pass/fail deterministically. Inclusive ranges must include the end date."""
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daterange.core import parse_date, date_range, days_in_range
from daterange.billing import BillingPeriod
from daterange.weekdays import count_weekdays, count_weekends

# --- inclusive enumeration includes BOTH endpoints ---
r = date_range("2024-03-01", "2024-03-03")
assert r == [datetime.date(2024, 3, 1), datetime.date(2024, 3, 2), datetime.date(2024, 3, 3)], r
assert r[-1] == parse_date("2024-03-03"), "range must include the end date"

# single-day inclusive range has exactly one day
assert date_range("2024-03-05", "2024-03-05") == [datetime.date(2024, 3, 5)]
assert days_in_range("2024-03-05", "2024-03-05") == 1

# a full month is counted with all its days
assert days_in_range("2024-03-01", "2024-03-31") == 31, days_in_range("2024-03-01", "2024-03-31")
assert days_in_range("2024-02-01", "2024-02-29") == 29  # 2024 is a leap year

# reversed range stays empty
assert date_range("2024-03-10", "2024-03-01") == []

# --- billing counts every day inclusively ---
bp = BillingPeriod("2024-03-01", "2024-03-31")
assert bp.days() == 31, bp.days()
assert bp.daily_dates()[-1] == parse_date("2024-03-31")
# proration for a full 31-day month at a 31-day monthly rate is the whole amount
assert bp.prorate(3100, 31) == 3100, bp.prorate(3100, 31)

one_day = BillingPeriod("2024-06-15", "2024-06-15")
assert one_day.days() == 1

# --- weekday/weekend counts also cover the final day ---
# 2024-03-01 is a Friday; 2024-03-03 is a Sunday -> Fri, Sat, Sun
assert count_weekdays("2024-03-01", "2024-03-03") == 1  # just the Friday
assert count_weekends("2024-03-01", "2024-03-03") == 2  # Sat + Sun (Sun is the end)

print("HELDOUT_OK")
