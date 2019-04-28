from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL

from .models import Student

class LoginForm(Form):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember me')

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = Student.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Username and password do not match')
            return False
        if not user.check_password(self.password.data):
            self.username.errors.append('Username and password do not match')
            return False

        return True

class RegisterForm(Form):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False

        user = Student.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('That username is taken')
            return False

        return True
