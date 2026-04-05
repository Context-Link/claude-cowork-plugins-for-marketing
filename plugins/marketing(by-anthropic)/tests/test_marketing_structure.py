#!/usr/bin/env python3
"""
Tests for Marketing Plugin (by Anthropic)

Structure validation tests:
- Plugin manifest (plugin.json)
- MCP configuration (.mcp.json)
- Command files (7 commands)
- Skill files (5 skills)
- CONNECTORS.md

No credentials required - static validation only.
"""

import json
import os
import sys
import unittest
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


class TestPluginJson(unittest.TestCase):
    """Test plugin.json manifest."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.plugin_json = self.plugin_dir / '.claude-plugin' / 'plugin.json'

    def test_plugin_json_exists(self):
        """Test that plugin.json exists."""
        self.assertTrue(self.plugin_json.exists(),
                       "plugin.json not found")

    def test_plugin_json_valid_json(self):
        """Test that plugin.json is valid JSON."""
        with open(self.plugin_json) as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)
        print(f"  ✓ plugin.json is valid JSON")

    def test_plugin_json_required_fields(self):
        """Test that plugin.json has required fields."""
        with open(self.plugin_json) as f:
            data = json.load(f)

        required_fields = ['name', 'version', 'description', 'author']
        for field in required_fields:
            self.assertIn(field, data,
                         f"Missing required field: {field}")

        self.assertEqual(data['name'], 'marketing')
        self.assertIn('name', data['author'])

        print(f"  ✓ plugin.json has all required fields")

    def test_plugin_version_format(self):
        """Test that version follows semver format."""
        with open(self.plugin_json) as f:
            data = json.load(f)

        version = data.get('version', '')
        # Simple semver pattern
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
        self.assertTrue(re.match(pattern, version),
                       f"Invalid version format: {version}")

        print(f"  ✓ Version {version} is valid semver")


class TestMcpJson(unittest.TestCase):
    """Test .mcp.json configuration."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.mcp_json = self.plugin_dir / '.mcp.json'

    def test_mcp_json_exists(self):
        """Test that .mcp.json exists."""
        self.assertTrue(self.mcp_json.exists(),
                       ".mcp.json not found")

    def test_mcp_json_valid_json(self):
        """Test that .mcp.json is valid JSON."""
        with open(self.mcp_json) as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)
        print(f"  ✓ .mcp.json is valid JSON")

    def test_mcp_servers_structure(self):
        """Test that mcpServers has correct structure."""
        with open(self.mcp_json) as f:
            data = json.load(f)

        self.assertIn('mcpServers', data)
        servers = data['mcpServers']

        # Check that each server has required fields
        for name, config in servers.items():
            self.assertIn('type', config,
                         f"Server '{name}' missing 'type'")
            self.assertIn('url', config,
                         f"Server '{name}' missing 'url'")

            # Validate URL format
            url = config['url']
            self.assertTrue(url.startswith('https://'),
                           f"Server '{name}' URL should use HTTPS: {url}")

        print(f"  ✓ {len(servers)} MCP servers configured correctly")

    def test_mcp_server_urls_valid(self):
        """Test that MCP server URLs are properly formatted."""
        with open(self.mcp_json) as f:
            data = json.load(f)

        servers = data.get('mcpServers', {})
        url_pattern = re.compile(r'^https://[a-zA-Z0-9.-]+(/[a-zA-Z0-9._/-]*)?$')

        for name, config in servers.items():
            url = config.get('url', '')
            self.assertTrue(url_pattern.match(url),
                           f"Invalid URL for '{name}': {url}")

        print(f"  ✓ All MCP server URLs are valid")


class TestCommands(unittest.TestCase):
    """Test command .md files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.commands_dir = self.plugin_dir / 'commands'

    def test_commands_directory_exists(self):
        """Test that commands directory exists."""
        self.assertTrue(self.commands_dir.exists(),
                       "commands/ directory not found")

    def test_expected_commands_exist(self):
        """Test that expected command files exist."""
        expected_commands = [
            'brand-review.md',
            'campaign-plan.md',
            'competitive-brief.md',
            'draft-content.md',
            'email-sequence.md',
            'performance-report.md',
            'seo-audit.md'
        ]

        for cmd in expected_commands:
            cmd_path = self.commands_dir / cmd
            self.assertTrue(cmd_path.exists(),
                           f"Command not found: {cmd}")

        print(f"  ✓ All {len(expected_commands)} expected commands exist")

    def test_commands_have_frontmatter(self):
        """Test that all commands have valid YAML frontmatter."""
        if yaml is None:
            self.skipTest("PyYAML not installed")

        command_files = list(self.commands_dir.glob('*.md'))
        self.assertGreater(len(command_files), 0, "No command files found")

        for cmd_file in command_files:
            with open(cmd_file) as f:
                content = f.read()

            # Check for YAML frontmatter
            self.assertTrue(content.startswith('---'),
                           f"{cmd_file.name} missing frontmatter")

            # Find closing ---
            second_dash = content.find('---', 3)
            self.assertGreater(second_dash, 3,
                              f"{cmd_file.name} invalid frontmatter")

            # Parse YAML
            frontmatter = content[3:second_dash].strip()
            data = yaml.safe_load(frontmatter)

            # Commands should have description
            self.assertIn('description', data,
                         f"{cmd_file.name} missing 'description'")

        print(f"  ✓ {len(command_files)} commands have valid frontmatter")

    def test_commands_have_content(self):
        """Test that command files have substantive content."""
        command_files = list(self.commands_dir.glob('*.md'))

        for cmd_file in command_files:
            with open(cmd_file) as f:
                content = f.read()

            # Should have at least 500 characters of content
            self.assertGreater(len(content), 500,
                              f"{cmd_file.name} has too little content")

            # Should have headers
            self.assertIn('#', content,
                         f"{cmd_file.name} missing headers")

        print(f"  ✓ All commands have substantive content")


class TestSkills(unittest.TestCase):
    """Test skill folders and SKILL.md files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.skills_dir = self.plugin_dir / 'skills'

    def test_skills_directory_exists(self):
        """Test that skills directory exists."""
        self.assertTrue(self.skills_dir.exists(),
                       "skills/ directory not found")

    def test_expected_skills_exist(self):
        """Test that expected skill folders exist."""
        expected_skills = [
            'brand-voice',
            'campaign-planning',
            'competitive-analysis',
            'content-creation',
            'performance-analytics'
        ]

        for skill in expected_skills:
            skill_dir = self.skills_dir / skill
            self.assertTrue(skill_dir.is_dir(),
                           f"Skill folder not found: {skill}")

            skill_file = skill_dir / 'SKILL.md'
            self.assertTrue(skill_file.exists(),
                           f"SKILL.md not found in {skill}")

        print(f"  ✓ All {len(expected_skills)} expected skills exist")

    def test_skills_have_frontmatter(self):
        """Test that all SKILL.md files have valid YAML frontmatter."""
        if yaml is None:
            self.skipTest("PyYAML not installed")

        skill_files = list(self.skills_dir.glob('*/SKILL.md'))
        self.assertGreater(len(skill_files), 0, "No SKILL.md files found")

        for skill_file in skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Check for YAML frontmatter
            self.assertTrue(content.startswith('---'),
                           f"{skill_file.parent.name}/SKILL.md missing frontmatter")

            # Find closing ---
            second_dash = content.find('---', 3)
            self.assertGreater(second_dash, 3,
                              f"{skill_file.parent.name}/SKILL.md invalid frontmatter")

            # Parse YAML
            frontmatter = content[3:second_dash].strip()
            data = yaml.safe_load(frontmatter)

            # Skills should have name and description
            self.assertIn('name', data,
                         f"{skill_file.parent.name}/SKILL.md missing 'name'")
            self.assertIn('description', data,
                         f"{skill_file.parent.name}/SKILL.md missing 'description'")

        print(f"  ✓ {len(skill_files)} skills have valid frontmatter")


class TestConnectors(unittest.TestCase):
    """Test CONNECTORS.md file."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.connectors_file = self.plugin_dir / 'CONNECTORS.md'

    def test_connectors_exists(self):
        """Test that CONNECTORS.md exists."""
        self.assertTrue(self.connectors_file.exists(),
                       "CONNECTORS.md not found")

    def test_connectors_has_content(self):
        """Test that CONNECTORS.md has substantive content."""
        with open(self.connectors_file) as f:
            content = f.read()

        self.assertGreater(len(content), 100,
                          "CONNECTORS.md has too little content")
        print(f"  ✓ CONNECTORS.md exists ({len(content)} chars)")

    def test_connectors_documents_placeholders(self):
        """Test that CONNECTORS.md explains placeholder usage."""
        with open(self.connectors_file) as f:
            content = f.read().lower()

        # Should mention placeholders or connectors
        has_explanation = any([
            'placeholder' in content,
            '~~' in content,
            'connector' in content,
            'tool' in content
        ])

        self.assertTrue(has_explanation,
                       "CONNECTORS.md should explain placeholders or tools")

        print(f"  ✓ CONNECTORS.md documents tool/placeholder usage")


class TestCrossReferences(unittest.TestCase):
    """Test that cross-references between files are valid."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent

    def test_commands_reference_connectors(self):
        """Test that commands reference CONNECTORS.md."""
        commands_dir = self.plugin_dir / 'commands'
        command_files = list(commands_dir.glob('*.md'))

        refs_found = 0
        for cmd_file in command_files:
            with open(cmd_file) as f:
                content = f.read()
            if 'CONNECTORS.md' in content:
                refs_found += 1

        # At least some commands should reference CONNECTORS.md
        self.assertGreater(refs_found, 0,
                          "No commands reference CONNECTORS.md")

        print(f"  ✓ {refs_found}/{len(command_files)} commands reference CONNECTORS.md")

    def test_no_broken_internal_links(self):
        """Test that internal markdown links point to existing files."""
        all_md_files = list(self.plugin_dir.rglob('*.md'))
        broken_links = []

        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        for md_file in all_md_files:
            with open(md_file) as f:
                content = f.read()

            for match in link_pattern.finditer(content):
                link_text, link_target = match.groups()

                # Skip external URLs
                if link_target.startswith(('http://', 'https://', 'mailto:')):
                    continue

                # Skip anchor links
                if link_target.startswith('#'):
                    continue

                # Resolve relative path
                target_path = md_file.parent / link_target.split('#')[0]
                if not target_path.exists():
                    broken_links.append(f"{md_file.name}: {link_target}")

        if broken_links:
            print(f"  ! Broken links found: {broken_links[:5]}")

        self.assertEqual(len(broken_links), 0,
                        f"Broken internal links: {broken_links}")

        print(f"  ✓ No broken internal links found")


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPluginJson))
    suite.addTests(loader.loadTestsFromTestCase(TestMcpJson))
    suite.addTests(loader.loadTestsFromTestCase(TestCommands))
    suite.addTests(loader.loadTestsFromTestCase(TestSkills))
    suite.addTests(loader.loadTestsFromTestCase(TestConnectors))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossReferences))

    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Marketing Plugin (by Anthropic) Tests")
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
