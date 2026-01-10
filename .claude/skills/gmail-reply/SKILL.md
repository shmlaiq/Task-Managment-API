---
name: gmail-reply
description: Gmail email workflow automation for reading inbox emails, drafting professional replies, and sending with user approval. This skill should be used when user wants to (1) Read and process Gmail inbox emails, (2) Draft replies to emails, (3) Send approved email replies, (4) Manage email drafts. Automatically filters spam emails and requires explicit user approval before sending any reply. Includes security checks to prevent sensitive information leakage.
---

# Gmail Reply Workflow

Automated Gmail workflow for reading emails, drafting replies, and sending with user approval.

## Before Implementation

Gather context before processing emails:

| Source | Gather |
|--------|--------|
| **MCP Server** | Gmail MCP server configured and authenticated |
| **Conversation** | User's reply preferences, tone, signature style |
| **User Guidelines** | Response templates, auto-reply rules, blocked senders |
| **Security** | Sensitive data patterns to block, compliance requirements |

## Clarifications

### Required (ask before processing)
1. **Reply tone?** Professional / Casual / Match sender's tone
2. **Include signature?** Yes / No / Use default
3. **Send immediately?** Yes, if approved / Always save as draft first

### Optional
4. **Filter by sender?** Specific senders only / All unread
5. **Priority handling?** Urgent first / Chronological order

## Official Documentation

| Resource | URL | Use For |
|----------|-----|---------|
| Gmail API Docs | https://developers.google.com/gmail/api | Official reference |
| OAuth2 Guide | https://developers.google.com/identity/protocols/oauth2 | Authentication |
| Gmail API Quotas | https://developers.google.com/gmail/api/reference/quota | Rate limits |
| MCP Servers | https://modelcontextprotocol.io | MCP integration |

> **Security Note**: This skill NEVER sends emails without explicit user approval. All replies are security-scanned before sending.

## Prerequisites

- Gmail MCP server configured with OAuth2 credentials
- Required scopes: `gmail.readonly`, `gmail.compose`, `gmail.send`, `gmail.modify`

## Workflow Overview

```
1. Fetch unread emails (exclude SPAM)
2. For each email:
   a. Analyze content and context
   b. Draft professional reply
   c. Security check (no sensitive data)
   d. Present draft to user for approval
   e. If approved → Send reply
   f. If rejected → Save to Drafts folder
```

## Step 1: Fetch Emails

Fetch unread emails from inbox, excluding spam:

```python
# Query: is:unread -in:spam -in:trash
# Labels: INBOX, UNREAD (exclude SPAM, TRASH)
results = service.users().messages().list(
    userId="me",
    labelIds=["INBOX", "UNREAD"],
    q="-in:spam -in:trash"
).execute()
```

**Important**: NEVER read or process emails with SPAM label.

## Step 2: Analyze Email

For each email, extract:
- Sender name and email
- Subject line
- Email body content
- Thread ID (for proper reply threading)
- Message ID (for References/In-Reply-To headers)

## Step 3: Draft Reply

Draft a professional reply considering:
- Match the tone of the original email
- Be concise and relevant
- Address all questions/points raised
- Include appropriate greeting and sign-off

## Step 4: Security Check (CRITICAL)

Before presenting draft to user, scan for sensitive information:

**BLOCK if draft contains:**
- Passwords or API keys
- Credit card numbers (pattern: `\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}`)
- Social Security Numbers (pattern: `\d{3}-\d{2}-\d{4}`)
- Bank account numbers
- Private keys or tokens
- Personal addresses or phone numbers (unless contextually appropriate)
- Internal system credentials
- Confidential business information

If sensitive data detected:
1. Remove or redact the sensitive information
2. Notify user about the redaction
3. Ask user to manually add necessary information if needed

## Step 5: User Approval

Present draft to user with clear options:

```
📧 Reply Draft for: [Subject]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
From: [Original Sender]
To: [User's Email]

[Draft Content]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options:
✅ Approve & Send
✏️ Edit draft
📁 Save to Drafts
❌ Discard
```

**NEVER send without explicit user approval.**

## Step 6: Execute Action

Based on user decision:

### If Approved → Send Reply

```python
# Ensure proper threading with headers
message["In-Reply-To"] = original_message_id
message["References"] = original_message_id
message["Subject"] = f"Re: {original_subject}"

# Send via Gmail API
service.users().messages().send(
    userId="me",
    body={"raw": encoded_message, "threadId": thread_id}
).execute()
```

### If Rejected → Save to Drafts

```python
# Create draft instead of sending
service.users().drafts().create(
    userId="me",
    body={"message": {"raw": encoded_message, "threadId": thread_id}}
).execute()
```

## Email Threading Requirements

For proper reply threading:
1. Set `Subject` to `Re: [Original Subject]`
2. Set `In-Reply-To` header to original Message-ID
3. Set `References` header to original Message-ID
4. Include `threadId` in the API call

## Security Guidelines

1. **Input Validation**: Sanitize all email content before processing
2. **No Auto-Send**: Always require explicit user approval
3. **Sensitive Data Filter**: Block replies containing credentials, PII, or secrets
4. **Spam Handling**: Ignore all spam emails completely
5. **Rate Limiting**: Respect Gmail API quotas
6. **Audit Trail**: Log all sent emails for user review

## Error Handling

- **API Errors**: Retry with exponential backoff (max 3 attempts)
- **Auth Errors**: Prompt user to re-authenticate
- **Draft Failures**: Save locally and notify user
- **Network Issues**: Queue for retry when connection restored

## API Reference

See [references/gmail-api.md](references/gmail-api.md) for complete Gmail API documentation and code examples.

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Sending without approval | Security/privacy violation | ALWAYS get explicit user approval |
| Processing spam emails | Wastes time, potential security risk | Filter with `-in:spam -in:trash` |
| Missing thread headers | Reply appears as new email | Set `In-Reply-To` and `References` headers |
| Including sensitive data | Privacy breach, security risk | Run security scan before presenting draft |
| Ignoring rate limits | API quota exceeded, service blocked | Implement exponential backoff |
| No error handling | Silent failures, lost emails | Handle API errors gracefully |

## Before Delivery Checklist

### Security (CRITICAL)
- [ ] User approval required before any send
- [ ] Sensitive data scan implemented
- [ ] Spam emails filtered out
- [ ] No credentials/PII in drafts

### Email Quality
- [ ] Proper threading (In-Reply-To, References headers)
- [ ] Subject prefixed with "Re:"
- [ ] Appropriate tone for context
- [ ] Signature included if configured

### Error Handling
- [ ] API errors handled with retry
- [ ] Auth failures prompt re-authentication
- [ ] Network issues queued for retry
- [ ] Failed sends saved to drafts

### User Experience
- [ ] Clear draft preview before sending
- [ ] Easy approve/edit/discard options
- [ ] Confirmation after successful send
- [ ] Audit trail of sent emails
