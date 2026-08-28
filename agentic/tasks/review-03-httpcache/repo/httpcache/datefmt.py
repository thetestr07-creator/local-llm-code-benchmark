"""RFC 7231 IMF-fixdate handling (the one preferred HTTP date format)."""
import calendar
import time

_IMF = "%a, %d %b %Y %H:%M:%S GMT"


def parse_http_date(text):
    """Parse an IMF-fixdate string into a POSIX timestamp (UTC), or None."""
    if not text:
        return None
    try:
        tm = time.strptime(text.strip(), _IMF)
    except ValueError:
        return None
    return calendar.timegm(tm)


def format_http_date(timestamp):
    """Format a POSIX timestamp as an IMF-fixdate string."""
    return time.strftime(_IMF, time.gmtime(timestamp))
