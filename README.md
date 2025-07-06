## AI-Powered Email Threat Detection

This project is an AI-powered **Email Security Agent** designed to intelligently scan, classify suspicious emails (phishing, spoofing, spam). It sends users a notification.
---

##  Use Case

-  **Inbound Email Protection**: Analyze every incoming email using a Large Language Model (LLM) for intent, tone, and threat indicators.
-  **LLM-Powered Detection**: Identify phishing, spam, spoofing, and other threats with contextual awareness.
-  **Quarantine Suspicious Mails**: Automatically move flagged messages to a "Phishing" folder for manual review.
-  **User Notification System**: Notify users with actionable links to allow or deny suspicious messages.
-  **Cloud Logging**: Store structured logs securely in Amazon S3, enabling traceability and analytics.

---

## 🔁 Workflow

1. **Email Intake**
   - Connect to Gmail inbox via IMAP.
   - Fetch `UNSEEN` messages.

2. **LLM Signal Extraction**
   - Use GPT-4 Turbo to extract:
     - Intent (phishing, benign, etc.)
     - Emotional tone
     - Suspicious elements
     - Requested actions
     - Anomalies

3. **Quarantine Logic**
   - If `intent` is `phishing/spam/spoofing`, move to "Phishing" folder.
   - Mark email as read and log detection.

4. **User Notification**
   - Send a notification email to the user with:
     - Sender, subject, snippet


6. **Cloud Logging**
   - Upload detection logs as NDJSON to S3 for future audits and analytics.

---

## 🏗️ Architecture

```plaintext
┌────────────┐        ┌────────────────┐       ┌──────────────────────┐
│   Gmail    │───────▶│  EmailSecurity │──────▶│  Quarantine Handler  │
│ (via IMAP) │        │    Agent (LLM) │       └────────────┬─────────┘
└────────────┘        └────────────────┘                    │
                                                           ▼
                                                  ┌────────────────┐
                                                  │ Phishing Folder│
                                                  └────────────────┘
                                                           │
                 ┌─────────────┐                           ▼
                 │ AWS S3 Logs │◀─────────────────┐   ┌────────────┐
                 └─────────────┘                  │   │ Flask API  │
                                                 │   └────┬───────┘
          ┌───────────────────────────────┐      │        ▼
          │ Quarantine Notification Email │──────┘   Allow / Deny
          └───────────────────────────────┘           Endpoints






**🛠️ Setup
Install dependencies
pip install -r requirements.txt
Set up Gmail IMAP access
Enable IMAP in Gmail settings
Create an App Password
Configure AWS CLI
aws configure
Run the handler
python handling.py


📂 Folder Structure
LLM-Agents/
├── agent.py                 # Core logic for email parsing and LLM analysis
├── handling.py              # Main entry script to process emails
├── notify.py                # Email notification handler
├── quarantine_api.py        # Flask API to handle Allow/Deny actions
├── logs/                    # Local log staging (optional)
├── requirements.txt
└── README.md
🧠 Future Enhancements
✅ UI dashboard for users to manage quarantined emails
✅ Athena integration for querying logs
✅ Daily summary digest of quarantined emails
✅ Feedback-based reinforcement learning
**
