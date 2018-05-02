#!/usr/bin/env python3.6
import unittest
import os
import json
from base64 import b64encode
from app import *

BASE_URL = 'http://127.0.0.1:5000/api'
username = 'user1'
password = 'password1'
headers = {
    'Authorization': 'Basic ' + b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')
}

class EventTestCase(unittest.TestCase):
    """This class represents the event test case"""

    def setUp(self):
        """Test API for home"""
        self.app = app.test_client()
        self.app.testing = True

    def test_01_home(self):
        """Test API for home"""
        response = self.app.get()
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'event service')

    def test_02_api_get_empty(self):
        """Test API for get fav events empty"""
        response = self.app.get('/api/events', headers=headers)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['events']), 0)

    def test_03_api_get_events_unauthorized(self):
        """Test API for unauthorized access to get fav events"""
        response = self.app.get('/api/events')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'Unauthorized access')

    def test_04_api_add_event(self):
        """Test API add fav event (POST request)"""
        sample_event_id = 'kulke:44519'
        data_event = json.dumps({'event_id':sample_event_id})
        response = self.app.post('/api/events', headers=headers, data=data_event, \
            content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['event']['id'], sample_event_id)
        self.assertEqual(data['event']['user'], username)

    def test_05_api_event_creation_bad_request(self):
        """Test API return bad request when create an fav event with unvalid input (POST request)"""
        sample_event_id = 'kulke:44519'
        data_event = json.dumps({'eventx_id':sample_event_id})
        response = self.app.post('/api/events', headers=headers, data=data_event, \
            content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Bad request')

    def test_06_api_add_event_2(self):
        """Test API add fav event (POST request)"""
        sample_event_id = 'kulke:44518'
        data_event = json.dumps({'event_id':sample_event_id})
        response = self.app.post('/api/events', headers=headers, data=data_event, \
            content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['event']['id'], sample_event_id)
        self.assertEqual(data['event']['user'], username)

    def test_07_api_can_get_all_events(self):
        """Test API can get all of user fav events (GET request)."""
        response = self.app.get('/api/events', headers=headers)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['events']), 2)
        
    def test_08_api_can_get_one_event(self):
        """Test API can get one user fav event based on input event_id (GET request)."""
        sample_event_id = 'kulke:44518'
        response = self.app.get('/api/events/%s' % sample_event_id, headers=headers)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['event']['id'], sample_event_id)
        self.assertEqual(data['event']['user'], username)

    def test_09_api_event_not_found(self):
        """Test API response event not found (GET request)."""
        sample_event_id = '-'
        response = self.app.get('/api/events/%s' % sample_event_id, headers=headers)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found')

    def test_10_api_can_get_all_free_events(self):
        """Test API can get only the free of user fav events (GET request)."""
        response = self.app.get('/api/events/free', headers=headers)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['events']), 0)