"""Interface/parser tests that pass on the current code."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tracker.interface.parser import parse
from tracker.interface.router import CommandRouter
from tracker.interface.cli import run

verb, args, opts = parse('new "hello world" --template bug --label urgent --label ui')
assert verb == "new"
assert args == ["hello world"]
assert opts["template"] == "bug"
assert opts["label"] == ["urgent", "ui"]

router = CommandRouter()
out = run([
    'new "first" --template feature',
    'status ISSUE-1 in_progress',
    'comment ISSUE-1 bob works now',
    'show ISSUE-1',
], router=router)
assert any("created ISSUE-1" in line for line in out)
assert any("status=in_progress" in line for line in out)
assert any("comment" in line for line in out)

print("interface OK")
