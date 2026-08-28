"""A tiny INI-ish parser (distinct from merging).

Turns lines like:

    [db]
    host = localhost
    port = 5432

into a nested mapping {"db": {"host": "localhost", "port": "5432"}}. This is
one way to *produce* a source dict; it has nothing to do with how layers are
combined. Values stay as strings — coercion happens later in the pipeline.
"""


def parse_ini(text):
    root = {}
    section = root
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            name = line[1:-1].strip()
            section = root.setdefault(name, {})
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            section[k.strip()] = v.strip()
    return root
