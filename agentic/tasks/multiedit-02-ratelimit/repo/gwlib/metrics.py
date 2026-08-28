"""A very small in-memory counter store for observability."""


class Metrics:
    def __init__(self):
        self._counts = {}

    def incr(self, name, by=1):
        self._counts[name] = self._counts.get(name, 0) + by

    def get(self, name):
        return self._counts.get(name, 0)

    def snapshot(self):
        return dict(self._counts)
