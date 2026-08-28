"""daterange — small utilities for working with inclusive calendar date ranges.

Public API:
    parse_date(s)                 -> datetime.date
    date_range(start, end)        -> list[date]   (INCLUSIVE of both endpoints)
    days_in_range(start, end)     -> int          (count of days, endpoints inclusive)
    BillingPeriod(start, end)     -> object with .days() and .contains(day)
"""
from .core import parse_date, date_range, days_in_range
from .billing import BillingPeriod

__all__ = ["parse_date", "date_range", "days_in_range", "BillingPeriod"]
