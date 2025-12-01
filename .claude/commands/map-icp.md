---
description: Map a company to Blynt's ICP (1-4 or N/A) based on voice/audio characteristics
argument-hint: <company_name or domain>
---

# ICP Mapping Task

Analyze the provided company using the **decision tree framework** to determine which of Blynt AI's 4 Ideal Customer Profiles (ICPs) they match best.

## Input
Company: {{arg}}

---

## Decision Tree Framework

Follow this decision tree sequentially to classify the company:

### Q0: Does the business involve conversation/speech?
**Question:** "Does the company's core product/service involve voice conversations, phone calls, meetings, or audio recordings?"

- **NO** → **ICP N/A** (No voice/audio use case)
- **YES** → Continue to Q1

---

### Q1: Is the company RECORDING audio?
**Question:** "Does the product capture/record audio (user-uploaded, API-recorded, or real-time streaming)?"

- **NO** → **ICP N/A** (No audio = no ASR need)
- **YES** → Continue to Q2

---

### Q2: Is the company TRANSCRIBING audio?
**Question:** "Does the product convert speech to text (ASR/transcription)?"

- **NO** → Ask: "Do they WANT to add transcription?"
  - **YES, want to add** → **ICP 1 (White-Label Runtime)**
  - **NO, don't need it** → **ICP N/A**
- **YES, already transcribing** → Continue to Q3

---

### Q3: Is the company APPLYING AI on transcripts?
**Question:** "Do they process transcripts with AI/ML for insights (summary, sentiment, actions, coaching, etc.)?"

- **NO** → **ICP 2 (Post-Call Intelligence)**
  - Just displaying/searching transcripts → basic use case, could upsell AI features
- **YES** → Continue to Q4

---

### Q4: WHEN does transcription happen?
**Question:** "Is transcription happening in REAL-TIME during conversation, or POST-CALL after?"

#### **REAL-TIME (during conversation)**
**Indicators:**
- User speaks → AI responds immediately
- Low latency critical (<500ms)
- Need turn-taking detection
- Streaming ASR required

**→ ICP 3 (Real-Time Voice Agents)**

#### **POST-CALL (after conversation)**
**Indicators:**
- Recording processed after conversation ends
- Latency tolerance: seconds to minutes
- Batch processing acceptable

**→ Continue to Q5**

---

### Q5: Volume + Custom Model Needs?
**Question:** "What's the monthly volume and do they need custom models?"

**Assess these factors:**
- **Monthly audio volume** (hours/month)
- **Industry jargon** (medical, legal, technical terms)
- **Unique acoustics** (noisy environments, far-field, specific hardware)
- **Specific demographics** (accents, age groups, non-native speakers)

#### Decision Matrix:

| Custom Model Need | → ICP |
|-------------------|-------|
| No (generic ASR works) | **ICP 2** (Post-Call Intelligence) |
| Yes (jargon/acoustics/demographics) | **ICP 4** (Studio + Benchmarking) |

**Note:** Volume doesn't determine ICP - both small note-takers and large conversation intelligence platforms are ICP 2. The differentiator is whether generic ASR is sufficient or custom models are needed.

---

## ICP Definitions

### ICP 1: White-Label Runtime Solutions
**Technical Maturity:** Low-Medium (Need turnkey solutions)
**Value Prop:** White-label Recall-like solution for ambient audio capture

**Target Profile:**
- Companies with **untapped ambient audio potential**
- Want to add voice capabilities WITHOUT building in-house
- Don't have speech AI yet, but users have speech-intensive workflows

**Key Characteristics:**
- Recording audio BUT not transcribing yet (or basic transcription only)
- Want to start processing conversations for value
- Small/non-existent ML team (need SDK/API that "just works")
- Volume: Low-Medium (<50K hours/month)
- Decision-maker: Product Manager, VP Product

**Target Sectors:**
- Construction/Field Services (Faks, Hosman)
- CRM/Sales platforms adding voice notes
- Customer Support tools adding voice context
- Healthcare admin (non-clinical)
- Travel agents (Worldia)

**Examples:** Faks, Hosman, Worldia

---

### ICP 2: Post-Call Intelligence / Conversation Intelligence
**Technical Maturity:** Medium to High (Use existing ASR, need better quality/cost)
**Value Prop:** High-quality ASR for transcription + downstream AI processing at any scale

**Target Profile:**
- Companies that RECORD meetings/calls and process for intelligence
- Post-call/meeting AI analysis (summary, actions, sentiment, coaching, analytics)
- Using generic ASR (Deepgram/Assembly/Azure) - want better quality OR lower costs
- **Includes both:** Early-stage note-takers AND established conversation intelligence platforms

**Key Characteristics:**
- Already transcribing + applying AI
- Timing: POST-call/meeting (not real-time)
- Volume: **Any scale** - from 10K to 10M hours/month
- Technical team (size varies by company stage)
- Decision-maker: CTO, VP Engineering, Head of AI/ML

**Pain Points by Stage:**
- **Early-stage (Circleback, Grain):** Need better accuracy, multilingual support, reasonable pricing
- **Scale-up (Modjo, Jiminny):** Quality + cost optimization as volume grows
- **Established (Gong, Chorus):** Cost reduction at massive scale, vendor diversification

**Target Sectors:**
- Meeting note-takers (Circleback, tl;dv, Fireflies, Otter, Grain)
- Sales conversation intelligence (Modjo, Gong, Chorus, Jiminny, Leexi)
- Customer support QA (call center analytics, Foundever)
- Meeting platforms (Zoom IQ, Microsoft Teams if external ASR)
- Compliance/legal (call recording + analysis)

**Examples:** Circleback, tl;dv, Modjo, Gong, Chorus, Jiminny, Leexi, Claap, Granola, Foundever, Aircall

---

### ICP 3: Real-Time Voice Agents
**Technical Maturity:** Medium-High (Building voice AI products)
**Value Prop:** Ultra-low latency ASR with turn-taking, interruption handling

**Target Profile:**
- Building REAL-TIME voice agents with conversational flow
- Low latency critical (<500ms end-to-end)
- Need turn-taking detection, interruption handling

**Key Characteristics:**
- Timing: **REAL-TIME** (streaming during conversation)
- User speaks → AI responds immediately
- Strong engineering + ML team
- Volume: Medium-Very High
- Decision-maker: CTO, VP Engineering, Co-founder (technical)

**Target Sectors:**
- Healthcare voice agents (Vocca, Talkie.ai, Hello Patient, Marshmallow)
- Customer support bots (conversational IVR)
- Sales/SDR automation (AI SDR callers)
- Voice-enabled chatbots (ChatGPT voice mode clones)
- Coaching/training (AI role-play)

**Examples:** Vocca, Marshmallow, Sandra AI, Talkie.ai, Yaqoot

---

### ICP 4: Audio ML Product Companies (Studio + Benchmarking)
**Technical Maturity:** High (Custom model development)
**Value Prop:** Studio platform for fine-tuning + Benchmarking tools

**Target Profile:**
- Building audio ML products - need custom model development
- Fine-tuning on proprietary data
- Specialized domains (medical, legal, hardware)

**Key Characteristics:**
- Need custom models (industry jargon, unique acoustics, specific demographics)
- Large ML/research team with ASR specialists
- Volume: Very High
- Cannot use generic ASR (accuracy too low)
- Decision-maker: Head of ML/AI, Chief Scientist, VP Research

**Specialized Needs:**
- **Industry jargon:** Medical (Doctolib, Nabla), legal, technical
- **Unique acoustics:** Smart speakers (Sonos), noisy environments
- **Specific demographics:** Accents, age groups, non-native speakers
- **Proprietary data:** On-prem/private cloud required

**Target Sectors:**
- Consumer audio hardware (Sonos, Bose, Apple HomePod)
- Healthcare AI scribes (Doctolib, Nabla, Abridge, Sully AI)
- Speech-to-text API providers (Assembly competitors)
- Audio analytics platforms (Pyannote.ai, speaker recognition)

**Examples:** Sonos, Doctolib, Nabla, Pyannote.ai

---

### ICP N/A: Not a Fit
Companies that don't align with any ICP.

**Reasons:**
- No audio/voice use case in product
- Not recording or transcribing audio
- Wrong scale (too small: <1K hours/month)
- Non-technical buyer (can't evaluate ASR)
- Embedded-only (no cloud API usage)
- Budget constraints (pre-seed, no revenue)

---

## Your Task

### Step 1: Research the Company
- If domain provided, enrich it with `/enrich-company`
- If company name, search for website and key information
- Gather data to answer decision tree questions

### Step 2: Apply Decision Tree
Work through Q0 → Q1 → Q2 → Q3 → Q4 → Q5 sequentially:

**Critical Data Points to Find:**
1. ✅ Business involves conversation/speech? (Y/N)
2. ✅ Recording audio? (Y/N)
3. ✅ Transcribing audio? (Y/N)
4. ✅ Applying AI on transcripts? (Y/N)
5. ✅ Timing: Real-time or Post-call?
6. ✅ Monthly volume estimate (hours/month)
7. ✅ Industry jargon / unique acoustics / specific demographics? (Y/N)

### Step 3: Provide Structured Output

```
# ICP Mapping: [Company Name]

## Best Fit ICP: [1, 2, 3, 4, or N/A]
**Confidence:** [High/Medium/Low]

## Decision Tree Analysis

### Q0: Business involves conversation/speech?
- **Answer:** [Yes/No]
- **Evidence:** [How you determined this]

### Q1: Recording audio?
- **Answer:** [Yes/No]
- **Evidence:** [e.g., "They offer meeting recording", "Voice agent takes calls"]

### Q2: Transcribing audio?
- **Answer:** [Yes/No/Want to add]
- **Evidence:** [e.g., "Website mentions transcription", "Currently only storing audio files"]

### Q3: Applying AI on transcripts?
- **Answer:** [Yes/No]
- **Evidence:** [e.g., "Generate meeting summaries", "Extract action items", "Sentiment analysis"]

### Q4: Timing of transcription?
- **Answer:** [Real-time / Post-call / N/A]
- **Evidence:** [e.g., "Voice agent responds in conversation = real-time", "Process after meeting = post-call"]

### Q5: Volume + Custom Model Needs?
- **Monthly Volume Estimate:** [X hours/month or "Unknown"]
- **Industry Jargon:** [Yes/No - specify domain]
- **Unique Acoustics:** [Yes/No - specify environment]
- **Specific Demographics:** [Yes/No - specify]

**Custom Model Need:** [Yes/No]

## ICP Classification Result

**Assigned ICP:** [1/2/3/4/N/A]

**Reasoning:**
[Explain how decision tree led to this ICP, referencing specific questions]

**Example:**
"Q0-Q3: Yes to all (recording, transcribing, AI processing). Q4: Real-time (voice agent responds during conversation). → ICP 3 (Real-Time Voice Agents). Turn-taking and low latency are critical for their appointment booking bot."

## Company Profile

- **Industry:** [e.g., Healthcare, Sales Tech, Meeting Intelligence]
- **Company Size:** [employees]
- **Product Type:** [e.g., Voice agent, Meeting note-taker, Conversation intelligence]
- **Current ASR Provider:** [Deepgram/Assembly/Azure/Unknown]
- **Estimated Monthly Volume:** [X hours/month]
- **Technical Maturity:** [Low/Medium/High]

## Key ICP Characteristics Matched

**From ICP [X] definition:**
- ✅ [Characteristic 1 from ICP definition that matches]
- ✅ [Characteristic 2]
- ✅ [Characteristic 3]
- ✅ [Characteristic 4]
- ⚠️ [Any partial matches or uncertainties]

## Decision-Maker Profile

**Likely buyer:** [role - e.g., CTO, VP Engineering, Head of AI/ML, Director of Product]
**Why:** [Brief reasoning based on ICP and company stage]

## Blynt Value Proposition

**For ICP [X]:**
[The specific value prop from the ICP definition]

**Key pain points Blynt solves:**
- [Pain point 1 specific to this company]
- [Pain point 2]
- [Pain point 3]

## Red Flags / Mismatches (if any)

[Note any characteristics that DON'T align with the ICP, or uncertainties]

**Examples:**
- "Volume unknown - need to validate in discovery call"
- "Unclear if they need real-time or batch processing"
- "Company size smaller than typical ICP 3, but use case fits"

## Recommended Next Steps

1. [e.g., "Reach out to CTO with ICP 3 pitch focused on low latency + turn-taking"]
2. [e.g., "Validate monthly call volume in discovery"]
3. [e.g., "Reference their Deepgram usage as switching opportunity"]
4. [e.g., "Emphasize HIPAA compliance for healthcare use case"]

## Data Sources

[List URLs where you found this information]
- Company website: [URL]
- LinkedIn: [URL]
- Product pages: [URLs]
- News/funding: [URLs]
- Technology stack: [URLs]
```

---

## Special Cases & Edge Cases

### Case 1: Real-time voice agent with specialized jargon
**Example:** Vocca (healthcare appointment booking with medical terms)

**Decision:** Timing trumps jargon → **ICP 3**
**Rationale:** Real-time latency/turn-taking is non-negotiable; jargon can be handled with prompt engineering

### Case 2: High-volume post-call WITH custom model needs
**Example:** Large healthcare system with millions of patient calls

**Decision:** Ask "What's your #1 pain point: cost, quality, or customization?"
- Customization → **ICP 4**
- Cost/Quality → **ICP 2**

### Case 3: Not transcribing yet but high potential
**Example:** Construction company (Faks) recording site meetings but only storing audio

**Decision:** Low technical maturity → **ICP 1**

### Case 4: Meeting platform with live captions + post-call AI
**Example:** Zoom showing real-time captions + generating post-call summaries

**Decision:** Ask "Which feature drives more value?"
- Live captions are core → **ICP 3**
- Post-call summaries are core → **ICP 2**

---

## Step 4: Save ICP to Notion (Token-Optimized)

After completing your analysis, save the ICP classification to Notion using the **Python script** instead of MCP tools to save ~8-12k tokens.

### Option A: Update existing company
```bash
# First, check if company exists
.venv/bin/python3 scripts/notion_contact_ops.py get-company --domain "company.com"

# If found, update ICP
.venv/bin/python3 scripts/notion_contact_ops.py update-icp \
  --company-id "PAGE_ID_FROM_ABOVE" \
  --icp "3"
```

### Option B: Create or update company with ICP
```bash
.venv/bin/python3 scripts/notion_contact_ops.py create-or-update-company \
  --name "Company Name" \
  --website "https://company.com" \
  --icp "3" \
  --vertical "Voice AI" \
  --product-desc "Brief 5-word description"
```

**Response Format:**
```json
{
  "success": true,
  "page_id": "xxx-xxx-xxx",
  "icp": "3",
  "url": "https://notion.so/xxxxx"
}
```

After saving to Notion, confirm:
```
✅ ICP Classification saved to Notion
**Company:** [Name]
**ICP:** [1/2/3/4/N/A]
**Notion Page:** [URL from script response]
```

## Important Notes

- **Token Savings:** Using Python script saves ~8-12k tokens per ICP update (83% reduction)
- **Use `/enrich-company`** if you need more data about the company before mapping
- **Be conservative** - if unclear between 2 ICPs, explain both and mark as "Medium/Low confidence"
- **Focus on CURRENT state**, not potential future
- **Volume thresholds:**
  - Low: <50K hours/month
  - Medium: 50K-500K hours/month
  - High: >500K hours/month
- **The Notion database property** `ICP` accepts: "1", "2", "3", "4", "N/A"
- **If uncertain**, ask follow-up questions rather than guessing

---

## Quick Decision Shortcuts

**Has these signals → Likely ICP:**
- ❌ Not transcribing yet → **ICP 1 or N/A**
- 🎤 Voice agent that responds in real-time → **ICP 3**
- 📝 Meeting note-taker / post-call summaries → **ICP 2**
- 📊 Conversation intelligence (any scale: Circleback to Gong) → **ICP 2**
- 🏥 Medical/legal jargon + need fine-tuning → **ICP 4**
- 🔴 No audio use case → **N/A**
