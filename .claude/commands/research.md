---
description: Interactive company research with lead scoring and outreach
arguments:
  - name: domain
    description: Company domain to research (e.g., vapi.ai)
    required: true
---

# Interactive Research: $ARGUMENTS

## Step 1: Choose Research Depth

**IMPORTANT**: Use **AskUserQuestion** FIRST before any research:

```
Question: "What type of research do you need for $ARGUMENTS?"
Header: "Depth"
Options:
- label: "Quick lookup"
  description: "Basic info + lead score (30 seconds)"
- label: "Standard"
  description: "Profile + ICP + contacts (2-3 min)"
- label: "Deep dive"
  description: "Full analysis + tech stack + outreach (5-10 min)"
```

---

## Quick Lookup Flow

1. WebSearch for company info + recent news
2. Calculate lead score
3. Display results:

```
## $COMPANY - Quick Lookup

| Field | Value |
|-------|-------|
| Company | ... |
| Website | ... |
| Country | ... |
| Industry | ... |
| Employees | ... |

### Sales Intelligence
| Metric | Value |
|--------|-------|
| **Lead Score** | 75/100 |
| **Priority** | 🔥 Hot / ⚡ Warm / ❄️ Cold |
| **ICP** | 1/2/3/4/N/A |
| **Trigger** | "Just raised $70M" or "Hiring voice engineers" |
```

4. **AskUserQuestion**:
   ```
   Question: "What's next?"
   Header: "Action"
   Options:
   - label: "Save to Notion"
     description: "Add to CRM pipeline"
   - label: "Upgrade to full research"
   - label: "Done"
   ```

---

## Standard Research Flow

1. WebSearch + WebFetch company website
2. Find key contact (CEO/CTO/VP Eng) with email
3. Classify ICP with reasoning
4. Calculate lead score
5. Identify trigger events (funding, hiring, launches)
6. Display results:

```
## $COMPANY - Research Summary

### Company Profile
| Field | Value |
|-------|-------|
| Company | ... |
| Website | ... |
| LinkedIn | ... |
| Country | ... |
| Employees | ... |
| Funding | ... |
| Product | (5 words) |

### Sales Intelligence
| Metric | Value |
|--------|-------|
| **Lead Score** | 85/100 |
| **Priority** | 🔥 Hot |
| **ICP** | 3 - Voice Agents |
| **Trigger** | "Raised $10M Series A last month" |
| **Timing** | Good - actively building |

### Key Contact
| Field | Value |
|-------|-------|
| Name | John Smith |
| Role | CTO |
| Email | john@company.com |
| LinkedIn | linkedin.com/in/johnsmith |
```

7. **AskUserQuestion**:
   ```
   Question: "What would you like to do?"
   Header: "Actions"
   multiSelect: true
   Options:
   - label: "Save to Notion"
     description: "Add company + contact to CRM"
   - label: "Generate outreach email"
     description: "Draft personalized cold email"
   - label: "Find lookalikes"
     description: "Find 10 similar companies"
   - label: "Done"
   ```

---

## Deep Dive Flow

1. Full enrichment (WebSearch + WebFetch multiple pages)
2. Tech stack discovery (privacy policy, job postings, GitHub)
3. Find 2-3 key contacts with emails
4. Research trigger events and timing signals
5. Calculate detailed lead score
6. Display comprehensive report:

```
## $COMPANY - Deep Dive

### Company Profile
(same as Standard)

### Sales Intelligence
| Metric | Value |
|--------|-------|
| **Lead Score** | 92/100 |
| **Priority** | 🔥 Hot |
| **ICP** | 3 - Voice Agents |
| **Blynt Fit** | High - needs real-time STT |

### Trigger Events
- 🚀 Raised $10M Series A (2 weeks ago)
- 👥 Hiring "Voice AI Engineer" (3 open roles)
- 📢 Launched new voice product (last month)

### Tech Stack
| Layer | Current Provider |
|-------|------------------|
| ASR | Deepgram |
| TTS | ElevenLabs |
| LLM | OpenAI |
| Framework | Custom WebSocket |

### Key Contacts
| Name | Role | Email | LinkedIn |
|------|------|-------|----------|
| Jane Doe | CEO | jane@co.com | /in/jane |
| John Smith | CTO | john@co.com | /in/john |

### Why Blynt?
- Current stack lacks turn-taking
- Job postings mention "latency issues"
- Could benefit from keyword boosting
```

7. **AskUserQuestion**:
   ```
   Question: "Select actions:"
   Header: "Actions"
   multiSelect: true
   Options:
   - label: "Save to Notion"
     description: "Add company + contacts to CRM"
   - label: "Generate outreach email"
     description: "Draft personalized cold email to key contact"
   - label: "Find lookalikes"
   - label: "Done"
   ```

---

## Lead Score Calculation

Score 0-100 based on:

| Factor | Points | Criteria |
|--------|--------|----------|
| ICP Fit | 0-30 | ICP 3 = 30, ICP 2 = 25, ICP 1 = 20, ICP 4 = 15, N/A = 0 |
| Company Size | 0-15 | 10-50 = 15, 50-200 = 12, 200-1000 = 10, <10 or >1000 = 5 |
| Funding | 0-15 | Recent funding = 15, Series A-C = 12, Seed = 10, None = 5 |
| Trigger Events | 0-20 | Recent funding = 10, Hiring = 5, Product launch = 5 |
| Tech Stack Match | 0-20 | Uses competitor ASR = 20, Building voice = 15, No voice = 0 |

**Priority Thresholds:**
- 🔥 Hot: 75-100
- ⚡ Warm: 50-74
- ❄️ Cold: 0-49

---

## Notion CRM Integration

### Step 1: Check for Duplicates FIRST

**IMPORTANT**: Before creating a new page, ALWAYS check if company exists:

```bash
# Query Notion by Website URL
curl -s -X POST "https://api.notion.com/v1/databases/{DATABASE_ID}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "property": "Website",
      "url": {"contains": "<domain>"}
    }
  }'
```

**If company exists:**
- Show: "⚠️ Company already in Notion: [Name](link)"
- Show existing data: Status, ICP, Contacts, Last Interaction
- Ask: "Update existing page?" (Yes/No)
- If Yes → PATCH existing page
- If No → Skip save

**If company is new:**
- Create new page with POST

### Step 2: Set Fields

#### Companies Database
- `Status / Engagement`: "To Contact" (for new leads)
- `ICP`: From classification
- `Lead Score`: Calculated score (if field exists)
- All other standard fields

#### People Database
- `Contact_Name`: Key contact name
- `Role`: Their title
- `Email`: Found email
- `LinkedIn URL`: Profile link
- `Company name`: Relation to company

---

## Outreach Email Generation

When "Generate outreach email" is selected:

1. Use the research data to create personalized email
2. Reference specific trigger events
3. Connect Blynt's value prop to their use case
4. Keep it short (3-4 sentences max)

**Template structure:**
```
Subject: [Trigger-based hook]

Hi [First Name],

[1 sentence about trigger event / what caught attention]

[1-2 sentences connecting their use case to Blynt's value]

[Soft CTA - question or offer to chat]

Best,
[Sender]
```

**Example:**
```
Subject: Congrats on the Series A - question about your voice stack

Hi Jane,

Saw Acme just raised $10M to scale your voice agent platform - congrats!

We're helping companies like yours cut STT latency by 40% with built-in turn-taking.
Curious if latency is on your radar as you scale?

Worth a quick chat?

Best,
Ben
```

---

## Interactive Rules

Use **AskUserQuestion** when:
- Starting research (choose depth)
- After displaying results (choose next action)
- ICP is ambiguous (ask user to confirm)
- Before Notion save (confirm status: "To Contact" / "Researching" / "Not a Fit")
- After generating email (ask to copy or revise)
