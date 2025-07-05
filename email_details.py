def parse_email(email_message):
    subject = email_message['subject']
    headers = dict(email_message.items())
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode()
    else:
        body = email_message.get_payload(decode=True).decode()

    return {
        "subject": subject,
        "headers": headers,
        "body": body
    }
