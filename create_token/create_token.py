import os
import time
import pickle
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from stravalib.client import Client

CLIENT_ID = os.environ['CLIENT_ID'] or 'GET FROM STRAVA https://www.strava.com/settings/api'
CLIENT_SECRET = os.environ['CLIENT_SECRET'] or 'GET FROM STRAVA https://www.strava.com/settings/api'
REDIRECT_URL = 'http://localhost:8000/authorized'

app = FastAPI()
client = Client()

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    with open(filename, 'rb') as input:
        loaded_object = pickle.load(input)
        return loaded_object


def check_token(client):
    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, refresh_token=client.refresh_token)
        access_token = refresh_response['access_token']
        refresh_token = refresh_response['refresh_token']
        expires_at = refresh_response['expires_at']
        client.access_token = access_token
        client.refresh_token = refresh_token
        client.token_expires_at = expires_at

@app.get("/")
def read_root():
    authorize_url = client.authorization_url(client_id=CLIENT_ID, redirect_uri=REDIRECT_URL)
    return RedirectResponse(authorize_url)


@app.get("/authorized/")
def get_code(state=None, code=None, scope=None):
    token_response = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=code)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']
    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at
    save_object(client, 'client.pkl')
    return {"state": state, "code": code, "scope": scope}

def get_client():
    try:
        client = load_object('client.pkl')
        check_token(client)
        athlete = client.get_athlete()
        print("For {id}, I now have an access token {token}".format(id=athlete.id, token=client.access_token))
        return client
        # To upload an activity
        # client.upload_activity(activity_file, data_type, name=None, description=None, activity_type=None, private=None, external_id=None)
    except FileNotFoundError:
        print("No access token stored yet, visit http://localhost:8000/ to get it")
        print("After visiting that url, a pickle file is stored, run this file again to upload your activity")
    
    
get_client()