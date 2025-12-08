# Product Focus Update - Changelog

**Date:** 2025-12-01
**Status:** ✅ Complete

---

## Summary of Changes

Updated the repository to reflect Blynt's new product focus: **Real-time Transcription API** with advanced features (natural turn-taking, keyword boosting, run-time contextualization, interruption handling).

---

## Key Changes

### 1. Product Positioning (claude.md)

**Old Focus:**
- General "conversation intelligence and speech technology" market
- Meeting transcription/recording solutions
- Conversation analytics tools

**New Focus:**
- **Real-time Transcription API** with specific features:
  - Built-in Natural turn-taking
  - Large scale Keyword Boosting
  - Run-time Contextualization
  - Interruption Handling

---

### 2. ICP Classification System

**New ICP Definitions:**

#### ICP #1: Speech/Dictation Products
Companies that want speech or dictation capabilities in their product:
- Healthcare documentation (medical dictation)
- Legal transcription tools
- Note-taking applications
- Productivity apps with voice input
- Accessibility features

**Key signals**: Dictation features, medical/legal transcription, voice-to-text in apps

#### ICP #2: Meeting AI Assistants
Companies building meeting assistants with AI capabilities:
- Meeting transcription platforms (Otter.ai, Fireflies.ai, tldv, Grain)
- Sales call intelligence (Gong, Chorus, Jiminny)
- Customer support QA (Observe.AI, Mindtickle)
- Collaboration tools with AI note-taking

**Key signals**: Real-time meeting transcription, AI summaries, conversation analytics

#### ICP #3: Voice Agents Platforms/Products
Companies building voice agent platforms or voice-enabled products:
- AI phone assistants (Bland AI, Air.ai, Vapi)
- Voice-enabled customer support
- AI receptionists (Beside, Goodcall)
- Conversational AI platforms
- Voice bots for scheduling/ordering

**Key signals**: Conversational AI, voice agents, AI phone systems, real-time voice interactions

#### ICP #4: Custom Speech/Voice Solutions
Companies building fully customized speech/voice products:
- Enterprise voice infrastructure
- Proprietary voice AI platforms
- White-label voice solutions
- Industry-specific voice applications (finance, healthcare, government)

**Key signals**: Custom ASR models, proprietary voice tech, enterprise voice infrastructure

---

### 3. Technical Discovery Priorities

**New Infrastructure Discovery Focus:**

#### Priority 1: Real-Time Infrastructure
- **Transport Protocol**: WebRTC, WebSockets, SIP, PSTN
- **Real-time Framework**: LiveKit, Pipecat, FastRTC, Daily, Agora, Twilio
- **Agentic Framework**: Vapi, LiveKit Agents, Pipecat Flow, Retell, Vocode

#### Priority 2: Speech Stack
- **ASR Providers**: Deepgram, Gladia, Assembly AI, Azure Speech, Google Speech, Whisper
- **LLM Providers**: OpenAI, Anthropic, Google Gemini, Cohere, Azure OpenAI, Mistral
- **TTS Providers**: ElevenLabs, Play.ht, Deepgram Aura, Azure TTS, Google TTS, OpenAI TTS

#### Priority 3: Supporting Infrastructure
- **Telephony**: Twilio Voice, Vonage, Bandwidth, SignalWire
- **Meeting Recording**: Recall.ai, Fireflies API, Tactiq
- **Audio Processing**: Krisp, Dolby.io, noise suppression

---

## Files Modified

### Core Documentation
1. **`claude.md`** - Updated product positioning, ICP definitions, and technical discovery priorities

### Slash Commands
2. **`.claude/commands/enrich-company.md`**
   - Added ICP classification guide
   - Updated output format to include ICP classification section
   - Added reasoning for ICP categorization

3. **`.claude/commands/discover-subprocessors.md`**
   - Renamed from "AI/speech subprocessors" to "Real-time voice infrastructure & speech stack"
   - Added Priority 1: Real-Time Infrastructure (transport, framework, agentic)
   - Added Priority 2: Speech Stack (ASR, LLM, TTS)
   - Updated research workflow with new searches for:
     - WebRTC, WebSockets, SIP
     - LiveKit, Pipecat, Daily, Agora
     - Vapi, Retell, Vocode
     - GitHub repositories and SDKs
   - Updated output format to include:
     - Transport Protocol section
     - Real-Time Framework section
     - Agentic Framework section
     - TTS Provider section
     - ICP classification in summary

---

## New Research Focus

### What We're Looking For Now

**Real-time Voice Infrastructure:**
1. How do they handle real-time audio? (WebRTC, WebSockets, SIP)
2. What framework do they use? (LiveKit, Pipecat, Daily)
3. Do they use an agentic platform? (Vapi, Retell, Vocode)

**Speech Stack:**
4. ASR provider (Deepgram, Gladia, Assembly AI)
5. LLM provider (OpenAI, Anthropic, Google)
6. TTS provider (ElevenLabs, Play.ht, Deepgram Aura)

**Key Research Indicators:**
- Job postings: "WebRTC engineer", "LiveKit", "Pipecat", "Voice AI engineer"
- Technical blog posts: Architecture diagrams, tech stack discussions
- GitHub repos: Open-source integrations, SDKs used
- API documentation: WebSocket endpoints, real-time APIs
- Privacy policies: List of AI/speech subprocessors

---

## Usage Examples

### Running Enrichment with ICP Classification
```bash
/enrich-company vapi.ai
```

**Output will now include:**
```
### ICP Classification
**ICP:** 3
**Category:** Voice Agents
**Reasoning:** Vapi is a voice agent platform that enables developers to build
conversational AI applications with real-time voice interactions.
```

### Running Subprocessor Discovery
```bash
/discover-subprocessors vapi.ai
```

**Output will now include:**
```
## Real-Time Infrastructure

### Transport Protocol
| Protocol | Evidence | Source | Source URL | Confidence |
|----------|----------|--------|------------|------------|
| WebRTC | Job posting for WebRTC Engineer | LinkedIn Jobs | [URL] | Confirmed |

### Real-Time Framework
| Framework | Purpose | Source | Source URL | Confidence |
|-----------|---------|--------|------------|------------|
| Daily | Real-time voice infrastructure | Blog post | [URL] | Confirmed |

### Agentic Framework
| Framework | Purpose | Source | Source URL | Confidence |
|-----------|---------|--------|------------|------------|
| Proprietary | Voice agent orchestration | Docs | [URL] | Inferred |
```

---

## Benefits of These Changes

1. **Clearer Target Market**: ICP definitions align with Blynt's real-time transcription product
2. **Better Sales Intelligence**: Discover competitors' full voice infrastructure, not just ASR
3. **Improved Competitive Analysis**: Understand transport protocols and frameworks used
4. **More Actionable Insights**: Know if they use agentic platforms (potential switching candidates)
5. **TTS Discovery**: Identify TTS providers (potential upsell/cross-sell opportunities)

---

## Migration Notes

### No Breaking Changes
- All existing commands still work the same way
- Output format expanded (backward compatible)
- ICP classification is additive (doesn't replace existing fields)

### What Stayed the Same
✅ Command names unchanged
✅ Core enrichment workflow unchanged
✅ Notion sync process unchanged
✅ Source URL citation requirements unchanged

### What Changed
✅ Product positioning updated to real-time transcription
✅ ICP definitions now reflect voice/speech use cases
✅ Subprocessor discovery expanded to include transport, frameworks, agentic platforms, TTS
✅ Research workflow includes new searches for WebRTC, LiveKit, Pipecat, etc.

---

## Next Steps

### Immediate Testing
Test the updated commands on a few companies to validate:
1. ICP classification accuracy
2. Real-time infrastructure discovery effectiveness
3. New search queries finding relevant data

### Suggested Test Companies
- **ICP #1**: Suki.ai (medical dictation), Otter.ai (note-taking)
- **ICP #2**: Fireflies.ai (meeting transcription), Gong (sales call intelligence)
- **ICP #3**: Vapi (voice agents platform), Bland.ai (AI phone calls), Retell
- **ICP #4**: Enterprise custom voice solution providers

### Potential Enhancements
1. Add automated ICP scoring (confidence level)
2. Create ICP-specific outreach templates
3. Build lookalike finder based on ICP + tech stack
4. Add TTS provider field to Notion database

---

**Status:** ✅ Ready for Use
**Version:** 2.0 (Real-time Focus)
**Last Updated:** 2025-12-01
