---
description: Search for information using Exa AI (company research, LinkedIn, web search)
argument-hint: <query or domain>
---

# Exa AI Search

Search for: {{arg}}

## Available Exa Tools

Use the appropriate Exa MCP tool based on the query:

### 1. Company Research
For company domains or business intelligence queries:
- **Tool:** `mcp__exa__company_research`
- **Use when:** Looking for company info, firmographics, business data
- **Returns:** Structured company information, news, insights

### 2. LinkedIn Search
For finding people, professionals, or contacts:
- **Tool:** `mcp__exa__linkedin_search`
- **Use when:** Searching for professionals, job titles, company employees
- **Returns:** LinkedIn profiles, professional information

### 3. Web Search
For general queries or research:
- **Tool:** `mcp__exa__web_search_exa`
- **Use when:** General information, articles, documentation
- **Returns:** Relevant web results with summaries

### 4. Deep Research
For complex multi-source research:
- **Tool:** `mcp__exa__deep_researcher_start` then `mcp__exa__deep_researcher_check`
- **Use when:** Comprehensive analysis requiring multiple sources
- **Returns:** Aggregated insights from multiple sources

## Task Instructions

1. **Analyze the query** to determine which Exa tool is most appropriate
2. **Execute the search** using the selected Exa tool
3. **Format results** in a clear, structured way with:
   - Key findings
   - Relevant data points
   - Source URLs
   - Confidence/quality indicators

## Output Format

```
🔍 Exa Search Results: [Query]

Tool Used: [company_research | linkedin_search | web_search_exa | deep_research]

## Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

## Detailed Results
[Structured information from Exa]

## Sources
- [URL 1]
- [URL 2]

## Next Steps
[Suggested actions based on findings]
```

## Examples

### Example 1: Company Research
```bash
/exa-search gladia.io
```
Uses: `company_research`
Returns: Company info, tech stack, funding, team size

### Example 2: LinkedIn Search
```bash
/exa-search "CEO at Deepgram"
```
Uses: `linkedin_search`
Returns: Professional profiles matching criteria

### Example 3: Web Search
```bash
/exa-search "speech recognition API comparison"
```
Uses: `web_search_exa`
Returns: Relevant articles and documentation

## Notes

- Exa provides high-quality, AI-optimized search results
- Results are token-efficient and reduce hallucinations
- Always cite sources from Exa results
- If Exa MCP is not available, fall back to WebSearch tool
