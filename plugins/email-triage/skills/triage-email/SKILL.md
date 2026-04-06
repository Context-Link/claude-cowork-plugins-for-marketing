---
name: triage-email
description: >
  Pull unread support emails from the last 24 hours, generate a draft reply for each,
  and push those drafts back into the correct thread — ready for a human to review and send.
  Supports Gmail (via MCP connector) and Zoho Mail (via MCP connector).
  Use this skill whenever the user says "triage emails", "triage inbox", "draft replies",
  "process support emails", "check support inbox", or any variation of pulling emails
  and creating draft responses. Also trigger when the user mentions triaging, batching,
  or bulk-replying to customer emails.
args:
  email_provider:
    description: "The email provider to use: 'gmail' or 'zoho'"
    required: false
  email_address:
    description: "The specific email address to triage (e.g. hello@preproduct.io). Use 'all' for all addresses."
    required: false
  output:
    description: "Where to put the draft replies: 'apple-mail', 'desktop', or 'chat'. Defaults to asking the user."
    required: false
---

# Triage Email Skill

Pull unread emails from the last 24 hours, generate a draft reply for each, and push
those drafts back as threaded replies — ready for a human to review and send.

---

## Pre-flight: Detect the email provider

Check if `email_provider` was passed as an argument. If so, use it directly.
If not, ask the user which provider to use.

The two supported providers are **Gmail** and **Zoho Mail**.

| Provider | Integration method | Reference file |
|----------|-------------------|----------------|
| Gmail (`gmail`) | MCP tools (discovered via `ToolSearch`) | `gmail.md` (same directory as this file) |
| Zoho Mail (`zoho`) | MCP tools (discovered via `ToolSearch`) | `zoho.md` (same directory as this file) |

Read the appropriate reference file before starting. Only ask if `email_provider`
was not provided:

> Which inbox should I pull from — **Gmail** or **Zoho**?

## Pre-flight: Choose the email address

Check if `email_address` was passed as an argument. If so, use it directly
(skip the address selection prompt). If the value is `"all"`, skip address filtering.

If `email_address` was not provided, fetch the available email addresses/aliases
from the account and present them to the user:

> I found these email addresses on your account:
>
> 1. **hello@example.com** (primary)
> 2. **admin@example.com** (alias)
> 3. **support@example.com** (alias)
>
> Which address should I triage? Or should I pull unread emails for all of them?

Use the selected address to filter results in Step 1 — only show emails sent **to**
that address. If the user picks "all", skip the filter and show everything.

See the provider-specific reference file for how to filter by recipient address.

---

## The workflow

### Step 0 — Load lessons from Context Link

Before processing any emails, fetch previously recorded support lessons once:

```
🔗 Retrieving lessons from Context Link → customer-support-email-lessons
```

Use the **get-context** skill with the slug `customer-support-email-lessons` (no mode
param needed). If lessons are returned, hold them in memory and pass them as context
when drafting replies in Step 2. These lessons take priority over general style rules
in draft-email-response — they represent real corrections from past edits.

If the fetch returns empty or fails, continue without lessons.

### Step 1 — Fetch unread emails from the last 24 hours

Pull all unread messages received in the last 24 hours. For each message, capture:

- `message_id` — unique ID for the message
- `thread_id` — thread/conversation ID (for threading the reply correctly)
- `from` — sender email address
- `subject` — email subject line
- `body` — full email body (plain text preferred, HTML fallback)
- `received_at` — timestamp

Follow the provider-specific reference file for exact tool calls / API requests.

After fetching, present a summary table to the user:

```
Found {N} unread emails from the last 24 hours:

| # | From | Subject | Received |
|---|------|---------|----------|
| 1 | customer@example.com | Order not received | 2h ago |
| 2 | ... | ... | ... |
```

Ask the user to confirm before proceeding:

> I found {N} unread emails. Want me to create draft replies for all of them,
> or would you like to pick specific ones?

### Step 2 — Generate reply using draft-email-response

For each email the user confirmed in Step 1, use the **draft-email-response** skill
to generate a context-aware draft reply. Pass the email details as args:

```
draft-email-response(
  from: "{fromAddress}",
  subject: "{subject}",
  body: "{summary or body content}",
  prompt_lessons: "false",
  get_lessons: "false"
)
```

The draft-email-response skill will:
1. Identify the core issue in the email
2. Look up relevant context via the **get-context** skill (Context Link)
3. Draft a warm, clear, practical reply

Collect the draft reply text returned by the skill for each email.

**If draft-email-response is not available**, fall back to the placeholder format:

```
Subject: Re: {original_subject}
Body:    [REPLY NEEDED] — This email requires a human reply.

--- Original message from {from} ---
{first 3 lines of body}
```

The placeholder tag `[REPLY NEEDED]` makes these easy to find and filter in the inbox.

### Step 3 — Deliver the drafts

Check the `output` arg to determine where to put the drafts. If `output` was not
provided, ask the user:

> Where would you like the draft replies?
>
> 1. **Apple Mail** — create drafts directly in Mail.app on your Mac
> 2. **Desktop folder** — save as .rtf files in a dated folder on your Desktop
> 3. **Chat** — display them here so you can copy-paste

#### Output: `apple-mail`

Use the Apple Mail MCP to create drafts locally in Mail.app via AppleScript.

First, check if Apple Mail tools are available:

```
ToolSearch(query: "+apple mail", max_results: 10)
```

If found, use the `create_draft` (or equivalent) tool for each reply:
- **to** — the original sender's email
- **subject** — `Re: {original_subject}`
- **body** — the draft reply from Step 2

If Apple Mail tools are NOT found, tell the user:

> The Apple Mail MCP isn't connected. You can set it up from:
> [github.com/Context-Link/apple-mail-mcp](https://github.com/Context-Link/apple-mail-mcp)
>
> In the meantime, would you like me to save to a **Desktop folder** or show
> them in **chat** instead?

After creating drafts:

```
✓ Created {N} draft replies in Apple Mail.
  Open Mail.app → Drafts to review and send.
```

#### Output: `desktop`

Create a dated folder on the user's Desktop and save each draft as an `.rtf` file.

1. Create the folder: `~/Desktop/email-drafts-{YYYY-MM-DD}/`
2. For each draft, create a file named: `reply-to-{from-address}-{short-subject}.rtf`
3. Each file contains the full draft reply, formatted as:

```
To: {fromAddress}
Subject: Re: {original_subject}

{draft reply body}
```

Use bash to create the folder and write the files. Keep filenames clean —
lowercase, dashes for spaces, strip special characters, truncate long subjects.

After saving:

```
✓ Saved {N} draft replies to ~/Desktop/email-drafts-{YYYY-MM-DD}/
  Open the folder to review, then copy-paste into your email client.
```

#### Output: `chat`

Display each draft in the conversation for the user to copy-paste manually.

For each draft, format as:

```
---
**To:** {fromAddress}
**Subject:** Re: {original_subject}

{draft reply body}
---
```

After displaying all drafts:

```
✓ {N} draft replies above — copy each into your email client as a reply
  to the original thread.
```

---

## Error handling

- If no unread emails are found, tell the user: "No unread emails from the last 24 hours — inbox zero!"
- If a specific draft fails to create, log the error, skip it, and continue with the rest. Report failures at the end.
- If the email provider connection fails (e.g. Gmail MCP not connected, Zoho MCP not connected), give the user clear instructions on how to fix it. For Zoho, direct them to [zoho.com/mcp](https://www.zoho.com/mcp/) to set up the connector.
- If the chosen output method fails (e.g. Apple Mail MCP not found), offer the fallback options.

---

## Dependencies

This skill relies on two other skills:

- **draft-email-response** — Generates context-aware draft replies (Step 2).
  Located in the same plugin at `skills/draft-email-response/`. If not available,
  the skill falls back to placeholder `[REPLY NEEDED]` drafts.
- **get-context** — Retrieves internal knowledge from Context Link. Used by
  draft-email-response to look up product docs, support history, and policies.
  If not available, draft-email-response can still generate replies but without
  internal context.
- **update-memory** — Saves lessons learned from the user's email edits to the
  `customer-support-email-lessons` namespace on Context Link. If not available,
  the lesson-learning step is skipped silently.

Optional:
- **Apple Mail MCP** — For creating drafts in Mail.app. Not required — the skill
  works without it using desktop folder or chat output. Setup:
  [github.com/Context-Link/apple-mail-mcp](https://github.com/Context-Link/apple-mail-mcp)

---

## Learning from edits

After all drafts have been delivered, prompt the user once (not per email):

> If you edited any of the drafts before sending, paste in the responses you actually
> sent — or just tell me what to do differently next time — so I can record lessons
> for future.

The user may respond in one of three ways:

**A) They paste one or more edited replies.** Diff each draft against what they sent.
Identify meaningful changes — tone shifts, factual corrections, structural changes,
things cut or added. Formulate concise, actionable lessons from the diffs.

**B) They give direct instructions** (e.g. "don't do X", "always do Y", "shorter intros").
Treat these as lessons directly — no diffing needed.

**C) They say they used drafts as-is or decline.** Move on — no lessons to record.

For options A and B:

1. **Formulate concise, actionable lessons.** One or two sentences each. Can cover
   tone, facts, preferred phrasing, when to request access, what to cut, etc.
2. **Save via update-memory.** Use the **update-memory** skill (see
   `skills/update-memory/SKILL.md` in this plugin) with the namespace slug
   `customer-support-email-lessons`.
   - **GET first** to retrieve existing lessons.
   - **Merge** new lessons in. Deduplicate — if a lesson overlaps with an existing
     one, update it rather than adding a near-duplicate.
   - **Never overwrite completely** unless the GET returned empty/nil. Always merge.
   - Keep the list context-window-efficient. Condense aggressively.
3. Confirm: `✓ Recorded {N} new lesson(s) to customer-support-email-lessons on Context Link.`

---

## Important notes

- Never send an email automatically. Only create drafts.
- Always ask for user confirmation before creating drafts.
- Respect the user's choice if they want to skip specific emails.
- The `[REPLY NEEDED]` tag is a convention — the user can customise it.
