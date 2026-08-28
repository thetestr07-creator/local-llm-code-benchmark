"""Status and priority vocabularies for issues."""


class Status:
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Priority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


VALID_STATUSES = (Status.OPEN, Status.IN_PROGRESS, Status.RESOLVED, Status.CLOSED)
VALID_PRIORITIES = (Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL)

# statuses that count as "done" for reporting
DONE_STATUSES = (Status.RESOLVED, Status.CLOSED)
