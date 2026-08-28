"""Case-insensitive header container and comma-list parsing."""


class Headers:
    """A minimal case-insensitive multi-map for HTTP headers."""

    def __init__(self, items=None):
        self._store = {}  # lower_name -> (original_name, [values])
        if items:
            for name, value in (items.items() if hasattr(items, "items") else items):
                self.add(name, value)

    def add(self, name, value):
        key = name.lower()
        if key in self._store:
            self._store[key][1].append(value)
        else:
            self._store[key] = (name, [value])

    def get(self, name, default=None):
        entry = self._store.get(name.lower())
        if not entry:
            return default
        return entry[1][0]

    def get_all(self, name):
        entry = self._store.get(name.lower())
        return list(entry[1]) if entry else []

    def __contains__(self, name):
        return name.lower() in self._store

    def __repr__(self):
        return "Headers(%r)" % {v[0]: v[1] for v in self._store.values()}


def parse_list(value):
    """Split a comma-separated header value into trimmed, non-empty tokens."""
    if value is None:
        return []
    return [tok.strip() for tok in value.split(",") if tok.strip()]
