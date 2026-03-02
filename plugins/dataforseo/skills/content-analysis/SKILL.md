---
name: content-analysis
description: "DataForSEO content analysis: brand mentions, sentiment analysis, content monitoring"
---

Use this skill when the user wants to:
- Find brand mentions across the web
- Analyze sentiment for a keyword or brand
- Monitor content and online mentions
- Track brand reputation
- Search for online mentions of a company, product, or topic

## Functions

### `content_search()`
Search for content mentions of a keyword or brand across the web.

**Parameters:**
- `keyword` (str, required): The keyword or brand name to search for
- `location_name` (str, optional): Target location. Default: "United States"
- `language_name` (str, optional): Target language. Default: "English"
- `limit` (int, optional): Maximum number of results to return. Default: 100

**Returns:** Dictionary containing content mentions with URLs, titles, snippets, and metadata.

### `content_sentiment()`
Get sentiment analysis for mentions of a keyword or brand.

**Parameters:**
- `keyword` (str, required): The keyword or brand name to analyze
- `location_name` (str, optional): Target location. Default: "United States"
- `language_name` (str, optional): Target language. Default: "English"

**Returns:** Dictionary containing sentiment breakdown (positive, negative, neutral) and related metrics.

## Output

Results are exported as CSV files to `~/dataforseo_outputs/`

## Example Usage

```python
import sys
sys.path.insert(0, '../../scripts')
from dataforseo_client import content_search, content_sentiment, extract_results, to_csv

# Search for brand mentions
keyword = "Tesla"
location = "United States"
language = "English"

# Get content mentions
response = content_search(
    keyword=keyword,
    location_name=location,
    language_name=language,
    limit=50
)
results = extract_results(response)
csv_path = to_csv(results, f"content_mentions_{keyword}")
print(f"Content mentions saved to: {csv_path}")

# Get sentiment analysis
sentiment_response = content_sentiment(
    keyword=keyword,
    location_name=location,
    language_name=language
)
sentiment_results = extract_results(sentiment_response)
sentiment_csv = to_csv(sentiment_results, f"sentiment_{keyword}")
print(f"Sentiment analysis saved to: {sentiment_csv}")
```

## Example: Monitor Multiple Brands

```python
import sys
sys.path.insert(0, '../../scripts')
from dataforseo_client import content_search, content_sentiment, extract_results, to_csv

brands = ["Apple", "Microsoft", "Google"]
location = "United States"
language = "English"

for brand in brands:
    # Get mentions
    mentions = content_search(
        keyword=brand,
        location_name=location,
        language_name=language,
        limit=100
    )
    mentions_data = extract_results(mentions)
    to_csv(mentions_data, f"mentions_{brand}")

    # Get sentiment
    sentiment = content_sentiment(
        keyword=brand,
        location_name=location,
        language_name=language
    )
    sentiment_data = extract_results(sentiment)
    to_csv(sentiment_data, f"sentiment_{brand}")

    print(f"Completed analysis for: {brand}")
```
