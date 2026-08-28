"""Small formatting helpers for dates and ranges."""


def iso(day):
    """Render a date as 'YYYY-MM-DD'."""
    return day.isoformat()


def describe_range(dates):
    """Human summary of a list of dates, e.g. '2024-03-01 .. 2024-03-03 (3 days)'."""
    if not dates:
        return "(empty range)"
    if len(dates) == 1:
        return "%s (1 day)" % iso(dates[0])
    return "%s .. %s (%d days)" % (iso(dates[0]), iso(dates[-1]), len(dates))
