import json
import os
from dotenv import load_dotenv

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from credentials import get_credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.modify',
              'https://www.googleapis.com/auth/calendar.events.readonly', 'https://www.googleapis.com/auth/tasks.readonly']

#from credentials import credentials
def google_authenticate(origin_url, token, what="email"):

    creds = None

    if token != "none":
        creds = Credentials.from_authorized_user_info(token, scopes=SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            try:
                creds.refresh(Request())
                return "done"
            except:
                return False
        elif creds and not creds.valid and creds.refresh_token:
            try:
                creds.refresh(Request())
                return "done"
            except:
                return False
        else:
            try:
                flow = InstalledAppFlow.from_client_config(get_credentials(), SCOPES, redirect_uri=(origin_url+"authCallback"))
                authorization_url, state = flow.authorization_url(prompt='consent')
                return authorization_url
            except:
                return "Error"

    ''' try:
        if what == "calendar":
            return build("calendar", "v3", credentials=creds)
        elif what == "tasks":
            return build("tasks", "v1", credentials=creds)
        else:
            return build("gmail", "v1", credentials=creds)
    except Exception:
        return Exception.__name__'''


def get_token(code, origin_url):

    flow = InstalledAppFlow.from_client_config(get_credentials(), SCOPES, redirect_uri=origin_url+"authCallback")
    try:
        access_token = flow.fetch_token(code=code)
        return access_token
    except Exception as e:
        return False