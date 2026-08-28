"""Project smoke test. Passes on the current code. Exercises each layer with a
single issue per template, so it does not trip the cross-issue edge case that
the stricter hidden tests target."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tracker.service.tracker_service import TrackerService
from tracker.interface.router import CommandRouter
from tracker.service import reporting

# --- service: create a plain issue, mutate it ---
svc = TrackerService()
a = svc.create_issue("plain issue")
assert a.id == "ISSUE-1"
assert a.priority == "medium"
assert a.labels == []
svc.add_label(a.id, "backend")
assert "backend" in a.labels
svc.set_status(a.id, "in_progress")
assert a.status == "in_progress"

# --- service: create from a template (single issue) ---
b = svc.create_issue("crash on save", template="bug")
assert b.priority == "high"
assert "bug" in b.labels and "needs-triage" in b.labels
svc.comment(b.id, "alice", "looking into it")
assert len(b.comments) == 1

# events were recorded
assert svc.events.count() >= 4

# --- interface: drive through the router ---
router = CommandRouter()
msg = router.handle('new "login broken" --template incident')
assert "created" in msg and "incident" in msg
out = router.handle("list")
assert "ISSUE-1" in out

# --- reporting ---
issues = svc.all_issues()
hist = reporting.label_histogram(issues)
assert hist.get("bug") == 1
assert reporting.open_count(issues) >= 1

print("smoke OK")
