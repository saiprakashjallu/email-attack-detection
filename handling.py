import imaplib
import json
import boto3
import datetime
from agent import EmailSecurityAgent, notify_user






def handle_suspicious_email(mail, email_id, signals, parsed_email):
    print(f"🔍 Detected intent: {signals.get('intent')}")  # Debug intent
    intent = signals.get('intent', '').lower()

    if intent in ['phishing', 'spoofing', 'spam']:
        print(f"⚠️ Suspicious Email Detected: {intent}")
        log_detection(signals, parsed_email)

        try:
            mail.copy(email_id, 'Phishing')
            mail.store(email_id, '+FLAGS', '\\Deleted')
            print("📥 Email moved to 'Phishing' folder and marked for deletion.")
        except Exception as e:
            print(f"❌ Failed to move/delete email: {e}")

        try:
            notify_user('saiprakashjallu@gmail.com', signals, parsed_email)
        except Exception as e:
            print(f"❌ Failed to notify user: {e}")
    else:
        print("✅ Email appears safe.")

log_data = []  # Collect logs during script run

def log_detection(signals, parsed_email):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "signals": signals,
        "subject": parsed_email.get("subject", ""),
        "from": parsed_email["headers"].get("From", ""),
        "body_snippet": parsed_email.get("body", "")[:200]
    }
    log_data.append(log_entry)


def upload_logs_to_s3(bucket_name, log_data):
    if not log_data:
        print("ℹ️ No logs to upload.")
        return

    s3 = boto3.client("s3")
    filename = f"logs/email_log_{datetime.datetime.utcnow().isoformat()}.json"

    # ✅ Convert to NDJSON format (one JSON object per line)
    body = "\n".join([json.dumps(entry) for entry in log_data])

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=body,
            ContentType='application/json'
        )
        print(f"✅ Logs uploaded to s3://{bucket_name}/{filename}")
    except Exception as e:
        print(f"❌ Failed to upload logs to S3: {e}")



if __name__ == "__main__":
    agent = EmailSecurityAgent(api_key="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")

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('mail.24gateway@gmail.com', 'nriy eydm ugsq ccpb')
    mail.select('inbox')

    _, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()
    print(f"📬 Found {len(email_ids)} unseen email(s).")


    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, '(RFC822)')
        raw_email = msg_data[0][1]

        parsed_email = agent.parse_email(raw_email)
        signals = agent.capture_signals(parsed_email)

        print("📥 Parsed Email:")
        print(json.dumps(parsed_email, indent=2))

        print("🧠 LLM Output:")
        print(json.dumps(signals, indent=2))

        handle_suspicious_email(mail, email_id, signals, parsed_email)
        upload_logs_to_s3("phishingmails", log_data)


    mail.expunge()
    mail.logout()
