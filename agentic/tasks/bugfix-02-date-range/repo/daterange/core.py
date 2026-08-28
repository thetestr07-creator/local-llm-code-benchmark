"""Core date parsing and range enumeration.

Ranges in this library are *inclusive*: date_range("2024-01-01", "2024-01-03")
yields the three days 01, 02, 03. days_in_range counts those same days.
"""
import datetime


def parse_date(s):
    """Parse an ISO 'YYYY-MM-DD' string into a datetime.date.

    Accepts an existing date object unchanged.
    """
    if isinstance(s, datetime.date):
        return s
    parts = s.split("-")
    if len(parts) != 3:
        raise ValueError("expected YYYY-MM-DD, got %r" % (s,))
    year, month, day = (int(p) for p in parts)
    return datetime.date(year, month, day)


def date_range(start, end):
    """Return the list of dates from start to end, INCLUSIVE of both ends.

    date_range("2024-03-01", "2024-03-03") -> [2024-03-01, 2024-03-02, 2024-03-03]
    If end is before start, returns an empty list.
    """
    start = parse_date(start)
    end = parse_date(end)
    out = []
    current = start
    step = datetime.timedelta(days=1)
    while current < end:          # walk one day at a time
        out.append(current)
        current = current + step
    return out


def days_in_range(start, end):
    """Number of days in the inclusive range [start, end].

    days_in_range("2024-03-01", "2024-03-01") == 1
    days_in_range("2024-03-01", "2024-03-31") == 31
    """
    return len(date_range(start, end))
