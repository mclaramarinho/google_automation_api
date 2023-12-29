import json
import os

from email_colector import email_colector
from flask import Flask, jsonify, redirect, request, make_response, session
from dotenv import load_dotenv
from events_list import events_list
from get_token_from_cookies import get_token_from_cookies
from gmail_authenticate import google_authenticate, get_token
from read_email import read_email
from tasks_list import tasks_list

app = Flask(__name__)

load_dotenv()

@app.route('/')
def home():
    return redirect("https://app.swaggerhub.com/apis-docs/MARINHOCLARAMB/google_automation/1.0.0", code=302)


@app.route('/authenticate')
def authenticate():
    token = get_token_from_cookies()

    result = google_authenticate(request.url_root, token)

    if result == False:
        return jsonify({"message": "An error occurred"}), 500
    elif result == "done":
        return jsonify({"message": "Successfully authorized!"}), 202
    else:
        if result == "Error":
            return jsonify({"message": "An error occurred"}), 500
        else:
            return jsonify({"url": result}), 200

@app.route('/authCallback')
def auth_callback():
    print("authcallback")
    state = request.args.get('state')
    code = request.args.get('code')
    req = get_token(code, request.url_root)
    if req != False:
        res = make_response({"message": "Success!"})
        res.set_cookie("daystream_token", json.dumps(req))
        return res
    else:
        return jsonify({"message": "Error fetching the authentication token."}), 500


# TODO: fix the authorization issue that will arise in the paths below from the changes above
@app.route('/gmail/getEmailUpdates')
def get_email_updates():
    token = get_token_from_cookies()
    result = email_colector(token)
    if not isinstance(result, str):
        return jsonify(result), 200
    else:
        return jsonify({"message": result}), 500

@app.route('/gmail/markAsRead/<id>')
def mark_as_read(id):
    token = get_token_from_cookies()
    result = read_email(token, id)

    if result == "Success":
        return jsonify(result), 200
    elif result == "This action requires authentication!":
        return jsonify({"message": result}), 401
    else:
        return jsonify({"message": result}), 400


@app.route('/calendar/getEventsList/<when>')
def get_events_list(when):
    token = get_token_from_cookies()

    if when == "today" or when == "tomorrow":
        response = events_list(token, when)
    else:
        return jsonify({"message": "Arguments available for this endpoint: /today or /tomorrow"}), 404

    if not isinstance(response, str):
        return jsonify(response), 200
    else:
        if response == "This action requires authentication!":
            return jsonify({"message": response}), 401
        else:
            return jsonify({"message": response}), 500


@app.route('/tasks/getTaskList/<when>')
def get_task_list(when):
    token = get_token_from_cookies()
    if when == "today" or when == "tomorrow":
        response = tasks_list(token, when)
    else:
        return jsonify({"message": "Arguments available for this endpoint: /today or /tomorrow"}), 404

    if type(response) != "str":
        return jsonify(response), 200
    else:
        return jsonify(response), 500


# CREATE FLASK APPLICATION
if __name__ == '__main__':
    app.run()






