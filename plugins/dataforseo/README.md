# DataForSEO Skill for Claude Code

A Claude Code skill that provides complete DataForSEO API integration for SEO data and analysis.

## Features

- **Keyword Research**: Search volume, CPC, competition, keyword ideas
- **SERP Analysis**: Google, Bing, YouTube organic results
- **Backlink Analysis**: Profile overview, referring domains, anchors
- **Competitor Analysis**: Domain intersection, keyword gap, competing domains
- **Technical SEO**: Page audits, Lighthouse scores, technology detection
- **Content Analysis**: Brand mentions, sentiment analysis
- **Trends**: Google Trends data
- **And more**: Business data, merchant data, app store data, AI optimization

## Installation

### Option 1: Using skills.sh (Recommended)


### Option 2: Manual Install

1. Copy the `dataforseo` folder to `~/.agents/skills/`:
   ```bash
   cp -r dataforseo ~/.agents/skills/
   ```

2. Create symlink in Claude skills directory:
   ```bash
   ln -sf ../../.agents/skills/dataforseo ~/.claude/skills/dataforseo
   ```

3. Restart Claude Code

## Setup API Credentials

Before first use, configure your DataForSEO API credentials:

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.agents/skills/dataforseo/scripts'))
from dataforseo_client import save_credentials, verify_credentials

# Get your credentials from https://app.dataforseo.com/
login = "your_email@example.com"
password = "your_api_password"

if verify_credentials(login, password):
    save_credentials(login, password)
    print("Credentials saved!")
```

Credentials are stored securely at `~/.dataforseo_config.json` with restricted permissions.

## Quick Start

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.agents/skills/dataforseo/scripts'))
from dataforseo_client import keywords_search_volume, extract_results, to_csv

# Get search volume for keywords
response = keywords_search_volume(
    keywords=["seo tools", "keyword research"],
    location_name="United States"
)
results = extract_results(response)
csv_path = to_csv(results, "keyword_volumes")
print(f"Results saved to: {csv_path}")
```

## API Function Reference

| Use Case | Function |
|----------|----------|
| Search volume, CPC, competition | `keywords_search_volume()` |
| Keyword ideas/suggestions | `labs_keyword_ideas()` |
| Keywords a site ranks for | `labs_ranked_keywords()` |
| SERP results for keyword | `serp_google_organic()` |
| Local/Maps rankings | `serp_google_maps()` |
| YouTube rankings | `serp_youtube()` |
| Backlink profile | `backlinks_summary()` |
| List of backlinks | `backlinks_list()` |
| Referring domains | `backlinks_referring_domains()` |
| Domain authority/rank | `backlinks_bulk_ranks()` |
| Competing domains | `labs_competitors_domain()` |
| Keyword gap analysis | `labs_domain_intersection()` |
| Link gap analysis | `backlinks_domain_intersection()` |
| Technical page audit | `onpage_instant_pages()` |
| Lighthouse scores | `lighthouse_live()` |
| Technology stack | `domain_technologies()` |
| Brand mentions | `content_search()` |
| Google Trends | `google_trends()` |

## Output

All results export to CSV at `~/dataforseo_outputs/`. Files are auto-named with timestamps.

## Documentation

- [API Reference](dataforseo/references/api_reference.md) - Complete endpoint documentation
- [Use Cases](dataforseo/references/use_cases.md) - Ready-to-use code recipes

## Requirements

- Python 3.9+
- [DataForSEO API account](https://dataforseo.com/) (free trial available)
- Claude Code CLI

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
