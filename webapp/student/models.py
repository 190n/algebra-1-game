from flask_login import AnonymousUserMixin
from argon2.exceptions import VerifyMismatchError

from .. import db

class StudentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='student_data')

    enrollments = db.relationship('StudentEnrollment', back_populates='student')

    def __init__(self, user):
        self.user = user

    def join_section(self, sec):
        se = StudentEnrollment(self, sec)
        db.session.add(se)

from ..teacher.models import StudentEnrollment
