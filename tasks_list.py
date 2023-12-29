import datetime

from gmail_authenticate import google_authenticate, get_service


def tasks_list(token, when="today"):

    min_time = datetime.datetime.utcnow().isoformat() + 'Z'
    max_time = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    if when == "tomorrow":
        now = datetime.datetime.utcnow()
        min_time = now + datetime.timedelta(days=1)
        max_time = min_time.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        min_time = min_time.replace(hour=0, minute=0, second=0).isoformat() + "Z"

    try:
        service = get_service(token, "tasks")
        if isinstance(service, str):
            e = Exception(service)
            raise e
        else:
            response = {}
            results = service.tasks().list(tasklist="@default", showHidden=False, showCompleted=False, dueMin=min_time, dueMax=max_time).execute()
            tasks = results.get("items", [])
            response['count'] = len(tasks)
            response['tasks'] = tasks
            return response
    except Exception as e:
        return e.__str__()
