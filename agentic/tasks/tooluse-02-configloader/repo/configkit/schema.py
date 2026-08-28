"""Declarative schema description used by the validator.

A schema is a nested mapping of field-name -> type (or nested schema). This
module only *describes* expected shape; enforcement lives in validate.py.
"""

# Example schema an application might declare. Not used for merging.
DEFAULT_SCHEMA = {
    "db": {
        "host": str,
        "port": int,
        "pool": {
            "size": int,
            "timeout": int,
        },
    },
    "cache": {
        "backend": str,
        "ttl": int,
    },
    "debug": bool,
}


def field_paths(schema, prefix=""):
    """Yield dotted paths of leaf fields declared by a schema."""
    for name, spec in schema.items():
        path = prefix + "." + name if prefix else name
        if isinstance(spec, dict):
            yield from field_paths(spec, path)
        else:
            yield path
