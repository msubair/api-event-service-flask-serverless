
API Event Services in AWS Serverless
====================================

This is simple Python API, for create services based on LinkedEvents (https://api.hel.fi/linkedevents/v1/). Whit this v.0.1 users can:

1. Add fav events for future use

2. Show/List of their fav events

3. Separate free events from the fav events

4. View/Browse detail of certain fav event

5. Remove an event from their fav events

6. Search event(s) from their list of fav events

Stacks: Python 3.6, Flask, PynamoDB, AWS Serverless (Lambda, DynamoDB, and API Gateway)

The deployment procedure is as follows:

1. Ensure you have valid AWS credentials for your account installed on your
   system. Use `aws configure` to set these.

2. Create a virtual environment and install all the requirements in it.

        $ virtualenv -p python3.6 venv
        $ source venv/bin/activate
        (venv) $ pip install -r requirements.txt

3. Create a zappa configuration with `zappa init` and answer all the questions (app function using app.app, etc. And additional, after zappa_settings.json is created, we can add exclude file/s or directory/ies which will exclude by zappa, e.g: "exclude"):

        (venv) $ zappa init

4. Deploy to AWS!"

        (venv) $ zappa deploy dev

5. Update every change in AWS!

        (venv) $ zappa update dev

6. Once the deployment completes, you can make requests to the endpoint that
   is associated with the deployment. For example, you can use [httpie](https://httpie.org/):

        (venv) $ pip install httpie
        (venv) $ http GET <URL>/api
        HTTP/1.0 200 OK
        Content-Length: 62
        Content-Type: application/json
        Date: Sun, 22 Apr 2018 06:35:53 GMT
        Server: Werkzeug/0.11.15 Python/3.6.5

        {
            "name": "tasks", 
            "stage": "dev"
        }
        (venv) $ http POST --auth username:password POST <URL>/api/events event_id='linkedevents:agg-100'
        HTTP/1.1 201 Created
        Access-Control-Allow-Origin: *
        Connection: keep-alive
        Content-Length: 955
        Content-Type: application/json
        Date: Sun, 22 Apr 2018 08:35:53 GMT
        Via: 1.1 3664cc1fd21a07e55327a9c256fa758a.cloudfront.net (CloudFront)
        X-Amz-Cf-Id: 4hr2gSWj4QGaPCI2rgrJ80jAh6ujzarSXu8srfiNJcw0iejPsDjHbg==
        X-Amzn-Trace-Id: sampled=0;root=1-5ae88a54-b47b21e13b61116c476a3558
        X-Cache: Miss from cloudfront
        x-amz-apigw-id: GNqNLH5BoAMF_BQ=
        x-amzn-Remapped-Content-Length: 955
        x-amzn-RequestId: eaf00edc-4d55-11e8-b6c8-43945790ffb1
        {
            "event": {
               "added_at": "Tue, 22 Apr 2018 08:35:53 GMT", 
               "end_time": "2018-05-08T08:30:00Z", 
               "id": "linkedevents:agg-100", 
               "is_free": true, 
               "location": null, 
               "name": {
                  "en": "Päivätanssit", 
                  "fi": "Päivätanssit", 
                  "sv": "Päivätanssit"
               }, 
               "short_description": {
                  "en": "Popular daytime dance events continue in Stoa, with the fantastic dance instructor couple Katja Koukkula and Jussi Väänänen.", 
                  "fi": "Suositut päivätanssit jatkuvat Stoassa kilpatanssija- ja tanssinopettajapariskunnan Katja Koukkulan ja Jussi Väänäsen rautaisella opastuksella.", 
                  "sv": "De populära dagsdanserna fortsätter på Stoa under handledning av tävlingsdans- och danslärarparet Katja Koukkula och Jussi Väänänen."
               }, 
               "start_time": "2018-03-06T08:30:00Z", 
               "user": "user1"
            }
        }

7. Endpoint

| METHOD | URL | DESC | INPUT POST |
| :--- | :--- | :--- | :--- |
| GET   | URL/api/events | API for GET list of events, only show the list of fav events data from specific user | - |
| POST  | URL/api/events | API for POST an event to become user specific event data. Data event will be taken from LinkedEvents, based on input event_id ( == id event in LinkedEvents)| event_id ( == id event in LinkedEvents, e.g: 'linkedevents:agg-100') |
| GET   | URL/api/events/<event_id> | API for GET detail of a fav event data from specific user | - |
| GET   | URL/api/events/free | API for GET list of (only) free fav event data from specific user | - |
| POST | URL/api/events/search | API for POST query search based on input query (str) from user, and will find into fav event data specific user. (In v.0.1 satill very basic, search contain words in all data) | query (free string) |
| DELETE | URL/api/events/<event_id> | API for DELETE a fav event data from specific user | - |
            
8. For unittest; make sure environment in testing STAGE (export STAGE="test") and the auth setting is valid.

        (venv) $ export STAGE="test"
        (venv) $ python test.py
        test_1_home (test_event.EventTestCase)
        Test API for home ... ok
        test_2_api_get_empty (test_event.EventTestCase)
        Test API for get fav events empty ... ok
        test_3_api_get_events_unauthorized (test_event.EventTestCase)
        Test API for unauthorized access to get fav events ... ok
        test_4_api_add_event (test_event.EventTestCase)
        Test API add fav event (POST request) ... ok
        test_5_api_event_creation_bad_request (test_event.EventTestCase)
        Test API return bad request when create an fav event with unvalid input (POST request) ... ok
        test_6_api_add_event_2 (test_event.EventTestCase)
        Test API add fav event (POST request) ... ok
        test_7_api_can_get_all_events (test_event.EventTestCase)
        Test API can get all of user fav events (GET request). ... ok
        test_7_api_can_get_all_free_events (test_event.EventTestCase)
        Test API can get only the free of user fav events (GET request). ... ok
        test_8_api_can_get_one_event (test_event.EventTestCase)
        Test API can get one user fav event based on input event_id (GET request). ... ok
        test_9_api_event_not_found (test_event.EventTestCase)
        Test API response event not found (GET request). ... ok

        ----------------------------------------------------------------------
        Ran 10 tests in 4.461s

        OK





