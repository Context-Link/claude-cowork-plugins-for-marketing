# DataForSEO API Reference

## Table of Contents
1. [SERP API](#serp-api)
2. [Keywords Data API](#keywords-data-api)
3. [DataForSEO Labs API](#dataforseo-labs-api)
4. [Backlinks API](#backlinks-api)
5. [OnPage API](#onpage-api)
6. [Domain Analytics API](#domain-analytics-api)
7. [Content Analysis API](#content-analysis-api)
8. [Business Data API](#business-data-api)
9. [Merchant API](#merchant-api)
10. [App Data API](#app-data-api)
11. [AI Optimization API](#ai-optimization-api)
12. [Common Parameters](#common-parameters)
13. [Error Codes](#error-codes)

---

## SERP API

Search engine results page data for Google, Bing, YouTube, Baidu, Yahoo, Naver, Seznam.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `serp_google_organic` | `/serp/google/organic/live/advanced` | Google organic results |
| `serp_google_maps` | `/serp/google/maps/live/advanced` | Google Maps local results |
| `serp_bing_organic` | `/serp/bing/organic/live/advanced` | Bing organic results |
| `serp_youtube` | `/serp/youtube/organic/live/advanced` | YouTube search results |

### Google SERP Features Supported
- Organic results, Featured snippets, Knowledge panel
- People Also Ask, Local pack, Images, Videos
- News, Shopping results, AI Overview
- Jobs, Events, Maps results

### Parameters
```python
serp_google_organic(
    keyword="seo tools",           # Required: search query
    location_name="United States", # Location (see get_locations)
    language_name="English",       # Language (see get_languages)
    device="desktop",              # desktop | mobile
    depth=100,                     # Results depth (10-700)
)
```

---

## Keywords Data API

Keyword metrics from Google Ads, Bing Ads, Google Trends, and Clickstream.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `keywords_search_volume` | `/keywords_data/google_ads/search_volume/live` | Search volume, CPC, competition |
| `keywords_for_site` | `/keywords_data/google_ads/keywords_for_site/live` | Keywords a site ranks for |
| `keywords_for_keywords` | `/keywords_data/google_ads/keywords_for_keywords/live` | Related keyword suggestions |
| `google_trends` | `/keywords_data/google_trends/explore/live` | Trend data over time |

### Parameters
```python
keywords_search_volume(
    keywords=["seo", "marketing"],  # Up to 1000 keywords
    location_name="United States",
    language_name="English",
)

google_trends(
    keywords=["bitcoin", "ethereum"],
    time_range="past_12_months",  # past_hour, past_4_hours, past_day, past_7_days, past_30_days, past_90_days, past_12_months, past_5_years
)
```

---

## DataForSEO Labs API

Advanced keyword research, competitor analysis, and domain intelligence.

### Keyword Research Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `labs_keyword_ideas` | `/dataforseo_labs/google/keyword_ideas/live` | Generate keyword ideas |
| `labs_related_keywords` | `/dataforseo_labs/google/related_keywords/live` | Semantically related keywords |

### Competitor Research Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `labs_ranked_keywords` | `/dataforseo_labs/google/ranked_keywords/live` | Keywords a domain ranks for |
| `labs_serp_competitors` | `/dataforseo_labs/google/serp_competitors/live` | Domains ranking for keywords |
| `labs_competitors_domain` | `/dataforseo_labs/google/competitors_domain/live` | Competing domains |
| `labs_domain_intersection` | `/dataforseo_labs/google/domain_intersection/live` | Common keywords (keyword gap) |
| `labs_domain_rank_overview` | `/dataforseo_labs/google/domain_rank_overview/live` | Domain authority metrics |

### Parameters
```python
labs_ranked_keywords(
    target="example.com",          # Domain to analyze
    location_name="United States",
    language_name="English",
    limit=100,                     # Results limit (max 1000)
)

labs_domain_intersection(
    targets=["domain1.com", "domain2.com", "domain3.com"],  # 2-20 domains
    limit=100,
)
```

---

## Backlinks API

Comprehensive backlink analysis and link intelligence.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `backlinks_summary` | `/backlinks/summary/live` | Backlink profile overview |
| `backlinks_list` | `/backlinks/backlinks/live` | List of backlinks |
| `backlinks_anchors` | `/backlinks/anchors/live` | Anchor text distribution |
| `backlinks_referring_domains` | `/backlinks/referring_domains/live` | Referring domains list |
| `backlinks_competitors` | `/backlinks/competitors/live` | Backlink competitors |
| `backlinks_domain_intersection` | `/backlinks/domain_intersection/live` | Link gap analysis |
| `backlinks_history` | `/backlinks/history/live` | Historical backlink data |
| `backlinks_bulk_ranks` | `/backlinks/bulk_ranks/live` | Bulk domain authority check |

### Parameters
```python
backlinks_list(
    target="example.com",
    limit=100,
    mode="as_is",  # as_is | one_per_domain | one_per_anchor
)

backlinks_domain_intersection(
    targets=["competitor1.com", "competitor2.com"],
    limit=100,
)
```

### Key Metrics Returned
- `rank`: Domain authority score (0-1000)
- `backlinks`: Total backlink count
- `referring_domains`: Unique referring domains
- `dofollow`/`nofollow`: Link attribute breakdown
- `spam_score`: Spam indicator (0-100)

---

## OnPage API

Website crawling and technical SEO audits.

### Workflow
1. Start crawl with `onpage_task_post()`
2. Wait for completion (check `onpage_summary()`)
3. Retrieve data with specific endpoints

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `onpage_task_post` | `/on_page/task_post` | Start crawl |
| `onpage_summary` | `/on_page/summary/{id}` | Crawl summary |
| `onpage_pages` | `/on_page/pages` | Crawled pages |
| `onpage_resources` | `/on_page/resources` | Page resources (JS, CSS, images) |
| `onpage_duplicate_tags` | `/on_page/duplicate_tags` | Duplicate titles/descriptions |
| `onpage_links` | `/on_page/links` | Internal/external links |
| `onpage_instant_pages` | `/on_page/instant_pages` | Single page analysis (no crawl) |
| `lighthouse_live` | `/on_page/lighthouse/live/json` | Google Lighthouse audit |

### Parameters
```python
onpage_task_post(
    target="https://example.com",
    max_crawl_pages=100,       # 1-100000
    load_resources=True,       # Analyze JS/CSS/images
    enable_javascript=False,   # JS rendering (slower, costlier)
)

lighthouse_live(
    url="https://example.com",
    device="desktop",  # desktop | mobile
    categories=["performance", "accessibility", "best-practices", "seo"],
)
```

---

## Domain Analytics API

Domain technology detection and WHOIS data.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `domain_technologies` | `/domain_analytics/technologies/domain_technologies/live` | Tech stack detection |
| `domain_whois` | `/domain_analytics/whois/overview/live` | Domain registration data |

### Technologies Detected
- CMS (WordPress, Shopify, Wix)
- Analytics (Google Analytics, Hotjar)
- Marketing (HubSpot, Mailchimp)
- Hosting (AWS, Cloudflare)
- Frameworks (React, Vue, Angular)
- E-commerce (Magento, WooCommerce)

---

## Content Analysis API

Brand monitoring, sentiment analysis, and content intelligence.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `content_search` | `/content_analysis/search/live` | Search brand mentions |
| `content_sentiment` | `/content_analysis/sentiment_analysis/live` | Sentiment analysis |

### Parameters
```python
content_search(
    keyword="anthropic claude",
    location_name="United States",
    language_name="English",
    limit=100,
)
```

---

## Business Data API

Local business data and reviews.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `business_my_business_info` | `/business_data/google/my_business_info/live` | Google Business Profile data |
| `business_google_reviews` | `/business_data/google/reviews/task_post` | Google reviews |

---

## Merchant API

E-commerce product data from Google Shopping and Amazon.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `merchant_google_products` | `/merchant/google/products/task_post` | Google Shopping results |
| `merchant_amazon_products` | `/merchant/amazon/products/task_post` | Amazon product search |

---

## App Data API

Mobile app store data for Google Play and Apple App Store.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `app_google_play_search` | `/app_data/google/app_searches/task_post` | Google Play search |
| `app_store_search` | `/app_data/apple/app_searches/task_post` | App Store search |

---

## AI Optimization API

Monitor brand visibility in AI/LLM responses.

### Endpoints

| Function | Endpoint | Description |
|----------|----------|-------------|
| `ai_llm_mentions_search` | `/ai_optimization/llm_mentions/search/live` | Track LLM mentions |

---

## Common Parameters

### Location Codes (Examples)
| Location | Code | Name |
|----------|------|------|
| United States | 2840 | "United States" |
| United Kingdom | 2826 | "United Kingdom" |
| India | 2356 | "India" |
| Germany | 2276 | "Germany" |

Use `get_locations("serp/google")` to get full list.

### Language Codes (Examples)
| Language | Code | Name |
|----------|------|------|
| English | en | "English" |
| Spanish | es | "Spanish" |
| Hindi | hi | "Hindi" |
| German | de | "German" |

Use `get_languages("serp/google")` to get full list.

---

## Error Codes

| Code | Meaning |
|------|---------|
| 20000 | Success |
| 20100 | Task created (async) |
| 40000 | Invalid request |
| 40001 | Invalid field |
| 40100 | Authentication failed |
| 40200 | Insufficient credits |
| 40400 | Not found |
| 50000 | Internal error |

---

## Rate Limits

- Default: 2000 requests/minute total
- POST calls: max 100 tasks per request
- Check headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Pricing Notes

- Live methods cost more than Standard methods
- Additional parameters multiply base cost
- Check `cost` field in responses
- Monitor usage via `get_user_data()`
