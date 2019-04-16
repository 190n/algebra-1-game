from flask import make_response, jsonify

def query_db(query, id):
    try:
        data = query.get(int(id))
    except ValueError:
        return (None, make_response(jsonify({
            'success': False,
            'error': 'ID not an integer',
            'data': None
        }), 400))

    if data is None:
        return (None, make_response(jsonify({
            'success': False,
            'error': 'Item not found',
            'data': None
        }), 404))
    else:
        return (data, None)

def get_one_item(query, id, process=(lambda n: n)):
    data, response = query_db(query, id)

    if response is not None:
        return response

    return jsonify({
        'success': True,
        'error': None,
        'data': process(data)
    })
