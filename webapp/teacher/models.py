import random
import string

from flask_login import AnonymousUserMixin
from argon2.exceptions import VerifyMismatchError

from .. import db
from ..assignment.models import Assignment

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    join_code = db.Column(db.String, unique=True, default='00000000')
    joinable = db.Column(db.Boolean, default=True)
    max_size = db.Column(db.Integer)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher_data.id'))
    teacher = db.relationship('TeacherData', back_populates='sections')

    enrolled = db.relationship('StudentEnrollment', back_populates='section')

    assignments = db.relationship('Assignment', order_by=Assignment.id, back_populates='section')

    __table_args__ = (db.UniqueConstraint('teacher_id', 'name', name='_name_teacher_id_uc'),)

    def __init__(self, name, teacher, joinable, max_size):
        self.name = name
        self.teacher = teacher
        self.joinable = joinable
        self.max_size = max_size
        if joinable:
            self.reset_join_code()

    def reset_join_code(self):
        self.join_code = Section.gen_join_code()

        dups = Section.query.filter(Section.id != self.id).filter_by(join_code=self.join_code, joinable=True).all()
        while len(dups) > 0:
            self.join_code = Section.gen_join_code()
            dups = Section.query.filter(Section.id != self.id).filter_by(join_code=self.join_code, joinable=True).all()

    def has_student(self, student):
        enrollment = StudentEnrollment.query.filter_by(section=self, student=student).first()
        if enrollment is not None:
            return True
        else:
            return False

    @staticmethod
    def gen_join_code():
        return str(random.randint(0, 99999999)).zfill(8)

class TeacherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='teacher_data')

    sections = db.relationship('Section', order_by=Section.id, back_populates='teacher')

    def __init__(self, user):
        self.user = user

class StudentEnrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_data.id'))
    student = db.relationship('StudentData', back_populates='enrollments')
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    section = db.relationship('Section', back_populates='enrolled')

    __table_args__ = (db.UniqueConstraint('student_id', 'section_id', name='_student_section_uc'),)

    def __init__(self, student, section):
        self.student = student
        self.section = section
