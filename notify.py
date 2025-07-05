import imaplib
import json
import os
from agent import EmailSecurityAgent, notify_user

def handle_suspicious_email(mail, email_id, signals, parsed_email):
    if signals['intent'] in ['phishing', 'spoofing', 'spam']:
        mail.copy(email_id, 'Phishing')
        mail.store(email_id, '+FLAGS', '\\Deleted')

        notify_user('saiprakashjallu@gmail.com', signals, parsed_email)

if __name__ == "__main__":
    agent = EmailSecurityAgent(api_key="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")

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('mail.24gateway@gmail.com', 'nriy eydm ugsq ccpb')
    mail.select('inbox')

    _, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, '(RFC822)')
        raw_email = msg_data[0][1]

        parsed_email = agent.parse_email(raw_email)
        signals = agent.capture_signals(parsed_email)

        handle_suspicious_email(mail, email_id, signals, parsed_email)

    mail.expunge()
    mail.logout()
