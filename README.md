# 📧 LLM Email Automation

A Python-based email automation system for LLM agents and applications. This repository provides **sanitized**, production-ready code for sending, reading, and managing emails through Gmail accounts.

> **Note:** This system is specifically designed for **Gmail/Google Workspace accounts**.

---

## ✨ Features

- ✅ Send text emails
- ✅ Send HTML-formatted emails (with styling support)
- ✅ Read/unread email inbox
- ✅ Search and filter emails (by sender, subject, body)
- ✅ Delete emails (bulk or single)
- ✅ Mark emails as read/unread
- ✅ Get email count and statistics
- ✅ Credential management with app password support

---

## 🔐 Prerequisites

### Gmail Account Setup

Before using this system, you must configure your Gmail account:

1. **Enable 2-Factor Authentication (2FA)**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Under "Signing in to Google," enable 2-Step Verification

2. **Generate an App Password**
   - After enabling 2FA, go to [App passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" as the app
   - Select "Other (Custom name)" and enter "LLM Email Automation"
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

3. **Create Credentials File**
   - Create a file named `email_creds.txt` with this format:
     ```
     username: your-email@gmail.com
     password: your-regular-password
     app_password: abcd efgh ijkl mnop
     ```

---

## 📁 Repository Structure

```
llm-email-automation/
├── src/
│   ├── send_email.py          # Send text emails (CLI + API)
│   ├── send_html_email.py     # Send HTML emails (CLI + API)
│   ├── read_emails.py         # Read/unread inbox
│   ├── search_emails.py       # Search/filter emails
│   ├── delete_emails.py       # Delete emails
│   └── utils.py              # Helper functions (credential loading, etc.)
├── examples/
│   ├── example_send_text.py   # Example: Send text email
│   ├── example_send_html.py   # Example: Send HTML email
│   └── example_read_emails.py # Example: Read inbox
├── README.md                  # This file
├── LICENSE                    # MIT License
└── requirements.txt          # Python dependencies
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone this repository
git clone https://github.com/your-username/llm-email-automation.git
cd llm-email-automation

# Create credentials file
touch email_creds.txt
# Edit with your credentials (see above)

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### Send a Text Email

```python
from src.send_email import send_text_email

# Send email using default credentials from email_creds.txt
send_text_email(
    to_address="recipient@example.com",
    subject="Test Email",
    body="Hello from LLM Email Automation!"
)
```

#### Send an HTML Email

```python
from src.send_html_email import send_html_email

html_content = """
<!DOCTYPE html>
<html>
<body>
    <h1>Hello!</h1>
    <p>This is an <strong>HTML email</strong>.</p>
</body>
</html>
"""

send_html_email(
    to_address="recipient@example.com",
    subject="HTML Test",
    html_content=html_content
)
```

#### Read Unread Emails

```python
from src.read_emails import read_unread_emails

emails = read_unread_emails()
for email in emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print("---")
```

---

## 📖 API Reference

### Credentials

**Location:** `email_creds.txt`

**Format:**
```
username: your-email@gmail.com
password: your-regular-password
app_password: abcd efgh ijkl mnop
```

**Important:** The system uses **line 3** (app_password) for SMTP authentication.

### Functions

#### `send_text_email(to_address, subject, body, from_address=None, attachments=None)`

Send a text email.

| Parameter | Type | Required | Description |
|---------|------|----------|-------------|
| `to_address` | `str` | ✅ | Recipient email address |
| `subject` | `str` | ✅ | Email subject line |
| `body` | `str` | ✅ | Email body text |
| `from_address` | `str` | ❌ | Sender address (defaults to credentials) |
| `attachments` | `list` | ❌ | List of file paths to attach |

#### `send_html_email(to_address, subject, html_content, from_address=None)`

Send an HTML-formatted email.

| Parameter | Type | Required | Description |
|---------|------|----------|-------------|
| `to_address` | `str` | ✅ | Recipient email address |
| `subject` | `str` | ✅ | Email subject line |
| `html_content` | `str` | ✅ | HTML content (full HTML document) |
| `from_address` | `str` | ❌ | Sender address (defaults to credentials) |

#### `read_unread_emails()`

Read all unread emails from inbox.

**Returns:** `list` of dictionaries with keys: `from`, `subject`, `body`, `date`, `message_id`

#### `search_emails(query, folder='inbox')`

Search emails by query string.

| Parameter | Type | Required | Description |
|---------|------|----------|-------------|
| `query` | `str` | ✅ | Search query (IMAP syntax) |
| `folder` | `str` | ❌ | Mailbox folder (default: 'inbox') |

**Example queries:**
- `FROM "gmail.com"` - Emails from Gmail
- `SUBJECT "meeting"` - Emails with "meeting" in subject
- `UNSEEN` - Unread emails only
- `SINCE "2024-01-01"` - Emails since date

#### `delete_emails(query, folder='inbox')`

Delete emails matching the query.

| Parameter | Type | Required | Description |
|---------|------|----------|-------------|
| `query` | `str` | ✅ | IMAP search query |
| `folder` | `str` | ❌ | Mailbox folder (default: 'inbox') |

**Returns:** `int` - Number of deleted emails

---

## 🧪 Examples

### Example 1: Send a Confirmation Email (HTML)

```python
from src.send_html_email import send_html_email

def send_order_confirmation(email, order_id, total):
    html = f"""
    <html>
    <body>
        <h1>Order Confirmed! 🎉</h1>
        <p>Thank you for your order.</p>
        <p><strong>Order ID:</strong> {order_id}</p>
        <p><strong>Total:</strong> ${total}</p>
    </body>
    </html>
    """
    send_html_email(email, "Your Order is Confirmed", html)
```

### Example 2: Monitor Incoming Emails

```python
from src.read_emails import read_unread_emails
from src.send_email import send_text_email

def monitor_inbox():
    emails = read_unread_emails()
    for email in emails:
        if "urgent" in email['subject'].lower():
            send_text_email(
                to_address="admin@example.com",
                subject="Urgent Email Detected",
                body=f"Subject: {email['subject']}\nFrom: {email['from']}"
            )
```

### Example 3: Clean Up Spam

```python
from src.delete_emails import delete_emails

# Delete all emails from a specific sender
delete_emails('FROM "noreply@spam.com"')

# Delete old newsletters (older than 30 days)
delete_emails('OLDER_THAN 30')
```

---

## 🛠️ CLI Usage

All scripts can be used from the command line:

```bash
# Send text email
python src/send_email.py --to recipient@example.com --subject "Test" --body "Hello"

# Send HTML email
python src/send_html_email.py recipient@example.com "HTML Test" < email_body.html

# Read unread emails
python src/read_emails.py

# Search emails
python src/search_emails.py --query 'FROM "boss@example.com"'

# Delete emails
python src/delete_emails.py --query 'FROM "newsletter@example.com"'
```

---

## 📋 Requirements

```
Python 3.8+
No external dependencies required (uses standard library only)
    - smtplib (SMTP)
    - imaplib (IMAP)
    - email (RFC822 parsing)
    - argparse (CLI)
```

---

## 🔒 Security Notes

1. **Never commit `email_creds.txt` to version control**
   - Add to `.gitignore`
   - Use environment variables in production: `EMAIL_USERNAME`, `EMAIL_APP_PASSWORD`

2. **App Passwords vs OAuth2**
   - This system uses **App Passwords** (simpler, sufficient for most use cases)
   - For OAuth2 (more secure, no app password needed), see `examples/oauth_example.py`

3. **Gmail Limitations**
   - 500 emails/day (free account)
   - 100 recipients per email
   - 25MB max attachment size

4. **Rate Limiting**
   - Google may temporarily block accounts with excessive activity
   - Add `time.sleep()` between bulk operations

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Add OAuth2 support (beyond app passwords)
- Support for other email providers (Outlook, Yahoo, etc.)
- Email template system
- Queue-based sending (for bulk operations)
- Webhook notifications for new emails

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Gmail SMTP/IMAP documentation
- Python `smtplib`, `imaplib`, and `email` modules
- LLM agent developers who inspired this system

---

## ❓ Troubleshooting

### "Application-specific password required"
- Use **line 3** from `email_creds.txt` (the app_password)

### "Connection refused" / "Timeout"
- Check internet connection
- Verify Gmail settings: [Less secure apps](https://myaccount.google.com/lesssecureapps) (if app password not configured)

### "Authentication failed"
- Regenerate app password
- Ensure 2FA is enabled on account
- Check credentials file format

For more help, see [Google's Gmail SMTP guide](https://support.google.com/mail/answer/7104828).

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-20  
**Maintainer:** LLM Email Automation Team
