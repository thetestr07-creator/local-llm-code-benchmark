# httpcache

A small, dependency-free toolkit for the server side of HTTP caching and
conditional/range requests. Pure stdlib.

Modules (`httpcache/`):

- `headers.py`     — case-insensitive header container + comma-list parsing.
- `datefmt.py`     — RFC 7231 IMF-fixdate parsing/formatting.
- `etags.py`       — ETag parsing and `If-None-Match` / `If-Match` comparison.
- `freshness.py`   — response age and freshness (`max-age`, `Age`, `Expires`).
- `vary.py`        — `Vary`-aware cache-key construction.
- `conditional.py` — evaluate conditional requests into a 200/304/412 decision.
- `ranges.py`      — parse a `Range: bytes=...` header into byte ranges.
- `content.py`     — apply a parsed byte range to a representation body.
- `cachekey.py`    — normalize a request into a cache key.
- `store.py`       — a trivial in-memory response cache.

See `docs/SPEC.md` for the precise byte-range rules this library follows.
