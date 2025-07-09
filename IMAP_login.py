import imaplib
import email

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('You Mail ID', 'APP Password')
mail.select('inbox')

_, data = mail.search(None, 'UNSEEN')
email_ids = data[0].split()
for email_id in email_ids:
    _, msg_data = mail.fetch(email_id, '(RFC822)')
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)
