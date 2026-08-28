"""A simple append-only event log for auditing service actions."""


class EventLog:
    def __init__(self):
        self._events = []

    def record(self, kind, **data):
        entry = {"kind": kind}
        entry.update(data)
        self._events.append(entry)
        return entry

    def all(self):
        return list(self._events)

    def of_kind(self, kind):
        return [e for e in self._events if e["kind"] == kind]

    def count(self):
        return len(self._events)
