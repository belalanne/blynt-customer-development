# Deep Dive Analysis: Rounded (callrounded.com)

**Report Generated:** November 6, 2025
**Analysis Type:** Complete Deep Dive (Enrichment + Lookalikes + Subprocessors)
**Target Company:** Rounded (callrounded.com)

---

## Executive Summary

**Rounded** is a French AI voice agent orchestration platform that enables businesses to build, deploy, and manage custom AI voice agents. Founded in 2022 by three co-founders (Aymeric Vaudelin, Mathieu Diaz, and Yassine M'hamdi), the company pivoted from web3 to voice AI in June 2023. They achieved early product-market fit with **Donna**, an AI voice assistant for hospital appointment scheduling serving 15 private hospitals and processing hundreds of thousands of conversations.

**Key Strengths:**
- ✅ Strong early traction in healthcare vertical
- ✅ €600K pre-seed funding from prestigious Berkeley SkyDeck
- ✅ Impressive technical performance (<700ms latency)
- ✅ Platform approach (not locked to single provider)
- ✅ Recent product expansion (January 2025 TechCrunch coverage)

**ICP Fit:** **3** - Early-stage B2B SaaS in competitive but growing market

---

## Company Enrichment Report

### Firmographics

| Field | Value |
|-------|-------|
| **Legal Name** | Rounded (formerly Rounded Technologies) |
| **Website** | https://callrounded.com |
| **LinkedIn** | https://www.linkedin.com/company/callrounded |
| **GitHub** | https://github.com/callRounded |
| **HQ Location** | Paris, France |
| **Founded** | 2022 |
| **Company Size** | 2-10 employees |
| **Industry** | AI Voice Technology / Conversational AI Platform |
| **Funding Stage** | Pre-Seed |
| **Total Funding** | €600,000 (~$620,000 USD) |
| **Investors** | Berkeley SkyDeck Fund, 212Founders, business angels |
| **Estimated Revenue** | Not publicly disclosed |

### Business Overview

#### What They Do
Rounded is an orchestration platform for assembling, deploying, and managing AI voice agents. Unlike competitors that provide ready-made voice agents, Rounded allows businesses to build custom voice agents by selecting their preferred AI models for speech-to-text, language processing (LLM), and text-to-speech.

#### Business Model
**B2B SaaS Platform** - Subscription-based platform with API access

The platform serves as an orchestration layer, enabling companies to:
- Build custom AI voice agents without code
- Choose from multiple AI provider options (STT, LLM, TTS)
- Deploy agents for inbound/outbound calls
- Integrate with 2000+ apps via Zapier, Make, and n8n
- Monitor and optimize agent performance

#### Target Market
**Primary:** SMB to Mid-Market B2B companies
**Verticals:** Healthcare (hospitals, clinics), restaurants, automotive dealerships, debt collection, customer support

**Initial Success:** Healthcare vertical with Donna product (15 hospital clients)

#### Value Proposition
1. **Platform flexibility** - Not locked into single AI provider
2. **No-code deployment** - Build agents in minutes
3. **Ultra-low latency** - <700ms for web calls, ~900ms total for phone
4. **Multilingual** - 30+ languages supported
5. **Full integration ecosystem** - CRM, calendar, support tools

#### Competitors

| Competitor | Location | Funding | Similarity Score |
|-----------|----------|---------|------------------|
| Vapi | USA | Not disclosed | 9/10 |
| Bland.ai | USA | $65M | 8/10 |
| Synthflow | Germany | $30M | 8/10 |
| Retell.ai | USA | $5.1M | 8/10 |
| Smallest.ai | India | $8M | 8/10 |

### Technology Stack

#### Core Platform Architecture
- **Orchestration Layer:** Custom (allows provider choice)
- **Telephony Infrastructure:** LiveKit (open-source SIP infrastructure)
- **Performance:** <700ms latency for web calls

#### AI/ML Providers (Supported Options)

**Language Models (LLM):**
- OpenAI GPT-4o (recommended default)
- OpenAI GPT-4o mini
- OpenAI GPT-3.5 Turbo (simple use cases)
- OpenAI GPT-4 Turbo (legacy, large context)

**Speech-to-Text (STT/ASR):**
- Microsoft Azure Speech-to-Text

**Text-to-Speech (TTS):**
- Microsoft Azure (primary - stable, low latency)
- ElevenLabs (secondary - most natural voices)

#### Infrastructure & Integrations
- **Telephony:** LiveKit SIP (confirmed via GitHub fork)
- **Automation Platforms:** Zapier, Make.com, n8n
- **API:** REST API for custom integrations
- **Supported Integrations:** 2000+ apps including CRMs (Salesforce, HubSpot), calendars (Google, Outlook), support tools (Zendesk, Intercom)

### Leadership Team

| Name | Title | LinkedIn | Notes |
|------|-------|----------|-------|
| Aymeric Vaudelin | Co-founder | [LinkedIn](https://www.linkedin.com/in/aymeric-vaudelin) | Quoted in TechCrunch article, product vision leader |
| Mathieu Diaz | Co-founder | Not found | Technical co-founder |
| Yassine M'hamdi | Co-founder | [LinkedIn](https://www.linkedin.com/in/yassine-m-hamdi-4791a6110/) | Berkeley SkyDeck connection, ETH background |

**Team Structure:** Small founding team (2-10 employees total)
**Recent Activity:** Major product announcement January 2025

### Sales Intelligence

#### Buying Signals
- ✅ **Recent press coverage** - TechCrunch article January 9, 2025
- ✅ **Product expansion** - Launched orchestration platform (beyond initial Donna product)
- ✅ **Strong traction** - 15 hospital customers, hundreds of thousands of conversations
- ✅ **Berkeley SkyDeck backing** - Prestigious accelerator validation
- ✅ **Growth stage** - Likely looking to scale from initial customers

#### Pain Points (Inferred)
- **Limited team size** - May need to scale engineering and sales
- **Early-stage funding** - €600K pre-seed suggests may need Series A soon
- **Geographic expansion** - Currently France-focused, may need US/global expansion
- **Provider dependencies** - Currently limited to OpenAI for LLM, Azure/ElevenLabs for voice
- **Open-source telephony** - Using LiveKit suggests limited telephony options vs. Twilio

#### Competitive Position
**Strengths:**
- Healthcare vertical expertise and proven customers
- Platform approach (multi-provider) vs. single-stack competitors
- Strong technical performance (<700ms latency)
- Berkeley SkyDeck validation

**Weaknesses:**
- Small team vs. well-funded competitors (Bland: $65M, Synthflow: $30M)
- Limited funding compared to competitors
- France-based vs. US market leaders
- Limited provider options (only Azure/ElevenLabs for voice)

#### Recommended Approach
**Best Contact:** Aymeric Vaudelin (Co-founder, product vision)
**Entry Point:** Technology partnerships, ASR/LLM provider partnerships
**Messaging Angle:**
- "Expand provider options beyond Azure/ElevenLabs"
- "Multi-provider strategy strengthens platform positioning"
- "Scale internationally with proven speech technology"

**Timing:** ⏰ **Good timing** - Recent product launch, likely seeking growth partners

### Relevant News Hooks
- **January 9, 2025:** TechCrunch coverage of platform expansion
- **June 2024:** €600K pre-seed funding announcement
- **Recent:** 15 hospitals using Donna product

---

## Lookalike Company Analysis

### Target Company Profile
- **Industry:** AI Voice Orchestration Platform
- **Size:** 2-10 employees, pre-seed stage
- **Business Model:** B2B SaaS platform
- **Key Characteristics:**
  - Platform approach (not single provider)
  - Healthcare vertical traction
  - European startup
  - Berkeley SkyDeck alumni
  - Low-latency focus (<700ms)

### Search Criteria
1. **AI voice orchestration platforms** - Companies building platforms for voice agent creation
2. **B2B SaaS in conversational AI** - Similar business model
3. **Healthcare AI voice** - Vertical similarity
4. **European AI startups** - Geographic similarity
5. **Seed-stage voice AI** - Similar funding stage

### Lookalike Companies Found

| Rank | Company | Website | Location | Score | Funding | Key Similarities | Notable Differences | Source URL |
|------|---------|---------|----------|-------|---------|------------------|---------------------|------------|
| 1 | Vapi | vapi.ai | USA | 9/10 | Not disclosed | Voice AI orchestration, modular approach, developer-focused | More telephone-focused, US-based | [AssemblyAI](https://www.assemblyai.com/blog/orchestration-tools-ai-voice-agents) |
| 2 | Synthflow | synthflow.ai | Germany | 8/10 | $30M Series A | No-code platform, healthcare focus, European startup | More funding, Berlin-based | [EU-Startups](https://www.eu-startups.com/2025/06/indistinguishable-from-a-human-voice-berlin-based-synthflow-ai-raise-e17-2-million-for-its-ai-voice-agent/) |
| 3 | Retell.ai | retellai.com | USA | 8/10 | $5.1M Seed | Healthcare focus, HIPAA-compliant, YC-backed, similar stage | US-based, Y Combinator vs. Berkeley | [Retell AI](https://www.retellai.com/blog/seed-announcement) |
| 4 | Bland.ai | bland.ai | USA | 8/10 | $65M Series B | Voice agent platform, B2B focus, scale capabilities | Much more funding, enterprise-scale | [TechCrunch](https://www.bland.ai/blogs/bland-raises-a-40m-series-b) |
| 5 | Smallest.ai | smallest.ai | India | 8/10 | $8M Seed | Enterprise voice AI, sub-100ms latency focus | Owns full stack (not platform), India-based | [Inc42](https://inc42.com/buzz/smallest-ai-raises-8-mn-to-build-enterprise-grade-voice-ai/) |
| 6 | Pipecat | pipecat.com | USA | 7/10 | Open-source | Open-source framework, modular approach, developer-focused | Open-source vs. SaaS, no revenue model | [Modal Blog](https://modal.com/blog/livekit-vs-vapi-article) |
| 7 | LiveKit | livekit.io | USA | 7/10 | Not disclosed | Real-time communication, SIP infrastructure | Infrastructure layer vs. platform, Rounded uses LiveKit | [AssemblyAI](https://www.assemblyai.com/blog/orchestration-tools-ai-voice-agents) |
| 8 | Hyro | hyro.ai | USA | 8/10 | Not disclosed | Healthcare AI voice, appointment scheduling, HIPAA | US-based, more enterprise-focused | [CB Insights](https://www.hyro.ai/) |
| 9 | Solda | solda.ai | Germany | 7/10 | $4M Seed | European startup, seed stage, sales calls focus | Sales vs. general voice, Berlin-based | [Sifted](https://sifted.eu/articles/ai-agent-funding-rounds) |
| 10 | LOVO | lovo.ai | USA | 7/10 | $4.5M Pre-A | Berkeley SkyDeck alumni, AI voice technology | TTS focus vs. orchestration platform | [TechCrunch](https://techcrunch.com/2021/08/26/ai-voice-synthetic-speech-company-lovo-gets-4-5m-pre-series-a-funding/) |
| 11 | Voiceflow | voiceflow.com | USA | 7/10 | Not disclosed | No-code conversational AI builder, platform approach | More chatbot vs. voice-first | [Voiceflow](https://www.voiceflow.com/) |
| 12 | H Company | hcompany.ai | France | 7/10 | $220M Seed | French startup, Paris-based, AI agents | Much more funding, general AI agents vs. voice-specific | [Sifted](https://sifted.eu/articles/ai-agent-funding-rounds) |

### Summary

**Total Lookalikes Found:** 12 high-quality matches (7-9/10 similarity)

**Key Patterns:**
1. **Strong US dominance** - 8 of 12 are US-based (market opportunity for European expansion)
2. **Wide funding range** - $4M to $220M (Rounded at €600K is on lower end)
3. **Platform vs. Full-stack** - Most are platform/orchestration layer like Rounded
4. **Healthcare vertical** - 4 companies have healthcare focus (validated vertical)
5. **Developer-first approach** - Most target technical buyers with API-first products

**Competitive Insights:**
- Rounded's platform approach is validated by competitors
- Healthcare vertical is crowded but proven
- European market less saturated than US (opportunity)
- Funding gap suggests Rounded may need Series A to compete

**Recommended Actions:**
1. ✅ **Enrich top 5 lookalikes** for deeper competitive analysis
2. ✅ **Track funding announcements** from these companies
3. ✅ **Monitor product launches** and feature releases
4. ✅ **Map customer overlap** in healthcare vertical

---

## AI/Speech Technology Stack Analysis

### Summary
- **Total AI/speech subprocessors found:** 4 core providers
- **LLM provider(s):** OpenAI (exclusive)
- **ASR provider(s):** Microsoft Azure (exclusive)
- **TTS provider(s):** Microsoft Azure, ElevenLabs
- **Telephony Infrastructure:** LiveKit (open-source)
- **Primary sources:** docs.callrounded.com, GitHub repository
- **Last updated:** January 2025 (based on latest documentation references)

### Core AI/Speech Technologies

#### LLM / AI Models

| Vendor | Purpose | Source | Source URL | Confidence |
|--------|---------|--------|------------|------------|
| OpenAI | Language processing, conversation logic (GPT-4o, GPT-4o mini, GPT-3.5 Turbo, GPT-4 Turbo) | Documentation | https://docs.callrounded.com/documentation/build/general-settings | Confirmed |

**Notes:**
- Currently **exclusive to OpenAI** for LLM providers
- Supports 5 OpenAI models with different use cases
- GPT-4o is recommended default model
- Initial prototype used "ChatGPT after a transcriber and before a synthesizer"

#### Speech-to-Text / ASR

| Vendor | Purpose | Source | Source URL | Confidence |
|--------|---------|--------|------------|------------|
| Microsoft Azure | Real-time speech-to-text transcription | Documentation | https://docs.callrounded.com/documentation/build/general-settings | Confirmed |

**Notes:**
- Currently **exclusive to Azure** for STT
- Described as "most stable" and "low latency"
- No alternative STT providers mentioned

#### Text-to-Speech

| Vendor | Purpose | Source | Source URL | Confidence |
|--------|---------|--------|------------|------------|
| Microsoft Azure | Primary TTS provider (stable, low latency) | Documentation | https://docs.callrounded.com/documentation/build/general-settings | Confirmed |
| ElevenLabs | Secondary TTS provider (most natural voices) | Documentation | https://docs.callrounded.com/documentation/build/general-settings | Confirmed |

**Notes:**
- **Dual provider strategy** for TTS
- Azure prioritized for stability and latency
- ElevenLabs for voice quality and naturalness
- French language optimization mentioned

#### Telephony Infrastructure

| Vendor | Purpose | Source | Source URL | Confidence |
|--------|---------|--------|------------|------------|
| LiveKit | SIP infrastructure for call connectivity | GitHub | https://github.com/callRounded/livekit-sip-fork | Confirmed |

**Notes:**
- Open-source telephony infrastructure
- Custom fork maintained on GitHub (livekit-sip-fork)
- Real-time communication framework
- WebRTC-based

#### Integration Platforms (Non-AI/Speech)

| Vendor | Purpose | Source | Source URL | Confidence |
|--------|---------|--------|------------|------------|
| Make.com | Workflow automation | Blog post | https://callrounded.com/blog/ai-voice-agent-api-make-zapier-integrations | Confirmed |
| Zapier | Workflow automation | Blog post | https://callrounded.com/blog/ai-voice-agent-api-make-zapier-integrations | Confirmed |
| n8n | Workflow automation | Blog post | https://callrounded.com/blog/ai-voice-agent-api-make-zapier-integrations | Confirmed |

### Key Findings

#### Technology Strategy
- **Platform Positioning:** Markets as "choose your own providers" but currently limited to specific vendors
- **Provider Lock-in:** Despite platform marketing, only supports:
  - LLM: OpenAI only
  - STT: Azure only
  - TTS: Azure + ElevenLabs only
- **Infrastructure:** Open-source telephony (LiveKit) vs. commercial (Twilio)

#### Competitive Intelligence

**Strengths:**
- ✅ Dual TTS provider strategy (Azure + ElevenLabs)
- ✅ Open-source telephony reduces costs
- ✅ Integration ecosystem (2000+ apps via Zapier/Make)
- ✅ Low latency (<700ms) with current stack

**Weaknesses:**
- ⚠️ **Limited provider options** - Not truly "choose your own" platform
- ⚠️ **No Deepgram/Gladia/AssemblyAI** - Missing competitive ASR providers
- ⚠️ **No Anthropic/Cohere** - OpenAI exclusive for LLM
- ⚠️ **Open-source telephony** - May limit enterprise features vs. Twilio

**Comparison to Competitors:**

| Feature | Rounded | Vapi | Synthflow | Retell.ai |
|---------|---------|------|-----------|-----------|
| **LLM Providers** | OpenAI only | Multiple | Multiple | Multiple |
| **STT Providers** | Azure only | Multiple | Multiple | Deepgram, Azure, AssemblyAI |
| **TTS Providers** | Azure, ElevenLabs | Multiple | Multiple | Multiple |
| **Telephony** | LiveKit | Twilio, others | Multiple | Twilio |
| **True Platform?** | Limited | ✅ Yes | Partial | ✅ Yes |

#### Market Positioning

**Current Position:** "Platform with limited provider choice"
**Opportunity:** Expand provider support to match "orchestration platform" positioning

**Recommended Provider Additions:**
1. **STT/ASR:** Deepgram, Gladia, AssemblyAI, OpenAI Whisper
2. **LLM:** Anthropic Claude, Cohere, Google Gemini
3. **TTS:** Google Cloud TTS, Cartesia, PlayHT
4. **Telephony:** Twilio (for enterprise), Telnyx

### Technical Architecture Insights

**From TechCrunch Interview:**
> "The idea was that we'd simply put ChatGPT after a transcriber and before a synthesizer" - Aymeric Vaudelin

**Evolution:**
- **V1 (June 2023):** Simple pipeline (STT → GPT → TTS)
- **V2 (2024):** Donna product (hospital scheduling)
- **V3 (Jan 2025):** Platform product (customer choice of models)

**Performance Metrics:**
- Web call latency: 600-700ms
- Phone call latency: ~900ms (includes 200ms phone connectivity)
- Support for 30+ languages

### Sources Consulted

1. **Documentation:** https://docs.callrounded.com/documentation/build/general-settings
2. **Blog Post:** https://callrounded.com/blog/ai-voice-agent-api-make-zapier-integrations
3. **GitHub:** https://github.com/callRounded/livekit-sip-fork
4. **TechCrunch:** https://techcrunch.com/2025/01/09/rounded-is-an-ai-orchestration-platform-that-lets-anyone-build-an-ai-voice-agent/
5. **Company Website:** https://callrounded.com

### Data Gaps & Unknown Information

**Not Publicly Disclosed:**
- ❓ Cloud hosting provider (AWS, Google Cloud, Azure)
- ❓ Database provider
- ❓ Monitoring/observability tools
- ❓ Security/compliance certifications (SOC 2, HIPAA)
- ❓ Privacy policy subprocessor list (no public DPA/GDPR docs found)
- ❓ Exact telephony provider beyond LiveKit (Twilio integration?)
- ❓ Call recording infrastructure

**Recommendation:** For sales/compliance verification, request:
1. Data Processing Agreement (DPA)
2. Full subprocessor list
3. Security certifications
4. Infrastructure whitepaper

---

## Notion Database Sync

### Data Prepared for Notion

**Database ID:** `2861bdff7e998000a14edb0bf56a75bf`
**Action:** Create new company page (or update if exists with matching URL)

**Properties:**
```
Company_Name: Rounded
Status / Engagement: Ice Box
Vertical: AI / Voice Technology
ICP: 3
Product description: AI voice agent orchestration platform
ASR provider: Microsoft Azure
Nbr of AI/ML/Speech engineer: 2-10
Main Office Country: France
Website: https://callrounded.com
Linkedin Link: https://www.linkedin.com/company/callrounded
```

**Page Content:** Full enrichment report with sections:
- Executive Summary
- Firmographics
- Business Overview
- Technology Stack
- Leadership Team
- Sales Intelligence
- Lookalike Companies
- Subprocessor Analysis

**Status:** ⚠️ Notion MCP tools not available in current session - manual sync required

---

## Key Insights & Recommendations

### Strategic Insights

1. **Platform Positioning vs. Reality Gap**
   - Markets as "choose your own AI providers" orchestration platform
   - Reality: Limited to OpenAI (LLM), Azure (STT), Azure/ElevenLabs (TTS)
   - **Opportunity:** True multi-provider support would strengthen positioning

2. **Healthcare Vertical Validation**
   - 15 hospital customers with Donna product
   - Proven product-market fit in appointment scheduling
   - **Opportunity:** Healthcare is crowded but validated market

3. **Funding Gap vs. Competitors**
   - €600K pre-seed vs. competitors with $8M-$65M
   - **Risk:** May struggle to scale against well-funded competition
   - **Opportunity:** Series A timing likely in 2025

4. **European Market Position**
   - One of few European AI voice orchestration platforms
   - Most competitors are US-based
   - **Opportunity:** European privacy/GDPR positioning

5. **Technical Performance**
   - <700ms latency is competitive
   - Open-source telephony (LiveKit) reduces costs
   - **Advantage:** Performance matches well-funded competitors

### Sales Intelligence Summary

**Target Buyer Personas:**
- 🎯 Aymeric Vaudelin (Co-founder) - Product partnerships, technology decisions
- 🎯 Mathieu Diaz (Co-founder) - Technical integration decisions
- 🎯 Yassine M'hamdi (Co-founder) - Business development, funding

**Best Outreach Angles:**

1. **For ASR/STT Providers (Deepgram, Gladia, AssemblyAI):**
   - "Expand beyond Azure to offer customer choice"
   - "Strengthen 'platform' positioning with multi-provider STT"
   - "Healthcare-grade accuracy for medical transcription"

2. **For LLM Providers (Anthropic, Cohere):**
   - "Break OpenAI exclusivity, offer customer choice"
   - "Anthropic Claude for HIPAA compliance in healthcare"
   - "Cost optimization with alternative LLM options"

3. **For Infrastructure (Twilio, AWS):**
   - "Enterprise telephony for scaling beyond 15 hospitals"
   - "Replace open-source LiveKit with enterprise Twilio"
   - "Global expansion infrastructure"

**Timing Indicators:**
- ✅ Recent product launch (Jan 2025) - in growth mode
- ✅ Early customers (15 hospitals) - ready to scale
- ⏰ Likely seeking Series A funding in 2025
- ⏰ Expanding beyond healthcare vertical

### Recommended Next Steps

**Immediate Actions:**
1. ✅ **Connect on LinkedIn** - Follow founders and company page
2. ✅ **Monitor news** - Set up Google Alerts for funding announcements
3. ✅ **Track product updates** - Watch for new features/providers
4. ✅ **Engage with content** - Comment on blog posts, share TechCrunch article

**Outreach Strategy:**
1. **Research trigger:** Series A funding announcement
2. **Product trigger:** New provider integration announcement
3. **Growth trigger:** Expanding beyond France/healthcare
4. **Tech trigger:** Blog post about scaling challenges

**Long-term Monitoring:**
1. Track lookalike company funding (indicates market health)
2. Monitor competitive feature releases
3. Watch for healthcare AI regulations (HIPAA, GDPR impacts)
4. Track voice AI market consolidation

---

## Data Sources & Citations

### Primary Sources
- **Company Website:** https://callrounded.com
- **Documentation:** https://docs.callrounded.com
- **LinkedIn:** https://www.linkedin.com/company/callrounded
- **GitHub:** https://github.com/callRounded
- **TechCrunch Article:** https://techcrunch.com/2025/01/09/rounded-is-an-ai-orchestration-platform-that-lets-anyone-build-an-ai-voice-agent/

### Funding & Firmographics
- **Crunchbase:** https://www.crunchbase.com/organization/rounded-d040
- **Tracxn:** https://tracxn.com/d/companies/rounded/__m9QC2RSC4bBNINAoHB5fY5yqhPlHs9z358R0IEkciNI
- **Berkeley SkyDeck:** https://skydeck.berkeley.edu/portfolio/

### Competitive Analysis
- **AssemblyAI Blog:** https://www.assemblyai.com/blog/orchestration-tools-ai-voice-agents
- **Speechmatics:** https://www.speechmatics.com/company/articles-and-news/best-voice-ai-agent-platforms-2025
- **Sifted:** https://sifted.eu/articles/ai-agent-funding-rounds

### Technology Stack
- **Blog Post:** https://callrounded.com/blog/ai-voice-agent-api-make-zapier-integrations
- **GitHub Repository:** https://github.com/callRounded/livekit-sip-fork
- **Documentation:** https://docs.callrounded.com/documentation/build/general-settings

### Lookalike Companies
- Individual company websites, Crunchbase profiles, funding announcements
- Sources cited in lookalike table above

---

## Appendix: Research Methodology

### Tools & Techniques Used
- ✅ Web search for company information, funding, team
- ✅ LinkedIn research for founders and company profile
- ✅ GitHub repository analysis for technology stack
- ✅ Documentation review for API and integration capabilities
- ✅ Competitive analysis via industry reports and comparisons
- ✅ News monitoring via TechCrunch, industry publications

### Confidence Levels
- **High Confidence:** Firmographics, funding, founders, technology stack
- **Medium Confidence:** Revenue estimates, exact team size, competitive positioning
- **Low Confidence:** Cloud hosting, internal tooling, exact telephony provider

### Limitations
- ⚠️ Website blocked direct access (403 errors) - relied on documentation subdomain
- ⚠️ No public privacy policy or DPA found - subprocessor list incomplete
- ⚠️ No public job postings - limited insight into hiring/growth
- ⚠️ No public customer list beyond "15 hospitals" - exact customers unknown
- ⚠️ Limited founder LinkedIn profiles - background information incomplete

### Data Freshness
- **Report Date:** November 6, 2025
- **Most Recent Data:** TechCrunch article (January 9, 2025)
- **Funding Data:** June 2024 (pre-seed announcement)
- **Documentation:** Accessed November 2025 (current)

---

## Contact Information

**For inquiries about this research:**
- Research conducted by: Claude AI (Blynt Customer Development)
- Report location: `logs/deep-dive-callrounded.com-2025-11-06.md`
- Repository: blynt-customer-development

**To update this research:**
- Re-run `/deep-dive callrounded.com` command
- Or run individual commands: `/enrich-company`, `/find-lookalikes`, `/discover-subprocessors`

---

**End of Report**
