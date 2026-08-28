"""Virtual clock so the engine is deterministic and never really sleeps.

Time only advances when the scheduler pops a job scheduled for the future: the
clock jumps forward to that job's scheduled_at. This lets tests assert on the
exact virtual delays the retry policy produced without wall-clock flakiness.
"""


class VirtualClock:
    def __init__(self, start=0.0):
        self._t = float(start)
        self._spans = []

    def now(self):
        return self._t

    def advance_to(self, t):
        if t > self._t:
            self._t = float(t)

    def advance_by(self, dt):
        self._t += float(dt)

    def record_span(self, dt):
        self._spans.append(dt)

    @property
    def spans(self):
        return list(self._spans)
