"""Resolve multiple config sources into one effective configuration.

The resolver orders sources by their `.priority` (ascending) and merges each
layer on top of the accumulated result. Merging is delegated to the shared
`deep_merge` utility so that nested sections combine instead of replacing one
another. The resolver itself only handles ordering and optional validation.
"""
from .util.merge import merge_all
from .validate import validate as _validate


class Resolver:
    def __init__(self, sources=None):
        self._sources = list(sources or [])

    def add(self, source):
        self._sources.append(source)
        return self

    def _ordered_layers(self):
        ordered = sorted(self._sources, key=lambda s: getattr(s, "priority", 0))
        return [s.load() for s in ordered]

    def resolve(self, schema=None):
        merged = merge_all(self._ordered_layers())
        if schema is not None:
            _validate(merged, schema)
        return merged


def load_config(sources, schema=None):
    """Convenience wrapper: build a Resolver and resolve in one call."""
    return Resolver(sources).resolve(schema=schema)
