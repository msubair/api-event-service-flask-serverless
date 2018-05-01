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

5. Once the deployment completes, you can make requests to the endpoint that
   is associated with the deployment. For example, you can use httpie:

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

6. Endpoint

| METHOD | URL | DESC | INPUT POST |
| :--- | :--- | :--- | :--- |
| GET   | URL/api/events | API for GET list of events, only show the list of fav events data from specific user | - |
| POST  | URL/api/events | API for POST an event to become user specific event data. Data event will be taken from LinkedEvents, based on input event_id ( == id event in LinkedEvents)| event_id ( == id event in LinkedEvents, e.g: 'linkedevents:agg-100') |
| GET   | URL/api/events/<event_id> | API for GET detail of a fav event data from specific user | - |
| GET   | URL/api/events/free | API for GET list of (only) free fav event data from specific user | - |
| POST | URL/api/events/search | API for POST query search based on input query (str) from user, and will find into fav event data specific user. (In v.0.1 satill very basic, search contain words in all data) | query (free string) |
| DELETE | URL/api/events/<event_id> | API for DELETE a fav event data from specific user | - |
            
