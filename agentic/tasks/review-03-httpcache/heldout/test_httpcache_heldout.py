"""HELD-OUT verification for review-03-httpcache.

The planted bug lives in `_resolve` (httpcache/content.py): the satisfiability
check is `if first > length` where docs/SPEC.md requires `first >= length`
(the last valid offset is length-1, so a `first` equal to `length` is one past
the end and must be HTTP 416). Because of the off-by-one, a range like
`bytes=L-` on an L-byte body wrongly slices to an empty body instead of raising
RangeNotSatisfiable. The correct byte-range PARSER in ranges.py is a distractor.

The model must name `_resolve`. This test only inspects the model's verdict
file; it does not import the repo. Pure stdlib. Deterministic.
"""
import os
import json

BUGGY = "_resolve"
ALLOWED = {
    "parse_list", "parse_http_date", "parse_etag", "etag_matches",
    "if_none_match_passes", "if_match_passes",
    "response_age", "freshness_lifetime", "is_fresh",
    "vary_fields", "cache_key_with_vary",
    "evaluate_conditional",
    "parse_range_header", "_resolve", "apply_range",
    "request_cache_key",
}

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
findings_path = os.path.join(repo, "findings.json")

if not os.path.exists(findings_path):
    raise AssertionError("findings.json was not created at the repo root")

with open(findings_path, encoding="utf-8") as fh:
    data = json.load(fh)

if not isinstance(data, dict):
    raise AssertionError("findings.json must contain a JSON object, got %r" % type(data).__name__)

name = data.get("buggy_function")

if name not in ALLOWED:
    raise AssertionError(
        "buggy_function %r is not one of the allowed function names %s"
        % (name, sorted(ALLOWED))
    )

if name != BUGGY:
    raise AssertionError("identified %r, expected %r" % (name, BUGGY))

print("HELDOUT_OK")
