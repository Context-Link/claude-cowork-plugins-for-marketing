#!/usr/bin/env python3
"""
DataForSEO API Client - Universal client for all DataForSEO APIs
Handles authentication, requests, and CSV export
"""

import json
import base64
import csv
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime
from typing import Optional, Any

# Config file location
CONFIG_PATH = Path.home() / ".dataforseo_config.json"
API_BASE = "https://api.dataforseo.com/v3"


def load_credentials() -> tuple[str, str]:
    """Load credentials from config file."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Credentials not found. Run: python dataforseo_client.py --setup"
        )
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    return config["login"], config["password"]


def save_credentials(login: str, password: str) -> None:
    """Save credentials to config file."""
    with open(CONFIG_PATH, "w") as f:
        json.dump({"login": login, "password": password}, f)
    os.chmod(CONFIG_PATH, 0o600)  # Secure permissions
    print(f"Credentials saved to {CONFIG_PATH}")


def get_auth_header(login: str, password: str) -> str:
    """Generate Base64 encoded auth header."""
    credentials = f"{login}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def api_request(
    endpoint: str,
    method: str = "GET",
    data: Optional[list[dict]] = None,
    login: Optional[str] = None,
    password: Optional[str] = None,
) -> dict:
    """Make API request to DataForSEO."""
    if login is None or password is None:
        login, password = load_credentials()

    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": get_auth_header(login, password),
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else str(e)
        return {"error": True, "status_code": e.code, "message": error_body}
    except URLError as e:
        return {"error": True, "message": str(e.reason)}


def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """Flatten nested dictionary for CSV export."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        elif isinstance(v, list):
            if v and isinstance(v[0], dict):
                # For list of dicts, just count them
                items.append((new_key + "_count", len(v)))
            else:
                items.append((new_key, "; ".join(str(x) for x in v)))
        else:
            items.append((new_key, v))
    return dict(items)


def extract_results(response: dict) -> list[dict]:
    """Extract result items from API response."""
    if response.get("error"):
        return [{"error": response.get("message", "Unknown error")}]

    results = []
    tasks = response.get("tasks", [])
    for task in tasks:
        task_results = task.get("result", [])
        if task_results:
            for result in task_results:
                if isinstance(result, dict):
                    # Handle nested items (common in SERP, backlinks, etc.)
                    items = result.get("items", [])
                    if items:
                        results.extend(items)
                    else:
                        results.append(result)
        else:
            # No results, capture task metadata
            results.append({
                "task_id": task.get("id"),
                "status_code": task.get("status_code"),
                "status_message": task.get("status_message"),
            })
    return results if results else [{"message": "No results found"}]


def to_csv(
    data: list[dict],
    filename: str,
    output_dir: str = None
) -> str:
    """Export data to CSV file."""
    if output_dir is None:
        output_dir = str(Path.home() / "dataforseo_outputs")
    if not data:
        data = [{"message": "No data to export"}]

    # Flatten all records
    flat_data = [flatten_dict(d) if isinstance(d, dict) else {"value": d} for d in data]

    # Collect all unique keys
    all_keys = set()
    for record in flat_data:
        all_keys.update(record.keys())
    fieldnames = sorted(all_keys)

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp if not provided
    if not filename.endswith(".csv"):
        filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    filepath = Path(output_dir) / filename

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(flat_data)

    return str(filepath)


def verify_credentials(login: str, password: str) -> bool:
    """Verify credentials by calling user_data endpoint."""
    response = api_request("appendix/user_data", login=login, password=password)
    return response.get("status_code") == 20000


# =============================================================================
# SERP API Functions
# =============================================================================

def serp_google_organic(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
    device: str = "desktop",
    depth: int = 100,
) -> dict:
    """Get Google organic SERP results."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
        "device": device,
        "depth": depth,
    }]
    return api_request("serp/google/organic/live/advanced", "POST", data)


def serp_google_maps(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get Google Maps results."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("serp/google/maps/live/advanced", "POST", data)


def serp_bing_organic(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get Bing organic SERP results."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("serp/bing/organic/live/advanced", "POST", data)


def serp_youtube(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get YouTube search results."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("serp/youtube/organic/live/advanced", "POST", data)


# =============================================================================
# Keywords Data API Functions
# =============================================================================

def keywords_search_volume(
    keywords: list[str],
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get search volume for keywords (Google Ads)."""
    data = [{
        "keywords": keywords,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("keywords_data/google_ads/search_volume/live", "POST", data)


def keywords_for_site(
    target: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get keywords for a website."""
    data = [{
        "target": target,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("keywords_data/google_ads/keywords_for_site/live", "POST", data)


def keywords_for_keywords(
    keywords: list[str],
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get related keywords."""
    data = [{
        "keywords": keywords,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("keywords_data/google_ads/keywords_for_keywords/live", "POST", data)


def google_trends(
    keywords: list[str],
    location_name: str = "United States",
    language_name: str = "English",
    time_range: str = "past_12_months",
) -> dict:
    """Get Google Trends data."""
    data = [{
        "keywords": keywords,
        "location_name": location_name,
        "language_name": language_name,
        "time_range": time_range,
    }]
    return api_request("keywords_data/google_trends/explore/live", "POST", data)


# =============================================================================
# DataForSEO Labs API Functions
# =============================================================================

def labs_ranked_keywords(
    target: str,
    location_name: str = "United States",
    language_name: str = "English",
    limit: int = 100,
) -> dict:
    """Get ranked keywords for a domain."""
    data = [{
        "target": target,
        "location_name": location_name,
        "language_name": language_name,
        "limit": limit,
    }]
    return api_request("dataforseo_labs/google/ranked_keywords/live", "POST", data)


def labs_serp_competitors(
    keywords: list[str],
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get SERP competitors for keywords."""
    data = [{
        "keywords": keywords,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("dataforseo_labs/google/serp_competitors/live", "POST", data)


def labs_domain_intersection(
    targets: list[str],
    location_name: str = "United States",
    language_name: str = "English",
    limit: int = 100,
) -> dict:
    """Find common keywords between domains."""
    # targets should have format {"1": "domain1.com", "2": "domain2.com"}
    target_dict = {str(i+1): t for i, t in enumerate(targets)}
    data = [{
        "targets": target_dict,
        "location_name": location_name,
        "language_name": language_name,
        "limit": limit,
    }]
    return api_request("dataforseo_labs/google/domain_intersection/live", "POST", data)


def labs_competitors_domain(
    target: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get competing domains."""
    data = [{
        "target": target,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("dataforseo_labs/google/competitors_domain/live", "POST", data)


def labs_keyword_ideas(
    keywords: list[str],
    location_name: str = "United States",
    language_name: str = "English",
    limit: int = 100,
) -> dict:
    """Get keyword ideas."""
    data = [{
        "keywords": keywords,
        "location_name": location_name,
        "language_name": language_name,
        "limit": limit,
    }]
    return api_request("dataforseo_labs/google/keyword_ideas/live", "POST", data)


def labs_related_keywords(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
    limit: int = 100,
) -> dict:
    """Get related keywords."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
        "limit": limit,
    }]
    return api_request("dataforseo_labs/google/related_keywords/live", "POST", data)


def labs_domain_rank_overview(
    target: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get domain rank overview."""
    data = [{
        "target": target,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("dataforseo_labs/google/domain_rank_overview/live", "POST", data)


# =============================================================================
# Backlinks API Functions
# =============================================================================

def backlinks_summary(target: str) -> dict:
    """Get backlink summary for a domain."""
    data = [{"target": target}]
    return api_request("backlinks/summary/live", "POST", data)


def backlinks_list(
    target: str,
    limit: int = 100,
    mode: str = "as_is",  # as_is, one_per_domain, one_per_anchor
) -> dict:
    """Get backlinks for a target."""
    data = [{
        "target": target,
        "limit": limit,
        "mode": mode,
    }]
    return api_request("backlinks/backlinks/live", "POST", data)


def backlinks_anchors(target: str, limit: int = 100) -> dict:
    """Get backlink anchors."""
    data = [{"target": target, "limit": limit}]
    return api_request("backlinks/anchors/live", "POST", data)


def backlinks_referring_domains(target: str, limit: int = 100) -> dict:
    """Get referring domains."""
    data = [{"target": target, "limit": limit}]
    return api_request("backlinks/referring_domains/live", "POST", data)


def backlinks_competitors(target: str, limit: int = 100) -> dict:
    """Get backlink competitors."""
    data = [{"target": target, "limit": limit}]
    return api_request("backlinks/competitors/live", "POST", data)


def backlinks_domain_intersection(targets: list[str], limit: int = 100) -> dict:
    """Find common backlinks between domains (link gap)."""
    target_dict = {str(i+1): t for i, t in enumerate(targets)}
    data = [{"targets": target_dict, "limit": limit}]
    return api_request("backlinks/domain_intersection/live", "POST", data)


def backlinks_history(target: str) -> dict:
    """Get backlink history."""
    data = [{"target": target}]
    return api_request("backlinks/history/live", "POST", data)


def backlinks_bulk_ranks(targets: list[str]) -> dict:
    """Get bulk domain ranks."""
    data = [{"targets": targets}]
    return api_request("backlinks/bulk_ranks/live", "POST", data)


# =============================================================================
# OnPage API Functions
# =============================================================================

def onpage_task_post(
    target: str,
    max_crawl_pages: int = 100,
    load_resources: bool = True,
    enable_javascript: bool = False,
) -> dict:
    """Start an OnPage crawl task."""
    data = [{
        "target": target,
        "max_crawl_pages": max_crawl_pages,
        "load_resources": load_resources,
        "enable_javascript": enable_javascript,
    }]
    return api_request("on_page/task_post", "POST", data)


def onpage_summary(task_id: str) -> dict:
    """Get OnPage task summary."""
    return api_request(f"on_page/summary/{task_id}")


def onpage_pages(task_id: str, limit: int = 100) -> dict:
    """Get crawled pages."""
    data = [{"id": task_id, "limit": limit}]
    return api_request("on_page/pages", "POST", data)


def onpage_resources(task_id: str, limit: int = 100) -> dict:
    """Get page resources."""
    data = [{"id": task_id, "limit": limit}]
    return api_request("on_page/resources", "POST", data)


def onpage_duplicate_tags(task_id: str) -> dict:
    """Get duplicate title/description tags."""
    data = [{"id": task_id}]
    return api_request("on_page/duplicate_tags", "POST", data)


def onpage_links(task_id: str, limit: int = 100) -> dict:
    """Get page links."""
    data = [{"id": task_id, "limit": limit}]
    return api_request("on_page/links", "POST", data)


def onpage_instant_pages(url: str) -> dict:
    """Get instant page analysis (no crawl needed)."""
    data = [{"url": url}]
    return api_request("on_page/instant_pages", "POST", data)


def lighthouse_live(
    url: str,
    device: str = "desktop",  # desktop or mobile
    categories: list[str] = None,
) -> dict:
    """Run Lighthouse audit."""
    if categories is None:
        categories = ["performance", "accessibility", "best-practices", "seo"]
    data = [{
        "url": url,
        "for_mobile": device == "mobile",
        "categories": categories,
    }]
    return api_request("on_page/lighthouse/live/json", "POST", data)


# =============================================================================
# Domain Analytics API Functions
# =============================================================================

def domain_technologies(target: str) -> dict:
    """Get technologies used by a domain."""
    data = [{"target": target}]
    return api_request("domain_analytics/technologies/domain_technologies/live", "POST", data)


def domain_whois(target: str) -> dict:
    """Get WHOIS data for a domain."""
    data = [{"target": target}]
    return api_request("domain_analytics/whois/overview/live", "POST", data)


# =============================================================================
# Content Analysis API Functions
# =============================================================================

def content_search(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
    limit: int = 100,
) -> dict:
    """Search content mentions."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
        "limit": limit,
    }]
    return api_request("content_analysis/search/live", "POST", data)


def content_sentiment(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get sentiment analysis."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("content_analysis/sentiment_analysis/live", "POST", data)


# =============================================================================
# Business Data API Functions
# =============================================================================

def business_google_reviews(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get Google Business reviews."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("business_data/google/reviews/task_post", "POST", data)


def business_my_business_info(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Get Google My Business info."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("business_data/google/my_business_info/live", "POST", data)


# =============================================================================
# Merchant API Functions
# =============================================================================

def merchant_google_products(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Search Google Shopping products."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("merchant/google/products/task_post", "POST", data)


def merchant_amazon_products(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Search Amazon products."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("merchant/amazon/products/task_post", "POST", data)


# =============================================================================
# App Data API Functions
# =============================================================================

def app_google_play_search(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Search Google Play apps."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("app_data/google/app_searches/task_post", "POST", data)


def app_store_search(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Search App Store apps."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("app_data/apple/app_searches/task_post", "POST", data)


# =============================================================================
# AI Optimization API Functions
# =============================================================================

def ai_llm_mentions_search(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
) -> dict:
    """Search LLM mentions."""
    data = [{
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
    }]
    return api_request("ai_optimization/llm_mentions/search/live", "POST", data)


# =============================================================================
# Utility Functions
# =============================================================================

def get_locations(api: str = "serp/google") -> dict:
    """Get available locations for an API."""
    return api_request(f"{api}/locations")


def get_languages(api: str = "serp/google") -> dict:
    """Get available languages for an API."""
    return api_request(f"{api}/languages")


def get_user_data() -> dict:
    """Get current user account data."""
    return api_request("appendix/user_data")


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        print("DataForSEO Credential Setup")
        print("-" * 40)
        login = input("Enter API Login (email): ").strip()
        password = input("Enter API Password: ").strip()

        print("\nVerifying credentials...")
        if verify_credentials(login, password):
            save_credentials(login, password)
            print("Credentials verified and saved!")
        else:
            print("Invalid credentials. Please check and try again.")
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Testing DataForSEO connection...")
        try:
            response = get_user_data()
            if response.get("status_code") == 20000:
                result = response["tasks"][0]["result"][0]
                print(f"Connected as: {result['login']}")
                print(f"  Timezone: {result['timezone']}")
            else:
                print(f"Error: {response.get('status_message', 'Unknown error')}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
    else:
        print("DataForSEO API Client")
        print("Usage:")
        print("  python dataforseo_client.py --setup  # Setup credentials")
        print("  python dataforseo_client.py --test   # Test connection")
        print("\nImport in Python:")
        print("  from dataforseo_client import serp_google_organic, to_csv")
