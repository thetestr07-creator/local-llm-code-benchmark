# daterange

Small utilities for working with **inclusive** calendar date ranges — the kind
of thing you need for billing periods and reporting windows.

## Modules
- `daterange/core.py` — `parse_date`, `date_range`, `days_in_range`
- `daterange/billing.py` — `BillingPeriod` (day counts + proration)
- `daterange/weekdays.py` — weekday/weekend counting
- `daterange/format.py` — rendering helpers
- `daterange/cli.py` — `python -m daterange.cli <start> <end>`
- `tests/` — smoke tests (`python3 tests/test_smoke.py`)

## Semantics
Ranges are **inclusive of both endpoints**. For example the range from
`2024-03-01` to `2024-03-03` contains three days: the 1st, 2nd, and 3rd. A
billing period from the 1st to the 31st of a 31-day month covers 31 billable
days.

## Known issue
Customers on monthly plans report their invoices are occasionally short by one
day of proration — a full-month period (e.g. `2024-03-01` .. `2024-03-31`) is
being counted as fewer days than the month actually has. Day counts for
inclusive ranges should include the final day.

## Run tests
```
python3 tests/test_smoke.py
python3 tests/test_format.py
```
