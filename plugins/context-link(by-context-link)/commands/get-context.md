---
description: Retrieve knowledge from Context Link
allowed-tools: Bash, WebFetch
argument-hint: [topic]
---

Retrieve content from the user's Context Link knowledge base for the topic: $ARGUMENTS

Use the get-context skill instructions from ${CLAUDE_PLUGIN_ROOT}/skills/get-context/SKILL.md to perform the retrieval.

If no topic argument is provided, infer the topic from the current conversation context.
