"""Highest-priority source: environment variables.

Variables are namespaced with a prefix and use a double-underscore path
separator, e.g. with prefix "APP" the variable `APP__DB__HOST=db1` becomes
`{"db": {"host": "db1"}}`. Values are type-coerced. Because env is the
top layer, anything it sets should override the file and defaults layers —
while leaving untouched sibling keys from lower layers intact.
"""
from ..util.flatten import unflatten
from ..util.coerce import coerce_tree


class EnvSource:
    priority = 100

    def __init__(self, environ, prefix="APP", sep="__"):
        self._environ = dict(environ)
        self._prefix = prefix
        self._sep = sep

    def load(self):
        pfx = self._prefix + self._sep
        flat = {}
        for key, val in self._environ.items():
            if not key.startswith(pfx):
                continue
            path = key[len(pfx):].lower().replace(self._sep, ".")
            flat[path] = val
        nested = unflatten(flat, sep=".")
        return coerce_tree(nested)
