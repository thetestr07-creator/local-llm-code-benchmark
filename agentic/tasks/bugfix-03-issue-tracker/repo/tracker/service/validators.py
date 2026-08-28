"""Input validation helpers used by the service facade."""
from ..domain.enums import VALID_STATUSES, VALID_PRIORITIES


def validate_title(title):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be a non-empty string")
    return title.strip()


def validate_priority(priority):
    if priority not in VALID_PRIORITIES:
        raise ValueError("invalid priority: %r" % (priority,))
    return priority


def validate_status(status):
    if status not in VALID_STATUSES:
        raise ValueError("invalid status: %r" % (status,))
    return status


def normalize_label(label):
    if not isinstance(label, str) or not label.strip():
        raise ValueError("label must be a non-empty string")
    return label.strip().lower()
