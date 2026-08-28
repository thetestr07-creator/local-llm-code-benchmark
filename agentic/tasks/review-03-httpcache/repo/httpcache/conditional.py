"""Evaluate conditional requests into a status decision.

Returns one of: 200 (send full response), 304 (not modified), 412 (precondition
failed). Precedence follows RFC 7232: If-Match is evaluated before
If-None-Match.
"""
from .etags import if_none_match_passes, if_match_passes
from .datefmt import parse_http_date


def evaluate_conditional(request_headers, current_etag, last_modified_ts, method="GET"):
    """Decide the response status for a conditional request.

    - If `If-Match` is present and fails -> 412.
    - Else if `If-None-Match` is present and matches -> 304 (GET/HEAD) / 412.
    - Else if `If-Modified-Since` is present and the resource is not newer -> 304.
    - Otherwise -> 200.
    """
    if "If-Match" in request_headers:
        if not if_match_passes(request_headers.get("If-Match"), current_etag):
            return 412

    if "If-None-Match" in request_headers:
        if not if_none_match_passes(request_headers.get("If-None-Match"), current_etag):
            return 304 if method in ("GET", "HEAD") else 412
        return 200

    if "If-Modified-Since" in request_headers and method in ("GET", "HEAD"):
        since = parse_http_date(request_headers.get("If-Modified-Since"))
        if since is not None and last_modified_ts is not None:
            if last_modified_ts <= since:
                return 304

    return 200
