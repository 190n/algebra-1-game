from flask_login import LoginManager
from argon2 import PasswordHasher

password_hasher = PasswordHasher()

from .models import Student

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please log in to access this page'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(userid):
    return Student.query.get(userid)

def create_module(app, **kwargs):
    login_manager.init_app(app)
    from .controllers import student_blueprint
    app.register_blueprint(student_blueprint)
