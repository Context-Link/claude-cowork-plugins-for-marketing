# Gmail Provider Reference

How to fetch emails and create drafts using the Gmail MCP connector.

---

## Prerequisites

The user must have Gmail connected as an MCP connector in Claude.
If the tools aren't found, tell the user:

> I can't find the Gmail tools. Make sure Gmail is connected:
> Go to **Settings → Connectors** and enable Gmail, then try again.

## Discovering Gmail tools

Gmail tools are loaded dynamically. Use the `ToolSearch` tool to find them:

```
ToolSearch(query: "+gmail", max_results: 10)
```

This searches for tools with "gmail" in the name. Look for tools like:
- A search/list tool — to search or list emails
- A read/get tool — to read a specific message
- A create-draft tool — to create a draft reply
- A send tool — **DO NOT USE THIS** (we only create drafts, never send)

The exact tool names may vary. Read the tool descriptions and parameter schemas
returned by `ToolSearch` to understand the correct parameter names and formats.
Do NOT guess parameter names — always check the tool schema first.

If `ToolSearch` returns no Gmail tools, the connector isn't connected. Tell the user:

> I can't find any Gmail tools. Make sure Gmail is connected as an MCP connector,
> then try again.

---

## Step 0: Discover email addresses

Use `ToolSearch` to check if there's a `get_profile` or similar tool that returns
the user's email addresses and aliases. Gmail's MCP connector may provide this.

If a profile tool exists, call it to get the list of addresses (primary + aliases
like send-as addresses). Present them to the user so they can choose which to triage.

If no profile tool is available, ask the user which email address they'd like to
triage, or whether to pull all unread emails regardless of recipient.

---

## Step 1: Fetch unread emails from the last 24 hours

Use the Gmail search/list tool with a query like:

```
is:unread newer_than:1d
```

**Filtering by address:** If the user selected a specific address, add a `to:`
filter to the search query:

```
is:unread newer_than:1d to:hello@example.com
```

This uses Gmail's native search syntax to find unread messages from the last day.

If the tool supports a `query` or `search` parameter, pass the above string.
If it uses separate filter parameters, set:
- `is_unread: true` (or equivalent)
- date filter for last 24 hours

For each message returned, you may need to call `get_message` or `read_email`
separately to fetch the full body content. The list/search endpoint often only
returns metadata (subject, from, date).

### Data to extract per message

| Field | Where to find it |
|-------|-----------------|
| `message_id` | Usually `id` or `messageId` in the response |
| `thread_id` | Usually `threadId` — critical for threading drafts |
| `from` | In message headers or a `from` field |
| `subject` | In message headers or a `subject` field |
| `body` | In message payload — prefer `text/plain` over `text/html` |
| `received_at` | `internalDate` or `date` header |

---

## Step 3: Create draft replies

Use the `create_draft` tool to create a reply draft. The key fields:

- **threadId** — set this to the original message's `threadId` so the draft
  appears in the same thread
- **to** — the original sender's email address (the `from` of the original)
- **subject** — `Re: {original_subject}` (unless the subject already starts with `Re:`)
- **body** — the placeholder content from Step 2
- **in_reply_to** or **references** — if the tool supports these headers, set them
  to the original message's `Message-ID` header. This ensures proper threading
  in email clients.

### Example flow (pseudocode)

```
# 1. Search
results = Gmail:search_emails(query="is:unread newer_than:1d")

# 2. For each result, get full message
for msg_id in results:
    message = Gmail:get_message(id=msg_id)
    
    # 3. Extract fields
    thread_id = message.threadId
    from_addr = message.from
    subject = message.subject
    body = message.body
    
    # 4. Create draft reply
    Gmail:create_draft(
        threadId=thread_id,
        to=from_addr,
        subject="Re: " + subject,
        body="[REPLY NEEDED] — This email requires a human reply.\n\n--- Original message from " + from_addr + " ---\n" + first_3_lines(body)
    )
```

Remember: the exact parameter names depend on what `ToolSearch` returns.
Always check the actual tool schema.
