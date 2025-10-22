# Blynt Customer Development - Go-to-Market Intelligence

## Project Overview
This project automates go-to-market intelligence gathering for the **conversation intelligence and speech technology** market. It identifies lookalike companies, enriches company data, discovers AI/speech subprocessors (ASR providers, LLM vendors), and syncs findings to Notion for sales/marketing workflows.

## Target Market
**Primary Focus:** Companies in the conversation intelligence, meeting transcription, and speech technology space.

Key characteristics of target companies:
- B2B SaaS platforms
- Meeting transcription/recording solutions
- Conversation analytics tools
- Sales coaching platforms using AI
- Customer support quality assurance tools
- Speech-to-text API providers
- Voice AI applications

## Architecture

### Core Modules

#### 1. `/src/enrichment`
Enriches company data using multiple data sources:
- Company firmographics (size, industry, location, funding)
- Technology stack detection
- Contact information
- Social media presence

**Key APIs to integrate:**
- Clearbit, Apollo, ZoomInfo, or similar
- LinkedIn Company API
- Built With / Wappalyzer for tech stack

#### 2. `/src/lookalike`
Finds similar companies based on various criteria:
- Industry classification
- Technology stack overlap
- Company size and growth stage
- Geographic location
- Customer segments

**Approach:**
- Feature vector creation from company attributes
- Similarity scoring algorithms (cosine similarity, etc.)
- Clustering for market segmentation

#### 3. `/src/subprocessors`
Discovers and maps out **AI/speech technology subprocessors** (NOT general infrastructure):
- **Speech-to-Text / ASR providers** (Deepgram, Gladia, Assembly AI, Azure Speech, etc.)
- **LLM providers** (OpenAI, Anthropic, Cohere, Google Gemini, etc.)
- **Meeting recording infrastructure** (Recall.ai, Fireflies API, etc.)
- **Audio processing tools** (noise suppression, enhancement)
- **NLP services** (summarization, sentiment analysis)

**Focus areas:**
- Privacy policies and subprocessor lists
- Technical documentation (API docs, developer docs)
- Job postings for AI/ML engineer roles
- Technology partnerships and announcements

**IGNORE:** General hosting, CDN, analytics, marketing tools, payment processors

#### 4. `/src/notion`
Integrates findings into Notion databases:
- Company database
- Enrichment data tables
- Lookalike prospects
- Subprocessor mapping
- Task creation for sales follow-up

**Notion Structure:**
- **Database ID:** `2861bdff7e998000a14edb0bf56a75bf`
- **Database Collection ID:** `collection://20a1bdff-7e99-81b9-badb-000bc5d45f78`

**Required Properties:**
- `Company_Name` (title)
- `Website` (URL) - unique identifier
- `Linkedin Link` (URL)
- `Status / Engagement` (select: "Ice Box", etc.)
- `Vertical` (select: industry/sector)
- `ICP` (select: "1", "2", "3", "N/A")
- `Product description` (text: 5 words)
- `ASR provider` (multi_select: Gladia, Microsoft Azure, Assembly AI, Deepgram, etc.)
- `Nbr of AI/ML/Speech engineer` (number)
- `Main Office Country` (text)

#### 5. `/src/utils`
Shared utilities:
- API client wrappers
- Rate limiting
- Caching layer
- Logging and error handling
- Configuration management

### Data Flow

```
Input Company → Enrichment → [
  → Lookalike Analysis → Notion Sync
  → Subprocessor Discovery → Notion Sync
] → Enriched Notion Database
```

## Configuration

Store API keys and settings in `config/.env`:
```
# Data Enrichment
CLEARBIT_API_KEY=
APOLLO_API_KEY=
LINKEDIN_API_KEY=

# Notion Integration
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=2861bdff7e998000a14edb0bf56a75bf

# Optional
OPENAI_API_KEY=  # For advanced analysis
BUILTWITH_API_KEY=  # For tech stack detection
```

## Available Slash Commands

Use these commands for common workflows:

- `/enrich-company [domain]` - Comprehensive company enrichment with sales intelligence
- `/discover-subprocessors [domain]` - Find AI/speech technology vendors (ASR, LLM providers)
- `/find-lookalikes [domain] [count] [min_score]` - Find similar companies in the space
- `/sync-to-notion [company] [data_type]` - Save research to Notion database
- `/deep-dive [domain]` - Complete analysis workflow (all operations)
- `/batch-process [file] [operations]` - Process multiple companies

## Key Workflows

1. **Single Company Deep Dive**
   - Enrich company data
   - Find lookalikes
   - Discover subprocessors
   - Sync all to Notion

2. **Batch Lookalike Discovery**
   - Start with seed companies
   - Generate lookalike candidates
   - Enrich and score
   - Export to Notion

3. **Subprocessor Mapping**
   - Analyze target company
   - Extract all vendors/subprocessors
   - Research each subprocessor
   - Map relationships in Notion

## Important Research Guidelines

### Source Citation
- **CRITICAL:** Every data point must have a verifiable source URL
- Include specific URLs in all reports (not just domain names)
- Cite: company websites, LinkedIn pages, Crunchbase profiles, job postings, news articles
- Distinguish between confirmed facts and inferred insights

### Subprocessor Discovery Focus
- **ONLY** focus on AI/speech technologies
- Primary goal: Identify ASR provider (Deepgram, Gladia, Assembly AI, etc.)
- Secondary: LLM provider (OpenAI, Anthropic, etc.)
- Ignore: Hosting, CDN, general analytics, marketing tools

### Data Quality
- Prefer official sources (privacy policies, subprocessor lists, API docs)
- Job postings are valuable for tech stack inference
- Note confidence levels (confirmed vs. inferred)
- Check data freshness and last update dates

## Development Guidelines

- Use async/await for API calls
- Implement retry logic with exponential backoff
- Cache API responses to reduce costs
- Log all enrichment operations
- Handle rate limits gracefully
- Store raw data before processing

## Testing Strategy

- Unit tests for each module
- Integration tests with mocked APIs
- End-to-end tests with test Notion workspace
- Rate limit testing

## Next Steps

1. Set up API credentials
2. Create Notion database templates
3. Implement enrichment module
4. Build lookalike algorithm
5. Add subprocessor discovery
6. Create Notion integration
