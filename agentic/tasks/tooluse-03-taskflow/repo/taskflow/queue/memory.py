"""In-memory priority queue ordered by (scheduled_at, insertion order).

A stable tiebreaker keeps ordering deterministic when two jobs share the same
scheduled time. This backend is pure data-structure plumbing and has no notion
of retries or delays — it just returns whatever job is due next.
"""
import heapq
from .base import Queue


class InMemoryQueue(Queue):
    def __init__(self):
        self._heap = []
        self._seq = 0

    def push(self, job):
        heapq.heappush(self._heap, (job.scheduled_at, self._seq, job))
        self._seq += 1

    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty queue")
        _at, _seq, job = heapq.heappop(self._heap)
        return job

    def peek(self):
        return self._heap[0][2] if self._heap else None

    def __len__(self):
        return len(self._heap)
