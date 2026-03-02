# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for values that each user needs to customize. This plugin uses one placeholder for your personal Context Link URL.

## Connectors for this plugin

| Category | Placeholder | What to replace it with |
|----------|-------------|------------------------|
| Context Link URL | `~~context link url~~` | Your personal Context Link URL as shown at the top of every screen (e.g. `https://oli.context-link.ai/TOPIC_HERE?p=xyz`) |

## How to get your URL

Your Context Link URL is displayed at the top of every screen when you're signed in. It looks like this:

```
https://yourname.context-link.ai/TOPIC_HERE?p=xyz
```

Just copy and paste it exactly as shown — no need to edit it. The URL may contain `TOPIC_HERE` or `{SLUG}` as the path placeholder; either is fine. The plugin will automatically replace it with the actual topic at runtime.
