---
name: save-seo-writing-context
description: >
  Save or update SEO writing context (brand voice, style guide, writing examples) to Context Link.
  Use when the user says "save brand voice", "update style guide", "save writing examples", or wants
  to persist writing-related information for future use.
version: 0.1.0
---

**What is Context Link?** Context Link is an external service that indexes connected sources (websites, Google Drive, Notion) and memories into a searchable knowledge base. It provides semantic search and memory storage via a simple URL: `subdomain.context-link.ai/query?p=optional_pincode`. If you don't know the user's Context Link URL, ask them for it.

---

### Save SEO Writing Context

Save or update writing context to Context Link for later retrieval. Use this to persist changes made during the conversation.

**Context Namespaces:**
- `seo_memory_brand_voice` - Brand voice, tone, and messaging framework
- `seo_memory_style_guide` - Grammar, formatting, and editorial standards
- `seo_memory_writing_examples` - Exemplary content samples for style reference

**Workflow:**

1. **Print this message:** `🔗 Saving SEO writing context to Context Link → {NAMESPACE}`

2. **Determine which context to save.** Ask the user if not clear:
   - "brand voice" or "voice" -> `seo_memory_brand_voice`
   - "style guide" or "style" -> `seo_memory_style_guide`
   - "examples" or "writing examples" -> `seo_memory_writing_examples`

3. **If updating existing content**, first GET the current version. Replace `~~context link url~~` with the user's Context Link URL:

```bash
curl -s "~~context link url~~/{NAMESPACE}"
```

Then merge changes with existing content.

4. **Compile the content.** Format as clean markdown with clear headings. Structure should follow these patterns:

**For seo_memory_brand_voice:**
```markdown
# [COMPANY] Brand Voice & Messaging

## Brand Voice Pillars

### 1. [Pillar Name]
- What it means: [explanation]
- How it sounds: [description]
- Example: "[example sentence]"
- Avoid: [what not to do]

### 2. [Pillar Name]
[Same structure]

## Tone Guidelines
### General Tone
[Description of overall tone]

### Tone by Content Type
- How-To Guides: [adjectives, examples]
- Strategy Content: [adjectives, examples]
- Product Content: [adjectives, examples]

## Core Brand Messages
1. [Message]: [description]
2. [Message]: [description]

## Value Propositions
- For [Segment]: "[value prop]"
- For [Segment]: "[value prop]"

## Voice Examples
### Excellent
"[Example paragraph]"

### Avoid
"[Counter-example]"
```

**For seo_memory_style_guide:**
```markdown
# Style Guide

## Grammar & Mechanics
- Headlines: [Title Case / Sentence case]
- Oxford comma: [Yes / No]
- Numbers: [spell out one-nine, numerals 10+]
- Dates: [format]

## Sentence & Paragraph Structure
- Sentence length: [X-Y words average]
- Paragraph length: [X-Y sentences]
- Voice: [Active preferred]

## Word Choice
### Say This / Not That
- [preferred] -> [avoid]
- [preferred] -> [avoid]

### Words to Avoid
- [word]
- [word]

## Formatting
- Bold: [when to use]
- Italics: [when to use]
- Lists: [guidelines]
- Links: [guidelines]

## Quality Checklist
- [ ] [item]
- [ ] [item]
```

**For seo_memory_writing_examples:**
```markdown
# Writing Examples

## About These Examples
These articles represent [COMPANY]'s best work and ideal voice.

## Example 1: [Title]
**URL**: [if available]
**Keyword**: [target keyword]
**What Makes It Great**: [reasons]

### Full Content
[Complete article text]

## Example 2: [Title]
[Same structure]

## Key Qualities
1. [Quality]
2. [Quality]
3. [Quality]

## Common Mistakes to Avoid
1. [Mistake]
2. [Mistake]
```

5. **POST to save:**

```bash
curl -s -X POST "~~context link url~~/{NAMESPACE}" \
  -H "Content-Type: text/plain" \
  -d 'Your markdown content here'
```

**Success response:** `{"message": "Saved", "namespace": "{NAMESPACE}"}` with HTTP 201.

**Rules:**
- Keep content under 100KB. Writing examples may need to be condensed if too long.
- If user says "save brand voice", save to `seo_memory_brand_voice`
- If user says "save style guide", save to `seo_memory_style_guide`
- If user says "save examples", save to `seo_memory_writing_examples`
- If user says "save all writing context", save all three (three separate POSTs)
- Saving to the same namespace creates a new version (latest wins on GET)
- After saving, confirm: "Saved to Context Link as `{NAMESPACE}`"
- If requests are blocked, ask the user to add `*.context-link.ai` to Claude's **Settings > Capabilities > Domain Allowlist** (or select "All domains"), then retry.
