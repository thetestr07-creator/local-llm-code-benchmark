"""Reporting/aggregation over a set of issues."""
from ..domain.enums import DONE_STATUSES


def label_histogram(issues):
    """Map each label -> number of issues carrying it."""
    hist = {}
    for issue in issues:
        for lab in issue.labels:
            hist[lab] = hist.get(lab, 0) + 1
    return hist


def status_counts(issues):
    counts = {}
    for issue in issues:
        counts[issue.status] = counts.get(issue.status, 0) + 1
    return counts


def open_count(issues):
    return sum(1 for i in issues if i.status not in DONE_STATUSES)


def issues_with_label(issues, label):
    return [i for i in issues if label in i.labels]
