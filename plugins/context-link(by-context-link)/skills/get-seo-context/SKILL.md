---
name: get-seo-context
description: >
  Retrieve or create SEO context (guidelines, target keywords, competitor analysis) from Context Link.
  Use when the user mentions "SEO context", "SEO guidelines", "target keywords", "competitor analysis",
  or wants to establish their SEO strategy foundation.
version: 0.1.0
---

**What is Context Link?** Context Link is an external service that indexes connected sources (websites, Google Drive, Notion) and memories into a searchable knowledge base. It provides semantic search and memory storage via a simple URL: `subdomain.context-link.ai/query?p=optional_pincode`. If you don't know the user's Context Link URL, ask them for it.

---

### Get SEO Context

Retrieve SEO context for content creation. Checks Context Link memory first, then runs a wizard if context doesn't exist.

**Context Namespaces** (3 total):
- `seo_memory_guidelines` - SEO rules (keyword density, structure, meta elements)
- `seo_memory_target_keywords` - Target keywords and topic clusters
- `seo_memory_competitor_analysis` - Competitive intelligence

**Workflow:**

1. **Print this message:** `🔗 Retrieving SEO context from Context Link`

2. **Fetch existing context.** Try to GET each namespace. Replace `~~context link url~~` with the user's Context Link URL and append the namespace as the path:

```bash
curl -s "~~context link url~~/seo_memory_guidelines"
curl -s "~~context link url~~/seo_memory_target_keywords"
curl -s "~~context link url~~/seo_memory_competitor_analysis"
```

3. **Check what exists.** If a request returns content (not 404), use it. If any namespace is missing, run the wizard for that context type.

4. **Run wizard for missing contexts.** Ask questions step-by-step to build the context. One context at a time.

---

**WIZARD: SEO Guidelines** (if `seo_memory_guidelines` is missing)

Ask these questions in order, one at a time:

1. "What's your target content length for standard blog posts? (e.g., 1500-3000 words)"
2. "What's the maximum article length before you'd break content into multiple posts?"
3. "What keyword density do you target for your primary keyword? (e.g., 1-2%)"
4. "How many H2 sections should a standard article have?"
5. "What's your meta title character limit? (typically 50-60)"
6. "What's your meta description character limit? (typically 150-160)"
7. "How many internal links should each article contain? (e.g., 3-5)"
8. "How many external links should each article contain? (e.g., 2-3)"
9. "What reading level do you target? (e.g., 8th-10th grade)"
10. "Any specific formatting rules? (e.g., subheadings every 300-400 words, always use lists)"

After collecting answers, compile into markdown and POST:

```bash
curl -s -X POST "~~context link url~~/seo_memory_guidelines" \
  -H "Content-Type: text/plain" \
  -d 'Your compiled SEO guidelines markdown here'
```

---

**WIZARD: Target Keywords** (if `seo_memory_target_keywords` is missing)

Ask these questions in order:

1. "What is your business/product? (1-2 sentences)"
2. "What are your 3-5 main topic clusters or pillar keywords?"
3. "For your FIRST pillar keyword, list 5-10 related cluster keywords"
4. "For your SECOND pillar keyword, list 5-10 related cluster keywords"
5. "For your THIRD pillar keyword, list 5-10 related cluster keywords"
6. (Continue for remaining pillars if any)
7. "What are 10-15 long-tail keywords you want to target?"
8. "What are the top 5 'People Also Ask' questions in your space?"
9. "Any seasonal or trending keywords to track?"

Compile into topic cluster format and POST:

```bash
curl -s -X POST "~~context link url~~/seo_memory_target_keywords" \
  -H "Content-Type: text/plain" \
  -d 'Your compiled target keywords markdown here'
```

---

**WIZARD: Competitor Analysis** (if `seo_memory_competitor_analysis` is missing)

Ask these questions in order:

1. "Who are your top 3-5 direct competitors? (company names and URLs)"
2. "For COMPETITOR 1: What's their content strategy? (frequency, types, avg length)"
3. "For COMPETITOR 1: What are their top 3 ranking articles/keywords?"
4. "For COMPETITOR 1: What are their SEO strengths and weaknesses?"
5. (Repeat for remaining competitors)
6. "What keywords do competitors rank for that you don't?"
7. "What content gaps exist that you could fill?"
8. "What's your unique advantage over these competitors?"
9. "Are there any content publishers (not product competitors) you compete with for visibility?"

Compile into competitor analysis format and POST:

```bash
curl -s -X POST "~~context link url~~/seo_memory_competitor_analysis" \
  -H "Content-Type: text/plain" \
  -d 'Your compiled competitor analysis markdown here'
```

---

**Rules:**
- Always try GET first before running wizards
- Run one wizard at a time, complete it fully before moving to next
- Keep answers concise but comprehensive
- If user says "skip" for any context type, don't create it
- After saving, confirm: "Saved SEO [context type] to Context Link"
- Return all retrieved/created context to the user for reference
- If requests are blocked, ask the user to add `*.context-link.ai` to Claude's **Settings > Capabilities > Domain Allowlist** (or select "All domains"), then retry.
