"""tracker — a tiny in-memory issue tracker.

Layers:
    tracker.domain     — pure data models (Issue, IssueTemplate, enums)
    tracker.service    — business logic over an in-memory store
    tracker.interface  — a text command router / CLI front end
"""
__version__ = "0.3.0"
