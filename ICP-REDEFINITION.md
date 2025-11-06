# Blynt ICP Redefinition
**Date:** 2025-10-27
**Classification Criteria:** Technical Maturity + Use Case + Volume

---

## Overview

The ICP framework is organized by **technical maturity** (from white-label adopters to custom fine-tuning users) and distinguishes between **use cases** (ambient audio, post-call intelligence, real-time voice agents, audio ML products).

---

## ICP 1: White-Label Runtime Solutions
**Technical Maturity:** Low to Medium (Need turnkey solutions)
**Proposition:** White-label Recall-like solution for ambient audio capture

### Target Profile
Companies with **untapped ambient audio potential** that want to add voice/audio capabilities WITHOUT building in-house expertise.

### Target Sectors
- **Construction/Field Services:** Faks, Hosman (capture on-site conversations, work orders)
- **CRM/Sales Platforms:** Add voice notes, call summaries as a feature
- **Customer Support Tools:** Zendesk-like platforms adding voice context
- **Healthcare Admin:** Medical scribes, patient intake (non-clinical)

### Key Characteristics
- **Volume:** Low to Medium (thousands to tens of thousands of hours/month)
- **Technical Team:** Small/non-existent ML team
- **Integration Need:** Embed voice capture as a feature in existing product
- **Use Case Timing:** Post-conversation processing (not real-time)
- **Decision Maker:** Product Manager, VP Product

### Pain Points
- Don't want to build voice infrastructure from scratch
- Need GDPR/compliance-ready solution out of box
- Want SDK/API that "just works"
- Limited ML expertise in-house

### Solution Fit
- **White-label runtime** (Recall-style)
- Pre-built diarization, transcription, basic summarization
- Easy embedding (SDK, iFrame, API)
- Compliance certifications included

### Examples
- Faks (construction management)
- Hosman (property management)
- Sales CRMs adding voice notes
- Ticketing systems adding call context

---

## ICP 2: Post-Call Intelligence / Note-Takers
**Technical Maturity:** Medium (Use existing ASR, need quality/reliability)
**Proposition:** High-quality ASR runtime for transcription + downstream AI processing

### Target Profile
Companies that **RECORD meetings/calls** and then process them for intelligence (summary, action items, sentiment, coaching insights).

### Target Sectors
- **Meeting Note-Takers:** Circleback, tl;dv, Fireflies, Otter.ai, Grain
- **Sales Conversation Intelligence:** Modjo, Gong, Chorus, Jiminny, Leexi
- **Customer Support QA:** Call center analytics, quality monitoring
- **Compliance/Legal:** Call recording for regulatory compliance + risk analysis

### Key Characteristics
- **Volume:** Medium to High (hundreds of thousands to millions of hours/month)
- **Technical Team:** Engineering + ML team (but not ASR specialists)
- **Timing:** **Post-call/Post-meeting** processing (not real-time constraints)
- **Use Case:** Transcription → AI analysis (summarization, sentiment, action extraction, coaching)
- **Decision Maker:** CTO, VP Engineering, Head of AI/ML

### Pain Points
- ASR accuracy directly impacts downstream AI quality
- Need multilingual support (especially European languages)
- Cost optimization (high volume = high ASR costs)
- Speaker diarization quality critical for attribution
- Existing provider (Deepgram, AssemblyAI, Azure) has limitations

### Solution Fit
- **High-accuracy ASR runtime** (better than incumbents)
- Strong diarization for multi-speaker scenarios
- Language breadth (FR, EN, ES, DE, IT, etc.)
- Cost-effective at scale
- Optional: Benchmarking tools to compare quality

### Examples
- **Meeting Intelligence:** Circleback, tl;dv, Grain, Otter.ai, Fireflies
- **Sales Intelligence:** Modjo, Gong, Chorus, Jiminny, Leexi
- **Support QA:** Call center analytics platforms
- **Compliance:** Legal/financial call recording processors

---

## ICP 3: Real-Time Voice Agents (ASR for Conversational AI)
**Technical Maturity:** Medium to High (Building voice AI products)
**Proposition:** Real-time ASR runtime with turn-taking, low latency, interruption handling

### Target Profile
Companies building **REAL-TIME voice agents** that have conversations with users (appointment booking, customer support, sales automation, coaching).

### Target Sectors
- **Healthcare Voice Agents:** Vocca, Talkie.ai, Hello Patient (appointment booking)
- **Customer Support Bots:** Conversational IVR, voice-first support
- **Sales/SDR Automation:** AI SDRs making outbound calls
- **Voice Assistants:** Chatbot voice interfaces (ChatGPT voice mode clones)
- **Coaching/Training:** AI role-play, interview practice

### Key Characteristics
- **Volume:** Medium to Very High (millions of minutes/month)
- **Technical Team:** Strong engineering + ML team
- **Timing:** **Real-time** (low-latency critical, <500ms)
- **Use Case:** Live conversations with turn-taking, interruptions, natural flow
- **Decision Maker:** CTO, VP Engineering, Co-founder (technical)

### Pain Points
- **Latency:** Deepgram/AssemblyAI streaming not fast enough for natural conversation
- **Turn-taking:** Need intelligent endpointing (when did user finish speaking?)
- **Interruptions:** Handling barge-in scenarios (user interrupts agent)
- **Cost at scale:** Real-time streaming is expensive
- **Reliability:** Can't have downtime in production voice agents

### Solution Fit
- **Ultra-low latency ASR** (streaming, <200ms)
- **Smart turn-taking/endpointing** (detect when to respond)
- **Interruption handling** (graceful barge-in)
- **High uptime SLA** (99.9%+)
- **Cost efficiency** for high-volume real-time use

### Examples
- **Healthcare:** Vocca, Marshmallow, Talkie.ai, Yaqoot, Hello Patient
- **Customer Support:** AI phone agents, conversational IVR
- **Sales Automation:** AI SDR callers (Artisan, 11x)
- **Voice-enabled chatbots:** ChatGPT voice mode alternatives
- **Coaching:** Mimir (speech coaching), interview practice tools

---

## ICP 4: Audio ML Product Companies (Studio + Benchmarking)
**Technical Maturity:** High (Custom model development)
**Proposition:** Studio platform for fine-tuning + Benchmarking tools for evaluation

### Target Profile
Companies **building audio ML products** who need to fine-tune models, evaluate ASR providers, or develop custom voice capabilities.

### Target Sectors
- **Consumer Audio Hardware:** Sonos, Bose, Apple (HomePod), Amazon (Alexa)
- **Healthcare AI Scribes:** Doctolib, Nabla, Abridge, Sully AI
- **Speech-to-Text API Providers:** Assembly AI competitors, regional ASR providers
- **Audio Analytics Platforms:** Pyannote.ai, speaker recognition services
- **Voice Biometrics:** Security/authentication using voice

### Key Characteristics
- **Volume:** Very High (millions to billions of utterances)
- **Technical Team:** Large ML/research team with ASR specialists
- **Need:** Custom model training, fine-tuning on proprietary data
- **Evaluation:** Rigorous benchmarking across providers (Deepgram, Azure, Gladia, etc.)
- **Decision Maker:** Head of ML/AI, Chief Scientist, VP Research

### Pain Points
- **Model Customization:** Generic ASR models don't work for domain-specific vocabulary
- **Fine-tuning Infrastructure:** Need tooling to train custom models on their data
- **Benchmarking:** Hard to systematically compare ASR providers (accuracy, latency, cost)
- **Proprietary Data:** Can't send sensitive audio to third-party APIs (need on-prem/private cloud)
- **Language/Accent Coverage:** Generic models underperform on specific accents, dialects, medical jargon

### Solution Fit
- **Studio Platform:** Fine-tuning interface for custom model development
- **Benchmarking Tools:** Automated evaluation across ASR providers (WER, latency, cost)
- **Private Deployment:** On-premise or private cloud options
- **Domain Adaptation:** Tools for medical terminology, industry jargon, accents

### Examples
- **Consumer Audio:** Sonos, Bose (voice control for speakers)
- **Healthcare:** Doctolib, Nabla, Abridge (medical transcription)
- **ASR Providers:** Regional competitors to Deepgram/Assembly
- **Audio ML:** Pyannote.ai (speaker diarization), voice biometrics companies

---

## ~~ICP 5: High-Volume Ambient Intelligence~~ → MERGED INTO ICP 2

**Note:** This ICP has been merged into ICP 2 (Post-Call Intelligence) as of 2025-10-27.

**Rationale:** Volume alone is not a sufficient differentiator for a separate ICP. Companies like Gong (high-volume, established) and Modjo (medium-volume, scale-up) share the same fundamental use case: post-call conversation intelligence with AI processing. Both are looking for better ASR quality and/or cost optimization.

**Key insight:** The distinction between early-stage note-takers and enterprise conversation intelligence platforms is one of **maturity stage within the same ICP**, not separate ICPs. ICP 2 now encompasses all post-call intelligence companies regardless of volume, from 10K to 10M hours/month.

**Companies previously classified as ICP 5 should now be classified as ICP 2:**
- Gong, Chorus, Wingman, Revenue.io (sales intelligence)
- Zoom IQ, Microsoft Teams (if external ASR)
- Call center QA platforms (Tethr, Balto)

---

## ICP N/A: Not a Fit
Companies that don't align with any ICP or have fundamental disqualifiers.

### Reasons for N/A
- **No audio use case:** Pure text-based products
- **Wrong scale:** Consumer apps with <1K hours/month (too small)
- **Non-technical buyer:** Can't evaluate ASR quality/technical trade-offs
- **Embedded-only needs:** Only on-device ASR (no cloud API usage)
- **Budget constraints:** Startups pre-seed with no revenue (<$100K ARR)

---

## Migration Path: Updating Existing Companies

### Step 1: Audit Current ICP Assignments
Run query to find all companies currently tagged as ICP 1, 2, 3:
- Export to spreadsheet with: Company Name, Current ICP, Website, Product Description, Vertical

### Step 2: Reclassification Rules

**Current ICP 1 → New ICP Mapping:**
- If **ambient audio potential** (Faks, Hosman) → **New ICP 1** (White-Label Runtime)
- If **meeting note-taker** (Circleback, tl;dv) → **New ICP 2** (Post-Call Intelligence)
- If **voice agent** (Vocca, Marshmallow) → **New ICP 3** (Real-Time Voice Agents)

**Current ICP 2 → New ICP Mapping:**
- If **fine-tuning needs** (Sonos, Doctolib, Nabla) → **New ICP 4** (Studio + Benchmarking)
- If **post-call intelligence** (Gong, Modjo, note-takers) → **New ICP 2** (Post-Call Intelligence - all scales)

**Current ICP 3 → New ICP Mapping:**
- If **benchmarking only** → **New ICP 4** (Studio + Benchmarking)
- If **high-volume post-call user** (large conversation intelligence) → **New ICP 2** (Post-Call Intelligence)

### Step 3: Batch Update Script
Use Notion API to update ICP field:
```python
# Pseudo-code for batch update
companies_to_update = [
    {"url": "vocca_notion_url", "old_icp": "3", "new_icp": "3"},  # Voice agent
    {"url": "circleback_url", "old_icp": "1", "new_icp": "2"},    # Post-call intelligence
    {"url": "sonos_url", "old_icp": "2", "new_icp": "4"},         # Studio
    # ... etc
]
```

---

## Summary Table

| **ICP** | **Technical Maturity** | **Use Case** | **Timing** | **Volume** | **Key Need** |
|---------|------------------------|--------------|------------|------------|--------------|
| **ICP 1** | Low-Medium | Ambient audio (new to voice) | Post-conversation | Low-Medium | White-label solution |
| **ICP 2** | Medium-High | Meeting/call transcription + AI | Post-conversation | **Any scale** (10K-10M hrs/mo) | ASR quality + cost |
| **ICP 3** | Medium-High | Real-time voice agents | Real-time | Medium-Very High | Latency + turn-taking |
| **ICP 4** | High | Audio ML product development | Varies | Very High | Fine-tuning + benchmarking |
| **N/A** | - | No audio use case | - | - | Not a fit |

---

## Next Steps

1. ✅ **Review & Approve:** Validate this ICP structure with team
2. **Create Migration Script:** Batch reclassify existing companies in Notion
3. **Update Slash Commands:** Modify `/map-icp` command logic to use new definitions
4. **Sales Messaging:** Create ICP-specific outreach templates
5. **Tracking:** Monitor which ICPs convert best (ICP 3 likely highest intent)

---

**Questions for Refinement:**
1. ✅ ~~Should we collapse ICP 2 and ICP 5?~~ → **RESOLVED:** Merged into single ICP 2 (2025-10-27)
2. Do we want sub-tiers within ICPs (e.g., ICP 3a = Healthcare agents, ICP 3b = Sales agents)?
3. What's the minimum volume threshold for each ICP (to avoid wasting time on tiny accounts)?
