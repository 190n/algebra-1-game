from flask_login import LoginManager
from argon2 import PasswordHasher

password_hasher = PasswordHasher()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please log in to access this page'
login_manager.login_message_category = 'info'

from .models import User

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

    if userid[:2] == 't_':
        return Teacher.query.get(userid[2:])
    elif userid[:2] == 's_':
        return Student.query.get(userid[2:])
    else:
        raise Exception('User ID in unsupported format')

def create_module(app, **kwargs):
    login_manager.init_app(app)

    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)
