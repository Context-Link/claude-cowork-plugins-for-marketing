---
name: technical-seo
description: "DataForSEO technical SEO: page audits, Lighthouse scores, site crawls, technology detection"
---

# Technical SEO Skill

Use this skill for technical SEO analysis including page audits, Lighthouse performance testing, site crawls, Core Web Vitals, site speed analysis, and technology stack detection.

## Triggers

- Technical SEO audit
- Page audit / page analysis
- Lighthouse audit / Lighthouse scores
- Site speed / page speed analysis
- Core Web Vitals
- Technology stack detection
- Site crawl / crawl analysis
- Duplicate meta tags / title tags
- Internal link analysis
- WHOIS lookup

## Available Functions

### Instant Page Analysis (No Crawl)

#### `onpage_instant_pages(url)`
Instant page analysis without requiring a full site crawl. Returns on-page SEO data for a single URL.

**Parameters:**
- `url` (str): Full URL to analyze (e.g., "https://example.com/page")

**Returns:** Page metrics including title, meta description, headers, word count, response time, status codes, and on-page issues.

---

### Lighthouse Audit

#### `lighthouse_live(url, device, categories)`
Run a Google Lighthouse audit to get performance, accessibility, best practices, and SEO scores.

**Parameters:**
- `url` (str): Full URL to audit
- `device` (str): "desktop" or "mobile" (default: "desktop")
- `categories` (list): Lighthouse categories to test (default: ["performance", "accessibility", "best-practices", "seo"])

**Returns:** Lighthouse scores, Core Web Vitals (LCP, FID, CLS), performance metrics, and detailed audit results.

---

### Site Crawl Functions

#### `onpage_task_post(target, max_crawl_pages, load_resources, enable_javascript)`
Start a full site crawl task. Returns a task_id to use with other OnPage functions.

**Parameters:**
- `target` (str): Domain to crawl (e.g., "example.com")
- `max_crawl_pages` (int): Maximum pages to crawl (default: 100)
- `load_resources` (bool): Load page resources (default: True)
- `enable_javascript` (bool): Enable JavaScript rendering (default: False)

**Returns:** Task ID for retrieving crawl results.

#### `onpage_summary(task_id)`
Get summary of a completed crawl task.

**Parameters:**
- `task_id` (str): Task ID from onpage_task_post

**Returns:** Crawl statistics including pages crawled, issues found, broken links, duplicate content counts.

#### `onpage_pages(task_id, limit)`
Get list of crawled pages with their issues and metrics.

**Parameters:**
- `task_id` (str): Task ID from onpage_task_post
- `limit` (int): Maximum pages to return (default: 100)

**Returns:** List of pages with status codes, load times, word counts, and SEO issues.

#### `onpage_duplicate_tags(task_id)`
Find pages with duplicate title tags or meta descriptions.

**Parameters:**
- `task_id` (str): Task ID from onpage_task_post

**Returns:** Groups of pages sharing the same title or meta description.

#### `onpage_links(task_id, limit)`
Analyze internal and external links from the crawl.

**Parameters:**
- `task_id` (str): Task ID from onpage_task_post
- `limit` (int): Maximum links to return (default: 100)

**Returns:** Link analysis including internal/external links, anchor text, dofollow/nofollow status.

---

### Domain Analysis

#### `domain_technologies(target)`
Detect the technology stack used by a website (CMS, frameworks, analytics, CDN, etc.).

**Parameters:**
- `target` (str): Domain to analyze (e.g., "example.com")

**Returns:** List of detected technologies categorized by type (CMS, JavaScript frameworks, analytics tools, hosting, etc.).

#### `domain_whois(target)`
Get WHOIS registration data for a domain.

**Parameters:**
- `target` (str): Domain to lookup (e.g., "example.com")

**Returns:** WHOIS data including registrar, creation date, expiration date, nameservers, and registrant info (if available).

---

## Example Usage

```python
import sys
sys.path.insert(0, '../../scripts')
from dataforseo_client import (
    onpage_instant_pages,
    lighthouse_live,
    onpage_task_post,
    onpage_summary,
    onpage_pages,
    onpage_duplicate_tags,
    onpage_links,
    domain_technologies,
    domain_whois,
    extract_results,
    to_csv
)

# --------------------------------------------------
# Example 1: Instant Page Analysis
# --------------------------------------------------
response = onpage_instant_pages("https://example.com/important-page")
results = extract_results(response)
csv_path = to_csv(results, "page_audit", "~/dataforseo_outputs")
print(f"Page audit saved to: {csv_path}")

# --------------------------------------------------
# Example 2: Lighthouse Audit (Desktop)
# --------------------------------------------------
response = lighthouse_live(
    url="https://example.com",
    device="desktop",
    categories=["performance", "accessibility", "best-practices", "seo"]
)
results = extract_results(response)
csv_path = to_csv(results, "lighthouse_desktop", "~/dataforseo_outputs")
print(f"Lighthouse results saved to: {csv_path}")

# --------------------------------------------------
# Example 3: Lighthouse Audit (Mobile)
# --------------------------------------------------
response = lighthouse_live(
    url="https://example.com",
    device="mobile",
    categories=["performance", "seo"]
)
results = extract_results(response)
csv_path = to_csv(results, "lighthouse_mobile", "~/dataforseo_outputs")
print(f"Mobile Lighthouse results saved to: {csv_path}")

# --------------------------------------------------
# Example 4: Full Site Crawl Workflow
# --------------------------------------------------
# Step 1: Start the crawl
crawl_response = onpage_task_post(
    target="example.com",
    max_crawl_pages=500,
    load_resources=True,
    enable_javascript=False
)
task_id = crawl_response["tasks"][0]["id"]
print(f"Crawl started with task_id: {task_id}")

# Step 2: Wait for crawl to complete, then get summary
# (Note: Crawl may take several minutes depending on site size)
summary_response = onpage_summary(task_id)
summary = extract_results(summary_response)
csv_path = to_csv(summary, "crawl_summary", "~/dataforseo_outputs")
print(f"Crawl summary saved to: {csv_path}")

# Step 3: Get pages with issues
pages_response = onpage_pages(task_id, limit=500)
pages = extract_results(pages_response)
csv_path = to_csv(pages, "crawled_pages", "~/dataforseo_outputs")
print(f"Crawled pages saved to: {csv_path}")

# Step 4: Find duplicate title/meta tags
duplicates_response = onpage_duplicate_tags(task_id)
duplicates = extract_results(duplicates_response)
csv_path = to_csv(duplicates, "duplicate_tags", "~/dataforseo_outputs")
print(f"Duplicate tags saved to: {csv_path}")

# Step 5: Analyze links
links_response = onpage_links(task_id, limit=500)
links = extract_results(links_response)
csv_path = to_csv(links, "site_links", "~/dataforseo_outputs")
print(f"Link analysis saved to: {csv_path}")

# --------------------------------------------------
# Example 5: Technology Stack Detection
# --------------------------------------------------
response = domain_technologies("example.com")
results = extract_results(response)
csv_path = to_csv(results, "tech_stack", "~/dataforseo_outputs")
print(f"Technology stack saved to: {csv_path}")

# --------------------------------------------------
# Example 6: WHOIS Lookup
# --------------------------------------------------
response = domain_whois("example.com")
results = extract_results(response)
csv_path = to_csv(results, "whois_data", "~/dataforseo_outputs")
print(f"WHOIS data saved to: {csv_path}")
```

## Output

All results are exported as CSV files to `~/dataforseo_outputs/` with timestamps appended to filenames.

## Common Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `url` | Full URL including protocol | "https://example.com/page" |
| `target` | Domain name without protocol | "example.com" |
| `device` | Device type for Lighthouse | "desktop", "mobile" |
| `categories` | Lighthouse audit categories | ["performance", "accessibility", "best-practices", "seo"] |
| `max_crawl_pages` | Maximum pages to crawl | Integer (default: 100) |
| `limit` | Maximum results to return | Integer (default: 100) |

## Notes

- **Instant vs Crawl**: Use `onpage_instant_pages()` for quick single-page analysis. Use the crawl workflow (`onpage_task_post` -> `onpage_summary` -> `onpage_pages`) for comprehensive site-wide audits.
- **Crawl Time**: Full site crawls may take several minutes to complete depending on site size and complexity.
- **Lighthouse Categories**: You can run partial Lighthouse audits by specifying only the categories you need.
- **Task IDs**: Store the task_id returned from `onpage_task_post()` to retrieve results later with the other OnPage functions.
