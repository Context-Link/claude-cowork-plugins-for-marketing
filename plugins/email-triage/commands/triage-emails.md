---
description: Pull unread emails from the last 24 hours, generate draft replies, and push them back to your inbox
allowed-tools: Bash, WebFetch, ToolSearch
argument-hint: "[--provider gmail|zoho] [--address email]"
---

# Triage Emails

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Triage unread support emails using the triage-email skill.

Use the skill instructions from `${CLAUDE_PLUGIN_ROOT}/skills/triage-email/SKILL.md` to run the full workflow.

## Arguments

Parse the following optional arguments from `$ARGUMENTS`:

- `--provider` or first positional arg → pass as `email_provider` (`gmail` or `zoho`)
- `--address` → pass as `email_address` (specific address or `all`)

If no arguments are provided, the skill will ask the user interactively.

## Examples

- `/triage-emails` — interactive (asks for provider and address)
- `/triage-emails --provider zoho --address hello@example.com` — full automation
- `/triage-emails gmail` — Gmail, interactive address selection
- `/triage-emails zoho all` — Zoho, all addresses
