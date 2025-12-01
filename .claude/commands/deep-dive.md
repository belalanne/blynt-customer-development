---
description: Complete deep dive analysis on a company (optimized - single data gathering phase)
---

**OPTIMIZED DEEP-DIVE WORKFLOW**

Perform a complete deep dive analysis on: {{arg1}}

This workflow uses a **single comprehensive data gathering phase** to eliminate redundancy and reduce token usage by ~40-50%.

---

## Phase 1: Comprehensive Data Gathering (ONE TIME ONLY)

Execute ALL research upfront in a single coordinated phase:

### 1.1 Company Basics & Firmographics
- Exa search: Company funding, team, metrics, news
- WebFetch: Company website homepage
- WebSearch: Recent announcements, funding rounds

### 1.2 Business Intelligence
- WebFetch: About page, product pages
- LinkedIn: Employee count, recent hires
- Crunchbase/PitchBook: Funding details

### 1.3 Technology Stack (Deep Dive)
- **Privacy & Security:** /privacy, /security, /subprocessors, /gdpr, /dpa
- **Technical Docs:** /api, /docs, /developers, /integrations
- **Blog:** Technical posts about AI/ML stack
- **Careers:** Job postings mentioning tech (ML Engineer, AI Engineer roles)
- **Partnerships:** Press releases, case studies mentioning vendors
- **Direct Searches:**
  - Exa: "Company ASR provider speech-to-text LLM technology stack"
  - WebSearch: "Company Deepgram OR Assembly AI OR Gladia OR OpenAI OR Anthropic"

### 1.4 Leadership & Team
- Exa: Founder backgrounds, team profiles
- LinkedIn: Key personnel (CEO, CTO, CPO, etc.)
- About page: Leadership team

### 1.5 Market Context
- Competitor research for lookalike criteria
- Industry vertical classification
- Similar companies search

**IMPORTANT:** Store ALL fetched data in session context. Do NOT re-fetch in later phases.

---

## Phase 2: Analysis & Report Generation (Use Cached Data)

### 2.1 Enrichment Report
Generate comprehensive company profile using Phase 1 data:
- Executive summary
- Firmographics (funding, size, location)
- Business overview (product, market, positioning)
- Technology stack (from Phase 1 deep dive)
- Leadership team
- Sales intelligence (pain points, buying signals, timing)
- Source URLs (all from Phase 1)

### 2.2 Lookalike Analysis
Using Phase 1 company profile, identify 10-15 similar companies:
- Use cached vertical/industry classification
- Use cached product description
- Use cached funding stage
- Search for competitors with similar characteristics
- Score by similarity (7-10 range)

### 2.3 Subprocessor Analysis
Using Phase 1 tech stack research, compile findings:
- ASR providers (from Phase 1 searches)
- LLM providers (from Phase 1 searches)
- Meeting recorders (if applicable)
- Audio processing vendors
- Strategic analysis (multi-vendor vs single, build vs buy)
- Competitive intelligence

**DO NOT repeat any web fetches or searches from Phase 1**

---

## Phase 3: Notion Sync

**Token-Optimized Approach:**

Use Python script for database operations:
```bash
.venv/bin/python3 scripts/notion_contact_ops.py create-or-update-company \
  --name "Company Name" \
  --website "https://company.com" \
  --linkedin "https://linkedin.com/company/..." \
  --vertical "Voice AI" \
  --icp "3" \
  --product-desc "5 word description" \
  --asr-providers "Provider1,Provider2 OR Not Disclosed" \
  --ai-engineers NUMBER \
  --country "Country"
```

Then use Notion MCP to add full research content to page.

**Token Savings:** ~13k tokens (87% reduction) vs MCP-only approach

---

## Phase 4: Generate Deep-Dive Report

Create comprehensive markdown report: `logs/deep-dive-{domain}-{YYYY-MM-DD}.md`

Include:
- All enrichment findings
- Lookalike companies table
- Subprocessor analysis
- Source URLs
- Notion page links
- Summary insights
- Recommended next steps

---

## Expected Token Usage

**Optimized:** ~25-30k tokens total
**Previous:** ~47k tokens (40% reduction)

**Breakdown:**
- Phase 1 (Data Gathering): ~18k tokens
- Phase 2 (Analysis): ~7k tokens
- Phase 3 (Notion Sync): ~3k tokens
- Phase 4 (Report): ~2k tokens

**Key Savings:**
- ✅ No redundant web fetches
- ✅ No redundant searches
- ✅ No re-analyzing company basics
- ✅ Python script for Notion (vs MCP)
- ✅ Single comprehensive tech stack search

---

## Implementation Notes

**Session Context Management:**
Store in memory during workflow:
```javascript
{
  company: {
    name, website, linkedin, founded, employees, funding, ...
  },
  techStack: {
    asrProvider, llmProvider, telephony, blog_posts, job_postings, ...
  },
  team: {
    ceo, cto, founders, key_contacts, ...
  },
  webFetches: {
    homepage: "content...",
    blog: "content...",
    careers: "content...",
    privacy: "404 or content...",
  }
}
```

**Conditional Fetching:**
- If privacy page = 404, don't try /security or /subprocessors
- If no blog, skip blog-based tech searches
- If no careers page, skip job posting searches

---

## Progress Tracking

Use TodoWrite to show progress:
1. ⏳ Phase 1: Gathering all company data
2. ⏳ Phase 2: Analyzing and generating reports
3. ⏳ Phase 3: Syncing to Notion
4. ⏳ Phase 4: Creating deep-dive report

Mark phases complete as you finish them.

---

**If no domain provided, ask user which company to analyze.**
