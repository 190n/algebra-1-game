from functools import wraps

from flask import Blueprint, g, render_template, redirect, url_for, flash, abort, current_app as app
from flask_login import current_user, login_user, logout_user, login_required

from .models import TeacherData, Section
from .forms import CreateSectionForm, CreateAssignmentForm
from ..auth.util import load_user, role_required
from .. import db

teacher_blueprint = Blueprint(
    'teacher',
    __name__,
    url_prefix='/teacher',
    template_folder='../templates/teacher'
)

teacher_blueprint.before_request(load_user)

@teacher_blueprint.route('/')
@role_required('teacher')
def home():
    my_sections = Section.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/home.html', sections=my_sections)

@teacher_blueprint.route('/sections/<id>')
@role_required('teacher')
def view_section(id):
    section = Section.query.get_or_404(id)
    if section.teacher_id != current_user.id:
        return abort(404)
    return render_template('teacher/section.html', section=section)

@teacher_blueprint.route('/sections/create', methods=['GET', 'POST'])
@role_required('teacher')
def create_section():
    form = CreateSectionForm()
    if form.validate_on_submit():
        s = Section(form.name.data, current_user.teacher_data, form.joinable.data, form.limit.data)
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('teacher.view_section', id=s.id))
    return render_template('teacher/create_section.html', form=form)

@teacher_blueprint.route('/sections/<section_id>/assignments/create')
@role_required('teacher')
def create_assignment(section_id):
    section = Section.query.get_or_404(section_id)
    form = CreateAssignmentForm()
    return render_template('teacher/create_assignment.html', section=section, form=form, select_section=False)

@teacher_blueprint.route('/create_assignment', methods=['GET', 'POST'])
@role_required('teacher')
def create_assignment_without_section():
    form = CreateAssignmentForm()
    if form.validate_on_submit():
        return form.questions_json.data
    sections = Section.query.filter_by(teacher_id=current_user.teacher_data.id).all()
    form.section_id.choices = [(s.id, s.name) for s in sections]
    return render_template('teacher/create_assignment.html', form=form, select_section=True)
