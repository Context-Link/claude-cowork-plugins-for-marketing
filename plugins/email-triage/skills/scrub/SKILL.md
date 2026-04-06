---
name: scrub
description: >
  Scrub AI-generated tells from draft text — em-dashes, filler phrases, overly
  enthusiastic language, and invisible Unicode watermarks. Works on inline text
  (not files). Called automatically by draft-email-response before output.
---

# Scrub Skill

Use this skill to clean AI tells from draft text so it reads like a human wrote it.

This skill operates on **text passed to it inline** — it does not read or write files.
It is typically called by other skills (like draft-email-response) as a post-processing
step before displaying output to the user.

---

## How to use

When another skill says "run the scrub skill", apply every rule below to the draft
text, then return the cleaned version. You do not need to report statistics — just
return the scrubbed text silently so the calling skill can use it in its output.

---

## What gets scrubbed

### 1. Invisible Unicode watermarks

Strip these characters entirely — they are invisible but detectable:

- Zero-width spaces (U+200B)
- Byte Order Mark (U+FEFF)
- Zero-width non-joiners (U+200C)
- Word joiner (U+2060)
- Soft hyphen (U+00AD)
- Narrow no-break space (U+202F)
- All Unicode Category Cf (format-control) codepoints

### 2. Em-dash replacement (U+2014)

Replace every em-dash with the most natural alternative based on context:

- **Comma** — for simple separation or parenthetical asides
- **Semicolon** — for closely related independent clauses
- **Period** — for strong breaks between complete thoughts
- **Colon** — when introducing an explanation
- **Remove entirely** — when the sentence reads fine without it

Examples:
- "This is great — you'll love it" → "This is great, you'll love it"
- "I tried everything — nothing worked" → "I tried everything. Nothing worked."
- "Here's the cause — Shopify requires..." → "Here's the cause: Shopify requires..."

### 3. Telltale AI phrases

Find and rewrite (or remove) these. Don't just delete them — make the sentence
read naturally without them.

**Transition phrases to cut or rewrite:**
- "Here's the thing" → remove or rewrite
- "Let's dive in" / "Let's dive into" → start directly
- "It's important to note that" → just state it
- "At the end of the day" → be specific or remove
- "When it comes to [X]" → discuss X directly
- "The reality is" / "The truth is" → state the fact

**Filler phrases:**
- "Essentially" (at sentence start) → cut
- "Basically" (at sentence start) → cut
- "Actually" (when not adding meaning) → cut
- "In order to" → "to"
- "Due to the fact that" → "because"
- "It goes without saying" → remove entirely
- "I completely understand" → "I understand" or cut entirely

**Overly enthusiastic language:**
- "Game-changer" / "game-changing"
- "Revolutionize" / "revolutionary"
- "Cutting-edge"
- "Seamlessly"
- "Robust"
- "Leverage" (as a verb)
- "Straightforward" → "simple" or "quick" or just cut

**AI structural tells:**
- Starting multiple paragraphs with "This"
- Excessive "Furthermore," "Moreover," "Additionally" → cut or use "and" / "also"
- "It's worth noting that" → cut, just say it
- "One thing to keep in mind" → cut
- Sentences starting with "So," as a transition → cut the "So,"
- Numbered bold headers inside what should be a casual email
- Bullet points in short emails (prefer flowing sentences)

### 4. Support email specific tells

These are particularly common in AI-drafted support replies:

- "I'd be happy to help!" → cut (you're already helping by replying)
- "Great question!" → cut
- "Thanks for reaching out!" → fine once, but don't pair with another opener
- "I hope this helps!" → cut
- "Please don't hesitate to..." → "Let me know if..." or just cut
- "I appreciate your patience" → cut unless there was genuinely a long wait
- "I understand your frustration" → only if they actually sound frustrated
- Signing off with multiple exclamation marks

---

## Process

1. Receive draft text from the calling skill
2. Apply all scrub rules above in a single pass
3. Re-read the result to make sure it still flows naturally
4. Return the cleaned text — no stats, no wrapper, just the text

The calling skill handles formatting and display.
