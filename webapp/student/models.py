from flask_login import AnonymousUserMixin
from argon2.exceptions import VerifyMismatchError

from .. import db
from . import password_hasher

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, default='')
    password_hash = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.email = email

    def __repr__(self):
        return f"<User '{self.username}>'"

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id)

    def set_password(self, pw):
        self.password_hash = password_hasher.hash(pw)

    def check_password(self, pw):
        try:
            password_hasher.verify(self.password_hash, pw) # raises VerifyMismatchError if they do not match
            if password_hasher.check_needs_rehash(self.password_hash):
                # params have changed
                self.set_password(pw)

            return True
        except VerifyMismatchError:
            return False
