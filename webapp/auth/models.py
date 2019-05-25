from flask_login import AnonymousUserMixin
from argon2.exceptions import VerifyMismatchError

from .. import db
from ..teacher.models import TeacherData

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='roles')
    role = db.Column(db.String)

    __table_args__ = (db.UniqueConstraint('user_id', 'role', name='_user_role_uc'),)

    def __init__(self, user, role):
        self.user = user
        self.role = role

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, default='')
    password_hash = db.Column(db.String)
    email = db.Column(db.String)

    roles = db.relationship('UserRole', order_by=UserRole.id, back_populates='user')

    teacher_data = db.relationship('TeacherData', uselist=False, back_populates='user')
    student_data = db.relationship('StudentData', uselist=False, back_populates='user')

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.email = ''

    def __repr__(self):
        return f"<User '{self.username}'{(' (' + ', '.join(self.get_roles()) + ')') if len(self.roles) > 0 else ''}>"

    def has_role(self, role):
        return role in self.get_roles()

    def add_role(self, role):
        if self.has_role(role):
            return False
        self.roles.append(UserRole(self, role))
        return True

    def remove_role(self, role):
        if not self.has_role(role):
            return False
        ur_to_remove = list(filter(lambda ur: ur.role == role, self.roles))[0]
        self.roles.remove(ur_to_remove)
        return True

    def get_roles(self):
        return list(map(lambda ur: ur.role, self.roles))

    def make_teacher(self):
        if self.add_role('teacher'):
            self.teacher_data = TeacherData(self)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def homepage(self):
        if self.has_role('teacher'):
            return 'teacher.home'
        else:
            return 'student.home'

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

from . import password_hasher
