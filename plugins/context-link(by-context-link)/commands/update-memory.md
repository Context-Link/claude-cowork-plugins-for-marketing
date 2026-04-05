---
description: Update existing content on Context Link
allowed-tools: Bash, WebFetch
argument-hint: [slug]
---

Retrieve existing content from Context Link for the slug "$ARGUMENTS", merge it with new information from the current conversation, and save it back.

Use the update-memory skill instructions from ${CLAUDE_PLUGIN_ROOT}/skills/update-memory/SKILL.md to perform the update.

If no slug argument is provided, ask the user which saved topic they want to update.
