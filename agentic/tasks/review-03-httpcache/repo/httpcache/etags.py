"""ETag parsing and conditional-match logic (If-None-Match / If-Match)."""
from .headers import parse_list


def parse_etag(raw):
    """Parse one ETag token into (is_weak, opaque_value).

    A weak tag is prefixed with W/. The opaque value keeps its surrounding
    double quotes stripped.
    """
    raw = raw.strip()
    weak = False
    if raw.startswith("W/"):
        weak = True
        raw = raw[2:].strip()
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        raw = raw[1:-1]
    return weak, raw


def etag_matches(a, b, strong=True):
    """Compare two raw ETag tokens.

    Strong comparison: both must be strong and their opaque values equal.
    Weak comparison: opaque values equal regardless of weakness.
    """
    wa, va = parse_etag(a)
    wb, vb = parse_etag(b)
    if strong and (wa or wb):
        return False
    return va == vb


def if_none_match_passes(header_value, current_etag):
    """Return True if the request should proceed (i.e. NOT a 304).

    `If-None-Match: *` matches any existing representation, so it fails (304)
    when a current ETag exists. Otherwise the request is a 304 iff the current
    ETag weakly matches one of the listed tags.
    """
    tokens = parse_list(header_value)
    if not tokens:
        return True
    if "*" in tokens:
        return current_etag is None
    for tok in tokens:
        if etag_matches(tok, current_etag, strong=False):
            return False
    return True


def if_match_passes(header_value, current_etag):
    """Return True if the precondition holds (else the caller should send 412).

    `If-Match: *` holds iff a representation exists. Otherwise it holds iff the
    current ETag strongly matches one of the listed tags.
    """
    tokens = parse_list(header_value)
    if not tokens:
        return True
    if "*" in tokens:
        return current_etag is not None
    for tok in tokens:
        if etag_matches(tok, current_etag, strong=True):
            return True
    return False
