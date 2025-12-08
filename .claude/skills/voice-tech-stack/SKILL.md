---
name: discovering-voice-stack
description: Discovers voice/speech technology vendors and infrastructure for a company. Used when identifying ASR, TTS, or real-time voice technologies, when researching voice AI stack, or when finding subprocessors in privacy policies and job postings.
---

# Voice Technology Stack Discovery

Identifies voice/speech infrastructure: transport protocols, real-time frameworks, ASR/TTS providers.

## Quick Reference

**Transport**: WebRTC, WebSockets, SIP, PSTN
**Frameworks**: LiveKit, Pipecat, Daily, Agora, Twilio
**Agentic**: Vapi, Retell, Bland AI, Vocode
**ASR**: Deepgram, Gladia, Assembly AI, Azure Speech
**TTS**: ElevenLabs, Play.ht, Deepgram Aura, Cartesia

## Discovery Workflow

Copy this checklist:

```
Stack Discovery Progress:
- [ ] Step 1: Check privacy policy/subprocessors
- [ ] Step 2: Search job postings for tech requirements
- [ ] Step 3: Review technical blog posts
- [ ] Step 4: Check GitHub for SDK integrations
- [ ] Step 5: Verify with documentation/API docs
```

## Detailed Reference

### Transport Protocols

| Protocol | Description | Use Case |
|----------|-------------|----------|
| **WebRTC** | Peer-to-peer real-time communication | Browser-based voice, video calls |
| **WebSockets** | Full-duplex communication over TCP | Real-time audio streaming |
| **SIP** | Session Initiation Protocol | Traditional telephony, VoIP |
| **PSTN** | Public Switched Telephone Network | Phone calls, legacy systems |

### Real-Time Frameworks

| Framework | Type | Key Features |
|-----------|------|--------------|
| **LiveKit** | Open-source | WebRTC SFU, room-based, agents SDK |
| **Pipecat** | Open-source | Voice AI pipelines, Python-first |
| **FastRTC** | Open-source | Gradio integration, lightweight |
| **Daily** | Commercial | Simple API, global infrastructure |
| **Agora** | Commercial | Enterprise scale, low latency |
| **Twilio** | Commercial | Programmable voice, SMS, video |

### Agentic Frameworks

| Framework | Description |
|-----------|-------------|
| **Vapi** | Voice AI platform, managed infrastructure |
| **LiveKit Agents** | Agent framework on LiveKit |
| **Pipecat Flow** | Conversation flow management |
| **Retell** | Voice agent platform |
| **Vocode** | Open-source voice agent framework |
| **Bland AI** | AI phone calls at scale |

---

## Speech Stack

### ASR (Automatic Speech Recognition) Providers

| Provider | Strengths | Latency |
|----------|-----------|---------|
| **Deepgram** | Real-time, accuracy, Nova-2 model | ~300ms |
| **Gladia** | Multi-language, Whisper-based | ~500ms |
| **Assembly AI** | Accuracy, speaker diarization | ~400ms |
| **Azure Speech** | Enterprise, many languages | ~300ms |
| **Google Speech** | Integration with GCP | ~300ms |
| **Whisper** | Open-source, self-hosted | Varies |
| **Rev AI** | Human-quality, accuracy focus | ~500ms |
| **Speechmatics** | Enterprise, multi-language | ~400ms |

### LLM Providers

| Provider | Models |
|----------|--------|
| **OpenAI** | GPT-4, GPT-4o, GPT-3.5 |
| **Anthropic** | Claude 3.5, Claude 3 |
| **Google** | Gemini Pro, Gemini Ultra |
| **Azure OpenAI** | GPT models via Azure |
| **Cohere** | Command, Enterprise focus |
| **Mistral** | Open-weight models |
| **Meta** | Llama 3, open-source |

### TTS (Text-to-Speech) Providers

| Provider | Strengths |
|----------|-----------|
| **ElevenLabs** | Natural voices, voice cloning |
| **Play.ht** | Wide voice selection, API |
| **Deepgram Aura** | Low latency, real-time |
| **Azure TTS** | Enterprise, SSML support |
| **Google TTS** | Integration, WaveNet |
| **OpenAI TTS** | Simple API, good quality |
| **Cartesia** | Ultra-low latency |
| **LMNT** | Expressive, fast |

---

## Supporting Infrastructure

### Telephony

| Provider | Description |
|----------|-------------|
| **Twilio Voice** | Programmable voice, global PSTN |
| **Vonage** | Voice API, video |
| **Bandwidth** | Enterprise telephony |
| **SignalWire** | Twilio alternative |
| **Plivo** | Voice and SMS |
| **Telnyx** | Global carrier |

### Meeting Recording

| Provider | Description |
|----------|-------------|
| **Recall.ai** | Bot-based meeting recording |
| **Fireflies API** | Meeting transcription |
| **Tactiq** | Chrome extension recording |

### Audio Processing

| Provider | Description |
|----------|-------------|
| **Krisp** | Noise cancellation AI |
| **Dolby.io** | Audio enhancement APIs |
| **AudioMob** | Background noise removal |

---

## Research Indicators

### Where to Find Stack Information

1. **Privacy Policy** - Lists subprocessors and vendors
2. **Subprocessor List** - Dedicated page for compliance
3. **Job Postings** - "Experience with X" reveals stack
4. **Technical Blog** - Architecture posts
5. **GitHub** - SDK integrations, open-source projects
6. **API Documentation** - Endpoints reveal providers
7. **Security Page** - SOC 2 reports list vendors

### Search Patterns

```
# Privacy/Subprocessors
site:{domain} privacy subprocessors
site:{domain} legal subprocessors

# Job Postings
site:{domain} careers "voice engineer"
"{company}" jobs "WebRTC" OR "LiveKit"
"{company}" hiring "speech" OR "ASR"

# Technical
"{company}" Deepgram OR Gladia OR "Assembly AI"
"{company}" "voice AI" architecture
"{company}" blog WebRTC

# GitHub
"{company}" github sdk voice
```

---

## IGNORE List

Do **NOT** report these as voice-related infrastructure:

- **Hosting**: AWS, GCP, Azure (compute/storage)
- **CDN**: Cloudflare, Fastly, Akamai
- **Analytics**: Google Analytics, Mixpanel, Amplitude
- **Marketing**: HubSpot, Mailchimp, Intercom
- **Payments**: Stripe, Braintree
- **Auth**: Auth0, Okta
- **Databases**: PostgreSQL, MongoDB, Redis
- **Monitoring**: Datadog, New Relic, Sentry

## Additional Resources

**Extended provider details**: See [reference.md](reference.md) for complete vendor list
**Search query templates**: See [templates/search-queries.txt](templates/search-queries.txt)
**Output template**: See [templates/stack-report.md](templates/stack-report.md)
**Programmatic detection**: Run `python scripts/detect_stack.py "text from privacy policy"`
