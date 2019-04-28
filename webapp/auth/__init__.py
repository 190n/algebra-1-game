from flask_login import LoginManager
from argon2 import PasswordHasher

password_hasher = PasswordHasher()

login_manager = LoginManager()
login_manager.login_view = 'student.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please log in to access this page'
login_manager.login_message_category = 'info'

from ..student.models import Student
# from ..teacher.models import Teacher

@login_manager.user_loader
def load_user(userid):
    # if userid[:2] == 't_':
    #     return Teacher.query.get(userid[2:])
    if userid[:2] == 's_':
        return Student.query.get(userid[2:])
    else:
        raise Exception('User ID in unsupported format')

def create_module(app, **kwargs):
    login_manager.init_app(app)
