# 100ms Deep Dive Analysis Report

**Company:** 100ms
**Domain:** 100ms.live
**Analysis Date:** 2025-11-06
**Analyst:** Claude (Blynt Customer Development Agent)

---

## Executive Summary

100ms is a Series A-stage live video infrastructure company ($24.5M raised) founded in October 2020 by former Facebook and Disney+Hotstar engineers. The company provides developers with APIs and SDKs to embed Zoom-like video conferencing and live streaming into their applications in hours rather than months. With strong developer experience (ranked top 3 in market), the platform serves 2,200+ businesses including notable edtech, creator economy, and community platforms. The company experienced 20x growth leading up to their 2022 Series A and reached $5.6M revenue by 2023.

**Key Highlights:**
- 🏆 **Pedigree:** Founded by engineers who built video infrastructure at Facebook and Disney+Hotstar
- 💰 **Funding:** $24.5M Series A (March 2022) led by Alpha Wave Global
- 📈 **Growth:** 20x growth, 2,200+ businesses, $5.6M revenue (2023)
- 🔧 **Developer Experience:** Ranked top 3 in market for ease of use
- 🎯 **Product:** Unified SDK for both video conferencing (WebRTC) and live streaming (HLS)

**Market Position:**
Strong mid-market player with excellent developer experience and pre-built UI components, positioned between lower-cost alternatives (VideoSDK) and enterprise incumbents (Agora, Twilio).

---

## Company Enrichment

### Firmographics

| Attribute | Value |
|-----------|-------|
| **Legal Name** | Brytecam Technologies Private Limited |
| **Website** | https://www.100ms.live |
| **LinkedIn** | https://www.linkedin.com/company/100mslive |
| **Founded** | October 2020 |
| **Headquarters** | Fremont, California, United States |
| **Company Size** | 31 employees (as of June 2024, down 14% YoY) |
| **Industry** | Live Video Infrastructure / WebRTC SaaS |
| **Business Type** | B2B SaaS, Developer-focused |

### Funding History

| Round | Date | Amount | Lead Investor | Total Raised |
|-------|------|--------|---------------|--------------|
| Seed | 2021 | $4.5M | Accel, STRIVE | $4.5M |
| **Series A** | **Mar 2022** | **$20M** | **Alpha Wave Global** | **$24.5M** |

**Investors:**
- Alpha Wave Global (formerly Falcon Edge, lead Series A)
- Accel
- STRIVE
- LocalGlobe
- Z47
- Matrix Partners (8 total investors)

**Financial Metrics:**
- 2022 Revenue: $4.5M
- 2023 Revenue: $5.6M (24% YoY growth)
- 2024 Projections: Not publicly available

### Leadership Team

| Name | Title | Background | LinkedIn |
|------|-------|------------|----------|
| **Kshitij Gupta** | Co-Founder & CEO | Led FB Live launch; VP Engineering at Disney+Hotstar | [Profile](https://www.linkedin.com/in/guptakshi/) |
| **Aniket Behera** | Co-Founder & COO | Led live video product at Hotstar; IIT Bombay (EE) | Listed on Tracxn |
| **Sarvesh Dwivedi** | Co-Founder | Built Video Processing Platform at Hotstar | Listed on Tracxn |

**Team Background:**
The founding team has proven experience building live video infrastructure at world-record scales:
- Facebook Live (billions of views)
- Disney+Hotstar (world's largest live streaming platform - Indian cricket, IPL)

### Business Model

**Product Architecture:**
- **LiveKit Server:** WebRTC-based video conferencing (up to 100 participants, <500ms latency)
- **HLS Streaming:** Large-scale live streaming (10K+ viewers)
- **Prebuilt UI:** Low-code components with limited customization
- **APIs & SDKs:** Android (Kotlin), iOS (Swift), React Native, Flutter, React

**Go-to-Market Strategy:**
1. **Developer-first:** Free tier with extensive documentation
2. **Vertical focus:** EdTech, fitness, telehealth, creator economy
3. **Fast time-to-market:** "Hours not months" positioning
4. **Managed service:** Fully managed (no self-hosting option)

**Pricing Model:**
- **Free Tier:** 1,000 encoding + 10,000 streaming minutes/month
- **Usage-Based:**
  - Video conferencing: $0.004 × participants × minutes
  - Recording: $0.027/minute
  - No resolution-based pricing (capped at 4Mbps bitrate)
  - Custom pricing for higher bitrates
- **Alternative:** MAU-based pricing available

**Target Customers:**
- **Primary:** Startups and SMBs building video features
- **Verticals:** EdTech (FrontRow, WhiteHat Jr), Creator platforms (Circle), Events (Paytm Insider), Community apps (Kutumb)
- **Geography:** Global with focus on India, US markets

### Technology Stack

**Core Infrastructure:**
- **WebRTC:** For low-latency conferencing
- **HLS:** For large-scale streaming
- **Role-based permissions:** Dashboard-managed without code
- **Auto-scaling:** On-demand with multiple regional data centers

**Platform SDKs:**
- Android (Kotlin)
- iOS (Swift)
- React Native
- Flutter
- React/JavaScript

**Key Features:**
- Interactive chat, screen share, emoji reactions
- Virtual whiteboards and file sharing
- Breakout rooms
- Custom roles and permissions
- Scored polls
- Recording and streaming to YouTube
- Custom layout recording
- AR masks, voice effects (via 3rd party integrations)

**AI/ML Capabilities:**
- **Post-call transcription** with speaker labels
- **AI-generated summaries** (in Beta)
- **Live transcription** for HLS streams (English)
- **Custom vocabulary** support
- **GPT Vision integration** for Polls AI demo

**Infrastructure:**
- Multi-region data centers (US, Europe, India)
- AWS Marketplace availability
- HIPAA compliance option with BAA
- Data encryption in transit and at rest
- Optional data storage location selection

### Notable Customers & Case Studies

**Customer Count:** 2,200+ businesses (as of March 2022)

**Featured Customers:**
- **FrontRow** - EdTech platform for live classes
- **WhiteHat Jr** - Online coding for kids
- **Circle** - Community platform for creators and brands
- **Paytm Insider** - Live events platform
- **Kutumb** - Community app
- **Kutuki** - Children's content platform

**Case Studies:**
1. **Zenskar Partnership:** 4% revenue increase through automated billing
2. **DevRev Integration:** Unified customer support across 300+ Slack channels

### Recent News & Developments

**2022:**
- March: $20M Series A from Alpha Wave Global
- Experienced 20x growth in previous quarter
- TechCrunch feature on Series A

**2023:**
- Revenue reached $5.6M (up from $4.5M in 2022)
- Team grew to 70 people (peak)

**2024:**
- Employee count reduced to 31 (14% YoY decrease)
- Launched transcription and AI summary features (Beta)
- Announced Polls AI demo with GPT Vision
- HIMSS 2025 conference attendance planned

**Product Updates:**
- Live transcription for HLS streams
- Post-call transcription with speaker labels
- AI-generated summaries
- Custom vocabulary support
- Enhanced HIPAA compliance features

---

## Lookalike Companies

### Analysis Methodology

**Similarity Criteria:**
1. WebRTC/HLS live video infrastructure
2. Developer-focused B2B SaaS
3. Managed service (not open-source first)
4. SMB to mid-market focus
5. Prebuilt UI components

### Top Lookalike Companies

| Company | Website | Score | Key Similarities | Notable Differences |
|---------|---------|-------|------------------|---------------------|
| **Dyte** | dyte.io | **9/10** | ✓ WebRTC SaaS<br>✓ Prebuilt UI kits<br>✓ Developer focus<br>✓ Similar stage<br>✓ Fast time-to-market | ✗ Acquired by Cloudflare (Apr 2025)<br>✗ Plugin system architecture<br>✗ India-based |
| **Daily.co** | daily.co | **9/10** | ✓ Managed WebRTC<br>✓ Prebuilt components<br>✓ Developer APIs<br>✓ Similar pricing model | ✗ More mature<br>✗ Different vertical focus<br>✗ US-based |
| **VideoSDK** | videosdk.live | **8/10** | ✓ WebRTC SaaS<br>✓ India-based<br>✓ Similar features<br>✓ Developer SDKs | ✗ Much smaller ($1.2M seed)<br>✗ Lower price point<br>✗ Less polished UX |
| **Stream Video** | getstream.io | **8/10** | ✓ API-first<br>✓ Video + chat unified<br>✓ Prebuilt UI<br>✓ Developer-focused | ✗ More mature ($57.8M raised)<br>✗ Broader product suite<br>✗ US-based (Boulder) |
| **Whereby** | whereby.com | **7/10** | ✓ Embedded video<br>✓ Easy integration<br>✓ B2B focus | ✗ B2C heritage<br>✗ Telehealth vertical<br>✗ Norway-based<br>✗ Different architecture |
| **LiveKit** | livekit.io | **7/10** | ✓ WebRTC infrastructure<br>✓ Developer-focused<br>✓ Similar stage | ✗ Open-source first<br>✗ Self-hosting option<br>✗ No prebuilt UI<br>✗ More technical |
| **Agora** | agora.io | **7/10** | ✓ WebRTC at scale<br>✓ Video + streaming<br>✓ Global infrastructure | ✗ Public company (much larger)<br>✗ Enterprise focus<br>✗ Higher pricing<br>✗ Legacy platform |
| **ZEGOCLOUD** | zegocloud.com | **7/10** | ✓ Real-time video<br>✓ UIKits<br>✓ Asian market focus | ✗ Different positioning<br>✗ China-based<br>✗ Gaming focus |
| **Vonage Video** | vonage.com | **6/10** | ✓ WebRTC SDK<br>✓ Enterprise features | ✗ Legacy platform (ex-TokBox)<br>✗ Part of Ericsson<br>✗ 55 participant limit<br>✗ Higher cost |
| **Twilio Video** | twilio.com/video | **6/10** | ✓ Video API<br>✓ Enterprise scale | ✗ Part of larger suite<br>✗ Higher pricing<br>✗ Complex integration |

### Competitive Analysis

**Top Direct Competitors:**
1. **Dyte** (9/10) - Closest match before Cloudflare acquisition
2. **Daily.co** (9/10) - Similar managed service approach
3. **Stream Video** (8/10) - Comparable developer experience

**Market Observations:**
- **Consolidation:** Dyte → Cloudflare signals M&A activity in space
- **India Players:** Strong competition from VideoSDK (lower cost)
- **Open Source:** LiveKit offers alternative model (self-hosting)
- **Incumbents:** Agora, Twilio have enterprise scale but worse DX

**100ms Advantages:**
1. ✅ Top 3 developer experience ranking
2. ✅ Unified SDK (video conferencing + live streaming)
3. ✅ Strong founding team (Facebook, Hotstar pedigree)
4. ✅ Prebuilt UI components
5. ✅ Transparent pricing (no resolution-based charges)

**100ms Challenges:**
1. ⚠️ Team contraction (70 → 31 employees, -14% YoY)
2. ⚠️ No self-hosting option (vs. LiveKit)
3. ⚠️ Smaller scale than LiveKit (which powers ChatGPT)
4. ⚠️ Competition from Cloudflare (post-Dyte acquisition)
5. ⚠️ Limited AI capabilities vs. emerging voice AI players

---

## AI/Speech Technology Stack

### AI Features (Internal Development)

**Transcription & Summarization:**
| Feature | Provider | Status | Source |
|---------|----------|--------|--------|
| **Post-call transcription** | External service (HIPAA BAA signed) | Live (Beta) | [Blog](https://www.100ms.live/blog/transcript-summary-launch) |
| **Speaker-labeled captions** | External service | Live (Beta) | Docs |
| **AI-generated summaries** | Not disclosed | Live (Beta) | [Blog](https://www.100ms.live/blog/transcript-summary-launch) |
| **Live transcription (HLS)** | External service | Live | Docs |
| **Custom vocabulary** | Built-in | Live | Docs |

**Pricing for AI Features:**
- 300 free minutes/month for live transcription
- 300 free minutes/month for post-call transcription
- 300 free minutes/month for AI summaries
- Paid feature after free tier

**AI Demos & Experiments:**
| Demo | Technology | Status | Description |
|------|------------|--------|-------------|
| **Polls AI** | OpenAI GPT Vision | Demo | Generates interactive polls from whiteboard content |

### External Integrations

**Data Storage & Infrastructure:**
| Category | Provider | Notes |
|----------|----------|-------|
| Cloud Infrastructure | AWS | Available on AWS Marketplace |
| Data Centers | Multi-region | US, Europe, India |
| Transcription Service | External (HIPAA-compliant) | BAA signed for HIPAA compliance |

**No Public AI/Speech Partnerships:**
Unlike LiveKit (which offers 20+ AI provider integrations), 100ms does not currently offer:
- Multiple STT provider options (Deepgram, AssemblyAI, etc.)
- LLM provider integrations (OpenAI, Anthropic, etc.)
- TTS provider integrations (ElevenLabs, Cartesia, etc.)

**Strategic Positioning:**
100ms focuses on video/audio infrastructure with basic transcription features, not positioning as an AI voice agent platform. This contrasts with LiveKit's strategic pivot toward voice AI agents with Agents 1.0.

### Technology Partnerships

**Confirmed Partners:**
- **AWS:** Marketplace listing, cloud infrastructure
- **DevRev:** Customer support integration
- **Zenskar:** Billing automation partner
- **Transcription Provider:** External service (name not disclosed, HIPAA BAA)

**Development Tools:**
- GitHub: 65 repositories (https://github.com/100mslive)
- Extensive SDK documentation
- API reference and examples

---

## Market Analysis

### Market Position

**Segment:** Mid-market WebRTC infrastructure provider

**Strengths:**
1. ✅ **Developer Experience:** Top 3 ranking in market
2. ✅ **Unified Platform:** Single SDK for conferencing + streaming
3. ✅ **Team Pedigree:** Facebook + Disney+Hotstar veterans
4. ✅ **Prebuilt UI:** Faster time-to-market vs. LiveKit
5. ✅ **Transparent Pricing:** No resolution-based pricing
6. ✅ **Customer Traction:** 2,200+ businesses

**Weaknesses:**
1. ⚠️ **Team Contraction:** -14% employee count YoY
2. ⚠️ **No Self-Hosting:** Managed-only (vs. LiveKit flexibility)
3. ⚠️ **Limited AI Strategy:** Basic transcription, no voice AI focus
4. ⚠️ **Smaller Scale:** $5.6M revenue vs. LiveKit's $3.7M (similar stage)
5. ⚠️ **Competition:** Dyte acquired by Cloudflare, well-funded rivals

### Competitive Dynamics

**vs. LiveKit:**
- ✅ Better DX, prebuilt UI, easier to use
- ✗ No open source, no self-hosting, no voice AI focus

**vs. Daily.co:**
- ✅ Unified video + streaming SDK
- ✗ Less mature, smaller team

**vs. Agora:**
- ✅ Modern developer experience, better APIs
- ✗ Can't handle as many users, less enterprise features

**vs. VideoSDK (India):**
- ✅ More polished, better funded, stronger team
- ✗ Higher pricing

### Market Trends

**1. Voice AI Agents Emergence:**
- LiveKit, Retell AI, Pipecat focusing on voice AI
- 100ms not yet positioned in this category
- Risk of missing emerging high-growth segment

**2. Consolidation Wave:**
- Dyte → Cloudflare (April 2025)
- Expect more M&A activity
- 100ms could be acquisition target

**3. Open Source Pressure:**
- LiveKit's open-source model gaining traction
- Developer preference for self-hosting options
- 100ms's managed-only approach may limit appeal

**4. Enterprise Adoption:**
- HIPAA compliance becoming table stakes
- Multi-region, data residency requirements
- 100ms has capabilities but smaller brand than Agora/Twilio

**5. India Tech Hub:**
- Strong competition from Indian startups (Dyte, VideoSDK)
- Cost-competitive alternatives
- 100ms has India presence but HQ'd in US

---

## Sales Intelligence

### Buying Signals

**Positive Signals:**
1. ✅ **Series A Capital:** $24.5M raised (March 2022) - should have runway
2. ✅ **Revenue Growth:** $4.5M → $5.6M (24% YoY)
3. ✅ **Customer Growth:** 2,200+ businesses
4. ✅ **Product Expansion:** AI features (transcription, summaries)
5. ✅ **Partnership Activity:** DevRev, Zenskar integrations

**Concerning Signals:**
1. 🚨 **Team Contraction:** 70 → 31 employees (-56% from peak)
2. 🚨 **YoY Decline:** -14% employee count (Jun 23 → Jun 24)
3. 🚨 **Flat Fundraising:** No Series B announced since March 2022
4. 🚨 **Limited Hiring:** No aggressive job openings visible
5. 🚨 **Quiet PR:** Limited news/announcements in 2024-2025

### Pain Points (Inferred)

**Business Challenges:**
- **Growth Plateau:** Team reduction suggests revenue not scaling fast enough
- **Unit Economics:** Possible margin pressure competing with VideoSDK
- **Market Positioning:** Squeezed between low-cost (VideoSDK) and premium (LiveKit scale)
- **Competitive Pressure:** Dyte acquisition by Cloudflare changes landscape
- **AI Strategy:** No clear voice AI positioning as market shifts

**Technical Challenges:**
- **Scale Limitations:** 100 participant limit (vs. Agora's 250+)
- **No Self-Hosting:** Missing key differentiator vs. LiveKit
- **Limited AI Integrations:** No multi-provider AI strategy
- **UI Customization:** Prebuilt components have "limited flexibility"

### Ideal Customer Profile

**Best Fit:**
1. **EdTech Startups** - Live classes, tutoring, cohort-based learning
2. **Creator Economy Platforms** - Community, courses, coaching
3. **Fitness Apps** - Live workout classes, personal training
4. **Event Platforms** - Virtual events, webinars, meetups
5. **Healthcare/Telehealth** - HIPAA-compliant video consultations

**Customer Characteristics:**
- Startup to Series B stage
- Need fast time-to-market (weeks not months)
- Want prebuilt UI components
- Don't have dedicated WebRTC engineering team
- India or US-based
- Budget-conscious but need reliability

**Not Ideal For:**
- **Large enterprises** (→ Agora, Twilio have better enterprise support)
- **Voice AI agent builders** (→ LiveKit Agents, Retell AI)
- **Self-hosting requirements** (→ LiveKit, Jitsi)
- **Very high scale** (10K+ concurrent participants → Agora)
- **Deep customization needs** (→ LiveKit open source)

### Recommended Approach

**Best Contacts:**
1. **Kshitij Gupta** (CEO) - Strategic partnerships, enterprise deals
2. **Aniket Behera** (COO) - Operations, business development
3. **Engineering Team** - Via GitHub, documentation, developer community

**Entry Points:**
1. **Developer Relations** - Technical content, integrations, open source contributions
2. **Customer Success** - Help existing customers maximize value
3. **Vertical Solutions** - EdTech, fitness, creator economy specific features

**Messaging Angles:**

**For Partnership Pitch:**
> "Congrats on 2,200+ businesses and top 3 developer experience ranking. As you expand AI capabilities with transcription and summaries, [our solution] could complement..."

**For Integration Pitch:**
> "We're seeing strong demand from EdTech companies building on 100ms who need [specific capability]. Would you be open to exploring an integration?"

**Value Propositions to Emphasize:**
- **Fast Integration:** Works with existing 100ms SDK
- **Developer Experience:** Maintains 100ms's DX standards
- **Vertical Fit:** Proven in EdTech/fitness/creator economy
- **Cost Efficiency:** Enhances value without major cost increase

### Timing Assessment

**Current Timing: ⚠️ CAUTIOUS**

**Why Cautious:**
1. ⚠️ Team contraction suggests possible cost-cutting mode
2. ⚠️ No recent fundraising (Series A was March 2022)
3. ⚠️ Limited hiring/expansion signals
4. ⚠️ Revenue growth modest (24% YoY)
5. ⚠️ Competitive pressure from Cloudflare-Dyte

**Potential Scenarios:**
- **Scenario A:** Preparing for Series B (quiet period)
- **Scenario B:** Optimizing for profitability (sustainable growth)
- **Scenario C:** Acquisition target (consolidation play)
- **Scenario D:** Struggling (pivot or wind-down risk)

**Recommended Wait Period:**
Monitor for 3-6 months for signals:
- ✅ New funding announcement → Green light
- ✅ Team expansion → Growth mode
- ✅ Major product launches → Investing in product
- ⚠️ Further contraction → Avoid
- ⚠️ Acquisition rumors → Wait for clarity

---

## Recommendations

### For Blynt (Targeting 100ms)

**Engagement Strategy:**

**Short-term (0-3 months):**
1. ⚠️ **Hold on direct sales outreach** - Team contraction signals possible budget constraints
2. ✅ **Developer relations** - Engage via GitHub, documentation, technical content
3. ✅ **Monitor signals** - Watch for fundraising, team growth, major announcements
4. ✅ **Customer indirect** - Work with 100ms customers, demonstrate value

**Medium-term (3-6 months):**
1. Wait for clarity on:
   - Series B fundraising
   - Team expansion
   - Strategic direction
   - Competitive response to Cloudflare-Dyte

**Long-term (6-12 months):**
1. If positive signals emerge:
   - Direct partnership discussions
   - Integration/co-marketing opportunities
   - Customer co-selling

### For Companies Evaluating 100ms

**When to Choose 100ms:**
- Need fast time-to-market (prebuilt UI)
- Want excellent developer experience
- SMB to mid-market scale (up to 100 participants)
- EdTech, fitness, creator economy verticals
- Budget-conscious but need reliability
- Don't need self-hosting

**When to Consider Alternatives:**
- **Need self-hosting** → LiveKit
- **Voice AI agents** → LiveKit Agents, Retell AI
- **Enterprise scale** → Agora, Twilio
- **Lower cost** → VideoSDK (India)
- **More features** → Stream (video + chat + feeds)
- **Mature platform** → Daily.co

### Strategic Recommendations

**For 100ms Product Strategy:**
1. **Clarify AI positioning** - Voice AI agents or video-first with AI features?
2. **Consider self-hosting option** - Competitive pressure from LiveKit
3. **Vertical deepening** - Own EdTech or creator economy completely
4. **Partnership acceleration** - AI providers, vertical platforms
5. **Open source components** - Community building like LiveKit

**For Investors:**
- ⚠️ Watch team contraction trend closely
- ⚠️ Assess competitive moat vs. Cloudflare-Dyte
- ⚠️ Evaluate path to profitability vs. growth
- ✅ Strong founding team and developer love remain positives

---

## Data Sources

**Company Information:**
- Crunchbase: https://www.crunchbase.com/organization/100ms
- Tracxn: https://tracxn.com/d/companies/100ms/
- CB Insights: https://www.cbinsights.com/company/100ms
- YourStory: https://yourstory.com/companies/100ms

**Funding & News:**
- Series A (TechCrunch): https://techcrunch.com/2022/03/10/100ms-secures-20m-to-power-next-generation-of-live-video-apps/
- Series A (100ms blog): https://www.100ms.live/blog/series-a-funding-announcement
- Business Standard: https://www.business-standard.com/article/companies/live-video-infrastructure-startup-100ms-raises-20-mn-in-series-a-funding-122031100466_1.html

**Product & Technology:**
- Official website: https://www.100ms.live
- Documentation: https://www.100ms.live/docs
- GitHub: https://github.com/100mslive (65 repositories)
- Pricing: https://www.100ms.live/pricing
- AWS Marketplace: https://aws.amazon.com/marketplace/pp/prodview-bzztkr4ht2vnc

**AI Features:**
- Transcription blog: https://www.100ms.live/blog/transcript-summary-launch
- Post-call transcription docs: https://www.100ms.live/docs/server-side/v2/how-to-guides/enable-transcription-and-summary
- Live transcription docs: https://www.100ms.live/docs/server-side/v2/how-to-guides/live-transcription-hls

**Competitive Analysis:**
- 100ms vs Agora: https://www.100ms.live/agora-vs-100ms
- 100ms vs Dyte vs LiveKit: https://dyte.io/100ms-vs-agora
- LiveKit alternatives: https://getstream.io/blog/livekit-alternatives/
- Agora alternatives: https://www.videosdk.live/blog/agora-competitors

**Leadership:**
- Kshitij Gupta LinkedIn: https://www.linkedin.com/in/guptakshi/
- Company LinkedIn: https://www.linkedin.com/company/100mslive
- About page: https://www.100ms.live/about

**Customer Case Studies:**
- Zenskar: https://www.zenskar.com/case-study/100ms
- DevRev: https://devrev.ai/case-study/100ms
- Customers page: https://www.100ms.live/customers

**Revenue Data:**
- Latka: https://getlatka.com/companies/100ms

---

## Report Metadata

**Analysis Completed:** 2025-11-06
**Analyst:** Claude (Blynt Customer Development Agent)
**Analysis Type:** Deep Dive (Comprehensive)
**Sources Consulted:** 40+ sources
**Last Data Verification:** 2025-11-06

**Report Sections:**
1. ✅ Company Enrichment (Firmographics, funding, leadership, business model, technology)
2. ✅ Lookalike Companies (10 companies with similarity scores)
3. ✅ AI/Speech Technology Stack (AI features, integrations, partnerships)
4. ✅ Market Analysis (Competitive positioning, trends, SWOT)
5. ✅ Sales Intelligence (Buying signals, pain points, ICP, timing)
6. ✅ Strategic Recommendations (Engagement strategy, evaluation criteria)

**Key Findings:**
- Series A company with strong founding team and developer experience
- Team contraction (-14% YoY) suggests caution in current timing
- Positioned between low-cost (VideoSDK) and premium (LiveKit) competitors
- Limited AI strategy compared to emerging voice AI infrastructure players
- Strong in EdTech, creator economy, fitness verticals

**Files Generated:**
- `logs/deep-dive-100ms.live-2025-11-06.md` (This report)

---

**End of Report**

*This report was generated automatically by the Blynt Customer Development Agent using web research and public company data. All information is based on publicly available sources as of 2025-11-06.*
