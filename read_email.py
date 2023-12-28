from gmail_authenticate import google_authenticate


def read_email(message_id):
    service = google_authenticate()
    try:
        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={
                "removeLabelIds": ["UNREAD"]
            }).execute()
        return True
    except:
        return False