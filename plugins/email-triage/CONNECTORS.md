# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~email provider` might mean Gmail, Zoho Mail, or any other email service with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Email provider | `~~email provider` | Gmail, Zoho Mail | Outlook (when MCP available) |
| Knowledge base | `~~knowledge base` | Context Link | Notion, Confluence |
