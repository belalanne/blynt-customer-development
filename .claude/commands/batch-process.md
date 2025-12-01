---
description: Process a batch of companies from a file or list
---

**Token Optimization:** Use the Python batch script for syncing to Notion to save ~83% tokens (30k → 5k for 10 companies).

Batch process companies from: {{arg1}}

Steps:
1. Read the company list from:
   - JSON file with company data (recommended for batch operations)
   - CSV file (if path provided)
   - Comma-separated domains (if inline list)
   - data/raw directory (if filename only)

2. For each company:
   - Enrich data
   - Find lookalikes (optional)
   - Discover subprocessors (optional)
   - Add rate limiting delays

3. Store results in data/processed/

4. **Sync all to Notion in batch (Token-Optimized)**
   - Convert enriched data to JSON format
   - Use batch Python script: `.venv/bin/python3 scripts/notion_contact_ops.py batch-create-companies --file data/processed/batch-companies.json`
   - **Token Savings:** ~83% (10 companies: 30k → 5k tokens)

5. Generate summary report:
   - Total companies processed
   - Success/failure rate
   - Common patterns found
   - Next steps

Options:
- {{arg2}}: Operations to run (enrich, lookalikes, subprocessors, or all)

## Batch JSON Format

Create a JSON file with company data:

```json
{
  "companies": [
    {
      "name": "Krisp",
      "website": "https://krisp.ai",
      "linkedin": "https://www.linkedin.com/company/krisp-technologies",
      "vertical": "Voice AI",
      "icp": "3",
      "product_description": "AI noise cancellation for calls",
      "asr_providers": ["Deepgram", "Assembly AI"],
      "ai_engineers": 25,
      "main_office_country": "United States"
    },
    {
      "name": "Modjo",
      "website": "https://modjo.ai",
      "linkedin": "https://www.linkedin.com/company/modjo",
      "vertical": "Sales Intelligence",
      "icp": "2",
      "product_description": "Conversation intelligence for sales teams",
      "asr_providers": ["Deepgram"],
      "ai_engineers": 12,
      "main_office_country": "France"
    }
  ]
}
```

## Example Batch Sync

```bash
# After enrichment, sync all companies to Notion in one call
.venv/bin/python3 scripts/notion_contact_ops.py batch-create-companies \
  --file data/processed/batch-companies.json
```

**Response:**
```json
{
  "success": true,
  "total": 10,
  "created": 7,
  "updated": 3,
  "failed": 0,
  "results": [
    {
      "company": "Krisp",
      "action": "created",
      "page_id": "xxx-xxx-xxx",
      "url": "https://notion.so/xxxxx"
    }
  ]
}
```

If no file is provided, ask for the input source.
