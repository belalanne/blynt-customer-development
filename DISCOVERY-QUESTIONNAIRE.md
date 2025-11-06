# Blynt ICP Discovery Questionnaire
**Date:** 2025-10-27 (Updated: ICP 5 merged into ICP 2)
**Purpose:** Gather data to accurately map prospects to ICP 1-4 using decision tree

> **📝 UPDATE (2025-10-27):** ICP 5 has been merged into ICP 2. All post-call intelligence companies (from small note-takers to large platforms like Gong) are now classified as ICP 2, with volume as a maturity indicator rather than a separate ICP.

---

## How to Use This Questionnaire

### Pre-Call Research
- Complete Sections 0-2 using public information (website, LinkedIn, news)
- Use `/enrich-company [domain]` to automate Section 0-1 research
- Mark **[VALIDATE]** next to any assumptions that need confirmation

### Discovery Call Flow
- Start with Section 3 (Audio Usage) - establishes if they're a fit
- Follow decision tree branches based on answers
- Skip irrelevant sections (e.g., if not recording audio, skip Section 4-7)
- **Goal:** Complete enough data points to confidently assign ICP

### Post-Call
- Fill in any missing data points
- Run `/map-icp [company]` to validate ICP assignment
- Update Notion with ICP and key findings

---

## Section 0: Company Basics

**Pre-call research - gather from website/LinkedIn**

| **Field** | **Answer** | **Source** |
|-----------|------------|------------|
| Company Name | | |
| Website | | |
| Industry / Vertical | | |
| Company Size (employees) | | LinkedIn |
| Funding Stage | | Crunchbase/news |
| Funding Amount (if public) | | |
| Headquarters Location | | |
| Founded Year | | |

---

## Section 1: Product & Market

**Pre-call research - understand their business model**

### 1.1 Product Type
□ B2B SaaS platform
□ Consumer application
□ API/Infrastructure service
□ Hardware + software
□ Professional services
□ Other: ___________

### 1.2 Product Description (1-2 sentences)
[What does their product do?]

### 1.3 Target Customers
**Industry verticals they serve:**
- [ ] Healthcare
- [ ] Sales/CRM
- [ ] Customer Support
- [ ] Legal
- [ ] Financial Services
- [ ] Real Estate
- [ ] Construction/Field Services
- [ ] Education
- [ ] Other: ___________

**Customer size:**
- [ ] SMB (<100 employees)
- [ ] Mid-market (100-1000 employees)
- [ ] Enterprise (>1000 employees)

---

## Section 2: Technical Profile

**Pre-call research + call validation**

### 2.1 Engineering Team Size
- **Total Engineers:** _____ (LinkedIn estimate)
- **ML/AI Team:** _____ [VALIDATE in call]
- **Engineering Leadership:** CTO? VP Eng? Head of AI/ML?

### 2.2 Current Tech Stack (if visible)
- **Cloud Provider:** AWS / GCP / Azure / On-prem / Unknown
- **Known Technologies:** [from BuiltWith, job postings, tech blog]

### 2.3 ASR Provider (if known)
- [ ] Deepgram
- [ ] AssemblyAI
- [ ] Microsoft Azure Speech
- [ ] Google Speech-to-Text
- [ ] Amazon Transcribe
- [ ] Gladia
- [ ] Custom in-house model
- [ ] Not using ASR yet
- [ ] Unknown [ASK IN CALL]

---

## Section 3: Audio Usage (DECISION TREE START)

**Critical questions - determines if they're a fit at all**

### Q0: Does your business involve conversation/speech?

**Discovery Questions:**
- "Does your product involve phone calls, meetings, voice interactions, or audio recordings?"
- "What role does voice/audio play in your customers' workflows?"

**Answer:**
□ **YES** - Product involves conversation/speech → **CONTINUE**
□ **NO** - No audio/voice use case → **ICP N/A - END CALL**

**Evidence/Notes:**

---

### Q1: Are you RECORDING audio?

**Discovery Questions:**
- "Does your product capture or record audio?"
- "How do users get audio into your system?" (upload, API, real-time capture, phone calls)

**Answer:**
□ **YES** - Recording audio → **CONTINUE TO Q2**
□ **NO** - Not recording audio → **ICP N/A - END CALL**

**Recording Method:**
- [ ] Meeting/call recording (Zoom, Teams, phone)
- [ ] User uploads audio files
- [ ] Real-time capture via API (Recall.ai, Fireflies)
- [ ] Voice agent takes live calls
- [ ] Hardware device microphone
- [ ] Other: ___________

**Evidence/Notes:**

---

### Q2: Are you TRANSCRIBING audio?

**Discovery Questions:**
- "Do you convert speech to text? Who provides your ASR/transcription?"
- "If not transcribing yet: Would adding transcription be valuable to your customers?"

**Answer:**
□ **YES, already transcribing** → **CONTINUE TO Q3**
□ **NO, but we WANT to add transcription** → **LIKELY ICP 1**
□ **NO, don't need transcription** → **ICP N/A**

**If YES, transcribing:**
- **ASR Provider:** ___________
- **Monthly transcription volume:** _____ hours/month [ESTIMATE]
- **Primary use case for transcripts:** ___________

**If WANT to add:**
- **Why not transcribing yet?** ___________
- **Technical maturity:** Do you have ML team? ___________
- **Budget for ASR:** $_____ /month

**Evidence/Notes:**

---

### Q3: Are you APPLYING AI on transcripts?

**Discovery Questions:**
- "Once you have transcripts, what do you do with them?"
- "Do you generate summaries, extract insights, analyze sentiment, etc.?"

**Answer:**
□ **YES, applying AI** → **CONTINUE TO Q4**
□ **NO, just display/search transcripts** → **Check volume** (Q3b)

#### Q3b: If NOT applying AI, what's your volume?

**Answer:**
□ **High volume (>500K hrs/month)** → **LIKELY ICP 2** (established player, cost optimization focus)
□ **Low-medium volume** → **LIKELY ICP 2** (could upsell AI features)

**AI Processing Details (if YES):**

- [ ] **Meeting summaries** (key points, action items)
- [ ] **Sales intelligence** (objections, sentiment, talk time, questions)
- [ ] **Customer support QA** (agent performance, compliance, sentiment)
- [ ] **Medical documentation** (clinical notes, diagnosis codes)
- [ ] **Compliance/legal analysis** (risk detection, policy violations)
- [ ] **Coaching/training** (feedback, performance scoring)
- [ ] **Other:** ___________

**Evidence/Notes:**

---

### Q4: WHEN does transcription happen?

**Discovery Questions:**
- "Is transcription happening DURING the conversation or AFTER it's finished?"
- "How critical is low latency for your use case?"
- "Do you need the AI to respond in real-time during the conversation?"

**Answer:**
□ **REAL-TIME (during conversation)** → **LIKELY ICP 3** - GO TO SECTION 4
□ **POST-CALL (after conversation)** → **CONTINUE TO Q5** - GO TO SECTION 5

**Real-Time Indicators:**
- User speaks → AI responds immediately (conversational flow)
- Latency critical (<500ms acceptable?)
- Need turn-taking detection (know when user finished speaking)
- Handle interruptions/barge-in

**Post-Call Indicators:**
- Process recording after call/meeting ends
- Batch or near-batch processing (seconds to minutes acceptable)
- Entire audio file available upfront

**Evidence/Notes:**

---

## Section 4: Real-Time Voice Agent Details (IF Q4 = REAL-TIME)

**If Q4 answered "Real-time" → Focus on ICP 3 characteristics**

### 4.1 Voice Agent Use Case

**Primary application:**
- [ ] Customer support bot (IVR, phone support)
- [ ] Sales automation (AI SDR, outbound calling)
- [ ] Healthcare appointment booking
- [ ] Voice-enabled chatbot (ChatGPT voice mode clone)
- [ ] Coaching/training (real-time feedback)
- [ ] Other: ___________

### 4.2 Latency Requirements

**Discovery Questions:**
- "What latency can you tolerate end-to-end?" (speech → transcription → LLM → TTS → response)
- "What's your current latency with [current ASR provider]?"
- "Do you have users complaining about response time?"

**Current Latency:** _____ ms
**Target Latency:** _____ ms
**Acceptable Latency:** _____ ms

### 4.3 Turn-Taking & Interruptions

**Discovery Questions:**
- "How do you detect when the user has finished speaking?"
- "Can users interrupt the AI mid-response?"
- "What happens if someone talks over the AI?"

**Current Solution:**
- [ ] VAD (Voice Activity Detection) with fixed timeout
- [ ] ASR provider's endpointing
- [ ] Custom model/logic
- [ ] Don't handle well yet (pain point!)

**Interruption Handling:**
- [ ] Users can interrupt (barge-in support)
- [ ] Agent finishes speaking, then processes interrupt
- [ ] Poor experience currently

### 4.4 Volume & Scale

**Current Metrics:**
- **Daily/monthly call volume:** _____calls or _____ minutes/month
- **Concurrent calls:** _____ (peak capacity)
- **Expected growth:** _____ % over next 12 months

### 4.5 Current ASR Pain Points

**Discovery Questions:**
- "What issues do you have with your current ASR provider?"
- "Where do you see transcription errors most often?"

**Rate Pain Points (1-5, 5=severe):**
- **Latency too high:** ___/5
- **Accuracy issues:** ___/5
- **Turn-taking detection:** ___/5
- **Cost:** ___/5
- **Reliability/uptime:** ___/5
- **Other:** ___________

### ICP 3 Confidence

Based on answers above:

□ **HIGH** - Clear real-time voice agent, latency critical, strong technical team
□ **MEDIUM** - Real-time but less sophisticated (may be ICP 2 if latency not critical)
□ **LOW** - Unsure if truly real-time or just fast batch processing

**→ Assign ICP 3 if HIGH confidence**

---

## Section 5: Post-Call Processing Details (IF Q4 = POST-CALL)

**If Q4 answered "Post-call" → Determine ICP 2, 4, or 5 based on volume + custom model needs**

### 5.1 Processing Use Case

**Primary application:**
- [ ] Meeting note-taker (Zoom, Teams, Google Meet)
- [ ] Sales conversation intelligence (analyze sales calls)
- [ ] Customer support QA (call center quality monitoring)
- [ ] Medical scribe (clinical documentation)
- [ ] Legal transcription (depositions, hearings)
- [ ] Compliance recording (financial, healthcare)
- [ ] Podcast/media transcription
- [ ] Other: ___________

### 5.2 Volume Assessment

**Discovery Questions:**
- "How many hours of audio do you process per month?"
- "What's your expected growth over the next year?"

**Current Monthly Volume:**
- [ ] **Low:** <10K hours/month
- [ ] **Medium-Low:** 10K-50K hours/month
- [ ] **Medium:** 50K-200K hours/month
- [ ] **Medium-High:** 200K-500K hours/month
- [ ] **High:** >500K hours/month → **LIKELY ICP 2** (established scale-up/enterprise)

**Volume Details:**
- **Exact estimate:** _____ hours/month
- **Growth rate:** _____ % per year
- **Seasonal variation:** Yes / No

### 5.3 Custom Model Needs Assessment

**Determine if generic ASR is sufficient or if they need fine-tuning**

#### 5.3a Industry Jargon

**Discovery Questions:**
- "Does your audio contain specialized terminology that generic ASR struggles with?"
- "What accuracy are you seeing with your current ASR on domain-specific terms?"

**Specialized Vocabulary:**
- [ ] **Medical:** Drug names, procedures, anatomy (Doctolib, Nabla) → **ICP 4 SIGNAL**
- [ ] **Legal:** Legal terms, case citations, courtroom language → **ICP 4 SIGNAL**
- [ ] **Technical:** Engineering jargon, product SKUs, code terms → **ICP 4 SIGNAL**
- [ ] **Financial:** Trading terms, financial instruments → **ICP 4 SIGNAL**
- [ ] **None/Generic:** Standard business vocabulary → **ICP 2 or 5**

**Current Accuracy on Jargon:** _____ % (if known)
**Target Accuracy:** _____ %

#### 5.3b Unique Acoustics

**Discovery Questions:**
- "What are the recording conditions for your audio?"
- "Do you have challenges with background noise, audio quality, or specific hardware?"

**Acoustic Environment:**
- [ ] **Clean:** Podcast-quality, Zoom meetings → **Generic ASR OK**
- [ ] **Noisy:** Construction sites, factories, restaurants → **ICP 4 SIGNAL**
- [ ] **Far-field:** Smart speakers, conference rooms → **ICP 4 SIGNAL**
- [ ] **Phone/VoIP:** Compressed audio, low bitrate → **May need ICP 4**
- [ ] **Medical:** Stethoscope, operating room → **ICP 4 SIGNAL**
- [ ] **Hardware-specific:** Custom microphones (Sonos, Bose) → **ICP 4 SIGNAL**

#### 5.3c Specific Demographics

**Discovery Questions:**
- "What accents, languages, or demographics are present in your audio?"
- "Do you see accuracy drop-offs with certain speaker groups?"

**Speaker Demographics:**
- [ ] **Standard accents:** US/UK English, well-covered → **Generic ASR OK**
- [ ] **Regional accents:** Southern US, Scottish, Indian English → **ICP 4 SIGNAL**
- [ ] **Non-native speakers:** Specific L1 backgrounds → **ICP 4 SIGNAL**
- [ ] **Age groups:** Children, elderly → **ICP 4 SIGNAL**
- [ ] **Sociolects:** Industry-specific speaking patterns → **Possible ICP 4**

### 5.4 Custom Model Need Summary

**Based on 5.3a-c, does this company need custom models?**

□ **YES - Need custom models** → **LIKELY ICP 4**
   - Specialized jargon OR unique acoustics OR specific demographics
   - Generic ASR accuracy insufficient
   - Willing to invest in fine-tuning

□ **NO - Generic ASR works** → **ICP 2 or 5 based on volume**
   - Standard vocabulary, clean audio, common accents
   - Current ASR provider accuracy acceptable (pain is cost or minor improvements)

### 5.5 ICP 2 Maturity Stages (if NO custom model need)

**ICP 2 now encompasses all post-call intelligence companies regardless of volume. Distinguish by maturity stage:**

| **Maturity Stage** | **Early-Stage** | **Scale-Up** | **Established/Enterprise** |
|-------------------|-----------------|--------------|----------------------------|
| **Volume** | <50K hrs/month | 50K-500K hrs/month | >500K hrs/month |
| **Examples** | Circleback, Grain | Modjo, Jiminny | Gong, Chorus |
| **Team Size** | <10 engineers | 10-50 engineers | 50+ engineers |
| **Primary Pain** | Better quality, multilingual | Quality + cost optimization | Cost reduction at scale |
| **Current Provider** | Using basic tier | Standard/Pro tier | Enterprise contract |

**All are ICP 2** - but maturity stage affects pitch focus and contract size expectations.

---

## Section 6: Technical Maturity & Decision-Maker

**Applies to all ICPs - helps refine pitch and approach**

### 6.1 Engineering Team Composition

**Discovery Questions:**
- "Tell me about your engineering team structure"
- "Do you have ML/AI specialists in-house?"
- "Who owns the ASR integration?"

**Team Details:**
- **Total Engineers:** _____
- **ML/AI Team Size:** _____
- **ASR Specialists:** Yes / No
- **Team Skill Level:** Junior / Mid / Senior / Mixed

**ML Maturity:**
- [ ] No ML expertise (rely on APIs)
- [ ] Basic ML usage (integrate existing models)
- [ ] Advanced ML (fine-tune, train models)
- [ ] Research-level (publish papers, build from scratch)

### 6.2 Decision-Making Process

**Discovery Questions:**
- "Who typically makes decisions about adopting new ASR/ML vendors?"
- "What's the approval process for tools like ours?"
- "Do you have budget authority, or does someone else?"

**Primary Decision-Maker:**
- [ ] CEO/Co-founder (startup)
- [ ] CTO
- [ ] VP Engineering
- [ ] Head of ML/AI
- [ ] Director of Product
- [ ] Product Manager
- [ ] Other: ___________

**Decision Process:**
- **Timeline:** _____ weeks/months
- **Budget:** $_____ /month available
- **Approval Required From:** ___________
- **Evaluation Criteria:** (price, accuracy, latency, ease of integration, support)

### 6.3 Current Vendor Relationship

**Discovery Questions:**
- "How long have you been with your current ASR provider?"
- "Are you locked into a contract?"
- "What would it take to switch providers?"

**Switching Readiness:**
- [ ] Actively evaluating alternatives (HIGH INTENT)
- [ ] Open to testing if significant improvement (MEDIUM INTENT)
- [ ] Happy with current provider, not looking (LOW INTENT)
- [ ] Locked in contract until _____ (TIMELINE CONSTRAINT)

---

## Section 7: Pain Points & Buying Triggers

**Understand what would motivate them to switch to Blynt**

### 7.1 Current Pain Points (Rate 1-5)

**Discovery Question:** "What are your biggest challenges with your current ASR solution?"

| **Pain Point** | **Severity (1-5)** | **Notes** |
|----------------|-------------------|-----------|
| **Accuracy/WER** | | |
| **Latency** | | |
| **Cost** | | |
| **Multilingual support** | | |
| **Diarization quality** | | |
| **Integration complexity** | | |
| **Reliability/uptime** | | |
| **Customer support** | | |
| **Scalability** | | |
| **Customization limits** | | |

### 7.2 Impact of ASR Quality

**Discovery Questions:**
- "What happens when your ASR makes mistakes?"
- "How much does transcription quality impact your end product?"

**Business Impact:**
- [ ] **Critical:** Poor ASR = unusable product
- [ ] **High:** Significant customer complaints, churn risk
- [ ] **Medium:** Users notice, but tolerate
- [ ] **Low:** Nice-to-have improvement

**Quantifiable Impact (if possible):**
- **Revenue at risk:** $_____ /year
- **Customer churn rate due to quality:** _____ %
- **Support tickets related to ASR:** _____ /month

### 7.3 Buying Triggers

**Discovery Question:** "What would need to be true for you to switch ASR providers?"

- [ ] **X% accuracy improvement** (specify: _____%)
- [ ] **Y% cost reduction** (specify: _____%)
- [ ] **Latency under Z ms** (specify: _____ ms)
- [ ] **Better language support** (which languages: _______)
- [ ] **Fine-tuning capabilities**
- [ ] **Compliance certifications** (HIPAA, SOC 2, GDPR)
- [ ] **Other:** ___________

### 7.4 Timeline & Urgency

**Discovery Question:** "When do you need to solve this problem?"

- [ ] **Urgent:** Need solution in <30 days
- [ ] **Near-term:** 1-3 months
- [ ] **Medium-term:** 3-6 months
- [ ] **Long-term:** 6+ months
- [ ] **Not urgent:** Exploring options

**Urgency Drivers:**
- [ ] Product launch deadline
- [ ] Contract renewal with current provider
- [ ] Customer churn pressure
- [ ] Funding milestone
- [ ] Other: ___________

---

## Section 8: ICP Assignment (POST-CALL)

### Final ICP Determination

**Based on all answers above, assign ICP:**

□ **ICP 1:** White-Label Runtime
   - Recording audio but not transcribing yet (or want to add transcription)
   - Low technical maturity, need turnkey solution

□ **ICP 2:** Post-Call Intelligence / Note-Takers
   - Post-call processing with AI
   - Medium volume (<500K hrs/month)
   - Generic ASR works, need better quality

□ **ICP 3:** Real-Time Voice Agents
   - Real-time transcription during conversation
   - Latency critical (<500ms)
   - Need turn-taking, interruption handling

□ **ICP 4:** Audio ML Product Companies (Studio + Benchmarking)
   - Need custom models (jargon/acoustics/demographics)
   - High technical maturity
   - Any volume if customization critical

□ **ICP 2 (Established):** High-volume post-call intelligence (formerly ICP 5)
   - Post-call processing
   - Very high volume (>500K hrs/month)
   - Cost optimization primary driver

□ **ICP N/A:** Not a Fit
   - No audio use case / Not recording / Not transcribing / Wrong buyer / Too small

### Confidence Level

□ **HIGH** - Clear fit, all criteria met, no ambiguity
□ **MEDIUM** - Good fit, some uncertainties (specify: _______)
□ **LOW** - Unclear fit, need more information (specify: _______)

### Next Steps

**Immediate Actions:**
1. [ ] Update Notion with ICP assignment
2. [ ] Share discovery notes with team
3. [ ] Schedule technical deep-dive (if HIGH confidence)
4. [ ] Send follow-up resources tailored to ICP
5. [ ] Add to appropriate email sequence

**Follow-Up Questions (if MEDIUM/LOW confidence):**
- [List any clarifying questions needed to increase confidence]

---

## Quick Reference: Decision Tree Cheat Sheet

```
Q0: Business involves speech?
    NO → N/A
    YES ↓

Q1: Recording audio?
    NO → N/A
    YES ↓

Q2: Transcribing?
    NO → Want to add? YES → ICP 1 | NO → N/A
    YES ↓

Q3: Applying AI?
    NO → ICP 2 (basic transcription, any volume)
    YES ↓

Q4: Real-time or Post-call?
    REAL-TIME → ICP 3
    POST-CALL ↓

Q5: Custom model need?
    YES (jargon/acoustics/demographics) → ICP 4
    NO → ICP 2 (all volumes: Circleback to Gong)
```

---

## Appendix: Sample Discovery Call Script

### Opening (5 min)
"Thanks for taking the time! I'd love to learn about [Company] and how voice/audio fits into your product. First, can you give me a quick overview of what you're building?"

### Qualifying Questions (10 min)
- "Does your product involve recording or processing audio/voice?" *[Q0-Q1]*
- "Are you transcribing that audio to text?" *[Q2]*
- "What do you do with the transcripts - just display them, or run AI analysis?" *[Q3]*
- "Is transcription happening in real-time during conversations, or after the call?" *[Q4]*

### Deep Dive Based on ICP (15-20 min)
- **If ICP 1:** Focus on ease of integration, white-label capabilities, time-to-value
- **If ICP 2 (Early-stage):** Focus on accuracy improvements, multilingual, reasonable pricing
- **If ICP 2 (Scale-up):** Focus on quality + cost optimization as volume grows
- **If ICP 2 (Established):** Focus on cost reduction at scale, vendor diversification
- **If ICP 3:** Focus on latency, turn-taking, reliability, scale
- **If ICP 4:** Focus on fine-tuning, benchmarking, custom models, domain expertise

### Closing (5 min)
"Based on what you've shared, it sounds like you'd be a great fit for [Blynt solution]. The next step would be [demo/POC/technical call]. Does [timeframe] work for you?"

---

**End of Questionnaire**

*Save this completed questionnaire in Notion under the company record for future reference*
