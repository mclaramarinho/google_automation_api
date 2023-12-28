from gmail_authenticate import google_authenticate
import datetime
import os
from base64 import urlsafe_b64decode
from bs4 import BeautifulSoup


def email_colector():

    try:
        service = google_authenticate()

        TODAY = datetime.date.today()
        TODAY_F = f"{TODAY.year}/{TODAY.month}/{TODAY.day}"

        TOMORROW = TODAY + datetime.timedelta(days=1)
        TOMORROW_F = f"{TOMORROW.year}/{TOMORROW.month}/{TOMORROW.day}"


        YESTERDAY = TODAY.replace(day=TODAY.day - 1)
        YESTERDAY_F = f"{YESTERDAY.year}/{YESTERDAY.month}/{YESTERDAY.day}"

        # list all messages labeled as unread + important + today
        result = service.users().messages().list(userId='me',q=f"is:important is:unread after: {TODAY_F} before: {TOMORROW_F}").execute()
        messages = []
        # if there's only one page
        if "messages" in result:
            messages.extend(result['messages'])
        # if there's more than one page
        while "nextPageToken" in result:
            page_token = result['nextPageToken']
            result = service.users().messages().list(userId='me', q=f"is:important is:unread after: {TODAY_F} before: {TOMORROW_F}",pageToken=page_token).execute()
            if "messages" in result:
                messages.extend(result['messages'])


        # after listing all the relevant messages
        count = 0
        response_data = {"count": count, "messages": []}
        for message in messages:
            count += 1
            # get each message's details
            m = service.users().messages().get(userId="me", id=message['id'], format="full").execute()
            current_id = m['id']
            thread_id = m["threadId"]


            payload = m['payload']
            headers = payload['headers']

            parts = []
            if 'parts' in payload:
                parts = payload['parts']

            current_subject = "(no subject)"
            sender = ""
            for h in headers:
                if h["name"] == "From":
                    sender = h["value"]

                if h["name"] == "Subject":
                    current_subject= h["value"]

            decoded_body = ""
            for p in parts:

                if p['mimeType'] == "text/plain":
                    body = p['body']['data']
                    decoded_body = urlsafe_b64decode(body).decode()
                if p['mimeType'] == "text/html":
                    filename = p['filename']
                    if not filename:
                        filename = "index.html"
                    filepath = os.path.join('', filename)
                    with open (filepath, "wb") as f:
                        body = p['body']['data']
                        f.write(urlsafe_b64decode(body))

                    with open (filepath, "rb") as f:
                        soup = BeautifulSoup(f.read(), "html.parser")
                        decoded_body = soup.text

            response_data["messages"].append({"id": current_id, "threadId": thread_id, "sender": sender, "subject": current_subject, "body": decoded_body.replace("  ", "")})
        response_data["count"] = count
        return response_data
    except Exception as e:
        return e.__str__()
