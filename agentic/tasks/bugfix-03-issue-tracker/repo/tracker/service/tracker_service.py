"""The TrackerService facade: creates and mutates issues via the store, records
events, and enforces validation. This is the seam the CLI/router talks to."""
from ..domain.issue import Issue
from ..domain.templates import get_template
from .store import InMemoryStore
from .events import EventLog
from . import validators


class TrackerError(Exception):
    pass


class TrackerService:
    def __init__(self, store=None, events=None):
        self.store = store or InMemoryStore()
        self.events = events or EventLog()

    # ---- creation ---------------------------------------------------------
    def create_issue(self, title, priority=None, labels=None, template=None):
        """Create and store a new issue.

        If `template` is given, the new issue is seeded from that template's
        priority and starter labels. Any explicit `labels` are added on top.
        """
        title = validators.validate_title(title)

        if template is not None:
            tmpl = get_template(template)
            tmpl_priority, seed_labels = tmpl.defaults()
            eff_priority = priority or tmpl_priority
        else:
            eff_priority = priority or "medium"
            seed_labels = list(labels) if labels else []

        eff_priority = validators.validate_priority(eff_priority)

        issue = Issue(self.store.next_id(), title, eff_priority, seed_labels)

        # explicit labels (from the caller) are layered on top of the template
        if template is not None and labels:
            for lab in labels:
                issue.add_label(validators.normalize_label(lab))

        self.store.put(issue)
        self.events.record("issue_created", id=issue.id, template=template)
        return issue

    # ---- lookups ----------------------------------------------------------
    def get_issue(self, issue_id):
        issue = self.store.get(issue_id)
        if issue is None:
            raise TrackerError("no such issue: %s" % issue_id)
        return issue

    def all_issues(self):
        return self.store.all()

    # ---- mutations --------------------------------------------------------
    def add_label(self, issue_id, label):
        issue = self.get_issue(issue_id)
        label = validators.normalize_label(label)
        issue.add_label(label)
        self.events.record("label_added", id=issue_id, label=label)
        return issue

    def set_status(self, issue_id, status):
        issue = self.get_issue(issue_id)
        status = validators.validate_status(status)
        issue.set_status(status)
        self.events.record("status_changed", id=issue_id, status=status)
        return issue

    def comment(self, issue_id, author, text):
        issue = self.get_issue(issue_id)
        n = issue.add_comment(author, text)
        self.events.record("commented", id=issue_id, author=author)
        return n
