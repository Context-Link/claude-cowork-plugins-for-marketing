---
name: update-memory
description: >
  Retrieve saved content from Context Link, update it with current context, and save it back.
  Use when the user says "update memory", "update context link", "add to {topic}",
  or wants to modify existing saved content with new information.
version: 0.1.0
---

## Update Content on Context Link

Retrieve existing content, merge in new information, and save it back. Two requests total — one GET, one POST.

**Workflow:**

1. **GET the existing content.** Take the URL below and replace the path placeholder (`TOPIC_HERE` or `{SLUG}` — whichever is present) with the slug.

```bash
curl -s "~~context link url~~"
```

Returns HTML. Extract the text content from inside the `<body>` tag — ignore HTML boilerplate.

2. **Merge and rewrite.** Combine existing content with new information from the conversation. Deduplicate, reorganize if needed, keep it concise. Output as clean markdown.

3. **POST the updated content back to the same slug.** Use the same URL (with the placeholder replaced by the same slug).

```bash
curl -s -X POST "~~context link url~~" \
  -H "Content-Type: text/plain" \
  -d 'Your updated markdown here'
```

The body is raw text/markdown — not JSON. The server handles chunking internally.

**Success response:** `{"message": "Saved", "namespace": "the-slug"}` with HTTP 201.

**Rules:**
- **Keep the body under 100KB.** If the merged content is too long, summarize or condense it before POSTing.
- Two requests max: one GET, one POST. Nothing else.
- Do NOT ask the user what to update unless genuinely unclear — infer from conversation.
- This creates a new version under the same slug (old versions still exist, slug points to latest).
- After saving, confirm briefly: "Updated `the-slug` on Context Link."
