"""In-memory result store.

Keeps the last JobResult per job name and a running tally of attempts, so an
application can inspect outcomes after `engine.run()` returns. This is a plain
key/value record; it does not participate in scheduling or backoff.
"""


class InMemoryStore:
    def __init__(self):
        self._results = {}
        self._attempts = {}

    def record_attempt(self, name):
        self._attempts[name] = self._attempts.get(name, 0) + 1

    def save_result(self, result):
        self._results[result.name] = result

    def get_result(self, name):
        return self._results.get(name)

    def attempts(self, name):
        return self._attempts.get(name, 0)
