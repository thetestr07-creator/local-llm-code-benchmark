"""Engine: drive jobs to completion.

Wires together a queue, scheduler, executor, virtual clock, event bus and result
store. `submit` enqueues a job; `run` processes the queue until it is empty,
executing each due job and, on failure, letting the scheduler apply the retry
policy. Successful or permanently-failed jobs produce a JobResult in the store.

    engine = Engine(policy=RetryPolicy(max_attempts=5, base_delay=1, max_delay=30))
    engine.submit(Job("flaky"))
    result = engine.run()

The engine records the virtual timeline of retries so callers can audit exactly
when each attempt was scheduled.
"""
from .job import JobResult
from .clock import VirtualClock
from .scheduler import Scheduler
from .executor import Executor
from ..queue import InMemoryQueue
from ..store import InMemoryStore
from ..observe import EventBus
from ..policy import RetryPolicy


class Engine:
    def __init__(self, policy=None, queue=None, clock=None, store=None,
                 events=None, middlewares=None):
        self.policy = policy or RetryPolicy()
        self.queue = queue or InMemoryQueue()
        self.clock = clock or VirtualClock()
        self.store = store or InMemoryStore()
        self.events = events or EventBus()
        self.executor = Executor(middlewares=middlewares)
        self.scheduler = Scheduler(self.queue, self.policy, self.clock)
        self.timeline = []   # (name, attempt, scheduled_at) as jobs run

    def submit(self, job):
        self.scheduler.submit(job)
        self.events.publish("job.submit", {"name": job.name})
        return self

    def run(self):
        last = None
        while self.scheduler.has_work():
            job = self.scheduler.next_due()
            self.timeline.append((job.name, job.attempt, job.scheduled_at))
            self.store.record_attempt(job.name)
            self.events.publish("job.start", {"name": job.name, "attempt": job.attempt})
            outcome = self.executor.run_once(job)
            if outcome.ok:
                res = JobResult(job.name, True, value=outcome.value, attempts=job.attempt + 1)
                self.store.save_result(res)
                self.events.publish("job.success", {"name": job.name})
                last = res
                continue
            requeued = self.scheduler.on_failure(job, outcome.error)
            if requeued:
                self.events.publish("job.retry", {"name": job.name, "attempt": job.attempt})
            else:
                res = JobResult(job.name, False, error=outcome.error, attempts=job.attempt + 1)
                self.store.save_result(res)
                self.events.publish("job.failure", {"name": job.name})
                last = res
        return last
