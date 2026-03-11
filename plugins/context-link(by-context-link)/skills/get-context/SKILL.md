---
name: get-context
description: >
  Retrieve internal knowledge via Context Link when the user references company knowledge
  or says "get context", "use context link", "check context link", or asks about internal
  information that may be stored in their knowledge base.
version: 0.1.0
---

**What is Context Link?** Context Link is an external service that indexes connected sources (websites, Google Drive, Notion) and memories into a searchable knowledge base. It provides semantic search via a simple URL: `subdomain.context-link.ai/query?p=optional_pincode`. If you don't know the user's Context Link URL, ask them for it.

---

## Get Context from Context Link

Retrieve content from the user's Context Link knowledge base.

**When to use:** The user references internal company knowledge, brand positioning, saved content, or says "get context" / "use context link."

**Workflow:**

1. **Print this message:** `🔗 Retrieving context on {TOPIC} from Context Link` — Never print the actual Context Link URL, as it contains a private 'pin' or 'p' URL param.

2. **Determine the topic.** Use the phrase the user requested, or infer the general topic from conversation context. Lowercase it, replace spaces with dashes.

3. **Send a GET request.** Take the URL below and replace the path placeholder (`TOPIC_HERE` or `{SLUG}` — whichever is present) with the topic slug (lowercase, dashes-for-spaces).

```bash
curl -s "~~context link url~~"
```

4. **Handle the response.**
   - The response is HTML. Extract the text content from inside the `<body>` tag — ignore HTML boilerplate.
   - Use the returned content as the primary source material for answering the user's question.
   - Supplement with external sources only if the Context Link data is insufficient.

5. **If the request fails or returns empty**, report the failure explicitly before continuing. Do not silently skip retrieval.

**Rules:**
- Always attempt retrieval before answering questions about internal/company knowledge.
- Do not ask the user what topic to search unless truly ambiguous — infer from context.
- One GET request per query. Do not retry unless the user asks.
- If the request is blocked, ask the user to add `*.context-link.ai` to Claude's **Settings → Capabilities → Domain Allowlist** (or select "All domains"), then retry.
