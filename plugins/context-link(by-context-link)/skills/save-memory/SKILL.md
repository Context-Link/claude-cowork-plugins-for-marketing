---
name: save-memory
description: >
  Save conversation content or specified text to Context Link for later retrieval.
  Use when the user says "save this", "remember this", "save memory", "save to context link",
  or asks to store information for future reference.
version: 0.1.0
---

## Save to Context Link

Save content from the current conversation to Context Link. One request, no fuss.

**Workflow:**

1. **Pick the slug.** If the user said "save {name}", use that name as the slug (lowercased, dashed). If the user said "save this conversation", "save this chat", or similar without a specific topic name, use `chat-session-{YYYY-MM-DD-HHMM}` as the slug. Otherwise, infer a short descriptive slug from the topic. Only ask if truly ambiguous.

2. **Summarize the content.** Distill the conversation into a concise, reusable reference document in markdown. Focus on what's useful to retrieve later — strip conversational back-and-forth, keep decisions, specs, and key details.

3. **POST it.** Take the URL below and replace the path placeholder (`TOPIC_HERE` or `{SLUG}` — whichever is present) with the chosen slug (lowercase, use-dashes-for-spaces).

```bash
curl -s -X POST "~~context link url~~" \
  -H "Content-Type: text/plain" \
  -d 'Your markdown content here'
```

The body is raw text/markdown — not JSON. The server's LlmPoweredParser handles chunking and structuring internally. Just send clean markdown.

**Success response:** `{"message": "Saved", "namespace": "the-slug"}` with HTTP 201.

**Rules:**
- **Keep the body under 100KB.** If content is longer, summarize or condense it before sending. Do NOT split into multiple requests — distill into one concise document.
- If the user says "save X" — X is the slug. Always. No questions asked.
- Do NOT test the endpoint first. It works. Just POST.
- Do NOT verify by fetching it back. Trust the 201.
- Do NOT send multiple requests. One POST, done.
- Saving to the same slug creates a new version (latest wins on GET).
- After saving, confirm briefly: "Saved to Context Link as `the-slug`."
