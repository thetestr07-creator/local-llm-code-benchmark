"""A trivial in-memory response cache keyed by cache-key string."""


class ResponseStore:
    def __init__(self):
        self._entries = {}  # key -> (headers, body, stored_at)

    def put(self, key, headers, body, stored_at):
        if key is None:
            return False
        self._entries[key] = (headers, body, stored_at)
        return True

    def get(self, key):
        return self._entries.get(key)

    def invalidate(self, key):
        self._entries.pop(key, None)

    def __len__(self):
        return len(self._entries)
