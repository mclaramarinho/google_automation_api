import datetime

from gmail_authenticate import google_authenticate


def tasks_list(when="today"):

    service = google_authenticate("tasks")

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    max_time = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    if when == "tomorrow":
        now = datetime.datetime.utcnow()
        max_time = now + datetime.timedelta(days=1)
        now = now.isoformat() + "Z"
        max_time = max_time.isoformat() + "Z"

    response = {}

    try:
        results = service.tasks().list(tasklist="@default", showHidden=False, showCompleted=False, dueMin=now, dueMax=max_time).execute()
        tasks = results.get("items", [])
        response['count'] = len(tasks)
        response['tasks'] = tasks
        return response

    except Exception as e:
        return e.__str__()
