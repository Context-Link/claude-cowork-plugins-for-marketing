---
name: serp-analysis
description: "DataForSEO SERP analysis: Google, Bing, YouTube organic search results and rankings"
---

# SERP Analysis Skill

Analyze search engine results pages (SERPs) across Google, Bing, and YouTube to understand rankings, competition, and search landscape.

## Triggers

Use this skill when the user asks about:
- SERP analysis or search results analysis
- Google search results or Google rankings
- Bing search results or Bing rankings
- YouTube search results or video rankings
- Organic search results for keywords
- Local/Maps search results
- Competitor rankings for specific keywords
- Search engine position tracking

## Functions

### serp_google_organic()

Get Google organic SERP results for a keyword.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| keyword | str | required | Search query to analyze |
| location_name | str | "United States" | Target location for search |
| language_name | str | "English" | Language for results |
| device | str | "desktop" | Device type: "desktop" or "mobile" |
| depth | int | 100 | Number of results to retrieve (max 700) |

**Returns:** Full SERP data including organic results, featured snippets, people also ask, knowledge panels, and more.

---

### serp_google_maps()

Get Google Maps/Local pack results for a keyword.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| keyword | str | required | Local search query (e.g., "pizza near me") |
| location_name | str | "United States" | Target location for search |
| language_name | str | "English" | Language for results |

**Returns:** Local business listings with ratings, reviews, addresses, and map positions.

---

### serp_bing_organic()

Get Bing organic SERP results for a keyword.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| keyword | str | required | Search query to analyze |
| location_name | str | "United States" | Target location for search |
| language_name | str | "English" | Language for results |

**Returns:** Bing organic search results with rankings, URLs, titles, and descriptions.

---

### serp_youtube()

Get YouTube search results for a keyword.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| keyword | str | required | Video search query |
| location_name | str | "United States" | Target location for search |
| language_name | str | "English" | Language for results |

**Returns:** YouTube video results with titles, channels, views, duration, and rankings.

---

## Example Usage

```python
import sys
sys.path.insert(0, "../../scripts")
from dataforseo_client import (
    serp_google_organic,
    serp_google_maps,
    serp_bing_organic,
    serp_youtube,
    extract_results,
    to_csv
)

# Example 1: Analyze Google organic results for a keyword
response = serp_google_organic(
    keyword="best project management software",
    location_name="United States",
    language_name="English",
    device="desktop",
    depth=100
)
results = extract_results(response)
csv_path = to_csv(results, "google_serp_project_management")
print(f"Google SERP results saved to: {csv_path}")

# Example 2: Get local business results from Google Maps
response = serp_google_maps(
    keyword="italian restaurants downtown chicago",
    location_name="Chicago,Illinois,United States",
    language_name="English"
)
results = extract_results(response)
csv_path = to_csv(results, "google_maps_italian_restaurants")
print(f"Google Maps results saved to: {csv_path}")

# Example 3: Analyze Bing search results
response = serp_bing_organic(
    keyword="cloud hosting providers",
    location_name="United States",
    language_name="English"
)
results = extract_results(response)
csv_path = to_csv(results, "bing_serp_cloud_hosting")
print(f"Bing SERP results saved to: {csv_path}")

# Example 4: Get YouTube video rankings
response = serp_youtube(
    keyword="python programming tutorial",
    location_name="United States",
    language_name="English"
)
results = extract_results(response)
csv_path = to_csv(results, "youtube_python_tutorials")
print(f"YouTube results saved to: {csv_path}")

# Example 5: Mobile vs Desktop comparison
desktop_response = serp_google_organic(
    keyword="buy running shoes online",
    device="desktop",
    depth=50
)
mobile_response = serp_google_organic(
    keyword="buy running shoes online",
    device="mobile",
    depth=50
)

desktop_results = extract_results(desktop_response)
mobile_results = extract_results(mobile_response)

to_csv(desktop_results, "serp_running_shoes_desktop")
to_csv(mobile_results, "serp_running_shoes_mobile")
print("Desktop and mobile SERP comparison saved")
```

## Output

All results are exported as CSV files to `~/dataforseo_outputs/` with automatic timestamping.

**Google Organic SERP output includes:**
- rank_group, rank_absolute (position data)
- type (organic, featured_snippet, people_also_ask, etc.)
- title, description, url
- domain, breadcrumb
- featured_snippet content (when applicable)
- links, images (counts)

**Google Maps output includes:**
- title, address, phone
- rating, reviews_count
- category, place_id
- latitude, longitude

**YouTube output includes:**
- title, channel_id, video_id
- views, duration
- description, publish_date
- thumbnail_url

## Common Locations

- "United States"
- "United Kingdom"
- "Canada"
- "Australia"
- "New York,New York,United States" (city-level)
- "Los Angeles,California,United States"
- "London,England,United Kingdom"

## Notes

- Google organic depth can be set from 10 to 700 results
- Mobile vs desktop results often differ significantly - analyze both for comprehensive SEO
- Local intent keywords work best with Google Maps function
- YouTube results include both video and channel results
