from datetime import date
import json

from flask import request, jsonify, make_response

from .. import app, models, auth
from . import BASE_URL, query_db, get_one_item

STUDENT_BASE_URL = f'{BASE_URL}/student'

@app.route(f'{STUDENT_BASE_URL}/assignments')
def get_assignments():
    auth.require_authorization_for_api(request)

    assignments = models.Assignment.query.filter(models.Assignment.date >= date.today()).all()

    return jsonify({
        'success': True,
        'error': None,
        'data': [a.to_dict() for a in assignments]
    })

@app.route(f'{STUDENT_BASE_URL}/assignments/<id>')
def get_one_assignment(id):
    auth.require_authorization_for_api(request)

    return get_one_item(models.Assignment.query, id, lambda a: a.to_dict(True))

@app.route(f'{STUDENT_BASE_URL}/submit_answer/<id>', methods=['POST'])
def answer_problem(id):
    auth.require_authorization_for_api(request)

    answer, response = query_db(models.Answer.query, id)
    if response is not None:
        return response

    return jsonify({
        'success': True,
        'error': None,
        'data': {
            'answer_correct': answer.is_correct
        }
    })
