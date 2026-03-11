---
name: get-seo-writing-context
description: >
  Retrieve or create SEO writing context (brand voice, style guide, writing examples) from Context Link.
  Use when the user mentions "brand voice", "style guide", "writing examples", or wants to establish
  their content writing standards.
version: 0.1.0
---

**What is Context Link?** Context Link is an external service that indexes connected sources (websites, Google Drive, Notion) and memories into a searchable knowledge base. It provides semantic search and memory storage via a simple URL: `subdomain.context-link.ai/query?p=optional_pincode`. If you don't know the user's Context Link URL, ask them for it.

---

### Get SEO Writing Context

Retrieve writing context for SEO content creation. Checks Context Link memory first, then runs a wizard if context doesn't exist.

**Context Namespaces** (3 total):
- `seo_memory_brand_voice` - Brand voice, tone, and messaging framework
- `seo_memory_style_guide` - Grammar, formatting, and editorial standards
- `seo_memory_writing_examples` - Exemplary content samples for style reference

**Workflow:**

1. **Print this message:** `🔗 Retrieving SEO writing context from Context Link`

2. **Fetch existing context.** Try to GET each namespace. Replace `~~context link url~~` with the user's Context Link URL and append the namespace as the path:

```bash
curl -s "~~context link url~~/seo_memory_brand_voice"
curl -s "~~context link url~~/seo_memory_style_guide"
curl -s "~~context link url~~/seo_memory_writing_examples"
```

3. **Check what exists.** If a request returns content (not 404), use it. If any namespace is missing, run the wizard for that context type.

4. **Run wizard for missing contexts.** Ask questions step-by-step to build the context. One context at a time.

---

**WIZARD: Brand Voice** (if `seo_memory_brand_voice` is missing)

Ask these questions in order, one at a time:

1. "What's your company/brand name?"
2. "Describe your brand in 1-2 sentences (what you do, who you serve)"
3. "List 3-5 voice pillars (personality traits of your brand voice). For example: 'Authoritative but friendly', 'Expert but accessible', 'Empowering not preachy'"
4. "For each voice pillar, give an example sentence that demonstrates it"
5. "What's your general tone? (e.g., 'Like an experienced friend who genuinely wants you to succeed')"
6. "How does your tone vary by content type? (How-to guides vs Strategy content vs Product content)"
7. "What are your 3-5 core brand messages that should be woven throughout content?"
8. "What are your value propositions for each target segment?"
9. "What words or phrases should you AVOID? (e.g., corporate jargon, specific terms)"
10. "What does excellent writing look like for your brand? Describe it or paste an example paragraph"
11. "What does BAD writing look like for your brand? Describe what to avoid"

After collecting answers, compile into brand voice markdown and POST:

```bash
curl -s -X POST "~~context link url~~/seo_memory_brand_voice" \
  -H "Content-Type: text/plain" \
  -d 'Your compiled brand voice markdown here'
```

---

**WIZARD: Style Guide** (if `seo_memory_style_guide` is missing)

Ask these questions in order:

1. "Headlines: Title Case or Sentence case?"
2. "Do you use the Oxford comma? (A, B, and C vs A, B and C)"
3. "What's your preferred sentence length? (e.g., 15-20 words average)"
4. "What's your preferred paragraph length? (e.g., 2-4 sentences)"
5. "Any specific capitalization rules? (e.g., always capitalize your product name)"
6. "List any 'Say This / Not That' terminology preferences (e.g., 'podcast creators' not 'podcasters')"
7. "Any words to always avoid? (e.g., 'very', 'really', 'actually')"
8. "Date format preference? (January 15, 2025 vs 15 January 2025)"
9. "How should code/technical elements be formatted?"
10. "Any formatting rules for lists, bold, italics?"
11. "What's your approach to inclusive language?"

Compile into style guide format and POST:

```bash
curl -s -X POST "~~context link url~~/seo_memory_style_guide" \
  -H "Content-Type: text/plain" \
  -d 'Your compiled style guide markdown here'
```

---

**WIZARD: Writing Examples** (if `seo_memory_writing_examples` is missing)

Ask these questions in order:

1. "Do you have existing blog posts that represent your best work? If yes, please paste 1-3 complete articles (or provide URLs I can fetch)"
2. "If you don't have existing examples, describe what ideal content looks like for your brand (structure, length, style)"
3. "What makes a piece of content 'excellent' in your view? List 3-5 qualities"
4. "What are common mistakes you want to avoid? List 3-5 things"
5. "Are there any competitor articles you admire? (I won't copy, just for style reference)"

**Important**: If user provides URLs, use GET to fetch the content:
```bash
curl -s "[USER_PROVIDED_URL]"
```

Compile examples into writing examples format and POST:

```bash
curl -s -X POST "~~context link url~~/seo_memory_writing_examples" \
  -H "Content-Type: text/plain" \
  -d 'Your compiled writing examples markdown here'
```

---

**Rules:**
- Always try GET first before running wizards
- Run one wizard at a time, complete it fully before moving to next
- For writing examples, encourage the user to paste actual content - the more examples, the better
- Keep the compiled markdown well-organized with clear headings
- If user says "skip" for any context type, don't create it
- After saving, confirm: "Saved [context type] to Context Link"
- Return all retrieved/created context to the user for reference
- If requests are blocked, ask the user to add `*.context-link.ai` to Claude's **Settings > Capabilities > Domain Allowlist** (or select "All domains"), then retry.
