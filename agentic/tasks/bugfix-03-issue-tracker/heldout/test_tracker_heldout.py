"""HELD-OUT verification for bugfix-03. The model under test never sees this file.
Decides pass/fail deterministically. Issues created from the same template must
have INDEPENDENT label lists; mutating one must not affect another."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tracker.service.tracker_service import TrackerService
from tracker.interface.router import CommandRouter
from tracker.service import reporting

# ---------------------------------------------------------------------------
# 1) Through the SERVICE: two issues from the same template are independent.
# ---------------------------------------------------------------------------
svc = TrackerService()
a = svc.create_issue("first bug", template="bug")
b = svc.create_issue("second bug", template="bug")

# both start with the template's starter labels
assert sorted(a.labels) == ["bug", "needs-triage"], a.labels
assert sorted(b.labels) == ["bug", "needs-triage"], b.labels

# the two lists must not be the same object
assert a.labels is not b.labels, "issues share the same label list object"

# add a label to A only
svc.add_label(a.id, "backend")
assert "backend" in a.labels
assert "backend" not in b.labels, "label leaked from A into B (%r)" % (b.labels,)

# remove a starter label from B only
b.remove_label("needs-triage")
assert "needs-triage" not in b.labels
assert "needs-triage" in a.labels, "removal on B affected A (%r)" % (a.labels,)

# ---------------------------------------------------------------------------
# 2) The template itself must not be corrupted by issue mutations.
# ---------------------------------------------------------------------------
from tracker.domain.templates import get_template
tmpl = get_template("bug")
_, fresh = tmpl.defaults()
assert sorted(fresh) == ["bug", "needs-triage"], (
    "template starter labels got mutated: %r" % (fresh,))
# a brand-new issue still gets the clean starter set
c = svc.create_issue("third bug", template="bug")
assert sorted(c.labels) == ["bug", "needs-triage"], c.labels

# ---------------------------------------------------------------------------
# 3) Through the ROUTER / CLI path: same guarantee end to end.
# ---------------------------------------------------------------------------
router = CommandRouter()
router.handle('new "alpha" --template incident')   # ISSUE-1
router.handle('new "beta" --template incident')    # ISSUE-2
router.handle("label ISSUE-1 hotfix")

i1 = router.service.get_issue("ISSUE-1")
i2 = router.service.get_issue("ISSUE-2")
assert "hotfix" in i1.labels
assert "hotfix" not in i2.labels, "router path leaked label across issues (%r)" % (i2.labels,)

# reporting over the router's issues counts hotfix exactly once
hist = reporting.label_histogram(router.service.all_issues())
assert hist.get("hotfix") == 1, hist
assert hist.get("incident") == 2, hist

print("HELDOUT_OK")
