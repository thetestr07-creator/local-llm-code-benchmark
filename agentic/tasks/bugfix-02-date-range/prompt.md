The `daterange` package works with **inclusive** calendar date ranges: a range
from one date through another is meant to include *both* endpoints. For example,
the range from `2024-03-01` through `2024-03-03` should contain three days (the
1st, 2nd, and 3rd), and a billing period covering `2024-03-01` through
`2024-03-31` should count as 31 billable days.

Customers on monthly plans are reporting that their invoices are short by one
day: a full-month billing period is being counted as one day fewer than the
month actually has, which also throws off proration. In general, the day counts
and enumerated dates for an inclusive range are dropping the final day.

Find and fix the bug so that inclusive ranges include their end date. Do not
change the public function or method signatures (`parse_date`, `date_range`,
`days_in_range`, `BillingPeriod.days`, `BillingPeriod.daily_dates`,
`BillingPeriod.contains`). Keep the package importable.

You can run the existing tests with `python3 tests/test_smoke.py` and
`python3 tests/test_format.py`.
