"""A trivial in-memory object store keyed by issue id."""


class InMemoryStore:
    def __init__(self):
        self._items = {}
        self._seq = 0

    def next_id(self):
        self._seq += 1
        return "ISSUE-%d" % self._seq

    def put(self, issue):
        self._items[issue.id] = issue
        return issue

    def get(self, issue_id):
        return self._items.get(issue_id)

    def all(self):
        # returns issues in insertion order (dict preserves it)
        return list(self._items.values())

    def count(self):
        return len(self._items)
