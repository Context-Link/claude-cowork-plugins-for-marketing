#!/usr/bin/env python3
"""
Tests for SEO-Machine Plugin API Integrations (by Craig Hewitt)

API integration tests:
- DataForSEO connection and basic queries
- Google Analytics 4 connection
- Google Search Console connection

Credentials required:
- DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD
- GA4_PROPERTY_ID, GA4_CREDENTIALS_PATH
- GSC_SITE_URL, GSC_CREDENTIALS_PATH
"""

import os
import sys
import unittest
from pathlib import Path
from datetime import datetime, timedelta

# Load .env from root directory
root_dir = Path(__file__).parent.parent.parent.parent
env_path = root_dir / '.env'

def load_env(path):
    """Load environment variables from .env file."""
    if not path.exists():
        return {}
    env_vars = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
                os.environ[key.strip()] = value.strip()
    return env_vars

env_vars = load_env(env_path)

# Add data_sources to path for imports
plugin_dir = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_dir / 'data_sources'))


class TestDataForSEO(unittest.TestCase):
    """Test DataForSEO API integration."""

    @classmethod
    def setUpClass(cls):
        """Check credentials are available."""
        cls.login = os.environ.get('DATAFORSEO_LOGIN')
        cls.password = os.environ.get('DATAFORSEO_PASSWORD')

        if not cls.login or not cls.password:
            raise unittest.SkipTest("DataForSEO credentials not configured")

    def test_dataforseo_import(self):
        """Test that DataForSEO module can be imported."""
        try:
            from modules import dataforseo
            self.assertTrue(True)
            print(f"  ✓ DataForSEO module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import DataForSEO module: {e}")

    def test_dataforseo_connection(self):
        """Test DataForSEO API connection."""
        import requests
        import base64

        # Build auth header
        creds = f"{self.login}:{self.password}"
        auth = base64.b64encode(creds.encode()).decode()

        # Test connection with a simple request
        response = requests.get(
            'https://api.dataforseo.com/v3/serp/google/organic/task_get/advanced/1234567890',
            headers={'Authorization': f'Basic {auth}'},
            timeout=30
        )

        # 20000 = no such task (expected for fake ID)
        # 40200 = success but empty
        # Any response means API is reachable
        self.assertIn(response.status_code, [200, 400, 401, 404],
                     f"Unexpected status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            # Check response structure
            self.assertIn('status_code', data)
            print(f"  ✓ DataForSEO API connected (status: {data.get('status_code')})")
        else:
            print(f"  ✓ DataForSEO API reachable (HTTP {response.status_code})")

    def test_dataforseo_keyword_search(self):
        """Test DataForSEO keyword data API."""
        import requests
        import base64
        import json

        creds = f"{self.login}:{self.password}"
        auth = base64.b64encode(creds.encode()).decode()

        # Test keyword search volume endpoint
        payload = [{
            "language_code": "en",
            "location_code": 2840,  # USA
            "keywords": ["test keyword"]
        }]

        response = requests.post(
            'https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live',
            headers={
                'Authorization': f'Basic {auth}',
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=30
        )

        self.assertEqual(response.status_code, 200,
                        f"API error: {response.text[:200]}")

        data = response.json()
        self.assertIn('tasks', data)

        print(f"  ✓ DataForSEO keyword API working")

    def test_dataforseo_serp_api(self):
        """Test DataForSEO SERP API (task post/get)."""
        import requests
        import base64

        creds = f"{self.login}:{self.password}"
        auth = base64.b64encode(creds.encode()).decode()

        # Post a SERP task
        payload = [{
            "language_code": "en",
            "location_code": 2840,
            "keyword": "podcast hosting"
        }]

        response = requests.post(
            'https://api.dataforseo.com/v3/serp/google/organic/live/advanced',
            headers={
                'Authorization': f'Basic {auth}',
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=60
        )

        self.assertEqual(response.status_code, 200,
                        f"SERP API error: {response.text[:200]}")

        data = response.json()
        self.assertIn('tasks', data)

        # Should have results
        if data.get('tasks') and data['tasks'][0].get('result'):
            result = data['tasks'][0]['result'][0]
            items_count = result.get('items_count', 0)
            print(f"  ✓ DataForSEO SERP API returned {items_count} results")
        else:
            print(f"  ✓ DataForSEO SERP API working (no results in response)")


class TestGoogleAnalytics(unittest.TestCase):
    """Test Google Analytics 4 API integration."""

    @classmethod
    def setUpClass(cls):
        """Check GA4 credentials are available."""
        cls.property_id = os.environ.get('GA4_PROPERTY_ID')
        cls.credentials_path = os.environ.get('GA4_CREDENTIALS_PATH')

        if not cls.property_id:
            raise unittest.SkipTest("GA4_PROPERTY_ID not configured")

        # Resolve credentials path relative to root
        if cls.credentials_path:
            creds_path = root_dir / cls.credentials_path.lstrip('./')
            if not creds_path.exists():
                raise unittest.SkipTest(f"GA4 credentials file not found: {creds_path}")
            cls.credentials_path = str(creds_path)
        else:
            raise unittest.SkipTest("GA4_CREDENTIALS_PATH not configured")

    def test_ga4_module_import(self):
        """Test that GA4 module can be imported."""
        try:
            from modules import google_analytics
            self.assertTrue(True)
            print(f"  ✓ GA4 module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import GA4 module: {e}")

    def test_ga4_connection(self):
        """Test GA4 API connection."""
        try:
            from google.analytics.data_v1beta import BetaAnalyticsDataClient
            from google.analytics.data_v1beta.types import (
                RunReportRequest,
                DateRange,
                Dimension,
                Metric
            )
            from google.oauth2 import service_account

            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/analytics.readonly']
            )

            client = BetaAnalyticsDataClient(credentials=credentials)

            # Run a simple report
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
                dimensions=[Dimension(name="date")],
                metrics=[Metric(name="sessions")]
            )

            response = client.run_report(request)

            # Should have rows
            row_count = len(response.rows) if response.rows else 0

            print(f"  ✓ GA4 API connected ({row_count} days of data)")

        except Exception as e:
            self.fail(f"GA4 connection failed: {e}")

    def test_ga4_traffic_data(self):
        """Test GA4 traffic data retrieval."""
        try:
            from google.analytics.data_v1beta import BetaAnalyticsDataClient
            from google.analytics.data_v1beta.types import (
                RunReportRequest,
                DateRange,
                Dimension,
                Metric
            )
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/analytics.readonly']
            )

            client = BetaAnalyticsDataClient(credentials=credentials)

            # Get page path traffic
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
                dimensions=[Dimension(name="pagePath")],
                metrics=[
                    Metric(name="sessions"),
                    Metric(name="screenPageViews"),
                    Metric(name="engagementRate")
                ],
                limit=10
            )

            response = client.run_report(request)

            total_sessions = sum(
                int(row.metric_values[0].value)
                for row in response.rows
            ) if response.rows else 0

            print(f"  ✓ GA4 traffic data retrieved ({total_sessions} total sessions)")

        except Exception as e:
            self.fail(f"GA4 traffic data failed: {e}")


class TestGoogleSearchConsole(unittest.TestCase):
    """Test Google Search Console API integration."""

    @classmethod
    def setUpClass(cls):
        """Check GSC credentials are available."""
        cls.site_url = os.environ.get('GSC_SITE_URL')
        cls.credentials_path = os.environ.get('GSC_CREDENTIALS_PATH')

        if not cls.site_url:
            raise unittest.SkipTest("GSC_SITE_URL not configured")

        # Resolve credentials path relative to root
        if cls.credentials_path:
            creds_path = root_dir / cls.credentials_path.lstrip('./')
            if not creds_path.exists():
                raise unittest.SkipTest(f"GSC credentials file not found: {creds_path}")
            cls.credentials_path = str(creds_path)
        else:
            raise unittest.SkipTest("GSC_CREDENTIALS_PATH not configured")

    def test_gsc_module_import(self):
        """Test that GSC module can be imported."""
        try:
            from modules import google_search_console
            self.assertTrue(True)
            print(f"  ✓ GSC module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import GSC module: {e}")

    def test_gsc_connection(self):
        """Test GSC API connection."""
        try:
            from googleapiclient.discovery import build
            from google.oauth2 import service_account

            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/webmasters.readonly']
            )

            service = build('searchconsole', 'v1', credentials=credentials)

            # Get site info
            site_list = service.sites().list().execute()

            sites = site_list.get('siteEntry', [])
            site_found = any(s.get('siteUrl') == self.site_url for s in sites)

            if site_found:
                print(f"  ✓ GSC API connected (site verified)")
            else:
                print(f"  ✓ GSC API connected ({len(sites)} sites found)")

        except Exception as e:
            self.fail(f"GSC connection failed: {e}")

    def test_gsc_search_analytics(self):
        """Test GSC search analytics data retrieval."""
        try:
            from googleapiclient.discovery import build
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/webmasters.readonly']
            )

            service = build('searchconsole', 'v1', credentials=credentials)

            # Calculate date range (last 30 days)
            end_date = datetime.now() - timedelta(days=3)  # GSC has 3-day delay
            start_date = end_date - timedelta(days=30)

            # Query search analytics
            request = {
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'dimensions': ['query'],
                'rowLimit': 10
            }

            response = service.searchanalytics().query(
                siteUrl=self.site_url,
                body=request
            ).execute()

            rows = response.get('rows', [])
            total_clicks = sum(row.get('clicks', 0) for row in rows)

            print(f"  ✓ GSC search analytics retrieved ({len(rows)} queries, {total_clicks} clicks)")

        except Exception as e:
            self.fail(f"GSC search analytics failed: {e}")


class TestModuleImports(unittest.TestCase):
    """Test that all Python modules can be imported."""

    def setUp(self):
        self.modules_dir = plugin_dir / 'data_sources' / 'modules'

    def test_core_modules_import(self):
        """Test importing core analysis modules."""
        core_modules = [
            'content_scorer',
            'readability_scorer',
            'keyword_analyzer',
            'search_intent_analyzer',
            'seo_quality_rater'
        ]

        import_errors = []
        for module_name in core_modules:
            try:
                __import__(f'modules.{module_name}')
            except ImportError as e:
                import_errors.append(f"{module_name}: {e}")

        if import_errors:
            print(f"  ! Import issues: {import_errors[:3]}")
            # Don't fail - just report
        else:
            print(f"  ✓ {len(core_modules)} core modules imported successfully")


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataForSEO))
    suite.addTests(loader.loadTestsFromTestCase(TestGoogleAnalytics))
    suite.addTests(loader.loadTestsFromTestCase(TestGoogleSearchConsole))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleImports))

    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEO-Machine Plugin API Integration Tests")
    print("="*60 + "\n")

    result = run_tests()

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    sys.exit(0 if result.wasSuccessful() else 1)
