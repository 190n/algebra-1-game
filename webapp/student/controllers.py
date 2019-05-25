from flask import Blueprint, flash, redirect, render_template, url_for, g, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm.exc import NoResultFound

from .forms import JoinForm
from .models import StudentData
from .. import db
from ..auth.util import load_user, role_required
from ..teacher.models import Section

student_blueprint = Blueprint(
    'student',
    __name__,
    url_prefix='/student',
    template_folder='../templates/student'
)

student_blueprint.before_request(load_user)

@student_blueprint.route('/')
def home():
    return render_template('student/home.html')

@student_blueprint.route('/invited/<join_code>')
def invited(join_code):
    try:
        section = Section.query.filter_by(join_code=join_code).one()
    except NoResultFound:
        abort(404)

    if not section.joinable:
        abort(404)

    if current_user.is_authenticated:
        if section.has_student(current_user.student_data):
            return render_template('student/already_enrolled.html', section=section)

        form = JoinForm()
        return render_template('student/invited.html', form=form, section=section)
    else:
        return render_template('student/invited.html', section=section)

@student_blueprint.route('/join', methods=['GET', 'POST'])
@role_required('student')
def join():
    form = JoinForm()
    if form.validate_on_submit():
        sec = Section.query.filter_by(join_code=form.join_code.data).one()
        if sec.has_student(current_user.student_data):
            return render_template('student/already_enrolled.html', section=sec)
        current_user.student_data.join_section(sec)
        db.session.commit()
        return redirect(url_for('.home'))
    return render_template('student/join.html', form=form)

@student_blueprint.route('/sections/<id>')
@role_required('student')
def view_section(id):
    return 'sup'
