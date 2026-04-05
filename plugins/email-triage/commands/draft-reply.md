---
description: Paste a customer email and get a context-aware draft reply
allowed-tools: Bash, WebFetch
argument-hint: "[paste email or describe the issue] [--output apple-mail|desktop|chat]"
---

# Draft Reply

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Draft a reply to a customer support email using the draft-email-response skill.

Use the skill instructions from `${CLAUDE_PLUGIN_ROOT}/skills/draft-email-response/SKILL.md` to generate the reply.

## Arguments

- `--output` → pass as `output` (`apple-mail`, `desktop`, or `chat`). Defaults to `chat`.
- Everything else in `$ARGUMENTS` is treated as the email content or issue description.

## Input

The user will either:
1. Paste a full customer email after running the command
2. Provide a summary of the issue as `$ARGUMENTS`

If `$ARGUMENTS` contains an email (look for subject lines, greetings, or email formatting), treat it as the customer email to reply to.

If `$ARGUMENTS` is a short description, ask the user to paste the full email for a better reply.
