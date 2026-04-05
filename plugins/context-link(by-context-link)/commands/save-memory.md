---
description: Save content to Context Link
allowed-tools: Bash
argument-hint: [slug]
---

Save the current conversation content to Context Link under the slug: $ARGUMENTS

Use the save-memory skill instructions from ${CLAUDE_PLUGIN_ROOT}/skills/save-memory/SKILL.md to perform the save.

If no slug argument is provided, infer an appropriate slug from the conversation topic.
