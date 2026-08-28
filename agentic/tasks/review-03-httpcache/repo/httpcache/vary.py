"""Vary-aware cache keying."""
from .headers import parse_list


def vary_fields(response_headers):
    """Return the list of request-header names named by `Vary` (lowercased).

    A `Vary: *` means the response is uncacheable by a shared key; we surface it
    as the single token '*' so the caller can refuse to cache.
    """
    names = []
    for value in response_headers.get_all("Vary"):
        for tok in parse_list(value):
            names.append(tok.lower())
    return names


def cache_key_with_vary(base_key, request_headers, response_headers):
    """Extend `base_key` with the request values of each Vary'd header.

    If Vary is '*' the representation is not shareable; we return None to signal
    the caller must not store it under a shared key.
    """
    fields = vary_fields(response_headers)
    if "*" in fields:
        return None
    parts = [base_key]
    for name in sorted(set(fields)):
        parts.append("%s=%s" % (name, request_headers.get(name, "")))
    return "|".join(parts)
