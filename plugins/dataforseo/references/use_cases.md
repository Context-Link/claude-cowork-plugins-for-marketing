# DataForSEO Common Use Cases

Quick recipes for common SEO analysis tasks.

---

## Keyword Research

### Get search volume for keywords
```python
from dataforseo_client import keywords_search_volume, extract_results, to_csv

response = keywords_search_volume(
    keywords=["seo tools", "keyword research", "backlink checker"],
    location_name="United States",
    language_name="English"
)
results = extract_results(response)
csv_path = to_csv(results, "keyword_volumes")
```

### Generate keyword ideas from seed keyword
```python
from dataforseo_client import labs_keyword_ideas, extract_results, to_csv

response = labs_keyword_ideas(
    keywords=["digital marketing"],
    location_name="United States",
    limit=500
)
results = extract_results(response)
csv_path = to_csv(results, "keyword_ideas")
```

### Find keywords a competitor ranks for
```python
from dataforseo_client import labs_ranked_keywords, extract_results, to_csv

response = labs_ranked_keywords(
    target="competitor.com",
    location_name="United States",
    limit=1000
)
results = extract_results(response)
csv_path = to_csv(results, "competitor_keywords")
```

---

## Competitor Analysis

### Find competing domains
```python
from dataforseo_client import labs_competitors_domain, extract_results, to_csv

response = labs_competitors_domain(
    target="yoursite.com",
    location_name="United States"
)
results = extract_results(response)
csv_path = to_csv(results, "competitors")
```

### Keyword gap analysis (find keywords competitors rank for that you don't)
```python
from dataforseo_client import labs_domain_intersection, extract_results, to_csv

response = labs_domain_intersection(
    targets=["yoursite.com", "competitor1.com", "competitor2.com"],
    location_name="United States",
    limit=500
)
results = extract_results(response)
csv_path = to_csv(results, "keyword_gap")
```

### SERP competitors for specific keywords
```python
from dataforseo_client import labs_serp_competitors, extract_results, to_csv

response = labs_serp_competitors(
    keywords=["content marketing", "seo services"],
    location_name="United States"
)
results = extract_results(response)
csv_path = to_csv(results, "serp_competitors")
```

---

## Backlink Analysis

### Quick backlink profile overview
```python
from dataforseo_client import backlinks_summary, extract_results, to_csv

response = backlinks_summary("example.com")
results = extract_results(response)
csv_path = to_csv(results, "backlink_summary")
```

### Get list of backlinks
```python
from dataforseo_client import backlinks_list, extract_results, to_csv

response = backlinks_list(
    target="example.com",
    limit=500,
    mode="one_per_domain"  # Deduplicate by domain
)
results = extract_results(response)
csv_path = to_csv(results, "backlinks")
```

### Link gap (find sites linking to competitors but not you)
```python
from dataforseo_client import backlinks_domain_intersection, extract_results, to_csv

response = backlinks_domain_intersection(
    targets=["competitor1.com", "competitor2.com"],  # Sites that link to both
    limit=500
)
results = extract_results(response)
csv_path = to_csv(results, "link_gap")
```

### Bulk domain authority check
```python
from dataforseo_client import backlinks_bulk_ranks, extract_results, to_csv

response = backlinks_bulk_ranks([
    "site1.com", "site2.com", "site3.com", "site4.com"
])
results = extract_results(response)
csv_path = to_csv(results, "domain_ranks")
```

---

## Rank Tracking

### Check rankings for keywords
```python
from dataforseo_client import serp_google_organic, extract_results, to_csv

# Check multiple keywords
keywords = ["your brand", "your service keyword", "product name"]
all_results = []

for kw in keywords:
    response = serp_google_organic(
        keyword=kw,
        location_name="United States",
        device="desktop",
        depth=100
    )
    results = extract_results(response)
    for r in results:
        r["search_keyword"] = kw
    all_results.extend(results)

csv_path = to_csv(all_results, "rankings")
```

### Local rank tracking (Maps)
```python
from dataforseo_client import serp_google_maps, extract_results, to_csv

response = serp_google_maps(
    keyword="coffee shop near me",
    location_name="New York,New York,United States"
)
results = extract_results(response)
csv_path = to_csv(results, "local_rankings")
```

---

## Technical SEO Audit

### Quick page analysis (instant)
```python
from dataforseo_client import onpage_instant_pages, extract_results, to_csv

response = onpage_instant_pages("https://example.com/page-to-audit")
results = extract_results(response)
csv_path = to_csv(results, "page_audit")
```

### Lighthouse performance audit
```python
from dataforseo_client import lighthouse_live, extract_results, to_csv

response = lighthouse_live(
    url="https://example.com",
    device="mobile",
    categories=["performance", "seo"]
)
results = extract_results(response)
csv_path = to_csv(results, "lighthouse")
```

### Full site crawl (async - check back for results)
```python
from dataforseo_client import onpage_task_post

response = onpage_task_post(
    target="https://example.com",
    max_crawl_pages=500,
    enable_javascript=True
)
# Note the task_id from response to retrieve results later
print(response)
```

---

## Domain Intelligence

### Check domain technology stack
```python
from dataforseo_client import domain_technologies, extract_results, to_csv

response = domain_technologies("competitor.com")
results = extract_results(response)
csv_path = to_csv(results, "tech_stack")
```

### WHOIS information
```python
from dataforseo_client import domain_whois, extract_results, to_csv

response = domain_whois("example.com")
results = extract_results(response)
csv_path = to_csv(results, "whois")
```

---

## Content & Brand Monitoring

### Search brand mentions
```python
from dataforseo_client import content_search, extract_results, to_csv

response = content_search(
    keyword="Your Brand Name",
    location_name="United States",
    limit=100
)
results = extract_results(response)
csv_path = to_csv(results, "brand_mentions")
```

### Sentiment analysis
```python
from dataforseo_client import content_sentiment, extract_results, to_csv

response = content_sentiment(
    keyword="your brand name",
    location_name="United States"
)
results = extract_results(response)
csv_path = to_csv(results, "sentiment")
```

---

## Trends & Research

### Google Trends comparison
```python
from dataforseo_client import google_trends, extract_results, to_csv

response = google_trends(
    keywords=["youtube marketing", "instagram marketing", "tiktok marketing"],
    location_name="United States",
    time_range="past_12_months"
)
results = extract_results(response)
csv_path = to_csv(results, "trends")
```

---

## YouTube Analysis

### YouTube search results
```python
from dataforseo_client import serp_youtube, extract_results, to_csv

response = serp_youtube(
    keyword="video marketing tutorial",
    location_name="United States"
)
results = extract_results(response)
csv_path = to_csv(results, "youtube_results")
```

---

## E-commerce Research

### Google Shopping results
```python
from dataforseo_client import merchant_google_products

response = merchant_google_products(
    keyword="camera equipment",
    location_name="United States"
)
# Note: This creates async task, retrieve results separately
```

---

## Multi-Keyword Analysis Pattern

```python
from dataforseo_client import (
    keywords_search_volume,
    labs_keyword_ideas,
    extract_results,
    to_csv
)

# Start with seed keywords
seeds = ["content marketing", "digital strategy", "seo optimization"]

# Get search volumes
vol_response = keywords_search_volume(seeds, location_name="United States")
volumes = extract_results(vol_response)

# Expand to more keywords
ideas_response = labs_keyword_ideas(seeds, location_name="United States", limit=500)
ideas = extract_results(ideas_response)

# Export both
to_csv(volumes, "seed_volumes")
to_csv(ideas, "expanded_keywords")
```

---

## Batch Domain Analysis Pattern

```python
from dataforseo_client import (
    backlinks_bulk_ranks,
    labs_domain_rank_overview,
    extract_results,
    to_csv
)

domains = ["site1.com", "site2.com", "site3.com"]

# Quick authority check
ranks = backlinks_bulk_ranks(domains)
to_csv(extract_results(ranks), "domain_ranks")

# Detailed analysis per domain
for domain in domains:
    overview = labs_domain_rank_overview(domain, location_name="United States")
    to_csv(extract_results(overview), f"overview_{domain.replace('.', '_')}")
```
