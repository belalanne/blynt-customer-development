---
description: Complete deep dive analysis on a company (enrich + lookalikes + subprocessors + sync)
---

Perform a complete deep dive analysis on: {{arg1}}

This is a comprehensive workflow that combines multiple operations:

1. **Enrich Company Data**
   - Gather firmographics
   - Detect tech stack
   - Find contact info

2. **Find Lookalike Companies**
   - Identify similar companies
   - Score by similarity
   - Enrich top matches

3. **Discover Subprocessors**
   - Map all vendors
   - Categorize by type
   - Document data flow

4. **Sync to Notion**
   - Create company page
   - Link lookalikes
   - Map subprocessor relationships

5. **Generate Report**
   - Summary of findings
   - Key insights
   - Recommended actions
   - Save markdown report to logs folder (logs/deep-dive-{company}-{timestamp}.md)

If no domain is provided, ask the user which company to analyze.

Progress through each step, showing results before moving to the next.

**IMPORTANT:** After completing all steps, create a comprehensive markdown report in the logs folder with filename format: `logs/deep-dive-{domain}-{YYYY-MM-DD}.md`

The report should include:
- Company overview and firmographics
- Technology stack details
- Key contacts found
- Top lookalike companies with scores
- Subprocessors discovered (ASR providers, LLM vendors, etc.)
- All findings with source URLs
- Summary insights and recommendations
- Links to Notion pages created
