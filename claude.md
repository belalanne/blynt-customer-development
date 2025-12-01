# Blynt Customer Development - Go-to-Market Intelligence

## Project Overview
This project automates go-to-market intelligence gathering for companies building **real-time voice and speech products**. It identifies lookalike companies, enriches company data, discovers their real-time voice infrastructure (transport protocols, frameworks, agentic platforms, and speech stack), and syncs findings to Notion for sales/marketing workflows.

## Blynt's Product
**Real-time Transcription API** with advanced features:
- **Built-in Natural turn-taking** - Seamless conversation flow
- **Large scale Keyword Boosting** - Custom vocabulary enhancement
- **Run-time Contextualization** - Dynamic context adaptation
- **Interruption Handling** - Robust handling of conversation overlaps

## Target Market & ICP Classification

### ICP #1: Speech/Dictation Products
Companies that want to add **speech or dictation capabilities** to their product:
- Healthcare documentation (medical dictation)
- Legal transcription tools
- Note-taking applications
- Productivity apps with voice input
- Accessibility features (voice control)

**Key signals**: Building dictation features, medical/legal transcription, voice-to-text in apps

### ICP #2: Meeting AI Assistants
Companies building **meeting assistants with AI capabilities**:
- Meeting transcription platforms (Otter.ai, Fireflies.ai, tldv, Grain)
- Sales call intelligence (Gong, Chorus, Jiminny)
- Customer support QA (Observe.AI, Mindtickle)
- Collaboration tools with AI note-taking

**Key signals**: Real-time meeting transcription, AI summaries, conversation analytics

### ICP #3: Voice Agents Platforms/Products
Companies building **voice agent platforms or voice-enabled products**:
- AI phone assistants (Bland AI, Air.ai, Vapi)
- Voice-enabled customer support
- AI receptionists (Beside, Goodcall)
- Conversational AI platforms
- Voice bots for scheduling/ordering

**Key signals**: Conversational AI, voice agents, AI phone systems, real-time voice interactions

### ICP #4: Custom Speech/Voice Solutions
Companies that want **fully customized speech/voice products**:
- Enterprise voice infrastructure
- Proprietary voice AI platforms
- White-label voice solutions
- Industry-specific voice applications (finance, healthcare, government)

**Key signals**: Custom ASR models, proprietary voice tech, enterprise voice infrastructure

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
Discovers and maps out **real-time voice infrastructure and technology stack** (NOT general infrastructure):

**Real-Time Infrastructure:**
- **Transport Protocol**: WebRTC, WebSockets, SIP, PSTN
- **Real-time Framework**: LiveKit, Pipecat, FastRTC, Daily, Agora, Twilio
- **Agentic Framework**: Vapi, LiveKit Agents, Pipecat Flow, Retell, Vocode

**Speech Stack:**
- **ASR providers** (Deepgram, Gladia, Assembly AI, Azure Speech, Google Speech, Whisper)
- **LLM providers** (OpenAI, Anthropic, Cohere, Google Gemini, Azure OpenAI)
- **TTS providers** (ElevenLabs, Play.ht, Azure TTS, Google TTS, OpenAI TTS, Deepgram Aura)

**Supporting Infrastructure:**
- **Meeting recording** (Recall.ai, Fireflies API, Tactiq)
- **Audio processing** (Krisp, Dolby.io, noise suppression)
- **Telephony** (Twilio Voice, Vonage, Bandwidth, SignalWire)

**Research Focus Areas:**
- Privacy policies and subprocessor lists
- Technical documentation (API docs, developer docs, SDKs)
- Job postings mentioning specific tech (WebRTC engineer, LiveKit, Pipecat, etc.)
- GitHub repositories and open-source projects
- Technology partnerships and vendor announcements
- Blog posts about technical architecture

**IGNORE:** General hosting, CDN, analytics, marketing tools, payment processors, databases

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

### Real-Time Voice Infrastructure Discovery

**Priority 1: Transport & Framework**
- Identify transport protocol: WebRTC, WebSockets, SIP
- Identify real-time framework: LiveKit, Pipecat, Daily, Agora, Twilio
- Identify agentic framework: Vapi, LiveKit Agents, Pipecat Flow, Retell, Vocode

**Priority 2: Speech Stack**
- ASR provider: Deepgram, Gladia, Assembly AI, Azure Speech, Whisper
- LLM provider: OpenAI, Anthropic, Google Gemini, Azure OpenAI
- TTS provider: ElevenLabs, Play.ht, Deepgram Aura, Azure TTS

**Priority 3: Supporting Infrastructure**
- Telephony: Twilio, Vonage, Bandwidth, SignalWire
- Meeting recording: Recall.ai, Fireflies API
- Audio processing: Krisp, Dolby.io

**Key Research Indicators:**
- Job postings: "WebRTC engineer", "LiveKit", "Pipecat", "Voice AI engineer"
- Technical blog posts: Architecture diagrams, tech stack discussions
- GitHub repos: Open-source integrations, SDKs used
- API documentation: WebSocket endpoints, real-time APIs
- Privacy policies: List of AI/speech subprocessors

**Ignore:** Hosting (AWS, GCP), CDN (Cloudflare), analytics (Google Analytics), marketing tools, payment processors, databases

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
