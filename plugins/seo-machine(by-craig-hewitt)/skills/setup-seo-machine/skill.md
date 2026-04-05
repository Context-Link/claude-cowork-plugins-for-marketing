# Setup SEO Machine

Interactive setup wizard for configuring SEO Machine for your business. This skill guides you through all necessary configuration steps to get the most out of the SEO content creation system.

## Overview

SEO Machine requires configuration of:
1. **Context Files** - Brand voice, writing examples, and SEO guidelines
2. **Data Sources** (optional) - Google Analytics 4, Search Console, DataForSEO
3. **WordPress** (optional) - For direct publishing via REST API

## Setup Workflow

When invoked, walk the user through each step interactively.

---

## Step 1: Python Dependencies

First, ensure the analysis modules can run:

```bash
pip install -r data_sources/requirements.txt
```

This installs:
- Google Analytics/Search Console integrations
- DataForSEO API client
- NLP libraries (nltk, textstat)
- Machine learning (scikit-learn)
- Web scraping tools (beautifulsoup4)

---

## Step 2: Essential Context Files

These 3 files are **required** for quality content generation:

### 2.1 Brand Voice (`context/brand-voice.md`)

Ask the user to provide:
- **Voice pillars** (3-5 adjectives that describe their brand voice)
- **Tone guidelines** (how formal/casual, technical/accessible)
- **Do's and Don'ts** (specific language preferences)
- **Core messages** (key value propositions)

Reference: `examples/castos/brand-voice.md` for a complete example.

### 2.2 Features (`context/features.md`)

Ask the user to provide:
- **Product/service features** (what they offer)
- **Benefits** (what problems they solve)
- **Differentiators** (what makes them unique vs competitors)
- **Use cases** (who uses their product and how)

### 2.3 Writing Examples (`context/writing-examples.md`)

Ask the user to provide:
- **3-5 exemplary blog posts** from their site (full content, not excerpts)
- For each example, note what makes it great
- These examples teach the AI their specific writing style

---

## Step 3: Recommended Context Files

These files significantly improve output quality:

### 3.1 Internal Links Map (`context/internal-links-map.md`)

Ask the user to provide:
- **Key product/feature pages** with URLs
- **Pillar content URLs** (comprehensive guides)
- **Top-performing blog posts** with URLs
- **Recommended anchor text** for each link

### 3.2 Target Keywords (`context/target-keywords.md`)

Ask the user to provide:
- **Topic clusters** (grouped by theme)
- **Primary keywords** for each cluster
- **Long-tail variations**
- **Search intent** (informational, commercial, transactional)
- **Current rankings** if known

### 3.3 Style Guide (`context/style-guide.md`)

Ask the user to provide:
- **Grammar preferences** (Oxford comma, etc.)
- **Capitalization rules** (title case vs sentence case)
- **Formatting standards** (header hierarchy, list styles)
- **Terminology** (preferred terms, words to avoid)

### 3.4 Competitor Analysis (`context/competitor-analysis.md`)

Ask the user to provide:
- **Primary competitors** (3-5 main competitors)
- **Their content strategies** (topics they cover)
- **Content gaps** (topics they don't cover well)
- **Differentiation opportunities**

---

## Step 4: Data Sources Setup (Optional)

These integrations enable data-driven content prioritization.

### 4.1 Google Analytics 4

Required information:
- **GA4 Property ID** (format: `123456789`)
- **Service account JSON key file** (from Google Cloud Console)

Setup steps:
1. Enable Google Analytics Data API in Google Cloud Console
2. Create a service account
3. Download JSON key as `credentials/ga4-credentials.json`
4. Add service account email to GA4 property with Viewer access
5. Add to `.env`: `GA4_PROPERTY_ID=123456789`

### 4.2 Google Search Console

Required information:
- **Site URL** (format: `https://yoursite.com/` or `sc-domain:yoursite.com`)
- **Service account access** (can reuse GA4 service account)

Setup steps:
1. Enable Google Search Console API in Google Cloud Console
2. Add service account email to Search Console with Full access
3. Add to `.env`: `GSC_SITE_URL=https://yoursite.com/`

### 4.3 DataForSEO

Required information:
- **Login** (username/email)
- **API Password** (different from account password)

Setup steps:
1. Create account at dataforseo.com
2. Get API credentials from dashboard
3. Add to `.env`:
   ```
   DATAFORSEO_LOGIN=your_username
   DATAFORSEO_PASSWORD=your_api_password
   ```

---

## Step 5: WordPress Setup (Optional)

For direct publishing via `/publish-draft` command.

Required information:
- **WordPress URL** (e.g., `https://yoursite.com`)
- **Admin username**
- **Application password** (not regular password)

Setup steps:
1. Install `wordpress/seo-machine-yoast-rest.php` as MU-plugin
2. Create Application Password in WordPress admin (Users > Profile)
3. Add to `.env`:
   ```
   WP_URL=https://yoursite.com
   WP_USERNAME=your_username
   WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
   ```

---

## Step 6: Competitor Configuration

For SEO analysis scripts, configure `config/competitors.json`:

```json
{
  "company_name": "Your Company",
  "domain": "yoursite.com",
  "competitors": [
    {
      "name": "Competitor 1",
      "domain": "competitor1.com"
    },
    {
      "name": "Competitor 2",
      "domain": "competitor2.com"
    }
  ],
  "target_keywords": [
    "keyword 1",
    "keyword 2",
    "keyword 3"
  ]
}
```

---

## Step 7: Verify Setup

After configuration, test the setup:

1. **Test a simple command**:
   ```
   /research [topic]
   ```

2. **Check output** in `/output/research/` directory

3. **Write a test article**:
   ```
   /write [topic]
   ```

4. **Review** the article and agent reports in `/output/drafts/`

---

## Quick Start Summary

**Minimum setup (5 minutes)**:
1. Fill out `context/brand-voice.md`
2. Fill out `context/features.md`
3. Add 3-5 examples to `context/writing-examples.md`
4. Run `/research [topic]` then `/write [topic]`

**Full setup (30-60 minutes)**:
1. Complete all context files
2. Set up data source integrations
3. Configure WordPress publishing
4. Run test commands to verify

---

## Troubleshooting

### Content doesn't match brand voice
- Add more specific examples to `writing-examples.md`
- Be more explicit in `brand-voice.md` about do's and don'ts

### Internal links aren't relevant
- Ensure `internal-links-map.md` is organized by topic
- Add descriptions for what each page covers

### API authentication errors
- Verify credentials in `.env` file
- Check service account permissions
- Ensure APIs are enabled in Google Cloud Console

### DataForSEO errors
- Check you're using API password, not account password
- Verify you have sufficient API credits

---

## Available Commands After Setup

**Core workflow**:
- `/research [topic]` - Research before writing
- `/write [topic]` - Create new article
- `/rewrite [topic]` - Update existing content
- `/optimize [file]` - Final SEO polish

**Analysis**:
- `/analyze-existing [URL]` - Analyze existing post
- `/performance-review` - Analytics-driven priorities
- `/priorities` - Content prioritization matrix

**Landing pages**:
- `/landing-write [topic]` - Create landing page
- `/landing-audit [file]` - CRO audit

See README.md for the complete command reference.
