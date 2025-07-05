import smtplib
from email.mime.text import MIMEText

def test_notify():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "mail.24gateway@gmail.com"
    sender_password = "nriy eydm ugsq ccpb"
    receiver_email = "saiprakashjallu@gmail.com"

    subject = "🚨 TEST Notification"
    body = "This is a test notification from your phishing email scanner."

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Test email sent.")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")

test_notify()
