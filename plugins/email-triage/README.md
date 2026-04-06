# Email Triage Plugin for Claude

Triage your support inbox from Claude. Pull unread emails, generate context-aware draft replies using your knowledge base, and review them in an interactive UI, ready for a human to copy, edit, and send.

The plugin learns from your corrections over time. After each triage run, you can paste the replies you actually sent or give direct feedback. Lessons are stored in your [Context Link](https://www.context-link.ai) knowledge base and applied to future drafts automatically.

Works in both **Claude Desktop (Cowork)** and **Claude Code (CLI)**. Everything runs in the cloud (email fetching via Gmail or Zoho MCP, context retrieval via Context Link) so there's nothing to install locally beyond the plugin itself.

## Installation

### Claude Desktop (Cowork)

1. Open the Claude Desktop app and switch to the **Cowork** tab
2. Click **Customize** in the left sidebar
3. Click **Browse plugins** and search for **email-triage**

If the plugin isn't listed, add the GitHub marketplace first:

1. In Cowork, go to **Customize → Personal plugins +**
2. **+ create plugin** → **Add marketplace**
3. Add the marketplace repo: `Context-Link/claude-cowork-plugins-for-marketing`
4. Then install **email-triage** from the plugin list

### Claude Code (CLI)

```bash
/plugin marketplace add Context-Link/claude-cowork-plugins-for-marketing
/plugin install email-triage@Context-Link-claude-cowork-plugins-for-marketing
/reload-plugins
```

Plugin source: [github.com/Context-Link/claude-cowork-plugins-for-marketing/tree/master/plugins/email-triage](https://github.com/Context-Link/claude-cowork-plugins-for-marketing/tree/master/plugins/email-triage)

## How it works

### Triage flow

1. **Connect** — Choose Gmail or Zoho Mail, pick which email address to triage
2. **Fetch** — Pull all unread emails from the last 24 hours (spam and automated notifications are skipped)
3. **Draft** — Each reply is generated using your Context Link knowledge base and any lessons from previous corrections
4. **Review** — Drafts appear in an interactive UI with collapsible cards, copy buttons, and action checklists
5. **Learn** — After you send the replies, paste back what you actually sent or tell Claude what to do differently. Lessons are saved to Context Link and used in future runs.

In **Cowork**, the draft UI renders inline as an artifact. In **Claude Code**, it opens in your default browser.

### Standalone reply

Paste any customer email and run `/draft-reply`. The plugin looks up relevant context, applies learned lessons, scrubs AI tells from the output, and drafts a reply you can send or lightly edit.

## Commands

| Command | Description |
|---|---|
| `/triage-emails` | Pull unread emails, generate draft replies, and display them in the interactive UI |
| `/draft-reply` | Paste a single customer email and get a context-aware draft reply |

## Skills

| Skill | What it does |
|-------|-------------|
| `triage-email` | Orchestrates the full triage workflow: fetch, draft, display, learn |
| `draft-email-response` | Generates a single context-aware draft reply with required actions |
| `scrub` | Removes AI tells from draft text (filler phrases, watermarks, overly enthusiastic language) |
| `get-context` | Retrieves product knowledge and support context from Context Link |
| `update-memory` | Saves learned lessons back to Context Link for future runs |

## Setup

### Email provider (required)

Connect at least one email provider:

- **Gmail** — Enable the Gmail connector in **Settings → Connectors → Gmail**
- **Zoho Mail** — Set up at [zoho.com/mcp](https://www.zoho.com/mcp/), select Zoho Mail, and follow the setup steps (required enabled tools: "getMailAccounts, listEmails, SearchEmails")

### Knowledge base (recommended)

This plugin uses [Context Link](https://context-link.ai) for two things: retrieving support context when drafting replies, and storing lessons learned from your corrections.

1. Sign in at [context-link.ai](https://context-link.ai)
2. Connect your support docs, website, and knowledge sources
3. The plugin will automatically look up relevant context when drafting and save lessons when you provide feedback

Without Context Link, the plugin still works. Replies are drafted from the email content alone, and lessons aren't persisted between sessions.

## Example usage

### Triage your inbox

```
> triage my zoho inbox for hello@preproduct.io
```

Pulls unread emails, drafts replies for each, and displays them as interactive cards.

### Quick reply to a single email

```
> /draft-reply
[paste customer email]
```

Looks up context, drafts a reply, and prompts you for feedback to learn from.

### Skip the prompts

```
> /triage-emails --provider zoho --address hello@preproduct.io
```

Passes arguments directly so there are no setup questions.

## MCP connectors

This plugin uses the following MCP servers (configured in `.mcp.json`):

- **Gmail** — Fetch and search emails via the Gmail MCP
- **Zoho Mail** — Fetch and search emails via the Zoho MCP
- **Context Link** — Retrieved via HTTP (no MCP server needed; uses the get-context skill)

See [CONNECTORS.md](CONNECTORS.md) for tool-specific reference.
