from flask import Blueprint, flash, redirect, render_template, url_for, g
from flask_login import login_user, logout_user, login_required, current_user

from .forms import LoginForm, RegisterForm
from .models import Student
from .. import db

student_blueprint = Blueprint(
    'student',
    __name__,
    url_prefix='/student',
    template_folder='../templates/student'
)

@student_blueprint.before_request
def load_user():
    if current_user.is_authenticated:
        g.logged_in = True
    g.user = current_user

@student_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        student = Student(form.username.data, form.password.data)
        db.session.add(student)
        db.session.commit()
        login_user(student)
        return redirect(url_for('.home'))
    return render_template('register.html', form=form)

@student_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).one()
        login_user(student, remember=form.remember.data)
        return redirect(url_for('.home'))
    return render_template('login.html', form=form)

@student_blueprint.route('/home')
def home():
    return render_template('home.html')

@student_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.home'))
