---
description: Map a company to Blynt's ICP (1, 2, or 3) based on their characteristics
argument-hint: <company_name or domain>
---

# ICP Mapping Task

Analyze the provided company and determine which of Blynt AI's 3 Ideal Customer Profiles (ICPs) they match best.

## Input
Company: {{arg}}

## ICP Definitions

### ICP #1: End-user with Speech-Intensive Workflow
**Keywords:** `#noSpeech` `#noAI`
**Value Prop:** Voice in your product with 3 lines of code. With capture.

**Characteristics:**
- B2B SaaS company with digital product used by professionals
- End-users spend 50%+ of their time in verbal interactions (client calls, site visits, consultations)
- Manual documentation is a major time sink (30-60 min per interaction)
- **Company Size:** 50-500 employees ("deer" not "rabbits" or "elephants")
- **Industry Verticals:** Travel Tech, Legal Tech, Real Estate Tech, Field Services Software, Healthcare Administration
- Product/Engineering team of 5-20 people
- Recently raised funding OR profitable with budget for AI features
- **Decision-maker:** Director of Product, UX
- **Key indicator:** They DON'T have speech AI yet, but their users have speech-intensive workflows

**Examples:** Worldia, Hosman, Passculture

---

### ICP #2: Vertical Meeting/Voice/Speech AI Product Companies
**Keywords:** `#VoiceAgents` `#AIEngineer`
**Value Prop:** The ML Ops platform to build your speech AI product. Speech AI made easy.

**Characteristics:**
- Building voice agents, meeting bots, or speech-first products (speech AI IS their product)
- Currently cobbling together Deepgram/Assembly + OpenAI + custom audio capture
- Struggling with production accuracy, evaluation, or domain adaptation
- Have shipped v1 but hitting quality/scale issues
- **Company Size:** 10-200 employees (startups to scale-ups)
- **Decision-maker:** Head of ML/AI, CTO
- **Key indicator:** They're BUILDING speech AI products and need infrastructure/evaluation

**Examples:** Sandra AI, Marshmallow, Doctolib (voice features), Sonos

**Sub-segments:**
- Getting product off the ground (need baseline performance)
- Scaling/optimizing (need benchmarking, cost reduction)

---

### ICP #3: Enterprise SaaS with Generalist Speech AI
**Keywords:** `#Recall.ai`
**Value Prop:** Platform for benchmarking and evaluation. Replace 3rd party dependencies with in-house solution.

**Characteristics:**
- Have ALREADY shipped basic speech features (transcription, voice commands)
- Using basic Deepgram/Assembly integration
- No systematic evaluation or optimization
- Engineering/ML team struggling to improve accuracy
- Facing user complaints about quality OR cost pressure
- **Company Size:** 200-5000 employees (larger "deer" to small "elephants")
- **Decision-maker:** VP Engineering, CTO
- **Key indicator:** Speech AI is a FEATURE in their product, already live, need to optimize/reduce costs

**Examples:** Modjo, Notion, Slack, Claap, Granola, Foundever, Aircall

---

## Your Task

1. **Research the company** (if domain provided, enrich it; if company name, search for info)
2. **Analyze against all 3 ICPs** using these criteria:
   - Company size
   - Industry/vertical
   - Current speech AI maturity (none / building / already shipped)
   - Product type (SaaS tool vs. speech AI product)
   - Decision-maker profile
   - Pain points

3. **Provide structured output:**

```
# ICP Mapping: [Company Name]

## Best Fit ICP: [1, 2, 3, or N/A]
**Confidence:** [High/Medium/Low]

## Analysis

### Company Profile
- **Industry:**
- **Size:**
- **Product Type:**
- **Current Speech AI Status:** [None / Building / Shipped]

### ICP Match Reasoning
[Explain why this company matches the selected ICP]

### Key Characteristics Matched
- [List 3-5 key characteristics from the ICP definition that match]

### Decision-Maker
**Likely buyer:** [role]

### Blynt Value Prop for This ICP
[The specific value prop for the matched ICP]

### Red Flags / Mismatches (if any)
[Note any characteristics that DON'T align with the ICP]

### Recommended Next Steps
- [e.g., "Reach out to Director of Product with ICP #1 pitch"]
- [e.g., "Validate if they've already built speech features"]

## Sources
[List URLs where you found this information]
```

4. **If uncertain between 2 ICPs**, explain both and ask for clarification

## Important Notes
- Use `/enrich-company` if you need more data about the company
- The Notion database property is called `ICP` with values: "1", "2", "3", "N/A"
- Be conservative - if a company doesn't clearly fit, mark as N/A and explain why
- Focus on CURRENT state, not potential future state
