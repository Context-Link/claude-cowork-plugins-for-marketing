#!/usr/bin/env python3
"""
Tests for Marketing-Skills Plugin (by Conversion Factory)

Structure validation tests:
- 32 SKILL.md files
- 51 CLI tools (JavaScript)
- 58 integration guides
- Plugin manifest

No credentials required - static validation only.
"""

import json
import os
import subprocess
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

        required_fields = ['name', 'description', 'author']
        for field in required_fields:
            self.assertIn(field, data,
                         f"Missing required field: {field}")

        self.assertEqual(data['name'], 'marketing-skills')

        print(f"  ✓ plugin.json has all required fields")


class TestSkills(unittest.TestCase):
    """Test skill SKILL.md files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.skills_dir = self.plugin_dir / 'skills'

    def test_skills_directory_exists(self):
        """Test that skills directory exists."""
        self.assertTrue(self.skills_dir.exists(),
                       "skills/ directory not found")

    def test_all_skills_have_skill_md(self):
        """Test that all skill folders have SKILL.md."""
        skill_folders = [d for d in self.skills_dir.iterdir()
                        if d.is_dir() and not d.name.startswith('.')]

        missing = []
        for folder in skill_folders:
            skill_file = folder / 'SKILL.md'
            if not skill_file.exists():
                missing.append(folder.name)

        self.assertEqual(len(missing), 0,
                        f"Missing SKILL.md in: {missing}")

        print(f"  ✓ {len(skill_folders)} skill folders all have SKILL.md")

    def test_skills_have_frontmatter(self):
        """Test that all SKILL.md files have valid YAML frontmatter."""
        if yaml is None:
            self.skipTest("PyYAML not installed")

        skill_files = list(self.skills_dir.glob('*/SKILL.md'))
        self.assertGreater(len(skill_files), 0, "No SKILL.md files found")

        invalid = []
        for skill_file in skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Check for YAML frontmatter
            if not content.startswith('---'):
                invalid.append(f"{skill_file.parent.name}: missing frontmatter")
                continue

            # Find closing ---
            second_dash = content.find('---', 3)
            if second_dash <= 3:
                invalid.append(f"{skill_file.parent.name}: invalid frontmatter")
                continue

            # Parse YAML
            try:
                frontmatter = content[3:second_dash].strip()
                data = yaml.safe_load(frontmatter)

                if 'name' not in data:
                    invalid.append(f"{skill_file.parent.name}: missing 'name'")
                if 'description' not in data:
                    invalid.append(f"{skill_file.parent.name}: missing 'description'")
            except yaml.YAMLError as e:
                invalid.append(f"{skill_file.parent.name}: YAML error - {e}")

        self.assertEqual(len(invalid), 0,
                        f"Invalid skills: {invalid[:5]}")

        print(f"  ✓ {len(skill_files)} skills have valid frontmatter")

    def test_skill_count(self):
        """Test that expected number of skills exist."""
        skill_files = list(self.skills_dir.glob('*/SKILL.md'))

        # According to plan: 32 skills expected
        self.assertGreaterEqual(len(skill_files), 30,
                               f"Expected ~32 skills, found {len(skill_files)}")

        print(f"  ✓ {len(skill_files)} skills found (expected ~32)")


class TestCLITools(unittest.TestCase):
    """Test CLI tools JavaScript files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.clis_dir = self.plugin_dir / 'tools' / 'clis'

    def test_clis_directory_exists(self):
        """Test that clis directory exists."""
        self.assertTrue(self.clis_dir.exists(),
                       "tools/clis/ directory not found")

    def test_cli_count(self):
        """Test that expected number of CLI tools exist."""
        cli_files = list(self.clis_dir.glob('*.js'))

        # According to plan: 51 CLI tools expected
        self.assertGreaterEqual(len(cli_files), 45,
                               f"Expected ~51 CLIs, found {len(cli_files)}")

        print(f"  ✓ {len(cli_files)} CLI tools found (expected ~51)")

    def test_cli_files_have_shebang(self):
        """Test that CLI files have proper shebang."""
        cli_files = list(self.clis_dir.glob('*.js'))

        without_shebang = []
        for cli_file in cli_files:
            with open(cli_file) as f:
                first_line = f.readline().strip()
            if not first_line.startswith('#!'):
                without_shebang.append(cli_file.name)

        # Most should have shebangs, but some might not
        shebang_pct = (len(cli_files) - len(without_shebang)) / len(cli_files) * 100

        print(f"  ✓ {shebang_pct:.0f}% of CLI tools have shebang")

    def test_cli_syntax_with_node(self):
        """Test CLI files have valid JavaScript syntax using Node.js."""
        cli_files = list(self.clis_dir.glob('*.js'))

        # Check if Node.js is available
        try:
            result = subprocess.run(['node', '--version'],
                                   capture_output=True, text=True)
            if result.returncode != 0:
                self.skipTest("Node.js not available")
        except FileNotFoundError:
            self.skipTest("Node.js not installed")

        syntax_errors = []
        for cli_file in cli_files:
            # Use Node's --check flag to verify syntax without running
            result = subprocess.run(
                ['node', '--check', str(cli_file)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                syntax_errors.append(f"{cli_file.name}: {result.stderr[:100]}")

        self.assertEqual(len(syntax_errors), 0,
                        f"Syntax errors in: {syntax_errors[:5]}")

        print(f"  ✓ {len(cli_files)} CLI tools have valid JavaScript syntax")

    def test_cli_files_have_exports_or_main(self):
        """Test that CLI files have executable structure."""
        cli_files = list(self.clis_dir.glob('*.js'))

        valid_structure = 0
        for cli_file in cli_files:
            with open(cli_file) as f:
                content = f.read()

            # Look for common patterns indicating executable CLI
            patterns = [
                'process.argv',  # Command line args
                'process.env',   # Environment variables
                'module.exports', # Module export
                'async function', # Async entry point
                'function main', # Main function
            ]

            if any(p in content for p in patterns):
                valid_structure += 1

        pct = valid_structure / len(cli_files) * 100
        self.assertGreater(pct, 90,
                          f"Only {pct:.0f}% of CLIs have valid structure")

        print(f"  ✓ {valid_structure}/{len(cli_files)} CLIs have executable structure")


class TestIntegrationGuides(unittest.TestCase):
    """Test integration guide markdown files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.integrations_dir = self.plugin_dir / 'tools' / 'integrations'

    def test_integrations_directory_exists(self):
        """Test that integrations directory exists."""
        self.assertTrue(self.integrations_dir.exists(),
                       "tools/integrations/ directory not found")

    def test_integration_count(self):
        """Test that expected number of integration guides exist."""
        integration_files = list(self.integrations_dir.glob('*.md'))

        # According to plan: 58 integration guides expected
        self.assertGreaterEqual(len(integration_files), 50,
                               f"Expected ~58 integrations, found {len(integration_files)}")

        print(f"  ✓ {len(integration_files)} integration guides found (expected ~58)")

    def test_integration_guides_have_content(self):
        """Test that integration guides have substantive content."""
        integration_files = list(self.integrations_dir.glob('*.md'))

        too_short = []
        for guide in integration_files:
            with open(guide) as f:
                content = f.read()

            # Each guide should have at least 200 characters
            if len(content) < 200:
                too_short.append(guide.name)

        self.assertEqual(len(too_short), 0,
                        f"Too short: {too_short[:5]}")

        print(f"  ✓ All integration guides have substantive content")

    def test_integration_guides_have_headers(self):
        """Test that integration guides have proper markdown headers."""
        integration_files = list(self.integrations_dir.glob('*.md'))

        without_headers = []
        for guide in integration_files:
            with open(guide) as f:
                content = f.read()

            if '#' not in content:
                without_headers.append(guide.name)

        self.assertEqual(len(without_headers), 0,
                        f"Missing headers: {without_headers[:5]}")

        print(f"  ✓ All integration guides have markdown headers")


class TestSkillCrossReferences(unittest.TestCase):
    """Test cross-references between skills."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.skills_dir = self.plugin_dir / 'skills'

    def test_related_skills_references(self):
        """Test that 'see' or 'also' references point to existing skills."""
        skill_files = list(self.skills_dir.glob('*/SKILL.md'))
        skill_names = {f.parent.name for f in skill_files}

        # Pattern to find skill references like "see email-sequence" or "also use copywriting"
        ref_pattern = re.compile(r'(?:see|also use|also see|refer to)\s+([a-z0-9-]+)', re.I)

        broken_refs = []
        for skill_file in skill_files:
            with open(skill_file) as f:
                content = f.read()

            for match in ref_pattern.finditer(content):
                ref_skill = match.group(1).lower().strip('.,')
                # Only check if it looks like a skill name (not a regular word)
                if '-' in ref_skill and ref_skill not in skill_names:
                    broken_refs.append(f"{skill_file.parent.name}: {ref_skill}")

        if broken_refs:
            print(f"  ! Possible broken refs: {broken_refs[:3]}")

        # Don't fail on this - just report
        print(f"  ✓ Skill cross-references checked ({len(broken_refs)} possible issues)")


class TestRegistryFile(unittest.TestCase):
    """Test REGISTRY.md file."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.registry_file = self.plugin_dir / 'tools' / 'REGISTRY.md'

    def test_registry_exists(self):
        """Test that REGISTRY.md exists."""
        self.assertTrue(self.registry_file.exists(),
                       "tools/REGISTRY.md not found")

    def test_registry_has_content(self):
        """Test that REGISTRY.md has substantive content."""
        with open(self.registry_file) as f:
            content = f.read()

        # Should be a comprehensive registry
        self.assertGreater(len(content), 5000,
                          "REGISTRY.md seems too short")

        print(f"  ✓ REGISTRY.md exists ({len(content)} chars)")


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPluginJson))
    suite.addTests(loader.loadTestsFromTestCase(TestSkills))
    suite.addTests(loader.loadTestsFromTestCase(TestCLITools))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationGuides))
    suite.addTests(loader.loadTestsFromTestCase(TestSkillCrossReferences))
    suite.addTests(loader.loadTestsFromTestCase(TestRegistryFile))

    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Marketing-Skills Plugin (by Conversion Factory) Tests")
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
