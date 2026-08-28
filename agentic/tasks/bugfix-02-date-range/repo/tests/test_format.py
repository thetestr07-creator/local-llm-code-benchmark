"""Formatting tests (independent of the range-length behavior)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daterange.core import parse_date
from daterange.format import iso, describe_range

assert iso(parse_date("2024-12-31")) == "2024-12-31"
assert describe_range([]) == "(empty range)"
assert describe_range([parse_date("2024-01-01")]) == "2024-01-01 (1 day)"
three = [parse_date("2024-01-01"), parse_date("2024-01-02"), parse_date("2024-01-03")]
assert describe_range(three) == "2024-01-01 .. 2024-01-03 (3 days)"
print("format OK")
