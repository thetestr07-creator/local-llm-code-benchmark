"""Domain-level tests that pass on the current code. These check a single Issue
in isolation and the template's *contents* (not cross-issue independence)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tracker.domain.issue import Issue
from tracker.domain.templates import get_template, BUILTIN_TEMPLATES
from tracker.domain.enums import Status, Priority

# a single issue owns and mutates its label list
issue = Issue("X-1", "title", Priority.LOW, ["a"])
issue.add_label("b")
issue.add_label("a")  # dedup
assert issue.labels == ["a", "b"]
issue.remove_label("a")
assert issue.labels == ["b"]

# status transitions validate
issue.set_status(Status.RESOLVED)
assert issue.is_done()

# templates expose the expected starter labels
bug = get_template("bug")
prio, labels = bug.defaults()
assert prio == Priority.HIGH
assert labels == ["bug", "needs-triage"]
assert set(BUILTIN_TEMPLATES) == {"bug", "feature", "chore", "incident"}

print("domain OK")
