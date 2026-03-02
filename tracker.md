I want to put together a 'marketplace called "Claude Cowork plugins for Marketing".
Official plugins doc here: https://code.claude.com/docs/en/plugins.md
Official plugins marketplace doc here: https://code.claude.com/docs/en/plugin-marketplaces

This directory stores the plugins for the market place.
My intention is to include our plugin (Context Link), but also other marketing plugins from the community.
We need to convert the below repos to Plugins so they can use Claude Cowork.
When we put together this gallery it's important to link to the official source for each plugin. I want this to be a curated list of high-quality plugins, not us replacing/stealing the official sources.

I've started the marketplace file here /.claude-plugin/marketplace.json
And the plugins are in ./plugins

We will use this folder to track the plugins we want to include in the market place.


## Plugin List

### Context Link
Ready to include: true
official URL: https://github.com/oliwoodsuk/context-link-plugin

- name: context-link
- description: Connect Claude to your Context Link knowledge base. Retrieve internal knowledge, save conversation insights, and keep your saved content up to date.
- version: 1.0.0

### marketing (by-anthropic)
Ready to include: true
official URL: https://github.com/anthropics/knowledge-work-plugins/tree/main/marketing

- name: marketing
- description: Create content, plan campaigns, and analyze performance across marketing channels. Maintain brand voice consistency, track competitors, and report on what's working.
- version: 1.1.0

### Marketing Skills (By Corey of Conversion Factory)
Ready to include: true
official URL: https://github.com/coreyhaines31/marketingskills (Coreys marketplace: https://github.com/coreyhaines31/marketingskills/blob/main/.claude-plugin/marketplace.json)

- name: marketing-skills
- description: A comprehensive collection of 25+ marketing skills and tactics for conversion-focused marketers. Includes expert guidance on copywriting, cold email outreach, marketing psychology (70+ mental models), pricing strategy, SEO audits, content strategy, social media content, email sequences, CRO, A/B testing, analytics tracking, paid advertising, sales enablement, and more.
- version: 1.0.0

### dataforseo
Ready to include: true
Based on: https://github.com/nikhilbhansali/dataforseo-skill-claude (significantly modified)

- name: dataforseo
- description: Complete DataForSEO API integration with 8 specialized skills: keyword research, SERP analysis, backlink analysis, competitor analysis, technical SEO, content analysis, and Google Trends.
- version: 1.0.0

Skills included (all tested against real API):
1. `setup-dataforseo` - Credential setup and verification
2. `keyword-research` - Search volume, CPC, competition, keyword ideas
3. `serp-analysis` - Google, Bing, YouTube organic results
4. `backlink-analysis` - Backlink profiles, referring domains, domain authority
5. `competitor-analysis` - Keyword gaps, competing domains, link gaps
6. `technical-seo` - Lighthouse audits, page analysis, technology detection
7. `content-analysis` - Brand mentions, sentiment analysis
8. `google-trends` - Search interest over time, trending topics

Test results: 8/8 skills passed (tested against context-link.ai)

### seo-machine-skills(by-craig-hewitt)
Ready to include: true
official URL: https://github.com/TheCraigHewitt/seomachine

- name: seo-machine
- description: A comprehensive Claude Code workspace for creating long-form, SEO-optimized blog content. Features custom commands for research, writing, and optimization workflows; specialized agents for content analysis, SEO optimization, meta creation, and internal linking; 26 marketing skills; Python-based SEO analysis modules; and data integrations with Google Analytics 4, Search Console, and DataForSEO.
- version: 1.0.0

Note: Converted full git repo to plugin structure. Includes /setup-seo-machine skill for guided setup.


## Changelog

### 2026-03-02 (Testing)
- **Created comprehensive test suites for all 4 remaining plugins:**

#### Context-Link Plugin Tests (9/9 passed)
- Location: `plugins/context-link(by-context-link)/tests/test_context_link.py`
- API tests: GET context, POST save memory, update memory, error handling
- Structure tests: plugin.json, SKILL.md frontmatter, CONNECTORS.md

#### Marketing Plugin Tests (20/20 passed)
- Location: `plugins/marketing(by-anthropic)/tests/test_marketing_structure.py`
- Structure tests: plugin.json, .mcp.json (11 MCP servers)
- Content tests: 7 commands, 5 skills with valid frontmatter
- Cross-reference tests: all commands reference CONNECTORS.md

#### Marketing-Skills Plugin Tests (19/19 passed)
- Location: `plugins/marketing-skills(by-conversion-factory)/tests/test_marketing_skills.py`
- Structure tests: 32 SKILL.md files, 51 CLI tools, 58 integration guides
- Syntax tests: All 51 CLI tools pass Node.js syntax check
- Content tests: REGISTRY.md (16,589 chars)

#### SEO-Machine Plugin Tests (30/30 passed, 2 skipped)
- Structure tests (25/25): `plugins/seo-machine(by-craig-hewitt)/tests/test_structure.py`
  - 10 agents, 20 commands, 27 skills, 24 Python modules
  - All Python modules pass syntax validation
  - Context files, requirements.txt, CLAUDE.md validated
- Integration tests (5/5, 2 skipped): `plugins/seo-machine(by-craig-hewitt)/tests/test_integrations.py`
  - DataForSEO: 4/4 passed (connection, keyword API, SERP API)
  - GA4: Skipped (credentials file not found)
  - GSC: Skipped (credentials file not found)
  - Core modules: 5/5 imported successfully

**Total: 78 tests passed, 2 skipped (due to missing GA4/GSC credentials)**

### 2026-03-02
- Created plugin.json manifests for all 5 plugins
- Converted dataforseo from single SKILL.md to proper plugin structure
- Converted seo-machine from nested .claude/ directory to root-level plugin structure
- Added /setup-seo-machine skill for guided setup wizard
- Updated marketplace.json with all 5 plugins including categories and tags
- **Split dataforseo into 8 specialized skills:**
  - setup-dataforseo, keyword-research, serp-analysis, backlink-analysis
  - competitor-analysis, technical-seo, content-analysis, google-trends
- Renamed dataforseo folder (removed nikhil-bhansali suffix)
- Updated authorship to Context Link
- **Tested all 8 dataforseo skills against real API** - 8/8 passed
- All plugins now ready to publish
