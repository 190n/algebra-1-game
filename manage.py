import os
from webapp import db, migrate, create_app
from webapp.assignment.models import Assignment, Problem, Answer
from webapp.student.models import StudentData
from webapp.teacher.models import Section, TeacherData, StudentEnrollment
from webapp.auth.models import User, UserRole

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app(f'config.{env.capitalize()}Config')

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Assignment=Assignment, Problem=Problem, Answer=Answer, StudentData=StudentData, Section=Section, TeacherData=TeacherData, User=User, UserRole=UserRole, StudentEnrollment=StudentEnrollment, migrate=migrate)
