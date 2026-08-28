"""Validate a resolved config against a schema.

This runs AFTER all layers are merged. It walks the schema and checks that
declared leaf fields, when present, have a compatible type. It does not add,
remove, or combine keys — validation is read-only.
"""
from .errors import ValidationError


def validate(config, schema):
    _walk(config, schema, path="")
    return config


def _walk(cfg, schema, path):
    for name, spec in schema.items():
        if name not in cfg:
            continue
        here = path + "." + name if path else name
        val = cfg[name]
        if isinstance(spec, dict):
            if not isinstance(val, dict):
                raise ValidationError("%s should be a section" % here)
            _walk(val, spec, here)
        else:
            if spec is int and isinstance(val, bool):
                raise ValidationError("%s should be %s" % (here, spec.__name__))
            if not isinstance(val, spec):
                raise ValidationError("%s should be %s" % (here, spec.__name__))
