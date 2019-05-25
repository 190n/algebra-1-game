from flask_wtf import FlaskForm as Form
from flask_login import current_user
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from sqlalchemy.orm.exc import NoResultFound

from .models import StudentData
from ..teacher.models import Section

class JoinForm(Form):
    join_code = StringField('Join code', [DataRequired()])

    def validate(self):
        check_validate = super(JoinForm, self).validate()
        if not check_validate:
            return False

        try:
            sec = Section.query.filter_by(join_code=self.join_code.data).one()
        except NoResultFound:
            self.join_code.errors.append('That join code is invalid')
            return False

        return True
