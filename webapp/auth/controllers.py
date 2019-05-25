from flask import Blueprint, g, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user, login_required

from .forms import LoginForm, RegisterForm
from .models import User
from .util import load_user
from .. import db
from ..student.models import StudentData

auth_blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    template_folder='../templates/auth'
)

auth_blueprint.before_request(load_user)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        user.add_role('student')
        user.student_data = StudentData(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('student.home'))
    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)
        return redirect(url_for(user.homepage))
    return render_template('auth/login.html', form=form)

@auth_blueprint.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('.login'))
