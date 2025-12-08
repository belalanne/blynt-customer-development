# Blynt Customer Development - Sales Research Assistant

## Overview

AI-powered sales research assistant for Blynt, automating company research, technology stack discovery, and Notion synchronization. Built with Claude Code slash commands and Python tools.

## Blynt's Product

**Real-time Transcription API** with advanced features:
- Built-in natural turn-taking
- Large-scale keyword boosting
- Run-time contextualization
- Interruption handling

## Target Market (ICP)

| ICP | Type | Examples | Key Signals |
|-----|------|----------|-------------|
| 1 | Speech/Dictation | Medical dictation, legal transcription, note apps | Voice-to-text input, accessibility |
| 2 | Meeting AI | Otter.ai, Fireflies, Gong, tldv | Meeting transcription, call analytics |
| 3 | Voice Agents | Vapi, Bland AI, Retell, Air.ai | AI phone, voice bots, conversational AI |
| 4 | Custom Solutions | Enterprise voice infrastructure | White-label, regulated industries |
| N/A | Not a fit | No voice/speech use case | Text-only AI, hardware |

## Project Structure

```
blynt-customer-development/
├── .claude/
│   ├── commands/           # Slash commands (3 core)
│   │   ├── research.md     # /research <domain> (main)
│   │   ├── find-lookalikes.md
│   │   └── discover-stack.md
│   ├── agents/             # Subagents
│   ├── skills/             # Domain knowledge
│   │   ├── icp-classification/
│   │   └── voice-tech-stack/
│   └── hooks/              # Event hooks
├── src/                    # Python tools
│   ├── agent.py            # Main agent
│   ├── config.py           # Configuration
│   └── tools/              # API integrations
├── scripts/                # Standalone CLI tools
├── research/               # Deep-dive outputs
├── docs/                   # ICP guides, changelogs
├── main.py                 # CLI entry point
└── .env                    # API keys
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/research <domain>` | **Main command** - Interactive research with depth choice (Quick/Standard/Deep) |
| `/find-lookalikes <domain>` | Find similar companies using Exa |
| `/discover-stack <domain>` | Deep tech stack analysis (ASR/TTS/LLM) |

## Tool Priority Strategy

When researching companies, use tools in this order:

### 1. n8n Webhooks (fastest, structured)
```bash
curl -X POST "https://n8n-dev.blynt.ai/webhook/enrich-company" \
  -d '{"domain": "example.com"}'
```

### 2. Tavily (best for company research)
- `tavily_search` - Company discovery with AI summaries
- `tavily_extract` - Deep page content extraction

### 3. Exa (best for lookalikes)
- `exa_search` - Neural search with metadata
- `exa_find_similar` - Find competitor companies

### 4. WebSearch (fallback)
- Built-in Claude web search
- Free, unlimited, good summaries

## Voice Tech Stack Focus

### Priority 1: Real-Time Infrastructure
- Transport: WebRTC, WebSockets, SIP, PSTN
- Framework: LiveKit, Pipecat, Daily, Agora, Twilio
- Agentic: Vapi, LiveKit Agents, Retell, Vocode

### Priority 2: Speech Stack
- ASR: Deepgram, Gladia, Assembly AI, Azure Speech
- LLM: OpenAI, Anthropic, Google Gemini
- TTS: ElevenLabs, Play.ht, Deepgram Aura

### IGNORE
AWS, GCP, Cloudflare, analytics, marketing tools, payment processors

## Research Sources

1. **Privacy policies** - Subprocessor lists
2. **Job postings** - Technology requirements
3. **Technical docs** - API documentation
4. **GitHub** - SDK integrations
5. **Blog posts** - Architecture discussions

## Notion Database Schema

### Companies Database
| Property | Type | Description |
|----------|------|-------------|
| `Company_Name` | title | Official company name |
| `Website` | URL | Unique identifier |
| `Linkedin Link` | URL | Company LinkedIn |
| `Vertical` | select | Industry/sector |
| `ICP` | select | 1, 2, 3, 4, or N/A |
| `Product description` | text | 5 words max |
| `ASR provider` | multi_select | ASR providers used |
| `Main Office Country` | text | HQ location |

### People Database
| Property | Type |
|----------|------|
| `Contact_Name` | title |
| `Role` | text |
| `LinkedIn URL` | URL |
| `Email` | email |
| `Company name` | relation |

## Environment Variables

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Search APIs
EXA_API_KEY=...
TAVILY_API_KEY=...

# Notion
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=20a1bdff7e9980c48f85c663fa70c2f2
NOTION_PEOPLE_DATABASE_ID=20a1bdff7e9980fb9d3cdfbfa7a8bd70

# n8n
N8N_API_URL=https://n8n-dev.blynt.ai/api/v1
N8N_API_KEY=...
N8N_WEBHOOK_COMPANY=https://n8n-dev.blynt.ai/webhook/enrich-company
N8N_WEBHOOK_PEOPLE=https://n8n-dev.blynt.ai/webhook/enrich-people
```

## Usage

### Claude Code (Interactive Research)
```bash
# Main command - choose depth interactively
/research vapi.ai

# Find similar companies
/find-lookalikes otter.ai

# Deep tech stack analysis
/discover-stack bland.ai
```

### Python CLI
```bash
python main.py                    # Interactive mode
python main.py research vapi.ai   # Research company
python main.py lookalikes vapi.ai # Find lookalikes
```

### n8n Agent
- Chat: https://n8n-dev.blynt.ai/webhook/sales-agent-chat/chat
- Workflow: https://n8n-dev.blynt.ai/workflow/FvYfJuQqEUKNkJfe

## Interactive Clarifications

Use **AskUserQuestion** when:
- Multiple companies match a search
- ICP classification is ambiguous
- Before saving to Notion (confirm details)
- Data conflicts between sources
