# Blynt ICP Decision Tree
**Date:** 2025-10-27 (Updated: ICP 5 merged into ICP 2)
**Purpose:** Map companies to correct ICP (1-4 or N/A) based on voice/audio characteristics

> **📝 UPDATE (2025-10-27):** ICP 5 has been merged into ICP 2. Volume alone does not differentiate ICPs - both Circleback (small) and Gong (large) are ICP 2 (Post-Call Intelligence). The flowchart below references ICP 5 in legacy format but should be interpreted as ICP 2 for all post-call intelligence use cases.

---

## Decision Tree Flowchart

```
START: Does the company's business involve conversation/speech?
│
├─ NO ──────────────────────────────────────────────────► ICP N/A (Not a fit)
│
└─ YES ──► Q1: Is the company RECORDING audio?
           │
           ├─ NO ──────────────────────────────────────► ICP N/A (Not a fit)
           │                                              [No audio to process = no ASR need]
           │
           └─ YES ──► Q2: Is the company TRANSCRIBING audio?
                      │
                      ├─ NO ──► Q2a: Why not transcribing?
                      │         │
                      │         ├─ "We want to add transcription" ──► ICP 1 (White-Label Runtime)
                      │         │                                      [Untapped potential, need turnkey solution]
                      │         │
                      │         └─ "We don't need transcription" ───► ICP N/A (Not a fit)
                      │                                                [Audio storage only, no processing]
                      │
                      └─ YES ──► Q3: Is the company APPLYING AI on transcripts?
                                 │                      (summary, sentiment, actions, coaching, etc.)
                                 │
                                 ├─ NO ──► Q3a: What do they do with transcripts?
                                 │         │
                                 │         ├─ "Just display/search transcripts" ──► ICP 2 (Post-Call Intelligence)
                                 │         │                                         [Basic transcription user, could upsell AI]
                                 │         │
                                 │         └─ "Compliance/archival only" ─────────► ICP N/A or ICP 5
                                 │                                                  [Very high volume = ICP 5, else N/A]
                                 │
                                 └─ YES ──► Q4: When does transcription happen?
                                            │
                                            ├─ "REAL-TIME (during conversation)" ──► ICP 3 (Real-Time Voice Agents)
                                            │                                         [Low latency critical, turn-taking needed]
                                            │
                                            └─ "POST-CALL (after conversation)" ──► Q5: Volume + Maturity?
                                                                                    │
                                                                                    ├─ Low volume (<50K hours/month) ──────► ICP 2 (Post-Call Intelligence)
                                                                                    │  + Low-Medium maturity                 [Note-takers, small conv intelligence]
                                                                                    │
                                                                                    ├─ High volume (>500K hours/month) ────► ICP 5 (High-Volume Ambient)
                                                                                    │  + Already has ASR provider            [Cost optimization, quality improvement]
                                                                                    │
                                                                                    └─ Medium-High volume ──────────────────► Q6: Custom model needs?
                                                                                       + Medium-High maturity                │
                                                                                                                            ├─ YES (need fine-tuning) ──► ICP 4 (Studio + Benchmark)
                                                                                                                            │                             [Sonos, Doctolib, Nabla]
                                                                                                                            │
                                                                                                                            └─ NO (generic ASR works) ──► ICP 2 or ICP 5
                                                                                                                                                          [Depends on volume/maturity]
```

---

## Detailed Decision Criteria

### Q0: Business involves conversation/speech?
**Question:** "Does your company's core product/service involve voice conversations, phone calls, meetings, or audio recordings?"

**Examples:**
- ✅ **YES:** Meeting platforms, call centers, voice agents, conversation intelligence, medical scribes, podcast platforms
- ❌ **NO:** Pure text chatbots, email tools, document processors, visual/image products

**If NO → ICP N/A**

---

### Q1: Recording audio?
**Question:** "Does your product CAPTURE/RECORD audio (either user-uploaded, API-recorded, or real-time streaming)?"

**Examples:**
- ✅ **YES:** Zoom meetings, Gong (sales calls), Vocca (patient calls), medical ambient scribes
- ❌ **NO:** Companies that only consume pre-transcribed text, or don't handle audio at all

**If NO → ICP N/A** (No audio = no ASR need)

---

### Q2: Transcribing audio?
**Question:** "Does your product convert speech to text (ASR/transcription)?"

**Branch A - Not transcribing yet:**
- **Scenario:** Company records audio but doesn't transcribe (e.g., construction company recording site meetings but storing as audio files only)
- **Follow-up:** "Do you WANT to add transcription capabilities?"
  - If YES → **ICP 1 (White-Label Runtime)** - They need a turnkey solution to unlock audio value
  - If NO → **ICP N/A** - Audio storage only, no ASR need

**Branch B - Already transcribing:**
- Continue to Q3 (applying AI?)

---

### Q3: Applying AI on transcripts?
**Question:** "Do you process transcripts with AI/ML for insights (summary, sentiment analysis, action items, coaching, compliance checks, etc.)?"

**Examples:**
- ✅ **YES:**
  - Meeting note-takers generating summaries/action items (Circleback, tl;dv)
  - Sales conversation intelligence extracting objections/sentiment (Modjo, Gong)
  - Support QA analyzing agent performance (call center analytics)
  - Medical scribes generating clinical notes (Nabla, Abridge)
- ❌ **NO:**
  - Simple transcription display (just showing captions)
  - Searchable transcript archive (no AI processing)
  - Compliance recording (storage for legal purposes only)

**If NO:**
- If just display/search → **ICP 2** (basic transcription user, potential for upsell)
- If very high volume compliance → **ICP 5** (cost optimization play)
- If low volume compliance → **ICP N/A**

**If YES → Continue to Q4 (timing)**

---

### Q4: When does transcription happen?
**Question:** "Is transcription happening IN REAL-TIME during the conversation, or POST-CALL after it's finished?"

#### **REAL-TIME (during conversation)**
**Indicators:**
- User speaks → AI responds immediately (conversational flow)
- Low latency critical (<500ms end-to-end)
- Need turn-taking detection (when did user finish speaking?)
- Handle interruptions/barge-in
- Streaming ASR required

**Examples:**
- Voice agents: Vocca (appointment booking), Marshmallow (customer support)
- Live phone bots: AI SDRs, IVR systems
- Voice-enabled chatbots: ChatGPT voice mode clones
- Live coaching: Real-time feedback during calls

**→ ICP 3 (Real-Time Voice Agents)**

#### **POST-CALL (after conversation)**
**Indicators:**
- Recording happens first, processing happens later (batch or near-batch)
- Latency tolerance: seconds to minutes acceptable
- No turn-taking needed (entire audio file available)
- Can use batch ASR APIs

**Examples:**
- Meeting note-takers: Process recording after Zoom call ends
- Sales conversation intelligence: Analyze recorded sales calls nightly
- Medical scribes: Generate notes after patient visit

**→ Continue to Q5 (volume + maturity assessment)**

---

### Q5: Volume + Maturity assessment (for POST-CALL use cases)
**Question:** "What's your monthly audio processing volume and technical maturity?"

#### **Low Volume (<50K hours/month) + Low-Medium Maturity**
- **Companies:** Small meeting note-takers, early-stage conversation intelligence startups
- **Technical Team:** <10 engineers, limited ML expertise
- **Current ASR:** Using Deepgram/AssemblyAI basic tier
- **Need:** Better accuracy, multilingual support, reasonable pricing

**→ ICP 2 (Post-Call Intelligence)**

#### **High Volume (>500K hours/month) + Already Established**
- **Companies:** Gong, Chorus, Zoom IQ (if they externalize ASR), Microsoft Teams Premium
- **Technical Team:** Large engineering org with ML specialists
- **Current ASR:** Already using Deepgram/Azure/custom models at scale
- **Need:** Cost reduction, quality improvement, vendor diversification

**→ ICP 5 (High-Volume Ambient Intelligence)**

#### **Medium-High Volume + Medium-High Maturity**
- Need to assess custom model requirements → **Continue to Q6**

---

### Q6: Custom model/fine-tuning needs?
**Question:** "Do you need to fine-tune ASR models on custom data, or does generic ASR work for your use case?"

**Indicators of fine-tuning need:**
- ✅ **Specific industry jargon:** Medical terminology (Doctolib, Nabla), legal terms, technical vocabulary
- ✅ **Unique acoustics:** Hardware devices with specific microphone characteristics (Sonos speakers)
- ✅ **Specific demographics:** Accents, dialects, age groups not well-covered by generic models
- ✅ **Proprietary data:** Can't send sensitive audio to third-party APIs (need on-prem/private)
- ✅ **Building audio ML product:** Core competency is voice/audio (not just using ASR as utility)

**Examples needing fine-tuning:**
- **Healthcare:** Doctolib, Nabla (medical jargon, HIPAA compliance)
- **Consumer audio:** Sonos, Bose (device-specific acoustics)
- **Specialized domains:** Legal transcription, aviation (ATC), oil & gas (field jargon)

**→ ICP 4 (Studio + Benchmarking)**

**If generic ASR works fine:**
- Low-medium volume → **ICP 2**
- High volume → **ICP 5**

---

## Special Decision Criteria

### Has Specific Industry Jargon?
**Question:** "Does your audio contain specialized vocabulary that generic ASR models struggle with?"

**Examples:**
- ✅ **Medical:** Drug names, procedures, anatomical terms (Doctolib, Nabla, Abridge)
- ✅ **Legal:** Legal terminology, case citations (court transcription services)
- ✅ **Technical:** Engineering jargon, product SKUs (manufacturing, construction)
- ✅ **Finance:** Financial instruments, trading terminology (compliance recording)
- ❌ **General business:** Sales calls, meetings with common vocabulary (Modjo, Gong)

**Impact on ICP:**
- If jargon + need custom models → **ICP 4**
- If jargon but willing to use generic ASR → **ICP 2 or 5** (depending on volume)

---

### Has Unique Acoustics?
**Question:** "Is your audio captured in challenging acoustic environments or with specialized hardware?"

**Examples:**
- ✅ **Noisy environments:** Construction sites (Faks), factories, restaurants
- ✅ **Far-field audio:** Smart speakers (Sonos, Alexa), conference room microphones
- ✅ **Phone/VoIP:** Compressed audio, low bitrate (call center recordings)
- ✅ **Medical:** Stethoscope audio, operating room background noise
- ❌ **Clean recordings:** Zoom meetings, podcast-quality audio

**Impact on ICP:**
- If challenging acoustics + need custom models → **ICP 4**
- If challenging but generic ASR acceptable → **ICP 2 or 5**

---

### Has Specific Demographics?
**Question:** "Does your audio feature speakers from demographics underserved by generic ASR models?"

**Examples:**
- ✅ **Accents:** Strong regional accents (Southern US, Scottish, Indian English)
- ✅ **Non-native speakers:** English spoken by non-native speakers in specific regions
- ✅ **Age groups:** Children (educational apps), elderly (healthcare)
- ✅ **Sociolects:** Industry-specific speaking patterns (medical residents, tech workers)

**Impact on ICP:**
- If specific demographics + need better coverage → **ICP 4** (fine-tuning)
- If willing to accept generic ASR accuracy → **ICP 2 or 5**

---

## Quick Reference Matrix

| **Criteria** | **ICP 1** | **ICP 2** | **ICP 3** | **ICP 4** | **N/A** |
|-------------|----------|----------|----------|----------|---------|
| **Recording audio?** | Want to start | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Transcribing?** | Want to start | ✅ Yes | ✅ Yes | ✅ Yes | No need |
| **Applying AI?** | Future goal | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Timing** | Post-call | Post-call | **Real-time** | Varies | N/A |
| **Volume** | Low-Medium | **Any scale** (10K-10M hrs/mo) | Med-High | Very High | Any |
| **Technical Maturity** | **Low** | Medium-High | Med-High | **High** | Any |
| **Custom models?** | ❌ No | ❌ No | ❌ No | ✅ **Yes** | N/A |
| **Industry jargon?** | Generic | Generic | Generic | ✅ **Specialized** | N/A |

---

## Edge Cases & Disambiguation Rules

### Case 1: High-volume post-call WITH custom model needs
**Example:** Large healthcare system (Kaiser Permanente) processing millions of patient calls with medical jargon

**Decision:**
- If primary need is **fine-tuning/custom models** → **ICP 4**
- If primary need is **cost/quality optimization** → **ICP 2**
- **Ask:** "What's your #1 pain point: cost, quality, or customization?"

---

### Case 2: Real-time voice agent with specialized jargon
**Example:** Medical appointment booking bot (Vocca) with healthcare terminology

**Decision:**
- **Timing trumps jargon** → **ICP 3** (Real-Time Voice Agents)
- Rationale: Real-time latency/turn-taking is non-negotiable; jargon can be handled with prompt engineering or post-processing

---

### Case 3: Company not transcribing yet but records high-volume audio
**Example:** Construction company (Faks) recording site meetings but only storing audio files

**Decision:**
- Low technical maturity + want to add transcription → **ICP 1** (White-Label)
- High volume + willing to invest in custom solution → **ICP 4** (Studio)
- **Ask:** "Do you want a turnkey solution, or do you have ML team to customize?"

---

### Case 4: Meeting platform with real-time captions but POST-call AI
**Example:** Zoom showing live captions during call, but AI summary generated after call ends

**Decision:**
- If **real-time captions are core value prop** → **ICP 3**
- If **post-call AI summary is core value prop** → **ICP 2**
- **Ask:** "Which feature drives more value for your users: live captions or post-call summaries?"

---

### Case 5: Very small volume but specialized jargon
**Example:** Legal transcription startup processing 1K hours/month with legal terminology

**Decision:**
- Specialized jargon + willing to pay premium → **ICP 4**
- Low volume + cost-sensitive → **ICP 2** (use generic ASR, accept lower accuracy)
- **Threshold:** <10K hours/month + budget <$10K/month → ICP 2; else ICP 4

---

## Implementation: `/map-icp` Command Logic

```python
def map_icp(company_data):
    # Q0: Business involves conversation/speech?
    if not company_data.get("involves_conversation"):
        return "N/A - No voice/audio use case"

    # Q1: Recording audio?
    if not company_data.get("recording_audio"):
        return "N/A - Not recording audio"

    # Q2: Transcribing audio?
    if not company_data.get("transcribing_audio"):
        wants_to_add = company_data.get("wants_transcription")
        return "ICP 1 - White-Label Runtime" if wants_to_add else "N/A - No transcription need"

    # Q3: Applying AI on transcripts?
    if not company_data.get("applying_ai"):
        volume = company_data.get("monthly_hours", 0)
        return "ICP 5 - High-Volume Ambient" if volume > 500_000 else "ICP 2 - Post-Call Intelligence"

    # Q4: Real-time or post-call?
    if company_data.get("timing") == "real-time":
        return "ICP 3 - Real-Time Voice Agents"

    # Q5 & Q6: Volume + Custom model needs (for post-call)
    volume = company_data.get("monthly_hours", 0)
    needs_custom_model = (
        company_data.get("industry_jargon") or
        company_data.get("unique_acoustics") or
        company_data.get("specific_demographics")
    )

    if needs_custom_model:
        return "ICP 4 - Studio + Benchmarking"

    if volume > 500_000:
        return "ICP 5 - High-Volume Ambient Intelligence"

    return "ICP 2 - Post-Call Intelligence"
```

---

## Next Steps

1. ✅ **Review decision tree logic** - Does this flow make sense?
2. **Test with real companies:**
   - Vocca (should map to ICP 3 ✓)
   - Circleback (should map to ICP 2 ✓)
   - Sonos (should map to ICP 4 ✓)
   - Gong (should map to ICP 5 ✓)
3. **Update `/map-icp` command** to use this decision tree
4. **Create assessment questionnaire** for discovery calls
5. **Reclassify existing Notion companies** using this logic

---

**Questions for you:**
1. Should real-time latency ALWAYS trump other factors (even specialized jargon)?
2. What's the minimum volume threshold for ICP 5? (I used 500K hours/month)
3. Do you want to add a "budget" criterion to filter out companies that can't afford premium ASR?
