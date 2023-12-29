from gmail_authenticate import google_authenticate, get_service


def read_email(token, message_id):
    try:
        service = get_service(token, "email")
        if isinstance(service, str):
            e = Exception(service)
            raise e
        else:
            service.users().messages().modify(
                userId="me",
                id=message_id,
                body={
                    "removeLabelIds": ["UNREAD"]
                }).execute()
            return "Success!"
    except Exception as e:
        return e.__str__()
