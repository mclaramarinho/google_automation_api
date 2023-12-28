import datetime
from gmail_authenticate import google_authenticate


def events_list(when="today"):
    min_time = datetime.datetime.utcnow().isoformat() + 'Z'
    max_time = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    if when == "tomorrow":
        now = datetime.datetime.utcnow()
        min_time = now + datetime.timedelta(days=1)
        max_time = min_time.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        min_time = min_time.replace(hour=0, minute=0, second=0).isoformat() + "Z"

    try:
        service = google_authenticate('calendar')
        response = {}
        result = service.events().list(
            calendarId="primary",
            timeMin=min_time,
            timeMax=max_time,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        response["events"] = result.get("items", [])
        response["count"] = len(response["events"])
        return response
    except Exception as e:
        return e.__str__()