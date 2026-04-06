# Email Triage Plugin

Triage your support inbox from Claude. Pull unread emails, generate context-aware draft replies using your knowledge base, and push them back as threaded drafts — ready for a human to review and send.

This plugin relies on [Context Link](https://www.context-link.ai) to semantically search and retrieve context from your emails, docs, websites, and anything else you connect. Context Link indexes your content sources into a searchable knowledge base, so when a customer email comes in, the plugin can pull in the most relevant information to draft an accurate reply. 

## Installation

### Claude Desktop (Cowork)

1. Open the Claude Desktop app and switch to the **Cowork** tab
2. Click **Customize** in the left sidebar
3. Click **Browse plugins** and search for **email-triage**, or upload the plugin file directly

If the plugin isn't listed in the marketplace, you can add the GitHub marketplace first:

1. In Cowork, go to **Customize → Personal plugins +**
2. **+ create plugin** -> **Add marketplace**
2. Add the marketplace repo: `Context-Link/claude-cowork-plugins-for-marketing`
3. Then install **email-triage** from the plugin list

### Claude Code (CLI)

Add the marketplace, then install the plugin:

```bash
/plugin marketplace add Context-Link/claude-cowork-plugins-for-marketing
/plugin install email-triage@Context-Link-claude-cowork-plugins-for-marketing
/reload-plugins
```

Plugin source: [github.com/Context-Link/claude-cowork-plugins-for-marketing/tree/master/plugins/email-triage](https://github.com/Context-Link/claude-cowork-plugins-for-marketing/tree/master/plugins/email-triage)

## Commands

| Command | Description |
|---|---|
| `/triage-emails` | Pull unread emails from the last 24 hours, generate draft replies, and push them back to your inbox |
| `/draft-reply` | Paste a customer email and get a context-aware draft reply |

## Skills

| Skill | Triggers when you... |
|-------|---------------------|
| `triage-email` | Say "triage emails", "triage inbox", "process support emails", or ask to batch-reply to customer emails |
| `draft-email-response` | Paste a support email and ask for a reply, or say "draft a reply", "reply to this email" |
| `get-context` | Reference internal knowledge, say "get context" (bundled from Context Link plugin) |
| `update-memory` | Save lessons from email edits to Context Link (bundled from Context Link plugin) |
| `scrub` | Clean AI tells from draft text before output |

## How it works

### Triage flow

1. **Connect** — Choose Gmail or Zoho Mail, pick which email address to triage
2. **Fetch** — Pull all unread emails from the last 24 hours
3. **Draft** — Each reply is automatically generated using your Context Link knowledge base (spam/phishing skipped)
4. **Deliver** — Choose where drafts go (preference is remembered):
   - **Apple Mail** — creates drafts directly in Mail.app via the Apple Mail MCP
   - **Desktop folder** — saves `.rtf` files to `~/Desktop/email-drafts-{date}/`
   - **Chat** — displays drafts in the conversation for copy-paste

### Standalone reply

Paste any customer email and run `/draft-reply` — the plugin looks up relevant context from your knowledge base and drafts a warm, practical reply you can send or lightly edit.

## Setup

### Email provider

Connect at least one email provider:

- **Gmail** — Enable in **Settings → Connectors → Gmail**
- **Zoho Mail** — Set up at [zoho.com/mcp](https://www.zoho.com/mcp/), select Zoho Mail, and follow the setup steps

### Apple Mail output (optional)

The Apple Mail MCP is bundled with this plugin and pre-configured in `.mcp.json` with `--read-only` mode (sending is disabled, drafts work). Requirements: macOS with Mail.app configured.

On first use, the plugin will ask permission to install the Python dependency (`fastmcp`) automatically. You'll also need to grant Automation permissions when macOS prompts (System Settings → Privacy & Security → Automation).

If Apple Mail isn't available, the plugin falls back to Desktop folder or Chat output.

### Knowledge base (optional but recommended)

This plugin includes a bundled copy of the `get-context` skill from the [Context Link](https://context-link.ai) plugin. To use it:

1. Sign in at [context-link.ai](https://context-link.ai)
2. Connect your support docs, website, and knowledge sources
3. The plugin will automatically look up relevant context when drafting replies

If Context Link is not configured, the plugin still works — replies will be drafted based on the email content alone.

## Example Workflows

### Triaging your inbox

```
> triage my zoho inbox for hello@preproduct.io
```

Claude will pull unread emails, show you a summary table, and generate a draft reply for each one you select.

### Quick reply to a single email

```
> /draft-reply
[paste customer email]
```

Claude will identify the issue, look up relevant context, and draft a reply.

### Triage with all arguments

```
> /triage-emails --provider zoho --address hello@preproduct.io --output apple-mail
```

Skip all setup questions — fetch from Zoho, filter to one address, and create drafts in Mail.app.

### Save drafts to Desktop

```
> /triage-emails --output desktop
```

Drafts are saved as `.rtf` files in `~/Desktop/email-drafts-2026-04-05/` — one file per reply.

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

This plugin works with the following MCP servers:

- **Gmail** — Fetch emails, read messages, create threaded draft replies
- **Zoho Mail** — Fetch emails, search messages (draft creation pending MCP support)
- **Apple Mail** — Bundled with this plugin (`apple-mail-mcp/`), runs in read-only mode (drafts work, sending disabled). Requires macOS, Mail.app, Python 3.10+. Source: [github.com/Context-Link/apple-mail-mcp](https://github.com/Context-Link/apple-mail-mcp)
- **Context Link** — Look up product knowledge, support docs, and past answers for reply generation
