from email_colector import email_colector
from flask import Flask, jsonify, request

from events_list import events_list
from gmail_authenticate import google_authenticate
from read_email import read_email
from tasks_list import tasks_list

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"message": "Endpoints available: \n/gmail/getEmailUpdates \n/authenticate \n/markAsRead/<id>"})

@app.route('/gmail/getEmailUpdates')
def get_email_updates():
    result = email_colector()
    if type(result) != "str":
        return jsonify(result), 200
    else:
        return jsonify({"message": "Error fetching email updates. Try again!"}), 400

@app.route('/authenticate')
def authenticate():
    result = google_authenticate()
    if(type(result) != "str"):
        return jsonify(True), 200
    else:
        return jsonify(False), 400

@app.route('/gmail/markAsRead/<id>')
def mark_as_read(id):
    result = read_email(id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@app.route('/calendar/getEventsList')
def get_events_list():
    response = events_list()
    if type(response) != "str":
        return jsonify(response), 200
    else:
        return jsonify({"message": "An error occurred."}), 400

@app.route('/calendar/eventsForTomorrow')
def events_for_tomorrow():
    response = events_list(when="tomorrow")
    if type(response) != "str":
        return jsonify(response), 200
    else:
        return jsonify({"message": "An error occurred."}), 400

@app.route('/tasks/getTaskList/<when>')
def get_task_list(when):
    if when == "today" or when == "tomorrow":
        response = tasks_list(when)
    else:
        return jsonify({"message": "Arguments available for this endpoint: /today or /tomorrow"}), 404

    if type(response) != "str":
        return jsonify(response), 200
    else:
        return jsonify(response), 500



# CREATE FLASK APPLICATION
if __name__ == '__main__':
    app.run()






