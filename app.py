#!/usr/bin/env python3.6
from flask import Flask, jsonify, abort, request, make_response, url_for
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from auth import *
from models import *
from functions import *

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.errorhandler(400)
def bad_request(error):
    '''
    Function error handler 400
    '''
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(405)
def bad_request(error):
    '''
    Function error handler 400
    '''
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

@app.errorhandler(404)
@app.errorhandler(Model.DoesNotExist)
def not_found(error):
    '''
    Function error handler 404
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(Exception)
def handle_error(error):
    '''
    Function error handler ohter errors
    '''
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    return make_response(jsonify({'error': str(error)}), code)

@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
def index():
    '''
    Function for route /
    '''
    return jsonify({'name': 'event service',
                    'stage': os.environ.get('STAGE', 'dev')})


@app.route('/api/events', methods=['POST'])
@auth.login_required
def create_event():
    '''
    Function for route POST /events, input {"event_id":"id events, refers from linkedevents"}
    '''
    data_input = request.get_json()
    if data_input is None or 'event_id' not in data_input:
        abort(400)
    data_event = get_linkedevents_detail(data_input['event_id'])
    if data_event is None or 'id' not in data_event:
        abort(404)
    try:
        is_free_data = data_event['offers'][0]['is_free'] 
    except:
        is_free_data = False
    event_data = dict_clean_empty(data_event)
    event_data_str = get_clean_str(event_data)
    event = Event(user=auth.username(), id=data_event['id'], is_free=is_free_data, event_orig=event_data, event_orig_str=event_data_str)
    event.save()
    return jsonify({'event': show_brief_event(event)}), 201

@app.route('/api/events', methods=['GET'])
@auth.login_required
def get_events_user():
    '''
    Function for route GET /events, only show the list of events data from specific user
    '''
    return jsonify({'events': [show_brief_event(event) for event in Event.query(auth.username())]})

@app.route('/api/events/<event_id>', methods=['GET'])
@auth.login_required
def get_events_user_detail(event_id):
    '''
    Function for route GET /events/<event_id>, only show the event data specific user
    '''
    return jsonify({'event': show_detail_event(Event.get(auth.username(), event_id))})

@app.route('/api/events/free', methods=['GET'])
@auth.login_required
def get_events_user_free():
    '''
    Function for route GET /events/free, only show the event data specific user and free
    '''
    return jsonify({'events': [show_brief_event(event) for event in \
        Event.scan((Event.user == auth.username()) & (Event.is_free == True))]})

@app.route('/api/events/search', methods=['POST'])
@auth.login_required
def search_events_user():
    '''
    Function for route POST /events/search, will do query to events of the user
    '''
    data_input = request.get_json()
    if data_input is None or 'query' not in data_input:
        abort(400)
    str_query = get_clean_str(data_input['query'])
    return jsonify({'events': [show_brief_event(event) for event in \
        Event.scan((Event.user == auth.username()) & (Event.event_orig_str.contains(str_query)))]})
    
@app.route('/api/events/<event_id>', methods=['DELETE'])
@auth.login_required
def delete_event(event_id):
    '''
    Function for route DELETE /events/<event_id>'
    '''
    event = Event.get(auth.username(), event_id)
    event.delete()
    return '', 204

if __name__ == '__main__':
    Event.create_table(read_capacity_units=1, write_capacity_units=1)
    app.run(host='0.0.0.0',debug=True)
