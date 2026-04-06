# Zoho Mail Provider Reference

How to fetch emails and create drafts using the official Zoho Mail MCP connector.

---

## Prerequisites

The user must have Zoho Mail connected as an MCP connector via [zoho.com/mcp](https://www.zoho.com/mcp/).

If the tools aren't found via `ToolSearch`, tell the user:

> I can't find the Zoho Mail tools. You can set up the Zoho Mail MCP connector
> at [zoho.com/mcp](https://www.zoho.com/mcp/) — select **Zoho Mail**, follow
> the setup steps, then come back and try again.

---

## Available tools

| Tool | Purpose |
|------|---------|
| `ZohoMail_getMailAccounts` | Retrieve account details (needed to get `accountId`) |
| `ZohoMail_listEmails` | List emails in a folder with filters (status, flags, labels) |
| `ZohoMail_SearchEmails` | Search emails using Zoho search syntax |

### Known limitations (as of April 2026)

- **No `create_draft` tool** — the MCP does not support saving drafts.
- **No `read_email` tool** — no way to fetch the full body of a single message.
  Use the `summary` field from `listEmails` to get a preview.
- **No `sendEmail` tool** may be available — depends on user's permission grants.

---

## Step 0: Get the account ID and email addresses

Call `getMailAccounts` first — every other tool requires `accountId` as a path variable.

```
ZohoMail_getMailAccounts()
```

Extract the `accountId` from the primary account in the response. Store it for all
subsequent calls.

### Discovering available email addresses

The `getMailAccounts` response contains an `emailAddress` array with all addresses
on the account (primary + aliases). Each entry has:
- `mailId` — the email address (e.g. `hello@example.com`)
- `isPrimary` — whether this is the primary address
- `isAlias` — whether this is an alias

Present these to the user so they can choose which address to triage. For example:

```
emailAddress: [
  { "mailId": "email@email.io", "isPrimary": true, "isAlias": false },
  { "mailId": "admin@email.io", "isPrimary": false, "isAlias": true }
]
```

Store the user's chosen address for filtering in Step 1.

---

## Step 1: Fetch unread emails from the last 24 hours

### Primary approach — `listEmails` with unread filter

This is the most reliable method. Use `status: "unread"` and request the fields
we need:

```
ZohoMail_listEmails(
  path_variables: { accountId: "{accountId}" },
  query_params: {
    status: "unread",
    fields: "summary,subject,messageId,folderId,fromAddress,toAddress,receivedTime,threadId",
    limit: 200,
    sortBy: "date",
    sortorder: false
  }
)
```

**Parameter notes:**
- `status` — set to `"unread"` to filter for unread messages only
- `fields` — comma-separated list of fields to return. Include `summary` for the
  email preview text. Available fields: `summary`, `sentDateInGMT`, `calendarType`,
  `subject`, `messageId`, `threadCount`, `flagid`, `status2`, `priority`, `hasInline`,
  `toAddress`, `folderId`, `ccAddress`, `threadId`, `hasAttachment`, `size`, `sender`,
  `receivedTime`, `fromAddress`, `status`
- `limit` — max 200 per request
- `sortBy` — `"date"` to get newest first
- `sortorder` — `false` for descending (newest first)
- `folderId` — optional; omit to search across folders, or set to Inbox folder ID

**Date filtering:** `listEmails` does not have a native date range parameter.
After fetching, filter results client-side: compare each email's `receivedTime`
to 24 hours ago and discard older messages.

**Address filtering:** If the user selected a specific email address in Step 0,
filter results to only include emails where the `toAddress` field contains the
chosen address. The `toAddress` value may include display names and angle brackets
(e.g. `"Hello"<hello@example.com>` or `<admin@example.com>`), so match by
checking if the chosen address appears anywhere in the `toAddress` string.
If the user chose "all", skip this filter.

### Alternative — `SearchEmails` with date syntax

Use Zoho's search syntax for date-bounded search:

```
ZohoMail_SearchEmails(
  path_variables: { accountId: "{accountId}" },
  query_params: {
    searchKey: "fromDate:{DD-MMM-YYYY}",
    limit: 200
  }
)
```

Replace `{DD-MMM-YYYY}` with yesterday's date (e.g. `04-APR-2026`).

**Filtering by address:** If the user selected a specific email address, combine
with the `to:` search key:

```
searchKey: "to:hello@example.com::fromDate:04-APR-2026"
```

**Search syntax reference:**
- `fromDate:04-APR-2026` — emails received from this date
- `toDate:05-APR-2026` — emails received up to this date
- Combine with `::` for AND: `fromDate:04-APR-2026::toDate:05-APR-2026`
- `sender:abc@domain.com` — filter by sender
- `subject:"keyword"` — filter by subject
- `has:attachment` — only emails with attachments
- `entire:keyword` — full-text search

**Note:** `SearchEmails` does not have a `status` (read/unread) filter in its
search syntax. You may need to cross-reference with `listEmails` results or
filter client-side if the response includes a status field.

### Data to extract per message

| Field | Source | Notes |
|-------|--------|-------|
| `message_id` | `messageId` | Unique message identifier |
| `thread_id` | `threadId` | May be absent for single new emails |
| `from` | `fromAddress` | Sender's email address |
| `subject` | `subject` | Email subject line |
| `body_preview` | `summary` | Preview/snippet — full body is NOT available |
| `received_at` | `receivedTime` | Timestamp (compare to 24h ago for filtering) |

---

## Step 3: Create draft replies

### If a `create_draft` tool now exists

Always check `ToolSearch` first — Zoho may have added draft support since this
reference was written. If a draft tool exists, use it.

### Current reality: no draft tool available

The Zoho Mail MCP currently has no draft or send tools available. Instead:

1. **Present the drafts in chat** for the user to copy into Zoho Mail manually:

   > The Zoho Mail connector doesn't support creating drafts yet. Here are the
   > draft replies — you can copy them into Zoho Mail:

2. For each email, format a ready-to-copy block:

   ```
   ---
   To: {fromAddress}
   Subject: Re: {subject}

   [REPLY NEEDED] — This email requires a human reply.

   --- Original message from {fromAddress} ---
   {summary / first 3 lines}
   ---
   ```

3. After presenting all drafts, tell the user:

   > I've prepared {N} draft replies above. Copy each one into Zoho Mail as a
   > reply to the original thread. I'll keep an eye on whether Zoho adds draft
   > creation to their MCP — once they do, this step will be fully automated.

### If `sendEmail` becomes available

If the user has granted send permissions and a `sendEmail` tool appears:

1. **Warn the user** — sending is irreversible, unlike creating drafts.
2. **Only send if the user explicitly confirms** for each email or as a batch.
3. Never send without confirmation, even if the user originally said "triage emails."

---

## Threading notes

- A single new email (no prior replies) may not have a `threadId`.
- The `threadId` field from `listEmails` is the most reliable threading reference.
- When composing replies manually, the user should reply from within the original
  thread in Zoho Mail to maintain threading.

---

## Error handling

- If `ToolSearch` finds no Zoho Mail tools → connector not connected, guide user to set up
- If `getMailAccounts` fails → authentication issue, ask user to reconnect the connector
- If `listEmails` returns empty with `status: "unread"` → no unread emails, report inbox zero
- If a specific operation fails → log the error, skip that message, continue with the rest
- Report all failures at the end with the error details
