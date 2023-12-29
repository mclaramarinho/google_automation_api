import os
from dotenv import load_dotenv


def get_credentials():
  load_dotenv()
  credentials = {
    "installed": {
      "client_id": os.getenv("CLIENT_ID"),
      "client_secret": os.getenv("CLIENT_SECRET"),
      "project_id": os.getenv("PROJECT_ID"),
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "redirect_uris":["http://127.0.0.1:5000/authCallback","http://127.0.0.1:5000","https://google-automation-api.vercel.app","https://localhost","https://google-automation-api.vercel.app/authCallback", "https://localhost/authCallback"],
      "javascript_origins":["https://localhost","https://google-automation-api.vercel.app"]
    }
  }
  return credentials