import json
import os

from flask import request
def get_token_from_cookies():
    token = request.cookies.get("daystream_token") or "none"
    if token != "none":
        token = json.loads(token)
        token["client_id"] = os.getenv("CLIENT_ID")
        token["client_secret"] = os.getenv("CLIENT_SECRET")

    return token