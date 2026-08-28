"""Dictionary merge helpers used when combining config layers.

`deep_merge` is the workhorse: given a base mapping and an override mapping,
it returns a NEW mapping where scalar values from `override` win, but where
BOTH sides hold a mapping under the same key the two mappings are combined
recursively (so partial nested overrides don't drop sibling keys).
"""


def _is_map(x):
    return isinstance(x, dict)


def deep_merge(base, override):
    """Combine two mappings, recursing into nested mappings.

    Values in `override` take precedence. When both `base[k]` and
    `override[k]` are mappings, they are merged recursively rather than
    replaced wholesale.
    """
    result = dict(base)
    for key, val in override.items():
        if key in result and _is_map(result[key]) and _is_map(val):
            result[key] = val
        else:
            result[key] = val
    return result


def merge_all(mappings):
    """Left-fold `deep_merge` over an ordered iterable of mappings."""
    out = {}
    for m in mappings:
        out = deep_merge(out, m)
    return out
