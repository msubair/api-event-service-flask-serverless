#!/usr/bin/env python3.6
import requests
import json
import pytz
import re
from datetime import datetime
from flask import jsonify

linkedevents_base_url = 'https://api.hel.fi/linkedevents/v1/'

def get_time_now():
    '''
    Function get time now EET
    '''
    return datetime.now(pytz.timezone('GMT'))

def get_linkedevents_detail(event_id):
    '''
    Function for search the linkedevents based on input parameters. 
    Output is tuple of data events and meta data for output
    '''
    final_url = linkedevents_base_url + 'event/' + event_id
    r = requests.get(final_url)
    data = json.loads(r.content.decode())
    return data

def show_brief_event(event):
    '''
    Function for templating event data presentation for user event
    '''
    event_orig = event.event_orig.as_dict()
    return {
        'user': event.user,
        'id': event.id,
        'is_free': event.is_free,
        'name': event_orig.get('name'),
        'location': event_orig.get('location'),
        'start_time' : event_orig.get('start_time'),
        'end_time' : event_orig.get('end_time'),
        'short_description' : event_orig.get('short_description'),
        'added_at': event.created_at
    }

def show_detail_event(event):
    '''
    Function for templating event data presentation for public
    '''
    return {
        'user': event.user,
        'id': event.id,
        'is_free': event.is_free,
        'event_orig': event.event_orig.as_dict(),
        'added_at': event.created_at
    }

def dict_clean_empty(d):
    '''
    Function clean null from dict before insert into DB
    Script taken from https://stackoverflow.com/questions/27973988/python-how-to-remove-all-empty-fields-in-a-nested-dict/35263074
    '''
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (dict_clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, dict_clean_empty(v)) for k, v in d.items()) if v}

def get_clean_str(d):
    '''
    Function extract all value to str from nested dict
    '''
    str_dict = re.sub(r'[^a-zA-Z0-9_-]', ' ', str(d).lower())
    str_dict = ' '.join(str_dict.split())
    return str_dict

def validate_data(item):
    '''
    Function for Validate data based on predefined format schema
    '''
    v = Validator(schema)
    if not v(item):
        return make_response(jsonify({'error': 'There was something wrong with your arguments'}), 400)
