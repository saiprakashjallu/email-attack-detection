import smtplib
from email.mime.text import MIMEText

def test_notify():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "Your Mail ID"
    sender_password = "App Password"
    receiver_email = "Receiver Mail ID"

    subject = "TEST"
    body = "This is a test notification from phishing email scanner."

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Test email sent.")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")

test_notify()
