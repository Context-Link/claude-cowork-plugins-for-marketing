---
name: competitor-analysis
description: "DataForSEO competitor analysis: keyword gaps, competing domains, domain intersection, link gaps. Use when the user mentions 'competitor analysis', 'keyword gap', 'content gap', 'competing domains', 'domain comparison', 'link gap', 'backlink gap', 'find competitors', or 'domain intersection'."
---

# Competitor Analysis with DataForSEO

Analyze competitors using DataForSEO APIs. Find competing domains, identify keyword gaps, discover link opportunities, and compare domain performance.

## Available Functions

Import all functions from the DataForSEO client:

```python
import sys
sys.path.insert(0, "../../scripts")
from dataforseo_client import (
    labs_competitors_domain,
    labs_domain_intersection,
    labs_serp_competitors,
    labs_domain_rank_overview,
    backlinks_competitors,
    backlinks_domain_intersection,
    extract_results,
    to_csv,
)
```

---

## Function Reference

### labs_competitors_domain()

Find domains that compete with your target domain in organic search results.

**Parameters:**
- `target` (str): The domain to analyze (e.g., "example.com")
- `location_name` (str): Target location (default: "United States")
- `language_name` (str): Target language (default: "English")

**Example:**
```python
from dataforseo_client import labs_competitors_domain, extract_results, to_csv

# Find competing domains
response = labs_competitors_domain(
    target="ahrefs.com",
    location_name="United States",
    language_name="English"
)

results = extract_results(response)
filepath = to_csv(results, "competing_domains")
print(f"Saved to: {filepath}")
```

**Output fields:** domain, avg_position, sum_position, intersections, full_domain_metrics

---

### labs_domain_intersection()

Keyword gap analysis - find keywords that multiple domains rank for. Identify content opportunities by comparing your domain against competitors.

**Parameters:**
- `targets` (list[str]): List of 2-20 domains to compare (e.g., ["yourdomain.com", "competitor1.com", "competitor2.com"])
- `location_name` (str): Target location (default: "United States")
- `language_name` (str): Target language (default: "English")
- `limit` (int): Maximum results to return (default: 100)

**Example:**
```python
from dataforseo_client import labs_domain_intersection, extract_results, to_csv

# Find keyword gaps between domains
response = labs_domain_intersection(
    targets=["yourdomain.com", "competitor1.com", "competitor2.com"],
    location_name="United States",
    language_name="English",
    limit=500
)

results = extract_results(response)
filepath = to_csv(results, "keyword_gap_analysis")
print(f"Saved to: {filepath}")
```

**Output fields:** keyword, keyword_data (search_volume, cpc, competition), intersection_result (rankings per domain)

---

### labs_serp_competitors()

Find domains that compete for specific keywords in SERP results.

**Parameters:**
- `keywords` (list[str]): List of keywords to analyze
- `location_name` (str): Target location (default: "United States")
- `language_name` (str): Target language (default: "English")

**Example:**
```python
from dataforseo_client import labs_serp_competitors, extract_results, to_csv

# Find SERP competitors for keywords
response = labs_serp_competitors(
    keywords=["seo tools", "backlink checker", "keyword research"],
    location_name="United States",
    language_name="English"
)

results = extract_results(response)
filepath = to_csv(results, "serp_competitors")
print(f"Saved to: {filepath}")
```

**Output fields:** domain, avg_position, median_position, rating, etv, keywords_count

---

### labs_domain_rank_overview()

Get comprehensive domain ranking metrics and overview data.

**Parameters:**
- `target` (str): The domain to analyze (e.g., "example.com")
- `location_name` (str): Target location (default: "United States")
- `language_name` (str): Target language (default: "English")

**Example:**
```python
from dataforseo_client import labs_domain_rank_overview, extract_results, to_csv

# Get domain rank overview
response = labs_domain_rank_overview(
    target="semrush.com",
    location_name="United States",
    language_name="English"
)

results = extract_results(response)
filepath = to_csv(results, "domain_overview")
print(f"Saved to: {filepath}")
```

**Output fields:** target, organic_etv, organic_count, organic_is_lost, organic_is_new

---

### backlinks_competitors()

Find domains that have similar backlink profiles - potential link building targets.

**Parameters:**
- `target` (str): The domain to analyze (e.g., "example.com")
- `limit` (int): Maximum results to return (default: 100)

**Example:**
```python
from dataforseo_client import backlinks_competitors, extract_results, to_csv

# Find backlink competitors
response = backlinks_competitors(
    target="moz.com",
    limit=100
)

results = extract_results(response)
filepath = to_csv(results, "backlink_competitors")
print(f"Saved to: {filepath}")
```

**Output fields:** target, intersections, rank

---

### backlinks_domain_intersection()

Link gap analysis - find referring domains that link to competitors but not to you.

**Parameters:**
- `targets` (list[str]): List of 2-20 domains to compare. First domain is typically yours, subsequent domains are competitors.
- `limit` (int): Maximum results to return (default: 100)

**Example:**
```python
from dataforseo_client import backlinks_domain_intersection, extract_results, to_csv

# Find link gaps (sites linking to competitors but not you)
response = backlinks_domain_intersection(
    targets=["yourdomain.com", "competitor1.com", "competitor2.com"],
    limit=500
)

results = extract_results(response)
filepath = to_csv(results, "link_gap_analysis")
print(f"Saved to: {filepath}")
```

**Output fields:** domain, intersections (which targets each referring domain links to)

---

## Common Workflows

### Complete Competitor Analysis

```python
import sys
sys.path.insert(0, "../../scripts")
from dataforseo_client import (
    labs_competitors_domain,
    labs_domain_intersection,
    labs_domain_rank_overview,
    backlinks_competitors,
    backlinks_domain_intersection,
    extract_results,
    to_csv,
)

target_domain = "yourdomain.com"
location = "United States"
language = "English"

# Step 1: Find competing domains
competitors_response = labs_competitors_domain(
    target=target_domain,
    location_name=location,
    language_name=language
)
competitors = extract_results(competitors_response)
to_csv(competitors, "1_competing_domains")

# Step 2: Get top competitor domains for comparison
top_competitors = [c["domain"] for c in competitors[:5] if "domain" in c]
all_domains = [target_domain] + top_competitors

# Step 3: Keyword gap analysis
if len(all_domains) >= 2:
    keyword_gap = labs_domain_intersection(
        targets=all_domains,
        location_name=location,
        language_name=language,
        limit=500
    )
    to_csv(extract_results(keyword_gap), "2_keyword_gap")

# Step 4: Link gap analysis
if len(all_domains) >= 2:
    link_gap = backlinks_domain_intersection(
        targets=all_domains,
        limit=500
    )
    to_csv(extract_results(link_gap), "3_link_gap")

# Step 5: Domain rank comparison
for domain in all_domains:
    overview = labs_domain_rank_overview(
        target=domain,
        location_name=location,
        language_name=language
    )
    to_csv(extract_results(overview), f"4_overview_{domain.replace('.', '_')}")

print("Analysis complete. Check ~/dataforseo_outputs/")
```

### Keyword Gap Analysis Only

```python
import sys
sys.path.insert(0, "../../scripts")
from dataforseo_client import labs_domain_intersection, extract_results, to_csv

# Compare your domain against specific competitors
response = labs_domain_intersection(
    targets=[
        "yourdomain.com",      # Your domain first
        "competitor1.com",
        "competitor2.com",
        "competitor3.com"
    ],
    location_name="United States",
    language_name="English",
    limit=1000
)

results = extract_results(response)
filepath = to_csv(results, "keyword_gap_report")
print(f"Keywords exported to: {filepath}")
```

### Link Gap Analysis Only

```python
import sys
sys.path.insert(0, "../../scripts")
from dataforseo_client import backlinks_domain_intersection, extract_results, to_csv

# Find sites linking to competitors but not you
response = backlinks_domain_intersection(
    targets=[
        "yourdomain.com",      # Your domain first
        "competitor1.com",
        "competitor2.com"
    ],
    limit=500
)

results = extract_results(response)
filepath = to_csv(results, "link_opportunities")
print(f"Link opportunities exported to: {filepath}")
```

---

## Parameters Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target` | str | required | Single domain to analyze |
| `targets` | list[str] | required | List of domains for intersection analysis (2-20 domains) |
| `location_name` | str | "United States" | Geographic location for search data |
| `language_name` | str | "English" | Language for search data |
| `limit` | int | 100 | Maximum number of results to return |

## Output

All results are exported to CSV files in `~/dataforseo_outputs/` with timestamps.

---

## Related Skills

- **keyword-research**: For expanding keyword lists
- **backlink-analysis**: For deep backlink profiling
- **serp-analysis**: For analyzing search result pages
