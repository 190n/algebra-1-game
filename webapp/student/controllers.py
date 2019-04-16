from flask import Blueprint, flash, redirect, render_template
from flask_login import login_user, logout_user

from .forms import LoginForm, RegisterForm
from .models import Student
from .. import db

student_blueprint = Blueprint(
    'student',
    __name__,
    url_prefix='/',
    template_folder='../templates/student'
)

@student_blueprint.route('/student/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        student = Student()
        student.username = form.username.data
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created. Please log in.', category='success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)
