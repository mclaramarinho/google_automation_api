import os
from dotenv import load_dotenv


def get_credentials():
  load_dotenv()
  credentials = {
    "installed": {
      "client_id": os.getenv("CLIENT_ID"),
      "project_id": os.getenv("PROJECT_ID"),
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_secret": os.getenv("CLIENT_SECRET"),
      "redirect_uris": ["http://localhost"]
    }
  }
  return credentials