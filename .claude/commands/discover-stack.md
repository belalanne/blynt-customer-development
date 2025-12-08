---
description: Discover a company's voice/speech technology stack
arguments:
  - name: domain
    description: Company domain to analyze (e.g., vapi.ai)
    required: true
---

Discover the voice/speech technology stack for $ARGUMENTS:

## Research Focus

### Real-Time Infrastructure

| Category | Options to Look For |
|----------|---------------------|
| Transport Protocol | WebRTC, WebSockets, SIP, PSTN |
| Real-time Framework | LiveKit, Pipecat, FastRTC, Daily, Agora, Twilio |
| Agentic Framework | Vapi, LiveKit Agents, Pipecat Flow, Retell, Vocode |

### Speech Stack

| Category | Options to Look For |
|----------|---------------------|
| ASR Provider | Deepgram, Gladia, Assembly AI, Azure Speech, Google Speech, Whisper |
| LLM Provider | OpenAI, Anthropic, Google Gemini, Azure OpenAI, Cohere |
| TTS Provider | ElevenLabs, Play.ht, Deepgram Aura, Azure TTS, Google TTS, OpenAI TTS |

### Supporting Infrastructure

| Category | Options to Look For |
|----------|---------------------|
| Telephony | Twilio Voice, Vonage, Bandwidth, SignalWire |
| Meeting Recording | Recall.ai, Fireflies API, Tactiq |
| Audio Processing | Krisp, Dolby.io |

## Research Strategy

1. **Privacy Policy**: Search for `/privacy` or `/legal/privacy` pages - often lists subprocessors
2. **Subprocessor List**: Look for `/subprocessors` or `/security` pages
3. **Job Postings**: Search `site:{domain} careers` or check LinkedIn jobs
4. **Technical Docs**: Look for `/docs`, `/api`, `/developers` pages
5. **GitHub**: Search for company repos or SDK integrations
6. **Blog/Engineering Blog**: Technical architecture posts

## Search Queries

Use these search patterns:
- `"{company}" ASR provider speech-to-text`
- `"{company}" WebRTC voice`
- `"{company}" Deepgram OR Gladia OR "Assembly AI"`
- `site:{domain} subprocessors OR vendors`

## Output Format

```
## Voice Infrastructure for {Company}

### Confirmed (with source)
- ASR: [Provider] - [Source URL]
- TTS: [Provider] - [Source URL]

### Inferred (high confidence)
- Framework: [Provider] - [Reasoning]

### Unknown
- LLM Provider: No evidence found
```

## IGNORE

Do NOT report on: AWS, GCP, Azure (hosting), Cloudflare (CDN), Google Analytics, Stripe, general SaaS tools.
