"""Job and JobResult value objects.

A Job pairs a registered task name with its arguments and carries bookkeeping
the engine mutates as it retries: `attempt` (0-based count of attempts already
made) and `scheduled_at` (virtual clock time the job is eligible to run).
"""


class Job:
    def __init__(self, name, args=None, kwargs=None, max_attempts=3):
        self.name = name
        self.args = tuple(args or ())
        self.kwargs = dict(kwargs or {})
        self.max_attempts = max_attempts
        self.attempt = 0          # attempts already completed
        self.scheduled_at = 0.0   # virtual-clock eligibility time
        self.history = []         # list of (attempt, delay) actually scheduled

    def __repr__(self):
        return "Job(%r, attempt=%d/%d)" % (self.name, self.attempt, self.max_attempts)


class JobResult:
    def __init__(self, name, ok, value=None, error=None, attempts=0):
        self.name = name
        self.ok = ok
        self.value = value
        self.error = error
        self.attempts = attempts

    def __repr__(self):
        state = "ok" if self.ok else "failed"
        return "JobResult(%r, %s, attempts=%d)" % (self.name, state, self.attempts)
