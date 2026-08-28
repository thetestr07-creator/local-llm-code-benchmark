"""Route parsed commands to the TrackerService and render text results."""
from ..service.tracker_service import TrackerService, TrackerError
from ..service import reporting
from .parser import parse


class RouterError(Exception):
    pass


class CommandRouter:
    def __init__(self, service=None):
        self.service = service or TrackerService()

    def handle(self, line):
        """Handle one command line, return a text response."""
        try:
            verb, args, options = parse(line)
        except ValueError as e:
            raise RouterError("parse error: %s" % e)

        method = getattr(self, "_cmd_" + verb, None)
        if method is None:
            raise RouterError("unknown command: %s" % verb)
        try:
            return method(args, options)
        except (TrackerError, ValueError) as e:
            raise RouterError(str(e))

    # ---- commands ---------------------------------------------------------
    def _cmd_new(self, args, options):
        if not args:
            raise ValueError("new requires a title")
        title = args[0]
        template = options.get("template")
        priority = options.get("priority")
        labels = options.get("label")  # list or None
        issue = self.service.create_issue(
            title, priority=priority, labels=labels, template=template)
        return "created %s (%s) labels=%s" % (issue.id, issue.priority, issue.labels)

    def _cmd_label(self, args, options):
        if len(args) != 2:
            raise ValueError("label requires <issue-id> <label>")
        issue = self.service.add_label(args[0], args[1])
        return "%s labels=%s" % (issue.id, issue.labels)

    def _cmd_status(self, args, options):
        if len(args) != 2:
            raise ValueError("status requires <issue-id> <status>")
        issue = self.service.set_status(args[0], args[1])
        return "%s status=%s" % (issue.id, issue.status)

    def _cmd_comment(self, args, options):
        if len(args) < 3:
            raise ValueError("comment requires <issue-id> <author> <text>")
        issue_id, author = args[0], args[1]
        text = " ".join(args[2:])
        n = self.service.comment(issue_id, author, text)
        return "%s now has %d comment(s)" % (issue_id, n)

    def _cmd_show(self, args, options):
        if len(args) != 1:
            raise ValueError("show requires <issue-id>")
        issue = self.service.get_issue(args[0])
        return repr(issue.to_dict())

    def _cmd_list(self, args, options):
        issues = self.service.all_issues()
        lines = ["%s %s [%s] %s" % (i.id, i.title, i.status, i.labels) for i in issues]
        hist = reporting.label_histogram(issues)
        lines.append("labels: %s" % hist)
        return "\n".join(lines) if lines else "(no issues)"
