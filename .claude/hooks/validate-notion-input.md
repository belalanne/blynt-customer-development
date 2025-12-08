---
event: PreToolUse
matchTools:
  - mcp__sales__notion_save_company
---

# Validate Notion Save Input

Before saving to Notion, verify:

1. **company_name** is provided and not empty
2. **website** is a valid URL format
3. **icp** if provided, must be "1", "2", "3", "4", or "N/A"
4. **product_description** if provided, should be 5 words or less

If any validation fails, respond with:
```
BLOCK: [reason for blocking]
```

If all validations pass, respond with:
```
ALLOW
```
