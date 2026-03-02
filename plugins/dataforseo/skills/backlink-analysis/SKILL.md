---
name: backlink-analysis
description: "DataForSEO backlink analysis: backlink profiles, referring domains, anchors, domain authority"
---

# Backlink Analysis Skill

Analyze backlink profiles, referring domains, anchor text distribution, and domain authority using the DataForSEO Backlinks API.

## Triggers

Use this skill when the user asks about:
- Backlinks or backlink profile for a domain
- Referring domains linking to a website
- Domain authority, domain rank, or DR/DA metrics
- Link profile analysis or link building research
- Anchor text distribution or anchor analysis

## Functions

### `backlinks_summary(target)`

Get a complete backlink profile overview for a domain including total backlinks, referring domains, dofollow/nofollow ratio, and domain rank.

**Parameters:**
- `target` (str): Domain to analyze (e.g., "example.com")

**Returns:** Summary metrics including backlink count, referring domains, rank, and link type breakdown.

---

### `backlinks_list(target, limit, mode)`

Get a detailed list of individual backlinks pointing to a domain.

**Parameters:**
- `target` (str): Domain to analyze (e.g., "example.com")
- `limit` (int): Maximum number of backlinks to return (default: 100)
- `mode` (str): Deduplication mode - "as_is" (all backlinks), "one_per_domain" (unique referring domains), "one_per_anchor" (unique anchor texts)

**Returns:** List of backlinks with source URL, anchor text, dofollow status, and page metrics.

---

### `backlinks_anchors(target, limit)`

Get anchor text distribution showing which text is used to link to the target domain.

**Parameters:**
- `target` (str): Domain to analyze (e.g., "example.com")
- `limit` (int): Maximum number of anchors to return (default: 100)

**Returns:** Anchor texts with frequency, backlink count, and referring domain count.

---

### `backlinks_referring_domains(target, limit)`

Get a list of domains linking to the target with their metrics.

**Parameters:**
- `target` (str): Domain to analyze (e.g., "example.com")
- `limit` (int): Maximum number of referring domains to return (default: 100)

**Returns:** Referring domains with rank, backlink count, and first/last seen dates.

---

### `backlinks_history(target)`

Get historical backlink data showing how the backlink profile has changed over time.

**Parameters:**
- `target` (str): Domain to analyze (e.g., "example.com")

**Returns:** Time series data of backlink counts, referring domains, and rank changes.

---

### `backlinks_bulk_ranks(targets)`

Get domain authority/rank metrics for multiple domains at once. Useful for comparing competitors or evaluating link prospects.

**Parameters:**
- `targets` (list[str]): List of domains to analyze (e.g., ["example.com", "competitor.com"])

**Returns:** Rank metrics for each domain including backlinks, referring domains, and rank score.

## Example Usage

```python
import sys
sys.path.insert(0, "/path/to/plugin")
from scripts.dataforseo_client import (
    backlinks_summary,
    backlinks_list,
    backlinks_anchors,
    backlinks_referring_domains,
    backlinks_history,
    backlinks_bulk_ranks,
    extract_results,
    to_csv
)

# Get backlink profile overview
response = backlinks_summary("example.com")
results = extract_results(response)
csv_path = to_csv(results, "backlinks_summary_example")
print(f"Summary exported to: {csv_path}")

# Get list of backlinks (one per referring domain)
response = backlinks_list("example.com", limit=500, mode="one_per_domain")
results = extract_results(response)
csv_path = to_csv(results, "backlinks_list_example")
print(f"Backlinks exported to: {csv_path}")

# Get anchor text distribution
response = backlinks_anchors("example.com", limit=200)
results = extract_results(response)
csv_path = to_csv(results, "backlinks_anchors_example")
print(f"Anchors exported to: {csv_path}")

# Get referring domains
response = backlinks_referring_domains("example.com", limit=300)
results = extract_results(response)
csv_path = to_csv(results, "referring_domains_example")
print(f"Referring domains exported to: {csv_path}")

# Get backlink history over time
response = backlinks_history("example.com")
results = extract_results(response)
csv_path = to_csv(results, "backlinks_history_example")
print(f"History exported to: {csv_path}")

# Compare domain authority for multiple domains
domains = ["example.com", "competitor1.com", "competitor2.com"]
response = backlinks_bulk_ranks(domains)
results = extract_results(response)
csv_path = to_csv(results, "domain_ranks_comparison")
print(f"Domain ranks exported to: {csv_path}")
```

## Output

All results are exported as CSV files to `~/dataforseo_outputs/` with timestamped filenames.

### Summary Output Fields
- `rank` - Domain rank score
- `backlinks` - Total backlink count
- `backlinks_spam_score` - Spam score indicator
- `broken_backlinks` - Count of broken backlinks
- `referring_domains` - Unique referring domain count
- `referring_domains_nofollow` - Nofollow referring domains
- `referring_main_domains` - Unique root domains
- `referring_ips` - Unique referring IPs
- `referring_subnets` - Unique referring subnets

### Backlinks List Output Fields
- `url_from` - Source page URL
- `url_to` - Target page URL
- `anchor` - Anchor text used
- `dofollow` - Whether link passes PageRank
- `page_from_rank` - Source page rank
- `domain_from_rank` - Source domain rank
- `first_seen` - When backlink was first discovered
- `last_seen` - When backlink was last verified

### Anchor Output Fields
- `anchor` - The anchor text
- `backlinks` - Number of backlinks using this anchor
- `referring_domains` - Domains using this anchor
- `first_seen` - First occurrence date

### Referring Domains Output Fields
- `domain` - Referring domain name
- `rank` - Domain rank score
- `backlinks` - Backlinks from this domain
- `first_visited` - First crawl date
- `last_visited` - Last crawl date
