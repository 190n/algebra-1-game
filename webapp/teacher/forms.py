import json

from flask_wtf import FlaskForm as Form
from flask_login import current_user
from wtforms import StringField, SelectField, BooleanField, IntegerField, HiddenField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, URL

from .models import TeacherData, Section

class CreateSectionForm(Form):
    name = StringField('Section name', [DataRequired()])
    joinable = BooleanField('Make immediately joinable')
    limit = IntegerField('Maximum number of students (set to 0 for no limit)')

    def validate(self):
        check_validate = super(CreateSectionForm, self).validate()
        if not check_validate:
            return False

        section = Section.query.filter_by(name=self.name.data, teacher_id=current_user.teacher_data.id).first()
        if section:
            self.name.errors.append('You already have a section with that name')
            return False

        return True

class CreateAssignmentForm(Form):
    section_id = SelectField('Section', [DataRequired()], coerce=int)
    questions_json = HiddenField()
    assignment_name = StringField('Assignment name', [DataRequired()])
    date = DateField('Date when students should complete it', [DataRequired()])
    publish = BooleanField('Publish immediately')

    def validate(self):
        check_validate = super(CreateAssignmentForm, self).validate()
        if not check_validate:
            return False

        section = Section.query.get(self.section_id.data)
        if not section:
            self.section_id.errors.append('That section does not exist')
            return False

        try:
            questions_data = json.loads(self.questions_json.data)
            
            # questions_json is array of questions
            # e.g.
            # [
            #     {"question": "What is 2+2?", "answers": ["4", "8"], "correct_answer": 0}
            # ]
            # this code gives unfriendly error messages which should never be
            # seen as the client-side JS will always produce a valid assignment
            if len(questions_data) < 1:
                self.questions_json.errors.append('That is not a valid assignment')
                return False

            for q in questions_data:
                if not ('question' in q and 'answers' in q and 'correct_answer' in q):
                    self.questions_json.errors.append('That is not a valid assignment')
                    return False
                elif len(q['answers']) < 1:
                    self.questions_json.errors.append('That is not a valid assignment')
                    return False
                elif q['correct_answer'] >= len(q['answers']):
                    self.questions_json.errors.append('That is not a valid assignment')
                    return False
        except:
            self.questions_json.errors.append('That is not a valid assignment')
            return False

        return True
