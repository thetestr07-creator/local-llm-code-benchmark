# tracker

A tiny in-memory issue tracker, split into three layers so the pieces stay
testable in isolation:

```
tracker/
  domain/       pure data models
    enums.py        Status / Priority vocabularies
    issue.py        the Issue aggregate (title, priority, status, labels, comments)
    templates.py    IssueTemplate + BUILTIN_TEMPLATES (bug/feature/chore/incident)
  service/      business logic over an in-memory store
    store.py        InMemoryStore (id generation + lookup)
    events.py       append-only EventLog
    validators.py   input validation
    tracker_service.py  TrackerService facade (create/label/status/comment)
    reporting.py    label histograms, status counts, etc.
  interface/    text command front end
    parser.py       parse a command line into (verb, args, options)
    router.py       CommandRouter dispatches to the service
    cli.py          batch/REPL over the router
tests/          smoke + per-layer tests
```

## Templates
New issues can be stamped from a template, which supplies a default priority and
a starter set of labels. The `bug` template, for instance, gives every new issue
the labels `bug` and `needs-triage`. Each new issue gets its own labels to work
with — labeling one issue must never change another.

## Known issue
Teams that file several issues from the same template report "ghost" labels:
after they add a label to one issue, the same label mysteriously shows up on
*other* issues created from that template. Labels applied to one issue are
bleeding across into sibling issues.

## Run tests
```
python3 tests/test_smoke.py
python3 tests/test_domain.py
python3 tests/test_interface.py
```
