---
name: google-trends
description: "DataForSEO Google Trends: search interest over time, trending topics, keyword trends"
---

# Google Trends Skill

Use this skill when the user asks about:
- Google Trends data or analysis
- Trending topics or searches
- Search trends over time
- Interest over time for keywords
- Trend analysis for keywords
- Comparing keyword popularity
- Seasonal search patterns
- Search interest fluctuations

## Function

### `google_trends()`

Get Google Trends data for one or more keywords. This function retrieves search interest data over time, allowing you to analyze trends, compare keywords, and identify seasonal patterns.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keywords` | `list[str]` | Required | List of keywords to analyze (up to 5 keywords for comparison) |
| `location_name` | `str` | `"United States"` | Target location for trends data |
| `language_name` | `str` | `"English"` | Language for the search |
| `time_range` | `str` | `"past_12_months"` | Time range for trend data |

**Time Range Options:**
- `"past_hour"` - Last 60 minutes
- `"past_4_hours"` - Last 4 hours
- `"past_day"` - Last 24 hours
- `"past_7_days"` - Last 7 days
- `"past_30_days"` - Last 30 days
- `"past_90_days"` - Last 90 days
- `"past_12_months"` - Last 12 months (default)
- `"past_4_years"` - Last 4 years
- `"past_5_years"` - Last 5 years

**Returns:** Dictionary containing trend data with interest values over time (0-100 scale where 100 is peak popularity).

**Output:** CSV files are exported to `~/dataforseo_outputs/`

## Example Usage

```python
import sys
sys.path.insert(0, "/Users/oli/Mac/Apps/claude-cowork-plugins-for-marketing/plugins/dataforseo(nikhil-bhansali)/scripts")

from dataforseo_client import google_trends, extract_results, to_csv

# Single keyword trend analysis
response = google_trends(
    keywords=["artificial intelligence"],
    location_name="United States",
    language_name="English",
    time_range="past_12_months"
)

# Extract and export results
results = extract_results(response)
csv_path = to_csv(results, "ai_trends")
print(f"Results saved to: {csv_path}")
```

## Comparing Multiple Keywords

To compare the relative search interest between multiple keywords, pass them as a list. Google Trends normalizes the data so you can see how keywords perform relative to each other.

```python
import sys
sys.path.insert(0, "/Users/oli/Mac/Apps/claude-cowork-plugins-for-marketing/plugins/dataforseo(nikhil-bhansali)/scripts")

from dataforseo_client import google_trends, extract_results, to_csv

# Compare up to 5 keywords
response = google_trends(
    keywords=["python", "javascript", "rust", "golang"],
    location_name="United States",
    language_name="English",
    time_range="past_4_years"
)

results = extract_results(response)
csv_path = to_csv(results, "programming_language_trends")
print(f"Comparison saved to: {csv_path}")
```

## Seasonal Trend Analysis

Identify seasonal patterns by using longer time ranges:

```python
import sys
sys.path.insert(0, "/Users/oli/Mac/Apps/claude-cowork-plugins-for-marketing/plugins/dataforseo(nikhil-bhansali)/scripts")

from dataforseo_client import google_trends, extract_results, to_csv

# Analyze seasonal trends over 4 years
response = google_trends(
    keywords=["christmas gifts", "summer vacation", "tax software"],
    location_name="United States",
    language_name="English",
    time_range="past_4_years"
)

results = extract_results(response)
csv_path = to_csv(results, "seasonal_trends")
print(f"Seasonal analysis saved to: {csv_path}")
```

## Regional Analysis

Get trends for specific countries or regions:

```python
import sys
sys.path.insert(0, "/Users/oli/Mac/Apps/claude-cowork-plugins-for-marketing/plugins/dataforseo(nikhil-bhansali)/scripts")

from dataforseo_client import google_trends, extract_results, to_csv

# UK market trends
response = google_trends(
    keywords=["electric vehicles"],
    location_name="United Kingdom",
    language_name="English",
    time_range="past_12_months"
)

results = extract_results(response)
csv_path = to_csv(results, "uk_ev_trends")
print(f"UK trends saved to: {csv_path}")
```

## Understanding the Output

The CSV output includes:
- **Date/Time**: Timestamp for each data point
- **Interest Values**: Search interest on a 0-100 scale
  - 100 = Peak popularity for the term
  - 50 = Half as popular as peak
  - 0 = Not enough data
- **Keyword**: The keyword associated with each data point (when comparing multiple keywords)

When comparing keywords, all values are relative to the highest point across all keywords in the comparison, making it easy to see which terms are most popular and how they trend over time.
