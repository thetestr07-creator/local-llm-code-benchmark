"""Scalar coercion helpers.

Environment variables arrive as strings; these helpers turn "true"/"42"/"3.5"
into real bools/ints/floats so downstream code sees typed values.
"""


def coerce_scalar(s):
    if not isinstance(s, str):
        return s
    low = s.strip().lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    try:
        return int(s)
    except (TypeError, ValueError):
        pass
    try:
        return float(s)
    except (TypeError, ValueError):
        pass
    return s


def coerce_tree(d):
    out = {}
    for k, v in d.items():
        out[k] = coerce_tree(v) if isinstance(v, dict) else coerce_scalar(v)
    return out
