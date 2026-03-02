---
name: keyword-research
description: "DataForSEO keyword research: search volume, CPC, competition metrics, keyword ideas, and keyword suggestions"
---

# Keyword Research Skill

Use this skill when the user asks about:
- Keyword research or keyword analysis
- Search volume data for keywords
- CPC (cost-per-click) or PPC data
- Keyword competition metrics
- Keyword ideas or keyword suggestions
- Related keywords or semantic keywords
- Keywords for a website or domain
- Keywords a domain ranks for

## Available Functions

### keywords_search_volume()
Get search volume, CPC, and competition metrics for a list of keywords using Google Ads data.

**Parameters:**
- `keywords` (list[str]) - List of keywords to analyze
- `location_name` (str) - Target location (default: "United States")
- `language_name` (str) - Target language (default: "English")

**Returns:** Search volume, CPC, competition level, and monthly trends for each keyword.

---

### keywords_for_site()
Get keyword suggestions based on a website's content.

**Parameters:**
- `target` (str) - Domain or URL to analyze (e.g., "example.com")
- `location_name` (str) - Target location (default: "United States")
- `language_name` (str) - Target language (default: "English")

**Returns:** Keywords relevant to the website with search volume and competition data.

---

### keywords_for_keywords()
Get related keyword suggestions based on seed keywords.

**Parameters:**
- `keywords` (list[str]) - Seed keywords to expand
- `location_name` (str) - Target location (default: "United States")
- `language_name` (str) - Target language (default: "English")

**Returns:** Related keywords with search volume and competition metrics.

---

### labs_keyword_ideas()
Get keyword ideas based on seed keywords using DataForSEO Labs.

**Parameters:**
- `keywords` (list[str]) - Seed keywords
- `location_name` (str) - Target location (default: "United States")
- `language_name` (str) - Target language (default: "English")
- `limit` (int) - Maximum results to return (default: 100)

**Returns:** Keyword ideas with search volume, CPC, competition, and keyword difficulty.

---

### labs_related_keywords()
Get semantically related keywords for a single keyword.

**Parameters:**
- `keyword` (str) - Single keyword to find related terms for
- `location_name` (str) - Target location (default: "United States")
- `language_name` (str) - Target language (default: "English")
- `limit` (int) - Maximum results to return (default: 100)

**Returns:** Semantically related keywords with metrics and relevance scores.

---

### labs_ranked_keywords()
Get keywords that a domain currently ranks for in Google.

**Parameters:**
- `target` (str) - Domain to analyze (e.g., "example.com")
- `location_name` (str) - Target location (default: "United States")
- `language_name` (str) - Target language (default: "English")
- `limit` (int) - Maximum results to return (default: 100)

**Returns:** Keywords the domain ranks for with position, search volume, and traffic estimates.

---

## Example Usage

```python
import sys, os
skill_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
sys.path.insert(0, os.path.join(skill_dir, '..', '..', 'scripts'))
from dataforseo_client import (
    keywords_search_volume,
    keywords_for_site,
    keywords_for_keywords,
    labs_keyword_ideas,
    labs_related_keywords,
    labs_ranked_keywords,
    extract_results,
    to_csv
)

# Example 1: Get search volume for specific keywords
response = keywords_search_volume(
    keywords=["seo tools", "keyword research", "backlink checker"],
    location_name="United States",
    language_name="English"
)
results = extract_results(response)
csv_path = to_csv(results, "keyword_search_volume")
print(f"Saved to: {csv_path}")

# Example 2: Get keywords for a website
response = keywords_for_site(
    target="ahrefs.com",
    location_name="United States",
    language_name="English"
)
results = extract_results(response)
csv_path = to_csv(results, "keywords_for_site")

# Example 3: Get keyword ideas from seed keywords
response = labs_keyword_ideas(
    keywords=["email marketing"],
    location_name="United States",
    language_name="English",
    limit=200
)
results = extract_results(response)
csv_path = to_csv(results, "keyword_ideas")

# Example 4: Get semantically related keywords
response = labs_related_keywords(
    keyword="content marketing",
    location_name="United States",
    language_name="English",
    limit=100
)
results = extract_results(response)
csv_path = to_csv(results, "related_keywords")

# Example 5: Get keywords a domain ranks for
response = labs_ranked_keywords(
    target="hubspot.com",
    location_name="United States",
    language_name="English",
    limit=500
)
results = extract_results(response)
csv_path = to_csv(results, "ranked_keywords")
```

## Common Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `location_name` | Geographic location for data | "United States" |
| `language_name` | Language for results | "English" |
| `limit` | Maximum number of results | 100 |

## Output

All results can be exported to CSV using the `to_csv()` helper function. Files are saved to `~/dataforseo_outputs/` by default with a timestamp appended to the filename.

### Typical Output Fields

- **keyword** - The keyword text
- **search_volume** - Average monthly search volume
- **cpc** - Cost per click (USD)
- **competition** - Competition level (0-1 scale)
- **competition_level** - Competition category (LOW, MEDIUM, HIGH)
- **monthly_searches** - Historical monthly search data
- **keyword_difficulty** - Difficulty score (Labs endpoints only)
