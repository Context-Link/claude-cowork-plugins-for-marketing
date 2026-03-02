# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this plugin.

## Project Overview

SEO Machine is a comprehensive Claude Code plugin for creating long-form, SEO-optimized blog content. It combines custom commands, specialized agents, marketing skills, and Python-based analytics to research, write, optimize, and publish articles for any business.

## Plugin Structure

This plugin follows the Claude Code plugin architecture:
- `agents/` - Specialized analysis agents
- `commands/` - Workflow commands (slash commands)
- `skills/` - Marketing skills and setup wizard
- `context/` - Brand guidelines and configuration
- `data_sources/` - Python analytics modules
- `scripts/` - Python research scripts
- `output/` - Generated content (topics, research, drafts, published)

## Setup

Run `/setup-seo-machine` for an interactive setup wizard, or manually:

```bash
pip install -r data_sources/requirements.txt
```

API credentials are configured in `.env` (GA4, GSC, DataForSEO, WordPress). GA4 service account credentials go in `credentials/ga4-credentials.json`.

## Commands

All commands are defined in `commands/` and invoked as slash commands:

- `/research [topic]` - Keyword/competitor research, generates brief in `output/research/`
- `/write [topic]` - Create full article in `output/drafts/`, auto-triggers optimization agents
- `/rewrite [topic]` - Update existing content, saves to `output/rewrites/`
- `/optimize [file]` - Final SEO polish pass
- `/analyze-existing [URL or file]` - Content health audit
- `/performance-review` - Analytics-driven content priorities
- `/publish-draft [file]` - Publish to WordPress via REST API
- `/article [topic]` - Simplified article creation
- `/priorities` - Content prioritization matrix
- `/scrub [file]` - Remove AI watermarks from content
- `/research-serp`, `/research-gaps`, `/research-trending`, `/research-performance`, `/research-topics` - Specialized research commands
- `/landing-write`, `/landing-audit`, `/landing-research`, `/landing-publish`, `/landing-competitor` - Landing page commands
- `/setup-seo-machine` - Interactive setup wizard

## Architecture

### Command-Agent Model

**Commands** (`commands/`) orchestrate workflows. **Agents** (`agents/`) are specialized roles invoked by commands. After `/write`, these agents auto-run: SEO Optimizer, Meta Creator, Internal Linker, Keyword Mapper.

Key agents: `content-analyzer.md`, `seo-optimizer.md`, `meta-creator.md`, `internal-linker.md`, `keyword-mapper.md`, `editor.md`, `headline-generator.md`, `cro-analyst.md`, `performance.md`, `landing-page-optimizer.md`.

### Marketing Skills

26 marketing skills in `skills/` including:
- Copywriting and copy editing
- CRO (page, form, signup, onboarding, popup, paywall)
- Strategy (content, pricing, launch, marketing ideas)
- Channels (email sequence, social content, paid ads)
- SEO (audit, schema markup, programmatic SEO, competitor alternatives)
- Analytics (tracking, A/B test setup)

### Python Analysis Pipeline

Located in `data_sources/modules/`. The Content Analyzer chains:
1. `search_intent_analyzer.py` - Query intent classification
2. `keyword_analyzer.py` - Density, distribution, stuffing detection
3. `content_length_comparator.py` - Benchmarks against top 10 SERP results
4. `readability_scorer.py` - Flesch Reading Ease, grade level
5. `seo_quality_rater.py` - Comprehensive 0-100 SEO score

### Data Integrations

- `google_analytics.py` - GA4 traffic/engagement data
- `google_search_console.py` - Rankings and impressions
- `dataforseo.py` - SERP positions, keyword metrics
- `data_aggregator.py` - Combines all sources into unified analytics
- `wordpress_publisher.py` - Publishes to WordPress with Yoast SEO metadata

### Opportunity Scoring

`opportunity_scorer.py` uses 8 weighted factors: Volume (25%), Position (20%), Intent (20%), Competition (15%), Cluster (10%), CTR (5%), Freshness (5%), Trend (5%).

## Running Python Scripts

```bash
# Research & analysis scripts (run from scripts/ directory)
python3 scripts/research_quick_wins.py
python3 scripts/research_competitor_gaps.py
python3 scripts/research_performance_matrix.py
python3 scripts/research_priorities_comprehensive.py
python3 scripts/research_serp_analysis.py
python3 scripts/research_topic_clusters.py
python3 scripts/research_trending.py
python3 scripts/seo_baseline_analysis.py
python3 scripts/seo_bofu_rankings.py
python3 scripts/seo_competitor_analysis.py

# Test API connectivity
python3 scripts/test_dataforseo.py
```

## Content Pipeline

`output/topics/` (ideas) -> `output/research/` (briefs) -> `output/drafts/` (articles) -> `output/published/` (final)

Rewrites go to `output/rewrites/`. Landing pages go to `output/landing-pages/`. Audits go to `output/audits/`.

## Context Files

`context/` contains brand guidelines that inform all content generation:
- `brand-voice.md` - Tone, messaging pillars
- `style-guide.md` - Grammar, formatting standards
- `seo-guidelines.md` - Keyword and structure rules
- `internal-links-map.md` - Key pages for internal linking
- `features.md` - Product features
- `competitor-analysis.md` - Competitive intelligence
- `cro-best-practices.md` - Conversion optimization guidelines
- `target-keywords.md` - Keyword research and topic clusters
- `writing-examples.md` - Exemplary blog posts for style reference

## WordPress Integration

Publishing uses the WordPress REST API with a custom MU-plugin (`wordpress/seo-machine-yoast-rest.php`) that exposes Yoast SEO fields. Articles are published in WordPress block format (HTML comments in Markdown files).

## Examples

Check `examples/castos/` for a complete real-world example of all context files filled out for a podcast hosting SaaS company.
