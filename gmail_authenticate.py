import json
import os
from dotenv import load_dotenv

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from credentials import get_credentials


#from credentials import credentials

def google_authenticate(what="email"):
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify',
              'https://www.googleapis.com/auth/calendar.events.readonly', 'https://www.googleapis.com/auth/tasks.readonly']
    creds = None
    if os.path.exists("./token.json"):
        creds = Credentials.from_authorized_user_file("./token.json", scopes=SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
           ''' with open('./creds.json', 'w') as f:
                f.write(json.dumps(get_credentials()))'''

           #flow = InstalledAppFlow.from_client_secrets_file('./creds.json', SCOPES)
           flow = InstalledAppFlow.from_client_config(get_credentials(), SCOPES)
           creds = flow.run_local_server(port=0, open_browser=False)

        with open("./token.json", "w") as token:
            token.write(creds.to_json())

    try:
        if what == "calendar":
            return build("calendar", "v3", credentials=creds)
        elif what == "tasks":
            return build("tasks", "v1", credentials=creds)
        else:
            return build("gmail", "v1", credentials=creds)
    except Exception:
        return Exception.__name__