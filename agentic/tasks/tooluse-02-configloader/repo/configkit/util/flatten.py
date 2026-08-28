"""Flatten / unflatten nested mappings using dotted key paths.

Used by the env source to turn `APP__DB__HOST` style variables into nested
config, and by diagnostics to render a config as flat `a.b.c = v` lines.
"""


def flatten(d, prefix="", sep="."):
    out = {}
    for k, v in d.items():
        key = prefix + sep + k if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key, sep))
        else:
            out[key] = v
    return out


def unflatten(flat, sep="."):
    root = {}
    for key, val in flat.items():
        parts = key.split(sep)
        node = root
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = val
    return root
