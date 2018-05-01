#!/usr/bin/env python3.6
from flask import make_response, jsonify
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

# Dummy users for auth, only form demo purpose
users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

@auth.get_password
def get_password(username):
    '''
    Function auth for basich auth mapping username and password, dummy only for demo purpose
    '''
    if username in users:
        return users.get(username)
    return None

@auth.error_handler
def unauthorized():
    '''
    Function error handler 401
    '''
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)