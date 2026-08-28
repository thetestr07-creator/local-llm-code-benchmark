"""Scheduler: turn a failed attempt into a future re-run.

After the executor reports a failure, the scheduler asks the retry policy two
questions: (1) should we retry this attempt? and (2) if so, what delay applies?
It then bumps the job's attempt counter and re-queues it with a new
`scheduled_at = now + delay`, advancing the virtual clock as jobs come due.

The scheduler is pure orchestration: it trusts the policy for the delay value
and the queue for ordering. It records each (attempt, delay) pair it schedules
onto the job's history for later inspection.
"""


class Scheduler:
    def __init__(self, queue, policy, clock):
        self._queue = queue
        self._policy = policy
        self._clock = clock

    def submit(self, job):
        job.scheduled_at = self._clock.now()
        self._queue.push(job)

    def next_due(self):
        """Pop the earliest job and advance the clock to its scheduled time."""
        job = self._queue.pop()
        self._clock.advance_to(job.scheduled_at)
        return job

    def on_failure(self, job, error):
        """Decide + enqueue a retry. Returns True if the job was re-queued."""
        if not self._policy.should_retry(job.attempt, error):
            return False
        delay = self._policy.next_delay(job.attempt)
        job.attempt += 1
        job.history.append((job.attempt, delay))
        job.scheduled_at = self._clock.now() + delay
        self._queue.push(job)
        return True

    def has_work(self):
        return not self._queue.empty()
