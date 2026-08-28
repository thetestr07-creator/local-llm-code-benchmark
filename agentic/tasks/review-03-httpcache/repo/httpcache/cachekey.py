"""Normalize a request into a base cache key.

Only safe, cacheable methods (GET/HEAD) are keyed. The key combines the method,
a normalized URL, and any Vary'd request headers (delegated to `vary`).
"""
from .vary import cache_key_with_vary


def _normalize_url(url):
    """Lowercase the scheme+host and drop a trailing '?' with no query."""
    url = url.strip()
    if url.endswith("?"):
        url = url[:-1]
    scheme, sep, rest = url.partition("://")
    if not sep:
        return url
    host, slash, path = rest.partition("/")
    return scheme.lower() + "://" + host.lower() + slash + path


def request_cache_key(method, url, request_headers, response_headers):
    """Return a shared cache key string, or None if the request is uncacheable."""
    if method not in ("GET", "HEAD"):
        return None
    base = "%s %s" % (method.upper(), _normalize_url(url))
    return cache_key_with_vary(base, request_headers, response_headers)
