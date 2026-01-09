# Gmail Reply Skill

Automated Gmail workflow for reading emails, drafting professional replies, and sending with user approval.

## Features

- **Read Inbox**: Fetch unread emails from Gmail inbox
- **Spam Filter**: Automatically ignore spam and promotional emails
- **Smart Drafting**: Draft contextual, professional replies
- **User Approval**: Never sends without explicit user consent
- **Security Checks**: Blocks sensitive data (passwords, credit cards, SSN, API keys)
- **Draft Management**: Save rejected drafts to Gmail Drafts folder
- **Thread Support**: Proper email threading with In-Reply-To headers

## Workflow

```
┌─────────────────┐
│  Fetch Emails   │ ← Exclude spam/trash
└────────┬────────┘
         ▼
┌─────────────────┐
│ Analyze Content │ ← Extract sender, subject, body
└────────┬────────┘
         ▼
┌─────────────────┐
│  Draft Reply    │ ← Professional, contextual
└────────┬────────┘
         ▼
┌─────────────────┐
│ Security Check  │ ← Block sensitive data
└────────┬────────┘
         ▼
┌─────────────────┐
│ User Approval   │ ← REQUIRED before send
└────────┬────────┘
         ▼
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│ Send  │ │ Draft │
└───────┘ └───────┘
```

## Prerequisites

### Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download `credentials.json`

### Required Scopes

```
gmail.readonly   - Read emails
gmail.compose    - Create drafts
gmail.send       - Send emails
gmail.modify     - Manage labels
```

## Usage

Trigger this skill by asking:

- "Check my Gmail and reply to emails"
- "Read my inbox and draft replies"
- "Process unread emails"
- "Help me respond to my emails"

## Security

### Blocked Patterns

| Type | Pattern |
|------|---------|
| Credit Card | `\d{4}-\d{4}-\d{4}-\d{4}` |
| SSN | `\d{3}-\d{2}-\d{4}` |
| API Keys | 32+ character strings |
| Passwords | `password: xxx` patterns |
| Private Keys | `-----BEGIN PRIVATE KEY-----` |

### Safety Rules

1. **No Auto-Send**: Every reply requires user approval
2. **Spam Ignored**: Never processes spam emails
3. **Data Filtering**: Sensitive info auto-redacted
4. **Audit Trail**: All actions logged

## Files

```
gmail-reply/
├── SKILL.md                    # Main workflow instructions
├── README.md                   # This file
└── references/
    └── gmail-api.md            # API documentation & code examples
```

## API Reference

See [references/gmail-api.md](references/gmail-api.md) for:

- Authentication setup
- List/Get messages
- Send/Create drafts
- Reply threading
- Error handling
- Rate limits

## License

MIT License - See LICENSE file for details.
