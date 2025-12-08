---
event: PostToolUse
matchTools:
  - mcp__sales__notion_save_company
  - mcp__sales__notion_update_company
  - mcp__sales__n8n_enrich_company
  - mcp__sales__n8n_enrich_person
---

# Tool Usage Audit

Log this tool execution for compliance tracking:

**Tool**: {{tool_name}}
**Timestamp**: {{timestamp}}
**Input Summary**: Brief description of what was requested
**Output Summary**: Brief description of the result

If this was a Notion operation, note the page URL if available.
If this was an enrichment operation, note the domain/person enriched.

Keep audit logs concise - one line per operation.
