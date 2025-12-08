---
name: classifying-companies
description: Classifies companies into Blynt's ICP categories (1-4 or N/A) based on their voice/speech product. Used when determining if a company fits Blynt's real-time transcription API, when assigning ICP scores, or when evaluating sales prospects.
---

# ICP Classification

Classifies companies for Blynt's **Real-time Transcription API** (turn-taking, keyword boosting, contextualization, interruption handling).

## Quick Reference

**ICP 1**: Speech/Dictation → medical dictation, note apps, voice input
**ICP 2**: Meeting AI → transcription, call intelligence, QA tools
**ICP 3**: Voice Agents → AI phone, voice bots, conversational AI
**ICP 4**: Custom Solutions → enterprise voice, white-label, regulated
**N/A**: No voice/speech use case

## Detailed Classification

### ICP 1: Speech/Dictation Products

**Description**: Companies adding speech or dictation capabilities to their product.

**Key Signals**:
- Healthcare documentation / medical dictation
- Legal transcription tools
- Note-taking applications with voice input
- Productivity apps with speech-to-text
- Accessibility features (voice control)

**Examples**: Dragon Medical, Nuance, Otter.ai (dictation mode), Speechmatics

**Blynt Value Prop**: Accurate real-time transcription with custom vocabulary boosting for domain-specific terms.

---

### ICP 2: Meeting AI Assistants

**Description**: Companies building meeting assistants with AI capabilities.

**Key Signals**:
- Meeting transcription platforms
- Sales call intelligence / conversation analytics
- Customer support QA tools
- Collaboration tools with AI note-taking
- Real-time captions for video calls

**Examples**: Otter.ai, Fireflies.ai, Gong, Chorus, Grain, tldv, Jiminny

**Blynt Value Prop**: Natural turn-taking for multi-speaker detection, real-time processing for live meetings.

---

### ICP 3: Voice Agents Platforms/Products

**Description**: Companies building voice agent platforms or voice-enabled products.

**Key Signals**:
- AI phone assistants / voice bots
- Conversational AI platforms
- Voice-enabled customer support
- AI receptionists
- Voice agents for scheduling/ordering

**Examples**: Vapi, Bland AI, Air.ai, Retell, Goodcall, Beside, Vocode

**Blynt Value Prop**: Low-latency transcription with interruption handling for natural conversations, real-time contextualization for dynamic responses.

---

### ICP 4: Custom Speech/Voice Solutions

**Description**: Companies building fully customized speech/voice products.

**Key Signals**:
- Enterprise voice infrastructure
- Proprietary voice AI platforms
- White-label voice solutions
- Industry-specific voice applications (finance, healthcare, government)
- Custom ASR model requirements

**Examples**: Large enterprises with internal voice teams, regulated industries

**Blynt Value Prop**: Flexible API with enterprise-grade features, customization options.

---

### N/A: Not a Fit

**When to use**:
- Company doesn't use voice/speech technology
- Primary focus is text-only AI (chatbots without voice)
- Consumer apps without transcription needs
- Hardware-only companies
- Companies using only pre-recorded audio (not real-time)

---

## Classification Decision Tree

```
Does the company use real-time voice/speech?
├── No → N/A
└── Yes → What's their primary use case?
    ├── Dictation/Speech-to-text input → ICP 1
    ├── Meeting recording/transcription → ICP 2
    ├── Voice agents/conversational AI → ICP 3
    └── Custom enterprise solution → ICP 4
```

## Confidence Indicators

**High Confidence**:
- Clear product description mentioning transcription/voice
- Job postings for voice/speech engineers
- Documentation mentioning ASR/STT providers
- Pricing page with transcription-related features

**Medium Confidence**:
- General AI product that might use voice
- Mentions "AI assistant" without specifics
- Competitor to known ICP companies

**Low Confidence**:
- Limited public information
- Early-stage with unclear product
- Multiple potential use cases

## Classification Workflow

Copy this checklist and track your progress:

```
Classification Progress:
- [ ] Step 1: Review company product/website
- [ ] Step 2: Identify voice/speech indicators
- [ ] Step 3: Match to ICP category
- [ ] Step 4: Assess confidence level
- [ ] Step 5: Document reasoning
```

## Additional Resources

**Real examples**: See [examples.md](examples.md) for classified companies with reasoning
**Output template**: See [templates/classification-output.md](templates/classification-output.md)
**Programmatic classification**: Run `python scripts/classify.py "company description"`
