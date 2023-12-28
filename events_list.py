import datetime
from gmail_authenticate import google_authenticate


def events_list(when="today"):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    max_time = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    if when == "tomorrow":
        now = datetime.datetime.utcnow()
        max_time = now + datetime.timedelta(days=1)
        now = now.isoformat() + "Z"
        max_time = max_time.isoformat()+"Z"

    try:
        service = google_authenticate('calendar')
        response = {}
        result = service.events().list(
            calendarId="primary",
            timeMin=now,
            timeMax=max_time,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        response["events"] = result.get("items", [])
        response["count"] = len(response["events"])
        return response
    except Exception:
        return Exception.__name__