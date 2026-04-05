# Context Link Plugin

Connect Claude to your [Context Link](https://context-link.ai) knowledge base. Retrieve internal knowledge, save conversation insights, and keep your saved content up to date — all from within Claude.

## What it does

- **Get Context** — Pull relevant knowledge from your Context Link when you reference internal topics
- **Save Memory** — Save conversation content to Context Link for later retrieval
- **Update Memory** — Retrieve existing saved content, merge in new information, and save it back

## Components

### Skills (auto-triggered)

| Skill | Triggers when you... |
|-------|---------------------|
| `get-context` | Reference internal knowledge, say "get context" or "use context link" |
| `save-memory` | Say "save this", "remember this", or ask to store information |
| `update-memory` | Say "update memory", "add to {topic}", or want to modify saved content |

### Commands (manual)

| Command | Usage |
|---------|-------|
| `/get-context [topic]` | Retrieve knowledge about a specific topic |
| `/save-memory [slug]` | Save current conversation under a name |
| `/update-memory [slug]` | Update existing saved content with new info |

## Setup

After installing the plugin, you'll need to customize it with your personal Context Link URL:

1. Sign in at [context-link.ai](https://context-link.ai)
2. Your URL is shown at the top of every screen — it looks like `https://yourname.context-link.ai/TOPIC_HERE?p=xyz`
3. Copy and paste it exactly as shown — no editing needed
4. The plugin customizer will ask you to replace `~~context link url~~` with your URL

## How it works

Context Link is a knowledge base that indexes your content (websites, Google Drive, Notion) into searchable embeddings. This plugin lets Claude query that knowledge and save new content back, using Context Link's REST API.

- **GET** `{your-url}/{topic}` — retrieves content matching the topic
- **POST** `{your-url}/{slug}` — saves markdown content under a named slug
