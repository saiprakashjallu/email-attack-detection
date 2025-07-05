from openai import OpenAI
import json
import email
import imaplib

import smtplib
from email.mime.text import MIMEText


class EmailSecurityAgent:
    def __init__(self, api_key, model="gpt-4-turbo"):
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def preprocess_email(self, email_data):
        return f"Subject: {email_data['subject']}\nHeaders: {json.dumps(email_data['headers'])}\nBody: {email_data['body']}"

    def capture_signals(self, email_data):
        prompt = f"""
        You are an AI agent tasked with email security. Analyze the email below and return structured JSON signals:

        - intent (benign, phishing, spam, spoofing)
        - emotional_tone (neutral, urgent, fearful, etc.)
        - suspicious_elements (spoofed domains, unusual links, attachments)
        - requested_actions (payments, credentials, clicks)
        - anomalies (linguistic errors, mismatched sender info, etc.)

        Email:\n{self.preprocess_email(email_data)}

        Return ONLY structured JSON without any additional text or commentary.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print("LLM Response could not be parsed as JSON:")
            print(content)
            raise e

    @staticmethod
    def parse_email(raw_email):
        email_message = email.message_from_bytes(raw_email)
        
        subject = email_message.get('subject', '')
        headers = dict(email_message.items())
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        body += payload.decode(errors='ignore')
        else:
            payload = email_message.get_payload(decode=True)
            if payload:
                body = payload.decode(errors='ignore')

        return {
            "subject": subject,
            "headers": headers,
            "body": body
        }

    def process_raw_email(self, raw_email):
        parsed_email = self.parse_email(raw_email)
        signals = self.capture_signals(parsed_email)
        return signals


def notify_user(receiver_email, signals, email_details):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "mail.24gateway@gmail.com"
    sender_password = "nriy eydm ugsq ccpb"

    subject = f"🚨 Suspicious Email Detected: {email_details['subject']}"
    body = f"""
    Suspicious email detected.

    LLM Signals:
    {json.dumps(signals, indent=4)}

    From: {email_details['headers'].get('From', 'N/A')}
    Body: {email_details['body'][:300]}
    """

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")



def notify_security_team(signals, parsed_email):
    smtp_server = 'smtp.yourdomain.com'
    smtp_port = 587
    sender_email = 'mail.24gateway@gmail.com'
    sender_password = 'nriy eydm ugsq ccpb'
    receiver_email = 'saiprakashjallu@gmail.com'

    subject = f"⚠️ Phishing Alert: {parsed_email['subject']}"
    body = f"""
    🚨 **Suspicious Email Detected** 🚨

    **Signals Captured:**  
    {json.dumps(signals, indent=4)}

    **Original Email Content:**  
    Subject: {parsed_email['subject']}  
    From: {parsed_email['headers'].get('From')}  
    Reply-To: {parsed_email['headers'].get('Reply-To', 'N/A')}  

    Email Body:  
    {parsed_email['body']}
    """

    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Security team notified successfully.")
    except Exception as e:
        print(f"❌ Error notifying security team: {e}")

def handle_suspicious_email(mail, email_id, signals, parsed_email):
    intent = signals.get('intent', '').lower()

    if intent in ['phishing', 'spoofing', 'spam']:
        print(f"⚠️ Suspicious Email Detected: {intent}")

        try:
            mail.copy(email_id, 'Phishing')
            mail.store(email_id, '+FLAGS', '\\Deleted')
            print("📥 Moved email to 'Phishing' and marked for deletion.")
        except Exception as e:
            print(f"❌ Error moving email: {e}")

        try:
            notify_user('saiprakashjallu@gmail.com', signals, parsed_email)
            # Or use notify_security_team(signals, parsed_email) if you prefer
        except Exception as e:
            print(f"❌ Notification failed: {e}")
    else:
        print("✅ Email appears safe.")




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

        print(json.dumps(signals, indent=4))

        handle_suspicious_email(mail, email_id, signals, parsed_email)




