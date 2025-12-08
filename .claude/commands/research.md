---
description: Interactive company research with user choices at each step
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
  description: "Basic info only via n8n (30 seconds)"
- label: "Standard"
  description: "Profile + ICP classification (2-3 min)"
- label: "Deep dive"
  description: "Full analysis + tech stack + contacts (5-10 min)"
```

---

## Quick Lookup Flow

1. Call n8n webhook: `POST https://blynt.app.n8n.cloud/webhook/enrich-company`
2. If fails, use WebSearch as fallback
3. Display basic table:
   | Field | Value |
   |-------|-------|
   | Company | ... |
   | Country | ... |
   | Employees | ... |
   | Industry | ... |

4. **AskUserQuestion**:
   ```
   Question: "What's next?"
   Header: "Action"
   Options:
   - label: "Save to Notion"
   - label: "Upgrade to full research"
   - label: "Done"
   ```

---

## Standard Research Flow

1. n8n webhook OR WebSearch for company info
2. WebFetch company website for product description
3. Classify ICP (1-4 or N/A) using skill
4. Find LinkedIn URL
5. Display results table

6. **AskUserQuestion**:
   ```
   Question: "What would you like to do next?"
   Header: "Actions"
   multiSelect: true
   Options:
   - label: "Save to Notion"
     description: "Add to Companies database"
   - label: "Discover tech stack"
     description: "Find ASR/TTS/LLM providers"
   - label: "Find lookalikes"
     description: "Find 10 similar companies"
   - label: "Done"
   ```

---

## Deep Dive Flow

1. Full enrichment (n8n + WebSearch + WebFetch)
2. Tech stack discovery (privacy policy, job postings, docs)
3. Find key contacts (CEO, CTO, VP Engineering)
4. ICP classification with detailed reasoning
5. Display comprehensive report

6. **AskUserQuestion**:
   ```
   Question: "Select actions to perform:"
   Header: "Actions"
   multiSelect: true
   Options:
   - label: "Save to Notion"
     description: "Add company to database"
   - label: "Add contacts"
     description: "Save people to People database"
   - label: "Find lookalikes"
     description: "Discover 10 similar companies"
   - label: "Done"
   ```

---

## Data Schema

### Quick
- Company name, Website, Country, Employees, Industry

### Standard (adds)
- Product description (5 words)
- ICP (1-4 or N/A)
- LinkedIn URL
- Funding

### Deep Dive (adds)
- Tech stack: Transport, Framework, ASR, TTS, LLM
- Key contacts: Name, Role, LinkedIn
- Recent news
- Competitors

---

## Interactive Rules

Use **AskUserQuestion** when:
- Starting research (choose depth)
- After displaying results (choose next action)
- ICP is ambiguous (ask user to confirm)
- Multiple companies match (ask which one)
- Before ANY Notion save (confirm data is correct)
