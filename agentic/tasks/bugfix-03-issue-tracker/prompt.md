The `tracker` package is a small in-memory issue tracker with three layers: pure
domain models (`tracker/domain`), a service layer over an in-memory store
(`tracker/service`), and a text command front end (`tracker/interface`).

New issues can be created from a **template** (for example the `bug` template),
which supplies a default priority and a starter set of labels such as `bug` and
`needs-triage`. Each issue is supposed to own its own labels: adding or removing
a label on one issue must never affect any other issue.

Teams are reporting a bug: when they create several issues from the *same*
template and then add a label to one of them, that label mysteriously appears on
the other issues created from that template too. Labels applied to one issue are
leaking across into its siblings. Issues that were created independently should
have completely independent label lists.

Find and fix the bug so that each issue has its own independent labels and
mutating one issue's labels never affects another. Do not change any public
function, method, or class signatures, and keep the package importable. The bug
is reproducible through the service and the command router, not just the models.

You can run the existing tests with:
```
python3 tests/test_smoke.py
python3 tests/test_domain.py
python3 tests/test_interface.py
```
