import re

class User:
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []

    @staticmethod
    def validate_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    def __lt__(self, other):
        return self.total_reactions < other.total_reactions


class Post:
    def __init__(self, id, author_id, text):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = []


