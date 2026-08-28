"""HELD-OUT verification for review-01. The bug: can_edit uses `!=` (grants edit to
every NON-owner) where it must use `==`. The model must name can_edit."""
import sys, os, json

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
findings_path = os.path.join(repo, "findings.json")
assert os.path.exists(findings_path), "findings.json was not created at the repo root"
data = json.load(open(findings_path))
assert data.get("buggy_function") == "can_edit", "identified %r, expected 'can_edit'" % data.get("buggy_function")

# sanity: roles.py must be unmodified in behaviour signature (not "fixed" — this is review only)
print("HELDOUT_OK")
