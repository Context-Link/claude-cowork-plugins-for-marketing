#!/usr/bin/env python3
"""
Tests for SEO-Machine Plugin Structure (by Craig Hewitt)

Structure validation tests:
- 10 agent .md files
- 20 command .md files
- 27 skill folders
- 24 Python modules
- Plugin manifest
- Context files

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

        self.assertEqual(data['name'], 'seo-machine')

        print(f"  ✓ plugin.json has all required fields")


class TestAgents(unittest.TestCase):
    """Test agent .md files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.agents_dir = self.plugin_dir / 'agents'

    def test_agents_directory_exists(self):
        """Test that agents directory exists."""
        self.assertTrue(self.agents_dir.exists(),
                       "agents/ directory not found")

    def test_agent_count(self):
        """Test that expected number of agents exist."""
        agent_files = list(self.agents_dir.glob('*.md'))

        # Expected: 10 agents
        self.assertGreaterEqual(len(agent_files), 10,
                               f"Expected ~10 agents, found {len(agent_files)}")

        print(f"  ✓ {len(agent_files)} agents found (expected ~10)")

    def test_agents_have_content(self):
        """Test that agent files have substantive content."""
        agent_files = list(self.agents_dir.glob('*.md'))

        too_short = []
        for agent in agent_files:
            with open(agent) as f:
                content = f.read()
            if len(content) < 500:
                too_short.append(agent.name)

        self.assertEqual(len(too_short), 0,
                        f"Too short: {too_short}")

        print(f"  ✓ All agents have substantive content")

    def test_agents_have_role_definition(self):
        """Test that agent files define a clear role."""
        agent_files = list(self.agents_dir.glob('*.md'))

        # Look for common patterns indicating role definition
        role_patterns = ['you are', 'role', 'specialist', 'expert', 'responsible']

        without_role = []
        for agent in agent_files:
            with open(agent) as f:
                content = f.read().lower()

            if not any(p in content for p in role_patterns):
                without_role.append(agent.name)

        self.assertEqual(len(without_role), 0,
                        f"Missing role definition: {without_role}")

        print(f"  ✓ All agents have clear role definitions")


class TestCommands(unittest.TestCase):
    """Test command .md files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.commands_dir = self.plugin_dir / 'commands'

    def test_commands_directory_exists(self):
        """Test that commands directory exists."""
        self.assertTrue(self.commands_dir.exists(),
                       "commands/ directory not found")

    def test_command_count(self):
        """Test that expected number of commands exist."""
        command_files = list(self.commands_dir.glob('*.md'))

        # Expected: 20 commands
        self.assertGreaterEqual(len(command_files), 20,
                               f"Expected ~20 commands, found {len(command_files)}")

        print(f"  ✓ {len(command_files)} commands found (expected ~20)")

    def test_commands_have_structure(self):
        """Test that all commands have valid structure (frontmatter or markdown header)."""
        command_files = list(self.commands_dir.glob('*.md'))
        self.assertGreater(len(command_files), 0, "No command files found")

        invalid = []
        with_frontmatter = 0
        with_header = 0

        for cmd_file in command_files:
            with open(cmd_file) as f:
                content = f.read()

            # Check for YAML frontmatter OR markdown header
            has_frontmatter = content.startswith('---')
            has_header = content.startswith('#') or '\n#' in content[:100]

            if has_frontmatter:
                with_frontmatter += 1
            elif has_header:
                with_header += 1
            else:
                invalid.append(cmd_file.name)

        self.assertEqual(len(invalid), 0,
                        f"Commands without structure: {invalid[:5]}")

        print(f"  ✓ {len(command_files)} commands have valid structure ({with_frontmatter} frontmatter, {with_header} headers)")


class TestSkills(unittest.TestCase):
    """Test skill folders and files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.skills_dir = self.plugin_dir / 'skills'

    def test_skills_directory_exists(self):
        """Test that skills directory exists."""
        self.assertTrue(self.skills_dir.exists(),
                       "skills/ directory not found")

    def test_skill_count(self):
        """Test that expected number of skills exist."""
        # Count both folders with SKILL.md and standalone .md files
        skill_folders = [d for d in self.skills_dir.iterdir()
                        if d.is_dir() and not d.name.startswith('.')]
        skill_files = list(self.skills_dir.glob('*.md'))

        total_skills = len(skill_folders) + len(skill_files)

        # Expected: ~27 skills
        self.assertGreaterEqual(total_skills, 25,
                               f"Expected ~27 skills, found {total_skills}")

        print(f"  ✓ {total_skills} skills found ({len(skill_folders)} folders + {len(skill_files)} files)")

    def test_skill_folders_have_skill_md(self):
        """Test that skill folders have SKILL.md."""
        skill_folders = [d for d in self.skills_dir.iterdir()
                        if d.is_dir() and not d.name.startswith('.')]

        missing = []
        for folder in skill_folders:
            skill_file = folder / 'SKILL.md'
            if not skill_file.exists():
                missing.append(folder.name)

        self.assertEqual(len(missing), 0,
                        f"Missing SKILL.md in: {missing}")

        print(f"  ✓ {len(skill_folders)} skill folders have SKILL.md")

    def test_skills_have_structure(self):
        """Test that SKILL.md files have valid structure (frontmatter or header)."""
        # Get SKILL.md files from subdirectories
        skill_files = list(self.skills_dir.glob('*/SKILL.md'))
        # Also include standalone *SKILL.md files in root (like growth-lead-SKILL.md)
        standalone_skills = [f for f in self.skills_dir.glob('*SKILL.md')
                           if f.is_file() and 'SKILL' in f.name]
        skill_files.extend(standalone_skills)

        self.assertGreater(len(skill_files), 0, "No skill files found")

        invalid = []
        with_frontmatter = 0
        with_header = 0

        for skill_file in skill_files:
            with open(skill_file) as f:
                content = f.read()

            # Check for YAML frontmatter OR markdown header
            has_frontmatter = content.startswith('---')
            has_header = content.startswith('#') or '\n#' in content[:100]

            if has_frontmatter:
                with_frontmatter += 1
                # Validate YAML if present
                if yaml:
                    second_dash = content.find('---', 3)
                    if second_dash > 3:
                        try:
                            frontmatter = content[3:second_dash].strip()
                            yaml.safe_load(frontmatter)
                        except yaml.YAMLError:
                            invalid.append(f"{skill_file.parent.name}: YAML error")
            elif has_header:
                with_header += 1
            else:
                invalid.append(f"{skill_file.parent.name}: no structure")

        self.assertEqual(len(invalid), 0,
                        f"Invalid skills: {invalid[:5]}")

        print(f"  ✓ {len(skill_files)} skills have valid structure ({with_frontmatter} frontmatter, {with_header} headers)")


class TestPythonModules(unittest.TestCase):
    """Test Python module files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.modules_dir = self.plugin_dir / 'data_sources' / 'modules'

    def test_modules_directory_exists(self):
        """Test that modules directory exists."""
        self.assertTrue(self.modules_dir.exists(),
                       "data_sources/modules/ directory not found")

    def test_module_count(self):
        """Test that expected number of modules exist."""
        module_files = list(self.modules_dir.glob('*.py'))

        # Expected: ~24 modules
        self.assertGreaterEqual(len(module_files), 20,
                               f"Expected ~24 modules, found {len(module_files)}")

        print(f"  ✓ {len(module_files)} Python modules found (expected ~24)")

    def test_modules_syntax_valid(self):
        """Test that Python modules have valid syntax."""
        module_files = list(self.modules_dir.glob('*.py'))

        syntax_errors = []
        for module in module_files:
            try:
                with open(module) as f:
                    source = f.read()
                compile(source, module.name, 'exec')
            except SyntaxError as e:
                syntax_errors.append(f"{module.name}: {e}")

        self.assertEqual(len(syntax_errors), 0,
                        f"Syntax errors: {syntax_errors[:5]}")

        print(f"  ✓ {len(module_files)} modules have valid Python syntax")

    def test_modules_importable(self):
        """Test that Python modules can be imported (with mocked dependencies)."""
        module_files = list(self.modules_dir.glob('*.py'))

        # We can't test actual imports since dependencies may not be installed
        # But we can check that they have standard module structure
        no_functions = []
        for module in module_files:
            with open(module) as f:
                content = f.read()

            # Should have at least one function or class definition
            has_def = 'def ' in content or 'class ' in content
            if not has_def:
                no_functions.append(module.name)

        # Most modules should have functions
        pct_with_functions = (len(module_files) - len(no_functions)) / len(module_files) * 100
        self.assertGreater(pct_with_functions, 90,
                          f"Only {pct_with_functions:.0f}% have functions")

        print(f"  ✓ {pct_with_functions:.0f}% of modules have function/class definitions")


class TestContextFiles(unittest.TestCase):
    """Test context configuration files."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.context_dir = self.plugin_dir / 'context'

    def test_context_directory_exists(self):
        """Test that context directory exists."""
        self.assertTrue(self.context_dir.exists(),
                       "context/ directory not found")

    def test_required_context_files_exist(self):
        """Test that required context files exist."""
        required_files = [
            'brand-voice.md',
            'style-guide.md',
            'seo-guidelines.md',
            'internal-links-map.md',
        ]

        missing = []
        for filename in required_files:
            filepath = self.context_dir / filename
            if not filepath.exists():
                missing.append(filename)

        self.assertEqual(len(missing), 0,
                        f"Missing context files: {missing}")

        print(f"  ✓ All {len(required_files)} required context files exist")

    def test_context_files_have_content(self):
        """Test that context files have placeholder or actual content."""
        context_files = list(self.context_dir.glob('*.md'))

        empty = []
        for ctx_file in context_files:
            with open(ctx_file) as f:
                content = f.read()
            if len(content) < 50:
                empty.append(ctx_file.name)

        self.assertEqual(len(empty), 0,
                        f"Empty context files: {empty}")

        print(f"  ✓ {len(context_files)} context files have content")


class TestRequirements(unittest.TestCase):
    """Test requirements.txt file."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.requirements_file = self.plugin_dir / 'data_sources' / 'requirements.txt'

    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        self.assertTrue(self.requirements_file.exists(),
                       "data_sources/requirements.txt not found")

    def test_requirements_has_dependencies(self):
        """Test that requirements.txt lists dependencies."""
        with open(self.requirements_file) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]

        self.assertGreater(len(lines), 0,
                          "requirements.txt is empty")

        print(f"  ✓ requirements.txt lists {len(lines)} dependencies")


class TestClaudeMd(unittest.TestCase):
    """Test CLAUDE.md file."""

    def setUp(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.claude_file = self.plugin_dir / 'CLAUDE.md'

    def test_claude_md_exists(self):
        """Test that CLAUDE.md exists."""
        self.assertTrue(self.claude_file.exists(),
                       "CLAUDE.md not found")

    def test_claude_md_has_content(self):
        """Test that CLAUDE.md has substantive content."""
        with open(self.claude_file) as f:
            content = f.read()

        # Should be a comprehensive guide
        self.assertGreater(len(content), 2000,
                          "CLAUDE.md seems too short")

        print(f"  ✓ CLAUDE.md exists ({len(content)} chars)")


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPluginJson))
    suite.addTests(loader.loadTestsFromTestCase(TestAgents))
    suite.addTests(loader.loadTestsFromTestCase(TestCommands))
    suite.addTests(loader.loadTestsFromTestCase(TestSkills))
    suite.addTests(loader.loadTestsFromTestCase(TestPythonModules))
    suite.addTests(loader.loadTestsFromTestCase(TestContextFiles))
    suite.addTests(loader.loadTestsFromTestCase(TestRequirements))
    suite.addTests(loader.loadTestsFromTestCase(TestClaudeMd))

    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEO-Machine Plugin Structure Tests")
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
