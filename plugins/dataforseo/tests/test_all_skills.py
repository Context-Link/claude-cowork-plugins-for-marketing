#!/usr/bin/env python3
"""
Comprehensive tests for all DataForSEO skills.
Tests against the real API using context-link.ai as the target domain.

Usage:
    python test_all_skills.py

Requires DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD in .env file.
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Load environment variables from .env file
env_file = Path(__file__).parent.parent.parent.parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

# Import the client
from dataforseo_client import (
    # Utility
    verify_credentials, get_user_data, extract_results, save_credentials,
    # Keyword Research
    keywords_search_volume, keywords_for_site, labs_keyword_ideas,
    labs_related_keywords, labs_ranked_keywords,
    # SERP Analysis
    serp_google_organic, serp_google_maps, serp_bing_organic, serp_youtube,
    # Backlink Analysis
    backlinks_summary, backlinks_list, backlinks_referring_domains, backlinks_bulk_ranks,
    # Competitor Analysis
    labs_competitors_domain, labs_domain_intersection, labs_serp_competitors,
    # Technical SEO
    onpage_instant_pages, lighthouse_live, domain_technologies,
    # Content Analysis
    content_search,
    # Google Trends
    google_trends,
)

# Test configuration
TEST_DOMAIN = "context-link.ai"
TEST_URL = "https://context-link.ai"
TEST_KEYWORDS = ["ai knowledge base", "semantic search", "llm context"]
COMPETITOR_DOMAIN = "notion.so"


def get_credentials():
    """Get credentials from environment variables."""
    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        raise ValueError(
            "Missing credentials. Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD in .env"
        )
    return login, password


def print_result(name, response, show_sample=True):
    """Print test result summary."""
    status_code = response.get("status_code", response.get("tasks", [{}])[0].get("status_code"))
    status_msg = response.get("status_message", "")
    cost = response.get("cost", 0)

    if status_code == 20000:
        results = extract_results(response)
        count = len(results) if results else 0
        print(f"  [PASS] {name}: {count} results (cost: ${cost:.4f})")
        if show_sample and results and count > 0:
            sample = results[0]
            # Show first few keys
            keys = list(sample.keys())[:5]
            print(f"         Sample keys: {keys}")
        return True
    else:
        print(f"  [FAIL] {name}: {status_code} - {status_msg}")
        return False


def test_setup():
    """Test 1: Setup & Credentials"""
    print("\n" + "="*60)
    print("TEST 1: Setup & Credentials Verification")
    print("="*60)

    login, password = get_credentials()
    print(f"  Login: {login[:3]}...{login[-10:]}")

    # Test credential verification
    is_valid = verify_credentials(login, password)
    if is_valid:
        print("  [PASS] Credentials verified successfully")
        # Save credentials for subsequent tests that don't pass them explicitly
        save_credentials(login, password)
        print("  [INFO] Credentials saved to config file")
    else:
        print("  [FAIL] Invalid credentials")
        return False

    # Get user data
    response = get_user_data()
    if response.get("status_code") == 20000:
        result = response["tasks"][0]["result"][0]
        print(f"  [PASS] User data retrieved")
        print(f"         Balance: ${result.get('money', {}).get('balance', 'N/A')}")
        return True
    else:
        print(f"  [FAIL] Could not get user data")
        return False


def test_keyword_research():
    """Test 2: Keyword Research Skill"""
    print("\n" + "="*60)
    print("TEST 2: Keyword Research Skill")
    print("="*60)

    login, password = get_credentials()
    results = []

    # Test search volume
    response = keywords_search_volume(
        keywords=TEST_KEYWORDS,
        location_name="United States",
        language_name="English",
    )
    results.append(print_result("keywords_search_volume", response))

    # Test keywords for site
    response = keywords_for_site(
        target=TEST_DOMAIN,
        location_name="United States",
    )
    results.append(print_result("keywords_for_site", response))

    # Test keyword ideas
    response = labs_keyword_ideas(
        keywords=["ai context"],
        location_name="United States",
        limit=10,
    )
    results.append(print_result("labs_keyword_ideas", response))

    # Test related keywords
    response = labs_related_keywords(
        keyword="knowledge management",
        location_name="United States",
        limit=10,
    )
    results.append(print_result("labs_related_keywords", response))

    # Test ranked keywords
    response = labs_ranked_keywords(
        target=TEST_DOMAIN,
        location_name="United States",
        limit=10,
    )
    results.append(print_result("labs_ranked_keywords", response))

    return all(results)


def test_serp_analysis():
    """Test 3: SERP Analysis Skill"""
    print("\n" + "="*60)
    print("TEST 3: SERP Analysis Skill")
    print("="*60)

    results = []

    # Test Google organic
    response = serp_google_organic(
        keyword="ai knowledge base",
        location_name="United States",
        depth=10,
    )
    results.append(print_result("serp_google_organic", response))

    # Test Google Maps
    response = serp_google_maps(
        keyword="software company san francisco",
        location_name="San Francisco,California,United States",
    )
    results.append(print_result("serp_google_maps", response))

    # Test Bing organic
    response = serp_bing_organic(
        keyword="semantic search tool",
        location_name="United States",
    )
    results.append(print_result("serp_bing_organic", response))

    # Test YouTube
    response = serp_youtube(
        keyword="ai assistant tutorial",
        location_name="United States",
    )
    results.append(print_result("serp_youtube", response))

    return all(results)


def test_backlink_analysis():
    """Test 4: Backlink Analysis Skill"""
    print("\n" + "="*60)
    print("TEST 4: Backlink Analysis Skill")
    print("="*60)

    results = []

    # Test backlinks summary
    response = backlinks_summary(target=TEST_DOMAIN)
    results.append(print_result("backlinks_summary", response))

    # Test backlinks list
    response = backlinks_list(
        target=TEST_DOMAIN,
        limit=10,
    )
    results.append(print_result("backlinks_list", response))

    # Test referring domains
    response = backlinks_referring_domains(
        target=TEST_DOMAIN,
        limit=10,
    )
    results.append(print_result("backlinks_referring_domains", response))

    # Test bulk ranks
    response = backlinks_bulk_ranks(
        targets=[TEST_DOMAIN, COMPETITOR_DOMAIN],
    )
    results.append(print_result("backlinks_bulk_ranks", response))

    return all(results)


def test_competitor_analysis():
    """Test 5: Competitor Analysis Skill"""
    print("\n" + "="*60)
    print("TEST 5: Competitor Analysis Skill")
    print("="*60)

    results = []

    # Test competitors domain
    response = labs_competitors_domain(
        target=TEST_DOMAIN,
        location_name="United States",
    )
    results.append(print_result("labs_competitors_domain", response))

    # Test domain intersection (keyword gap)
    response = labs_domain_intersection(
        targets=[TEST_DOMAIN, COMPETITOR_DOMAIN],
        location_name="United States",
        limit=10,
    )
    results.append(print_result("labs_domain_intersection", response))

    # Test SERP competitors
    response = labs_serp_competitors(
        keywords=["knowledge management tool"],
        location_name="United States",
    )
    results.append(print_result("labs_serp_competitors", response))

    return all(results)


def test_technical_seo():
    """Test 6: Technical SEO Skill"""
    print("\n" + "="*60)
    print("TEST 6: Technical SEO Skill")
    print("="*60)

    results = []

    # Test instant page analysis
    response = onpage_instant_pages(url=TEST_URL)
    results.append(print_result("onpage_instant_pages", response))

    # Test Lighthouse audit
    response = lighthouse_live(
        url=TEST_URL,
        device="desktop",
        categories=["performance", "seo"],
    )
    results.append(print_result("lighthouse_live", response))

    # Test domain technologies
    response = domain_technologies(target=TEST_DOMAIN)
    results.append(print_result("domain_technologies", response))

    return all(results)


def test_content_analysis():
    """Test 7: Content Analysis Skill"""
    print("\n" + "="*60)
    print("TEST 7: Content Analysis Skill")
    print("="*60)

    results = []

    # Test content search (brand mentions)
    response = content_search(
        keyword="context link ai",
        location_name="United States",
        limit=10,
    )
    results.append(print_result("content_search", response))

    return all(results)


def test_google_trends():
    """Test 8: Google Trends Skill"""
    print("\n" + "="*60)
    print("TEST 8: Google Trends Skill")
    print("="*60)

    results = []

    # Test Google Trends
    response = google_trends(
        keywords=["ai assistant", "chatgpt", "claude ai"],
        location_name="United States",
        time_range="past_12_months",
    )
    results.append(print_result("google_trends", response))

    return all(results)


def main():
    """Run all tests."""
    print("\n" + "#"*60)
    print("# DataForSEO Skills Test Suite")
    print(f"# Target: {TEST_DOMAIN}")
    print("#"*60)

    test_results = {
        "Setup & Credentials": test_setup(),
        "Keyword Research": test_keyword_research(),
        "SERP Analysis": test_serp_analysis(),
        "Backlink Analysis": test_backlink_analysis(),
        "Competitor Analysis": test_competitor_analysis(),
        "Technical SEO": test_technical_seo(),
        "Content Analysis": test_content_analysis(),
        "Google Trends": test_google_trends(),
    }

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for v in test_results.values() if v)
    total = len(test_results)

    for name, result in test_results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")

    print(f"\n  Total: {passed}/{total} skills passed")
    print("="*60)

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
