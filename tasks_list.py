import datetime

from gmail_authenticate import google_authenticate, get_service


def tasks_list(token, when="today"):
    now = datetime.datetime.now(datetime.timezone.utc)
    start_today = now.replace(hour=0, minute=0, second=0)
    start_tomorrow = start_today + datetime.timedelta(days=1)

    min_time = start_today.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    max_time = start_tomorrow.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    if when == "tomorrow":
        end_tomorrow = start_tomorrow + datetime.timedelta(days=1)
        min_time = start_tomorrow.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        max_time = end_tomorrow.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    try:
        service = get_service(token, "tasks")
        if isinstance(service, str):
            e = Exception(service)
            raise e
        else:
            response = {}
            task_list_id = service.tasklists().list().execute()
            task_list_id = task_list_id["items"][0]["id"]
            results = service.tasks().list(tasklist=task_list_id, dueMin=min_time, dueMax=max_time).execute()
            tasks = results.get("items", [])
            response['count'] = len(tasks)
            response['tasks'] = tasks
            return response
    except Exception as e:
        return e.__str__()
