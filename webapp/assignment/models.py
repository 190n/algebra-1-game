from .. import db

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    is_correct = db.Column(db.Boolean)

    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
    problem = db.relationship('Problem', back_populates='answers')

    def __init__(self, answer, is_correct=False):
        self.answer = answer
        self.is_correct = is_correct

    def to_dict(self):
        return {
            'id': self.id,
            'answer': self.answer
        }

    def __repr__(self):
        return f"<Answer '{self.answer}'>"

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    assignment = db.relationship('Assignment', back_populates='problems')

    answers = db.relationship('Answer', order_by=Answer.id, back_populates='problem')

    def __init__(self, question, answers):
        self.question = question
        self.answers = answers

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answers': [a.to_dict() for a in self.answers]
        }

    def __repr__(self):
        return f"<Problem '{self.question}'>"

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.Date)

    problems = db.relationship('Problem', order_by=Problem.id, back_populates='assignment')

    def __init__(self, name, date, problems):
        self.name = name
        self.date = date
        self.problems = problems

    def to_dict(self, include_problems=False):
        d = {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat()
        }

        if include_problems:
            d['problems'] = [p.to_dict() for p in self.problems]
        
        return d

    def __repr__(self):
        return f"<Assignment '{self.name}'>"
