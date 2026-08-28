"""The Issue aggregate."""
from .enums import Status, Priority, VALID_STATUSES, VALID_PRIORITIES, DONE_STATUSES


class Issue:
    """A single tracked issue.

    `labels` is a per-issue list of string tags that the issue then owns and
    mutates in place. Whatever list is passed in becomes this issue's list, so
    callers are responsible for handing each issue its own list. Mutating one
    issue's labels must never affect another issue.
    """

    def __init__(self, issue_id, title, priority=Priority.MEDIUM, labels=None):
        if priority not in VALID_PRIORITIES:
            raise ValueError("bad priority: %r" % (priority,))
        self.id = issue_id
        self.title = title
        self.priority = priority
        self.status = Status.OPEN
        # The issue adopts the caller-provided list as its own mutable state.
        self.labels = labels if labels is not None else []
        self.comments = []

    def add_label(self, label):
        """Attach a label if not already present. Mutates this issue's list."""
        if label not in self.labels:
            self.labels.append(label)
        return self.labels

    def remove_label(self, label):
        if label in self.labels:
            self.labels.remove(label)
        return self.labels

    def add_comment(self, author, text):
        self.comments.append({"author": author, "text": text})
        return len(self.comments)

    def set_status(self, status):
        if status not in VALID_STATUSES:
            raise ValueError("bad status: %r" % (status,))
        self.status = status

    def is_done(self):
        return self.status in DONE_STATUSES

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "status": self.status,
            "labels": list(self.labels),
            "comments": list(self.comments),
        }

    def __repr__(self):
        return "<Issue %s %r [%s/%s] labels=%s>" % (
            self.id, self.title, self.priority, self.status, self.labels)
