"""A tiny synchronous event bus.

The engine publishes named events ("job.start", "job.retry", "job.success",
"job.failure") with a payload dict. Subscribers are called in registration
order. Handlers must not raise; exceptions are swallowed so observability can
never break job execution.
"""


class EventBus:
    def __init__(self):
        self._subs = {}
        self.log = []   # records (event, payload) for inspection/testing

    def subscribe(self, event, handler):
        self._subs.setdefault(event, []).append(handler)

    def publish(self, event, payload=None):
        payload = payload or {}
        self.log.append((event, dict(payload)))
        for h in self._subs.get(event, []):
            try:
                h(payload)
            except Exception:
                pass

    def count(self, event):
        return sum(1 for e, _ in self.log if e == event)
