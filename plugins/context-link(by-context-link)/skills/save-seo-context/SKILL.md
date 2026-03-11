---
name: save-seo-context
description: >
  Save or update SEO context (guidelines, target keywords, competitor analysis) to Context Link.
  Use when the user says "save SEO context", "update SEO guidelines", "save keywords", or wants
  to persist SEO-related information for future use.
version: 0.1.0
---

**What is Context Link?** Context Link is an external service that indexes connected sources (websites, Google Drive, Notion) and memories into a searchable knowledge base. It provides semantic search and memory storage via a simple URL: `subdomain.context-link.ai/query?p=optional_pincode`. If you don't know the user's Context Link URL, ask them for it.

---

### Save SEO Context

Save or update SEO context to Context Link for later retrieval. Use this to persist changes made during the conversation.

**Context Namespaces:**
- `seo_memory_guidelines` - SEO rules (keyword density, structure, meta elements)
- `seo_memory_target_keywords` - Target keywords and topic clusters
- `seo_memory_competitor_analysis` - Competitive intelligence

**Workflow:**

1. **Print this message:** `🔗 Saving SEO context to Context Link → {NAMESPACE}`

2. **Determine which context to save.** Ask the user if not clear:
   - "guidelines" -> `seo_memory_guidelines`
   - "keywords" or "target keywords" -> `seo_memory_target_keywords`
   - "competitors" or "competitor analysis" -> `seo_memory_competitor_analysis`

3. **If updating existing content**, first GET the current version. Replace `~~context link url~~` with the user's Context Link URL:

```bash
curl -s "~~context link url~~/{NAMESPACE}"
```

Then merge changes with existing content.

4. **Compile the content.** Format as clean markdown with clear headings. Structure should follow these patterns:

**For seo_memory_guidelines:**
```markdown
# SEO Guidelines

## Content Length Requirements
- Standard posts: X-Y words
- Maximum: Z words

## Keyword Optimization
- Primary keyword density: X%
- Placement: [list critical locations]

## Content Structure
- H2 sections: X-Y per article
- Subheadings: Every X words

## Meta Elements
- Title: X characters
- Description: Y characters

## Linking Strategy
- Internal links: X-Y per article
- External links: X-Y per article

## Readability
- Target reading level: Xth grade
- Sentence length: X-Y words
```

**For seo_memory_target_keywords:**
```markdown
# Target Keywords & Topic Clusters

## Cluster 1: [Topic]
### Pillar Keyword
- Keyword: [keyword]
- Volume: [if known]
- Intent: [informational/commercial/transactional]

### Cluster Keywords
1. [keyword]
2. [keyword]
...

### Long-Tail Keywords
- [keyword phrase]
- [keyword phrase]
...

## Cluster 2: [Topic]
[Same structure]
```

**For seo_memory_competitor_analysis:**
```markdown
# Competitor Analysis

## Competitor 1: [Name]
- URL: [website]
- Position: [market position]
- Content Strategy: [description]
- Top Content: [list]
- Strengths: [list]
- Weaknesses: [list]
- Gaps: [opportunities]

## Competitor 2: [Name]
[Same structure]

## Content Opportunities
- [opportunity 1]
- [opportunity 2]
```

5. **POST to save:**

```bash
curl -s -X POST "~~context link url~~/{NAMESPACE}" \
  -H "Content-Type: text/plain" \
  -d 'Your markdown content here'
```

**Success response:** `{"message": "Saved", "namespace": "{NAMESPACE}"}` with HTTP 201.

**Rules:**
- Keep content under 100KB
- If user says "save SEO guidelines", save to `seo_memory_guidelines`
- If user says "save keywords", save to `seo_memory_target_keywords`
- If user says "save competitor analysis", save to `seo_memory_competitor_analysis`
- If user says "save all SEO context", save all three (three separate POSTs)
- Saving to the same namespace creates a new version (latest wins on GET)
- After saving, confirm: "Saved to Context Link as `{NAMESPACE}`"
- If requests are blocked, ask the user to add `*.context-link.ai` to Claude's **Settings > Capabilities > Domain Allowlist** (or select "All domains"), then retry.
