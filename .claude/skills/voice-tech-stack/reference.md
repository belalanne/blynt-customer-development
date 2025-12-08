# Voice Tech Stack - Extended Reference

## Contents

- ASR Provider Comparison Matrix
- TTS Provider Comparison Matrix
- Real-Time Framework Feature Matrix
- Agentic Platform Comparison
- Provider Detection Signals (Privacy, Jobs, Docs, GitHub)
- Competitive Intelligence (Who Uses What)
- Integration Patterns (Voice Agent, Meeting Bot)

---

## ASR Provider Comparison Matrix

| Provider | Real-time | Latency | Languages | Diarization | Custom Vocab | Pricing Model |
|----------|-----------|---------|-----------|-------------|--------------|---------------|
| Deepgram | Yes | ~300ms | 30+ | Yes | Yes | Per minute |
| Gladia | Yes | ~500ms | 100+ | Yes | Yes | Per minute |
| Assembly AI | Yes | ~400ms | 30+ | Yes | Yes | Per minute |
| Azure Speech | Yes | ~300ms | 100+ | Yes | Yes | Per minute |
| Google Speech | Yes | ~300ms | 125+ | Yes | Limited | Per minute |
| Whisper (OpenAI) | No | Varies | 99 | No | No | Per minute |
| Rev AI | Yes | ~500ms | 30+ | Yes | Yes | Per minute |
| Speechmatics | Yes | ~400ms | 50+ | Yes | Yes | Per minute |

## TTS Provider Comparison Matrix

| Provider | Latency | Voices | Languages | Voice Cloning | Streaming | Emotion |
|----------|---------|--------|-----------|---------------|-----------|---------|
| ElevenLabs | ~200ms | 100+ | 29 | Yes | Yes | Yes |
| Play.ht | ~300ms | 900+ | 142 | Yes | Yes | Yes |
| Deepgram Aura | ~150ms | 10+ | 10+ | No | Yes | Limited |
| Azure TTS | ~200ms | 400+ | 140+ | Yes | Yes | Yes |
| Google TTS | ~200ms | 200+ | 40+ | No | Yes | Limited |
| OpenAI TTS | ~300ms | 6 | 50+ | No | Yes | No |
| Cartesia | ~100ms | 20+ | 10+ | Yes | Yes | Yes |
| LMNT | ~150ms | 20+ | 10+ | Yes | Yes | Yes |

## Real-Time Framework Feature Matrix

| Framework | Protocol | Open Source | Hosting | Agents SDK | Phone/PSTN | Pricing |
|-----------|----------|-------------|---------|------------|------------|---------|
| LiveKit | WebRTC | Yes | Self/Cloud | Yes | Via SIP | Free/Usage |
| Pipecat | WebRTC/WS | Yes | Self | Yes | Via Twilio | Free |
| Daily | WebRTC | No | Cloud | Limited | No | Usage |
| Agora | WebRTC | No | Cloud | No | Yes | Usage |
| Twilio | WebRTC/PSTN | No | Cloud | No | Yes | Usage |

## Agentic Platform Comparison

| Platform | Complexity | Customization | Latency | PSTN | Pricing |
|----------|------------|---------------|---------|------|---------|
| Vapi | Low | Medium | ~2s | Yes | Per minute |
| Retell | Low | Medium | ~2s | Yes | Per minute |
| Bland AI | Low | Low | ~3s | Yes | Per minute |
| LiveKit Agents | High | High | <1s | Via SIP | Usage |
| Pipecat | High | High | <1s | Via Twilio | Free |
| Vocode | Medium | High | ~1.5s | Yes | Free/Usage |

## Provider Detection Signals

### In Privacy Policies
```
Look for: "subprocessors", "third-party services", "data processors"
Common sections: "Privacy Policy", "Legal", "Security", "Compliance"
```

### In Job Postings
```
ASR signals: "speech recognition", "STT", "ASR", "transcription"
TTS signals: "text-to-speech", "TTS", "voice synthesis"
Real-time signals: "WebRTC", "real-time audio", "low-latency"
Framework signals: "LiveKit", "Pipecat", "Twilio", "Agora"
```

### In Technical Documentation
```
API endpoints: "/transcribe", "/synthesize", "/stream"
SDKs: "deepgram-sdk", "@livekit/agents", "pipecat"
Config: "ASR_PROVIDER", "TTS_PROVIDER", "VOICE_MODEL"
```

### In GitHub Repositories
```
package.json: "deepgram", "elevenlabs", "livekit"
requirements.txt: "deepgram-sdk", "elevenlabs", "pipecat-ai"
Docker images: "livekit/livekit-server", "pipecat"
```

## Competitive Intelligence

### Who Uses What (Known)

| Company | ASR | TTS | Framework |
|---------|-----|-----|-----------|
| Vapi | Deepgram | ElevenLabs/PlayHT | Custom |
| Retell | Deepgram | ElevenLabs | Custom |
| Bland AI | Deepgram | ElevenLabs | Custom |
| Otter.ai | Proprietary | N/A | Custom |
| Fireflies | Assembly AI | N/A | Custom |

## Integration Patterns

### Voice Agent Stack
```
User → PSTN/WebRTC → ASR → LLM → TTS → PSTN/WebRTC → User
         ↓
    [Real-time Framework]
         ↓
    LiveKit / Pipecat / Daily
```

### Meeting Bot Stack
```
Meeting → Bot Join → Audio Capture → ASR → Storage/LLM
              ↓
         [Recall.ai / Custom]
              ↓
         Zoom/Teams/Meet API
```
