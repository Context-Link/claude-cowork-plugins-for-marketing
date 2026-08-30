---
name: ask-question
description: >
  Ask a question against the user's Context Link and receive a concise, cited
  answer drawn from their connected sources. Use when the user says "ask my
  context", "what does my knowledge base say about…", "answer this from my
  docs", or asks a direct question whose answer should be grounded in the
  user's own content.
version: 0.1.1
---

**What is Context Link?** Context Link is an external service that indexes connected sources (websites, Google Drive, Notion, files, email) and memories into a searchable knowledge base. The ask-question endpoint returns a single concise answer (≤ 1 paragraph) with citations, grounded in the user's own content. If you don't know the user's Context Link URL, ask them for it.

> A `402` response means the user's subscription doesn't include this endpoint — suggest they check their Context Link plan.

---

## Ask a Question via Context Link

Ask a direct question and receive a short, cited answer from the user's Context Link.

**When to use:** the user wants a direct answer grounded in their own knowledge base, e.g. "ask my docs…", "ask context link what …", "use context link to answer…", or invokes `/ask-question` in Claude Code. Prefer this over `get-context` when the user wants the answer itself rather than raw source material.

**Workflow:**

1. **Print this message:** `🔗 Asking Context Link about {TOPIC}`. Never print the full Context Link URL, as it contains a private pin.

2. **Form the question slug.** Take the user's question, lowercase, replace spaces with dashes.

3. **Send a GET request.** Take the URL below and replace the path placeholder with `q/{QUESTION_SLUG}`.

```bash
curl -s "~~context link url~~"
```

   - Optionally append `&mode=MODE_NAME` (or `?mode=MODE_NAME` if no pin is set) to weight results toward a specific mode configured by the user.

4. **Handle the response.** The response is JSON:

```json
{
  "result": "ok",
  "answer": "Concise paragraph with inline [1] citation markers.",
  "citations": [{ "n": 1, "title": "Refund policy", "url": "https://…" }],
  "format": "markdown"
}
```

   - Present the `answer` field to the user verbatim (or lightly reformatted). **Keep the inline `[1]`, `[2]` citation markers.**
   - After the answer, list the `citations` as a small "Sources" footer (title + url).
   - Never fabricate citations. Only surface those returned by the endpoint.

5. **Handle the other result states:**
   - `result: "no_context"`: tell the user their Context Link had no relevant material and ask whether to broaden the question.
   - `result: "llm_unavailable"` (HTTP 503): the upstream LLM is momentarily down; retry once, then stop and tell the user.

6. **If the request fails or is blocked**, report the failure explicitly. Do not silently skip.

**Rules:**

- One GET request per question. Do not retry unless the user asks.
- Do not supplement with outside information unless the user explicitly asks. The value is the grounded, cited answer.
- If the response is `402`, tell the user their subscription doesn't include the ask-question endpoint and link them to `www.context-link.ai` to check their plan.
- If the response is `429` with an "allowance" message, tell the user they have exceeded their monthly Context Link question allowance.
- If the request is blocked, ask the user to add `*.context-link.ai` to Claude's **Settings → Capabilities → Domain Allowlist** (or select "All domains"), then retry.
