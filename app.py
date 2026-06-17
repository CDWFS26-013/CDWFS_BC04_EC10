from flask import Flask, request, render_template, jsonify
from math import sqrt
from datetime import datetime

app = Flask('my_distance')

distances = list()

INDEX_TEMPLATE = 'index.html'


@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
        return render_template(INDEX_TEMPLATE, result=None)
    if request.method == 'POST':
        try:
            start_point = [int(y) for y in request.form['bpoint'].split(',')[0:2]]
            end_point = tuple(int(x) for x in request.form['apoint'].split(',')[0:2])
        except (ValueError, KeyError):
            return render_template(INDEX_TEMPLATE, result=None, error="Coordonnées invalides.")
        distance = sqrt((end_point[1] - start_point[1])**2 + (end_point[0] - start_point[0])**2)
        result = {
            'requested_at': datetime.now(),
            'result_distance': distance,
            'start_point': start_point,
            'end_point': end_point
        }
        distances.append(result)
        return render_template(INDEX_TEMPLATE, result=result)


@app.route('/api')
def index():
    return {}


@app.route('/api/distances')
def already_calculated():
    result = [
        {
            'requested_at': x['requested_at'],
            'result_distance': x['result_distance'],
            'start_point': x['start_point'],
            'end_point': x['end_point']
        }
        for x in distances
    ]
    return jsonify(result)


@app.route('/api/distance', methods=['POST'])
def calculate():
    try:
        start_point = [int(y) for y in request.json['start_point'].split(',')[0:2]]
        end_point = tuple(int(x) for x in request.json['end_point'].split(',')[0:2])
    except (ValueError, KeyError, TypeError):
        return jsonify({'error': 'Coordonnées invalides.'}), 400
    distance = sqrt((end_point[1] - start_point[1])**2 + (end_point[0] - start_point[0])**2)
    result = {
        'requested_at': datetime.now(),
        'result_distance': distance,
        'start_point': start_point,
        'end_point': end_point
    }
    return jsonify(result)