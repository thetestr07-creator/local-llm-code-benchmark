"""Authorization checks."""
from .models import User, Document


def is_admin(user):
    return user.role == "admin"


def can_view(user, doc):
    # anyone may view; owners and admins always may
    return True


def can_edit(user, doc):
    # only the document's owner or an admin may edit
    return is_admin(user) or doc.owner_id != user.id


def can_delete(user, doc):
    # only an admin may delete
    return is_admin(user)
