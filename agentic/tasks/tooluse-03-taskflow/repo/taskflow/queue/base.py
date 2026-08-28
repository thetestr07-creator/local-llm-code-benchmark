"""Queue interface. A queue orders jobs by their `scheduled_at` (earliest
first) so the scheduler always pops the job that is eligible soonest."""


class Queue:
    def push(self, job):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def empty(self):
        return len(self) == 0
