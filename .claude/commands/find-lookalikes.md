---
description: Find lookalike companies similar to a target company based on industry, size, tech stack, and business model
arguments:
  - name: domain
    description: Company domain to find lookalikes for (e.g., otter.ai)
    required: true
  - name: count
    description: Number of lookalikes to find (default 10)
    required: false
---

Find companies similar to $ARGUMENTS:

## Step 1: Use Exa findSimilar (best for lookalikes)

```bash
curl -s -X POST "https://api.exa.ai/findSimilar" \
  -H "x-api-key: <EXA_API_KEY from .env>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://<domain>",
    "numResults": <count or 10>,
    "contents": {"text": {"maxCharacters": 500}}
  }'
```

## Step 2: Filter & Classify Results

For each result:
1. Check if they're in the voice/speech AI space
2. Determine ICP classification (1-4 or N/A)
3. Assess fit for Blynt's real-time transcription API

## Output Format

| Company | Domain | Description | ICP | Fit |
|---------|--------|-------------|-----|-----|
| Name    | url    | 5 words max | 1-4 | High/Med/Low |

## ICP Classification

- **ICP 1**: Speech/dictation products (medical, legal, note-taking)
- **ICP 2**: Meeting AI assistants (Otter, Fireflies, Gong)
- **ICP 3**: Voice agent platforms (Vapi, Bland, Retell)
- **ICP 4**: Custom voice solutions (enterprise)
- **N/A**: No voice/speech use case

## Post-Discovery

Ask if user wants to:
1. Research any specific company in detail (`/enrich <domain>`)
2. Sync results to Notion (`/sync-to-notion`)
3. Find more lookalikes from a specific result
4. Deep dive a high-potential company (`/deep-dive <domain>`)
