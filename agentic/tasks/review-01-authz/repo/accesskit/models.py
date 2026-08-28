"""Domain models."""


class User:
    def __init__(self, id, role="member"):
        self.id = id
        self.role = role


class Document:
    def __init__(self, doc_id, owner_id):
        self.doc_id = doc_id
        self.owner_id = owner_id
