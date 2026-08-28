"""Issue templates.

A template is a reusable preset (priority + a starter set of labels) that new
issues are stamped from. For example the "bug" template starts every new issue
with the labels ["bug", "needs-triage"].

Because the same template is used to create many issues, a template must hand
each new issue a *fresh* copy of its starter labels. If two issues ended up
sharing one label list, adding a label to one would leak into the other.
"""
from .enums import Priority


class IssueTemplate:
    def __init__(self, name, priority, default_labels):
        self.name = name
        self.priority = priority
        # canonical starter labels for this template (never handed out directly)
        self._default_labels = list(default_labels)

    def starter_labels(self):
        """Return the starter labels to seed a new issue with.

        Each caller gets an independent list it is free to mutate.
        """
        return self._default_labels

    def defaults(self):
        """Return (priority, starter_labels) for a new issue from this template."""
        return self.priority, self.starter_labels()


BUILTIN_TEMPLATES = {
    "bug": IssueTemplate("bug", Priority.HIGH, ["bug", "needs-triage"]),
    "feature": IssueTemplate("feature", Priority.MEDIUM, ["feature"]),
    "chore": IssueTemplate("chore", Priority.LOW, ["chore"]),
    "incident": IssueTemplate("incident", Priority.CRITICAL, ["incident", "needs-triage"]),
}


def get_template(name):
    if name not in BUILTIN_TEMPLATES:
        raise KeyError("unknown template: %r" % (name,))
    return BUILTIN_TEMPLATES[name]
