---
description: Process a batch of companies from a file or list
---

Batch process companies from: {{arg1}}

Steps:
1. Read the company list from:
   - CSV file (if path provided)
   - Comma-separated domains (if inline list)
   - data/raw directory (if filename only)

2. For each company:
   - Enrich data
   - Find lookalikes (optional)
   - Discover subprocessors (optional)
   - Add rate limiting delays

3. Store results in data/processed/

4. Sync all to Notion in batch

5. Generate summary report:
   - Total companies processed
   - Success/failure rate
   - Common patterns found
   - Next steps

Options:
- {{arg2}}: Operations to run (enrich, lookalikes, subprocessors, or all)

If no file is provided, ask for the input source.
