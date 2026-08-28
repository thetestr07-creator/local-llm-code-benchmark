"""Response age and freshness-lifetime computation."""
from .datefmt import parse_http_date


def response_age(headers, now, response_time):
    """Estimate a cached response's current age in seconds.

    Uses the explicit `Age` header if present, plus the time elapsed since the
    response was received (`now - response_time`). Never negative.
    """
    age = 0
    age_header = headers.get("Age")
    if age_header is not None:
        try:
            age = max(0, int(age_header.strip()))
        except ValueError:
            age = 0
    resident = now - response_time
    if resident < 0:
        resident = 0
    return age + resident


def freshness_lifetime(headers, date_time=None):
    """Compute how long (seconds) the response stays fresh.

    Prefers `Cache-Control: max-age`; falls back to `Expires - Date`. Returns 0
    if neither is available (i.e. treat as stale and revalidate).
    """
    cc = headers.get("Cache-Control")
    if cc:
        for token in cc.split(","):
            token = token.strip().lower()
            if token.startswith("max-age="):
                try:
                    return max(0, int(token[len("max-age="):]))
                except ValueError:
                    return 0
    expires = parse_http_date(headers.get("Expires"))
    if expires is not None:
        base = date_time if date_time is not None else parse_http_date(headers.get("Date"))
        if base is not None:
            return max(0, expires - base)
    return 0


def is_fresh(headers, now, response_time, date_time=None):
    """A response is fresh iff its age is strictly less than its lifetime."""
    return response_age(headers, now, response_time) < freshness_lifetime(headers, date_time)
