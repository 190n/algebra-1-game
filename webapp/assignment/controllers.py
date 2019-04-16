from datetime import date

from flask import Blueprint, jsonify

from .models import Assignment, Problem, Answer
from .. import util

assignment_blueprint = Blueprint(
    'assignment',
    __name__,
    url_prefix='/api/v1/assignments'
)

@assignment_blueprint.route('/')
def all_assignments():
    assignments = Assignment.query.filter(Assignment.date >= date.today()).all()

    return jsonify({
        'success': True,
        'error': None,
        'data': [a.to_dict() for a in assignments]
    })

@assignment_blueprint.route('/<id>')
def get_one_assignment(id):
    return util.get_one_item(Assignment.query, id, lambda a: a.to_dict(True))

@assignment_blueprint.route('/submit_answer/<id>', methods=['POST'])
def answer_problem(id):
    answer, response = util.query_db(Answer.query, id)
    if response is not None:
        return response

    return jsonify({
        'success': True,
        'error': None,
        'data': {
            'answer_correct': answer.is_correct
        }
    })
