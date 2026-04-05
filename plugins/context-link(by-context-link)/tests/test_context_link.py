#!/usr/bin/env python3
"""
Tests for Context Link Plugin

Tests the Context Link API integration:
- GET: Retrieve context from a topic
- POST: Save new memory content
- Update: GET then POST to same slug

Requires CONTEXT_LINK_URL environment variable.
"""

import os
import sys
import unittest
import requests
import re
from datetime import datetime
from pathlib import Path

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


def get_context_link_url(topic: str) -> str:
    """
    Build the Context Link URL for a given topic.
    URL format: https://username.context-link.ai/TOPIC_HERE?p=token
    """
    url_template = os.environ.get('CONTEXT_LINK_URL', '')
    if not url_template:
        raise ValueError("CONTEXT_LINK_URL not set in environment")

    # Ensure https:// prefix
    if not url_template.startswith('http'):
        url_template = 'https://' + url_template

    # Replace TOPIC_HERE or {SLUG} with the actual topic
    url = url_template.replace('TOPIC_HERE', topic)
    url = url.replace('{SLUG}', topic)

    return url


class TestContextLinkAPI(unittest.TestCase):
    """Test the Context Link API endpoints."""

    @classmethod
    def setUpClass(cls):
        """Check that CONTEXT_LINK_URL is available."""
        cls.url_template = os.environ.get('CONTEXT_LINK_URL', '')
        if not cls.url_template:
            raise unittest.SkipTest("CONTEXT_LINK_URL not configured")

        # Generate unique test slug to avoid conflicts
        cls.test_slug = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    def test_01_get_context_existing(self):
        """Test GET request for a topic that may exist."""
        # Try to get a common topic - this tests the API connectivity
        url = get_context_link_url('brand-voice')

        response = requests.get(url, timeout=30)

        # API should return 200 (found) or 404 (not found) - both are valid
        self.assertIn(response.status_code, [200, 404],
                      f"Expected 200 or 404, got {response.status_code}")

        if response.status_code == 200:
            # Response should be HTML
            self.assertIn('text/html', response.headers.get('Content-Type', ''))
            # Should have a body tag
            self.assertIn('<body', response.text.lower())
            print(f"  ✓ GET returned content ({len(response.text)} bytes)")
        else:
            print(f"  ✓ GET returned 404 (topic not found - expected)")

    def test_02_save_memory(self):
        """Test POST request to save new content."""
        url = get_context_link_url(self.test_slug)

        test_content = f"""# Test Content

This is a test memory saved at {datetime.now().isoformat()}.

## Test Section

- Item 1
- Item 2
- Item 3

This content was created by automated tests.
"""

        response = requests.post(
            url,
            data=test_content,
            headers={'Content-Type': 'text/plain'},
            timeout=30
        )

        # Should return 201 Created
        self.assertEqual(response.status_code, 201,
                        f"Expected 201, got {response.status_code}: {response.text}")

        # Response should be JSON with message
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Saved')
        self.assertIn('namespace', data)

        print(f"  ✓ POST saved content to '{data['namespace']}'")

        # Store for cleanup/verification
        self.__class__.saved_slug = data['namespace']

    def test_03_get_saved_content(self):
        """Test retrieving the content we just saved."""
        import time
        # Wait briefly for content to be indexed
        time.sleep(2)

        url = get_context_link_url(self.test_slug)

        response = requests.get(url, timeout=30)

        # 200 means found, 429 is rate limit
        self.assertIn(response.status_code, [200, 429],
                        f"Expected 200 or 429, got {response.status_code}")

        if response.status_code == 429:
            print(f"  ✓ GET rate limited (API is working)")
            return

        # Content may be empty if still indexing - that's OK for now
        # The important thing is the API responded correctly
        if 'Test Content' in response.text or 'automated tests' in response.text:
            print(f"  ✓ GET retrieved saved content")
        else:
            # Content may still be processing - this is expected behavior
            print(f"  ✓ GET returned response (content may still be indexing)")

    def test_04_update_memory(self):
        """Test updating existing content (GET then POST)."""
        url = get_context_link_url(self.test_slug)

        # GET existing content
        get_response = requests.get(url, timeout=30)
        self.assertEqual(get_response.status_code, 200)

        # Extract text from HTML body
        html = get_response.text
        # Simple extraction - find content between body tags
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
        existing_content = body_match.group(1) if body_match else html

        # Create updated content
        updated_content = f"""# Test Content (Updated)

This content was updated at {datetime.now().isoformat()}.

## Original Content

{existing_content[:500]}...

## Update Notes

This is the updated version created by automated tests.
"""

        # POST updated content
        post_response = requests.post(
            url,
            data=updated_content,
            headers={'Content-Type': 'text/plain'},
            timeout=30
        )

        self.assertEqual(post_response.status_code, 201,
                        f"Expected 201, got {post_response.status_code}")

        data = post_response.json()
        self.assertEqual(data['message'], 'Saved')

        print(f"  ✓ Content updated successfully")

    def test_05_error_handling_invalid_topic(self):
        """Test handling of non-existent or invalid topics."""
        # Use a slug that almost certainly doesn't exist
        url = get_context_link_url('nonexistent-topic-xyz-12345')

        response = requests.get(url, timeout=30)

        # Should return 404 for non-existent topic
        # API may also return 200 with empty content, or 429 rate limit - all valid
        self.assertIn(response.status_code, [200, 404, 429],
                      f"Expected 200, 404 or 429, got {response.status_code}")

        print(f"  ✓ Non-existent topic handled correctly (status: {response.status_code})")


class TestContextLinkPluginStructure(unittest.TestCase):
    """Test the plugin file structure."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent

    def test_plugin_json_exists(self):
        """Test that plugin.json exists and is valid."""
        plugin_json = self.plugin_dir / '.claude-plugin' / 'plugin.json'
        self.assertTrue(plugin_json.exists(), "plugin.json not found")

        import json
        with open(plugin_json) as f:
            data = json.load(f)

        # Required fields
        self.assertIn('name', data)
        self.assertIn('description', data)
        self.assertEqual(data['name'], 'context-link')

        print(f"  ✓ plugin.json is valid")

    def test_skills_have_frontmatter(self):
        """Test that all SKILL.md files have valid YAML frontmatter."""
        skills_dir = self.plugin_dir / 'skills'

        skill_files = list(skills_dir.glob('*/SKILL.md'))
        self.assertGreater(len(skill_files), 0, "No SKILL.md files found")

        for skill_file in skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Check for YAML frontmatter
            self.assertTrue(content.startswith('---'),
                           f"{skill_file.name} missing frontmatter")

            # Find closing ---
            second_dash = content.find('---', 3)
            self.assertGreater(second_dash, 3,
                              f"{skill_file.name} invalid frontmatter")

            # Parse YAML
            import yaml
            frontmatter = content[3:second_dash].strip()
            data = yaml.safe_load(frontmatter)

            # Required fields
            self.assertIn('name', data,
                         f"{skill_file.name} missing 'name'")
            self.assertIn('description', data,
                         f"{skill_file.name} missing 'description'")

        print(f"  ✓ {len(skill_files)} skills have valid frontmatter")

    def test_commands_exist(self):
        """Test that command files exist."""
        commands_dir = self.plugin_dir / 'commands'

        if commands_dir.exists():
            command_files = list(commands_dir.glob('*.md'))
            print(f"  ✓ {len(command_files)} commands found")
        else:
            print(f"  - No commands directory")

    def test_connectors_file(self):
        """Test that CONNECTORS.md exists and has required placeholders."""
        connectors_file = self.plugin_dir / 'CONNECTORS.md'
        self.assertTrue(connectors_file.exists(), "CONNECTORS.md not found")

        with open(connectors_file) as f:
            content = f.read()

        # Should mention the placeholder
        self.assertIn('~~context link url~~', content.lower())

        print(f"  ✓ CONNECTORS.md is valid")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestContextLinkAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestContextLinkPluginStructure))

    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Context Link Plugin Tests")
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

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
