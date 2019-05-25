from functools import wraps

from flask import g, current_app
from flask_login import current_user

def load_user():
    if current_user.is_authenticated:
        g.logged_in = current_user.is_authenticated
        g.user = current_user
    else:
        g.logged_in = False
        g.user = None

# adapted from https://stackoverflow.com/a/15884811
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if not current_user.has_role(role):
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated
    return wrapper
