---
description: Pull unread emails from the last 24 hours, generate draft replies, and push them back to your inbox
allowed-tools: Bash, WebFetch, ToolSearch
argument-hint: "[--provider gmail|zoho] [--address email] [--output apple-mail|desktop|chat]"
---

# Triage Emails

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Triage unread support emails using the triage-email skill.

Use the skill instructions from `${CLAUDE_PLUGIN_ROOT}/skills/triage-email/SKILL.md` to run the full workflow.

## Arguments

Parse the following optional arguments from `$ARGUMENTS`:

- `--provider` or first positional arg → pass as `email_provider` (`gmail` or `zoho`)
- `--address` → pass as `email_address` (specific address or `all`)
- `--output` → pass as `output` (`apple-mail`, `desktop`, or `chat`)

If no arguments are provided, the skill will ask the user interactively.

## Examples

- `/triage-emails` — interactive (asks for provider, address, and output)
- `/triage-emails --provider zoho --address hello@preproduct.io --output desktop` — full automation
- `/triage-emails gmail --output apple-mail` — Gmail, drafts to Mail.app
- `/triage-emails zoho all --output chat` — Zoho, all addresses, show drafts in chat
