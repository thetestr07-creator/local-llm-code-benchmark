"""A minimal in-memory key/value collection used by the concrete stores."""
from ..errors import NotFound


class InMemoryCollection:
    def __init__(self):
        self._items = {}

    def put(self, key, value):
        self._items[key] = value
        return value

    def get(self, key):
        try:
            return self._items[key]
        except KeyError:
            raise NotFound("no item for key %r" % key)

    def get_or_none(self, key):
        return self._items.get(key)

    def has(self, key):
        return key in self._items

    def delete(self, key):
        self._items.pop(key, None)

    def all(self):
        return list(self._items.values())

    def keys(self):
        return list(self._items.keys())
