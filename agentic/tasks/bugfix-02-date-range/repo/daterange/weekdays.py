"""Helpers for counting and filtering weekdays within an inclusive range."""
from .core import date_range

# Monday is 0 ... Sunday is 6 (matches datetime.date.weekday()).
_WEEKEND = {5, 6}


def weekdays_in_range(start, end):
    """List of dates in the inclusive range that fall on Mon-Fri."""
    return [d for d in date_range(start, end) if d.weekday() not in _WEEKEND]


def count_weekdays(start, end):
    """Number of Mon-Fri days in the inclusive range."""
    return len(weekdays_in_range(start, end))


def count_weekends(start, end):
    """Number of Sat/Sun days in the inclusive range."""
    return sum(1 for d in date_range(start, end) if d.weekday() in _WEEKEND)
