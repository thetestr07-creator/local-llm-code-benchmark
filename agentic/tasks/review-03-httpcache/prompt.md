# Code review: find the boundary/validation bug in httpcache

`httpcache` is a small server-side HTTP caching / conditional-request / byte-range
library (see `README.md` and `docs/SPEC.md`). Pure stdlib.

Exactly ONE function in this repository has a **boundary/validation bug**: for a
specific edge input it accepts something it must reject (or returns the wrong
result at a boundary). Every other function is correct. The precise rules the
library must follow are written in `docs/SPEC.md`.

Finding it takes reading a couple of related modules (how a value is parsed in
one module vs. how it is validated/applied in another) and comparing the code
against `docs/SPEC.md`. The shipped tests in `tests/` all pass — they do not
exercise the exact boundary where the bug lives, so read the code, don't rely on
the suite.

## What to produce

Do NOT fix the code. Do NOT modify any file under `httpcache/`. Instead, write a
file named `findings.json` at the repository root with EXACTLY this shape:

```json
{"buggy_function": "<function_name>"}
```

`<function_name>` must be the single function that CONTAINS the defect, given as
one of these exact strings (the reviewable functions in this library):

- `parse_list`
- `parse_http_date`
- `parse_etag`
- `etag_matches`
- `if_none_match_passes`
- `if_match_passes`
- `response_age`
- `freshness_lifetime`
- `is_fresh`
- `vary_fields`
- `cache_key_with_vary`
- `evaluate_conditional`
- `parse_range_header`
- `_resolve`
- `apply_range`
- `request_cache_key`

Use the plain function name only (no module prefix, no parentheses). Name the
function where the faulty check actually lives, not merely a caller of it. Write
`findings.json` and then finish.
