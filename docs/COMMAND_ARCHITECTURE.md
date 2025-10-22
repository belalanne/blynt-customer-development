# Command Architecture & Interactions

This diagram shows how all slash commands interact with each other and with external data sources.

## Command Interaction Flow

```mermaid
graph TB
    %% User Entry Points
    User([User Input])

    %% Core Commands
    Enrich[/enrich-company<br/>Domain/Name]
    MapICP[/map-icp<br/>Domain/Name]
    FindLook[/find-lookalikes<br/>Domain]
    DiscSub[/discover-subprocessors<br/>Domain]
    AddContact[/add-contact<br/>Domain/Name]
    FindEmail[/find-email<br/>Contact/Company]
    SyncNotion[/sync-to-notion<br/>Company + Data]

    %% Orchestration Commands
    DeepDive[/deep-dive<br/>Domain]
    BatchProc[/batch-process<br/>File/List]

    %% External Data Sources
    WebSearch((Web Search))
    LinkedIn((LinkedIn))
    Crunchbase((Crunchbase))
    ExaMCP((Exa AI MCP))
    HunterAPI((Hunter.io API))
    ApolloAPI((Apollo.io API))

    %% Notion Database
    NotionCompanies[(Notion<br/>Companies DB)]
    NotionPeople[(Notion<br/>People DB)]

    %% Data Storage
    LogsFolder[/logs/<br/>Reports]
    DataProcessed[/data/processed/<br/>Cached Data]

    %% User to Commands
    User --> Enrich
    User --> MapICP
    User --> FindLook
    User --> DiscSub
    User --> AddContact
    User --> FindEmail
    User --> SyncNotion
    User --> DeepDive
    User --> BatchProc
    User --> ExaSearch[/exa-search<br/>Query]

    %% Deep Dive Orchestration
    DeepDive --> |1. Enrich| Enrich
    DeepDive --> |2. Find Similar| FindLook
    DeepDive --> |3. Map Vendors| DiscSub
    DeepDive --> |4. Save All| SyncNotion
    DeepDive --> |5. Generate| LogsFolder

    %% Batch Process Orchestration
    BatchProc --> |Per Company| Enrich
    BatchProc --> |Optional| FindLook
    BatchProc --> |Optional| DiscSub
    BatchProc --> |Bulk Sync| SyncNotion
    BatchProc --> |Cache| DataProcessed

    %% Exa Search Flow
    ExaSearch --> ExaMCP

    %% Enrich Company Flow
    Enrich --> |Priority| ExaMCP
    Enrich --> |Fallback| WebSearch
    Enrich --> LinkedIn
    Enrich --> Crunchbase
    Enrich --> NotionCompanies

    %% Map ICP Flow
    MapICP --> |May call| Enrich
    MapICP --> NotionCompanies

    %% Find Lookalikes Flow
    FindLook --> |Analyze Target| Enrich
    FindLook --> WebSearch
    FindLook --> |Enrich Each| Enrich
    FindLook --> NotionCompanies

    %% Discover Subprocessors Flow
    DiscSub --> WebSearch
    DiscSub --> |Check Privacy| WebSearch
    DiscSub --> NotionCompanies

    %% Add Contact Flow
    AddContact --> |Find Company| NotionCompanies
    AddContact --> |Check Duplicates| NotionPeople
    AddContact --> |Priority| ExaMCP
    AddContact --> |Fallback| WebSearch
    AddContact --> |Fallback| LinkedIn
    AddContact --> |Email Discovery| HunterAPI
    AddContact --> |Email Discovery| ApolloAPI
    AddContact --> NotionPeople

    %% Find Email Flow
    FindEmail --> |Get Contacts| NotionPeople
    FindEmail --> WebSearch
    FindEmail --> HunterAPI
    FindEmail --> ApolloAPI
    FindEmail --> |Update| NotionPeople

    %% Sync to Notion Flow
    SyncNotion --> |Check Duplicates| NotionCompanies
    SyncNotion --> |Save/Update| NotionCompanies

    %% Styling
    classDef userEntry fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef coreCmd fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef orchCmd fill:#f3e5f5,stroke:#4a148c,stroke-width:3px
    classDef external fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef exaMcp fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    classDef database fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef storage fill:#f1f8e9,stroke:#33691e,stroke-width:2px

    class User userEntry
    class Enrich,MapICP,FindLook,DiscSub,AddContact,FindEmail,SyncNotion,ExaSearch coreCmd
    class DeepDive,BatchProc orchCmd
    class WebSearch,LinkedIn,Crunchbase,HunterAPI,ApolloAPI external
    class ExaMCP exaMcp
    class NotionCompanies,NotionPeople database
    class LogsFolder,DataProcessed storage
```

## Command Categories

### 1. Core Research Commands
Individual operations for specific research tasks:

- **`/exa-search`** - AI-powered search using Exa
  - Input: Query or domain
  - Output: Structured search results with sources
  - Uses: Exa MCP (company_research, linkedin_search, web_search_exa)
  - Purpose: Testing and standalone searches

- **`/enrich-company`** - Gather comprehensive company data
  - Input: Domain or company name
  - Output: Firmographics, tech stack, contacts, funding
  - Uses: **Exa MCP (priority)**, Web search, LinkedIn, Crunchbase
  - Saves to: Notion Companies DB

- **`/map-icp`** - Classify company into ICP 1, 2, 3, or N/A
  - Input: Domain or company name
  - Output: ICP classification with reasoning
  - May call: `/enrich-company` if data needed
  - Saves to: Notion Companies DB (ICP field)

- **`/find-lookalikes`** - Find similar companies
  - Input: Domain, count (15), min score (7/10)
  - Output: List of similar companies with scores
  - Uses: `/enrich-company` for target analysis
  - Saves to: Notion Companies DB (linked)

- **`/discover-subprocessors`** - Find AI/speech vendors
  - Input: Domain
  - Output: ASR providers, LLM vendors, speech tech
  - Uses: Privacy policies, job postings, tech docs
  - Saves to: Notion Companies DB (ASR provider field)

### 2. Contact Management Commands
Focus on people and email discovery:

- **`/add-contact`** - Research and add contacts
  - Input: Domain or company name
  - Output: New contacts with emails
  - Uses: **Exa LinkedIn search (priority)**, LinkedIn, Hunter.io, Apollo.io
  - Checks: Duplicates by LinkedIn URL
  - Saves to: Notion People DB

- **`/find-email`** - Find emails for existing contacts
  - Input: Contact name or company
  - Output: Email addresses with confidence scores
  - Uses: Web search, Hunter.io, Apollo.io
  - Updates: Notion People DB

### 3. Data Management Commands

- **`/sync-to-notion`** - Save research to Notion
  - Input: Company + data type (all/company/lookalikes/subprocessors)
  - Output: Notion pages created/updated
  - Checks: Duplicates by Website URL
  - Saves to: Notion Companies DB

### 4. Orchestration Commands
High-level workflows that combine multiple commands:

- **`/deep-dive`** - Complete company analysis
  - Workflow:
    1. `/enrich-company` - Gather data
    2. `/find-lookalikes` - Find similar companies
    3. `/discover-subprocessors` - Map vendor ecosystem
    4. `/sync-to-notion` - Save everything
    5. Generate markdown report → `logs/`
  - Output: Comprehensive report + Notion pages

- **`/batch-process`** - Process multiple companies
  - Input: CSV file or comma-separated list
  - Workflow:
    1. For each company: `/enrich-company`
    2. Optional: `/find-lookalikes`
    3. Optional: `/discover-subprocessors`
    4. Rate limiting delays
    5. Bulk `/sync-to-notion`
    6. Summary report
  - Output: Processed data in `data/processed/`

## Data Flow Patterns

### Pattern 1: Single Company Research
```
User → /enrich-company → Web Research → Notion Companies DB
```

### Pattern 2: Contact Discovery
```
User → /add-contact →
  ├─ Find Company in Notion
  ├─ Check People DB for duplicates
  ├─ Research contacts (LinkedIn, Web)
  ├─ Discover emails (Hunter.io, Apollo.io)
  └─ Create in Notion People DB
```

### Pattern 3: Complete Analysis (Deep Dive)
```
User → /deep-dive →
  ├─ /enrich-company → Notion
  ├─ /find-lookalikes → Notion (linked)
  ├─ /discover-subprocessors → Notion (ASR field)
  ├─ /sync-to-notion → Verify all saved
  └─ Generate Report → logs/
```

### Pattern 4: Batch Processing
```
User → /batch-process [file.csv] →
  ├─ Read companies from file
  ├─ For each: /enrich-company
  ├─ For each: /find-lookalikes (optional)
  ├─ For each: /discover-subprocessors (optional)
  ├─ Cache in data/processed/
  ├─ /sync-to-notion (bulk)
  └─ Summary report
```

## External Dependencies

### Required APIs
- **Notion API** - Database access (required)
  - Companies DB: `2861bdff7e998000a14edb0bf56a75bf`
  - People DB: `collection://20a1bdff-7e99-81a7-8612-000b6f8a32f4`

### Recommended APIs (Enhanced Performance)
- **Exa AI MCP** - AI-powered search and research (HIGHLY RECOMMENDED)
  - Company research with structured data
  - LinkedIn search for contacts
  - Web search with better quality results
  - Setup: Add to `.mcp.json` with API key
  - Benefits: Faster, more accurate, token-efficient
  - Used by: `/enrich-company`, `/add-contact`, `/exa-search`

### Optional APIs (for enhanced features)
- **Hunter.io** - Email discovery (25 free/month)
- **Apollo.io** - Contact enrichment (50 free/month)
- **Clearbit/Apollo** - Company enrichment (optional)
- **BuiltWith** - Tech stack detection (optional)

### Free Data Sources (Always Used)
- Web Search - Company research
- LinkedIn - Company pages, contacts
- Crunchbase - Funding, team data
- Company websites - Team pages, privacy policies

## Duplicate Detection Strategy

### Companies
- **Unique Key:** Website URL (normalized)
- **Check Before:** Creating in Notion
- **Commands:** `/enrich-company`, `/sync-to-notion`

### People
- **Unique Key:** LinkedIn URL (primary)
- **Fallback:** Name + Company (less reliable)
- **Check Before:** Creating contacts
- **Commands:** `/add-contact`, `/find-email`

## Command Dependencies

### No Dependencies
- `/enrich-company` - Standalone
- `/map-icp` - Standalone (may call enrich)
- `/find-email` - Standalone

### Requires Company Data
- `/find-lookalikes` - Needs target company data
- `/discover-subprocessors` - Needs company domain
- `/add-contact` - Requires company in Notion DB first

### Orchestration (Multi-Command)
- `/deep-dive` - Calls: enrich → lookalikes → subprocessors → sync
- `/batch-process` - Calls: enrich (+ optional: lookalikes, subprocessors) → sync

## Best Practices

### Recommended Workflow
1. **New Company Research:**
   ```
   /enrich-company domain.com
   /map-icp domain.com
   /discover-subprocessors domain.com
   /sync-to-notion domain.com all
   ```

2. **Add Contacts After Enrichment:**
   ```
   /add-contact domain.com
   ```

3. **Find Similar Companies:**
   ```
   /find-lookalikes domain.com 20
   ```

4. **Complete Analysis:**
   ```
   /deep-dive domain.com
   ```

5. **Bulk Processing:**
   ```
   /batch-process companies.csv all
   ```

## Output Locations

- **Notion Companies DB** - All company data, lookalikes, subprocessors
- **Notion People DB** - Contacts with emails
- **`logs/`** - Deep dive reports, analysis summaries
- **`data/processed/`** - Cached batch processing results
