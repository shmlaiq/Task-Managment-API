# Gmail API Reference

Complete reference for Gmail API operations used in the gmail-reply workflow.

## Table of Contents

1. [Authentication Setup](#authentication-setup)
2. [List Messages](#list-messages)
3. [Get Message Details](#get-message-details)
4. [Send Message](#send-message)
5. [Create Draft](#create-draft)
6. [Send Reply in Thread](#send-reply-in-thread)
7. [Spam Detection Patterns](#spam-detection-patterns)
8. [Error Codes](#error-codes)

---

## Authentication Setup

```python
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify"
]

def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)
```

---

## List Messages

Fetch unread messages from inbox, excluding spam and trash.

```python
def list_unread_messages(service, max_results=10):
    """List unread messages excluding spam and trash."""
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        q="-in:spam -in:trash",
        maxResults=max_results
    ).execute()

    return results.get("messages", [])
```

### Query Filters

| Query | Description |
|-------|-------------|
| `is:unread` | Unread messages only |
| `-in:spam` | Exclude spam folder |
| `-in:trash` | Exclude trash folder |
| `from:email@example.com` | From specific sender |
| `newer_than:1d` | Messages from last day |

---

## Get Message Details

```python
def get_message_details(service, message_id):
    """Get full message details including headers and body."""
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    headers = message["payload"]["headers"]

    # Extract key headers
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")
    message_id_header = next((h["value"] for h in headers if h["name"] == "Message-ID"), "")

    # Get body
    body = get_message_body(message["payload"])

    return {
        "id": message["id"],
        "threadId": message["threadId"],
        "subject": subject,
        "from": sender,
        "message_id": message_id_header,
        "body": body,
        "labels": message.get("labelIds", [])
    }

def get_message_body(payload):
    """Extract text body from message payload."""
    if "body" in payload and payload["body"].get("data"):
        import base64
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data", "")
                if data:
                    import base64
                    return base64.urlsafe_b64decode(data).decode("utf-8")

    return ""
```

---

## Send Message

```python
import base64
from email.message import EmailMessage

def send_message(service, to, subject, body):
    """Send a new email message."""
    message = EmailMessage()
    message.set_content(body)
    message["To"] = to
    message["Subject"] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    result = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()

    return result
```

---

## Create Draft

```python
def create_draft(service, to, subject, body, thread_id=None):
    """Create a draft email (save without sending)."""
    message = EmailMessage()
    message.set_content(body)
    message["To"] = to
    message["Subject"] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    draft_body = {"message": {"raw": encoded_message}}
    if thread_id:
        draft_body["message"]["threadId"] = thread_id

    draft = service.users().drafts().create(
        userId="me",
        body=draft_body
    ).execute()

    return draft
```

---

## Send Reply in Thread

Critical for proper email threading.

```python
def send_reply(service, original_message, reply_body):
    """Send a reply to an existing email thread."""
    message = EmailMessage()
    message.set_content(reply_body)

    # Reply headers
    message["To"] = original_message["from"]
    message["Subject"] = f"Re: {original_message['subject']}"
    message["In-Reply-To"] = original_message["message_id"]
    message["References"] = original_message["message_id"]

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    result = service.users().messages().send(
        userId="me",
        body={
            "raw": encoded_message,
            "threadId": original_message["threadId"]
        }
    ).execute()

    return result
```

---

## Spam Detection Patterns

Check if a message should be skipped (spam detection).

```python
def is_spam_or_skip(message_details):
    """Check if message should be skipped."""
    labels = message_details.get("labels", [])

    # Skip if spam or promotional
    skip_labels = ["SPAM", "CATEGORY_PROMOTIONS", "TRASH"]
    if any(label in labels for label in skip_labels):
        return True

    # Skip auto-generated emails
    skip_senders = [
        "noreply@",
        "no-reply@",
        "donotreply@",
        "notifications@",
        "mailer-daemon@"
    ]
    sender = message_details.get("from", "").lower()
    if any(skip in sender for skip in skip_senders):
        return True

    return False
```

---

## Sensitive Data Patterns

Regex patterns for detecting sensitive information.

```python
import re

SENSITIVE_PATTERNS = {
    "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "api_key": r"\b[A-Za-z0-9_-]{32,}\b",
    "password": r"(?i)(password|passwd|pwd)\s*[:=]\s*\S+",
    "private_key": r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
    "aws_key": r"\bAKIA[0-9A-Z]{16}\b",
    "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "email_in_reply": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
}

def check_sensitive_data(text):
    """Check if text contains sensitive information."""
    findings = []
    for name, pattern in SENSITIVE_PATTERNS.items():
        if re.search(pattern, text):
            findings.append(name)
    return findings
```

---

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Re-authenticate |
| 403 | Forbidden | Check scopes/permissions |
| 404 | Not Found | Message may be deleted |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry with backoff |

### Retry Logic

```python
import time
from googleapiclient.errors import HttpError

def retry_with_backoff(func, max_retries=3):
    """Execute function with exponential backoff on failure."""
    for attempt in range(max_retries):
        try:
            return func()
        except HttpError as e:
            if e.resp.status in [429, 500, 503]:
                wait_time = (2 ** attempt) + 1
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## Rate Limits

- **Per user**: 250 quota units per second
- **messages.list**: 5 units per call
- **messages.get**: 5 units per call
- **messages.send**: 100 units per call
- **drafts.create**: 10 units per call

Implement delays between bulk operations to stay within limits.
