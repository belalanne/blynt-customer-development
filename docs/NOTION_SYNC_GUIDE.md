# Notion Sync Guide

This guide explains how to sync the deep dive research data to your Notion database.

## Overview

After completing deep dive analyses on companies (LiveKit, 100ms, Daily), you can sync the structured data to your Notion database for easy tracking and management.

**Companies ready to sync:**
- ✅ LiveKit (livekit.io)
- ✅ 100ms (100ms.live)
- ✅ Daily (daily.co)

**Notion Database:** [2861bdff7e998000a14edb0bf56a75bf](https://notion.so/2861bdff7e998000a14edb0bf56a75bf)

---

## Method 1: Local Script (Recommended)

**Best for:** Running on your laptop with local .env file

### Prerequisites

```bash
pip install notion-client
```

### Setup

1. **Create config/.env file:**

```bash
# config/.env
NOTION_API_KEY=secret_your_notion_key_here
NOTION_DATABASE_ID=2861bdff7e998000a14edb0bf56a75bf
```

2. **Ensure integration has database access:**
   - Open your Notion database
   - Click "..." → "Add connections"
   - Select your integration

### Sync Single Company

```bash
python scripts/quick_sync_to_notion.py livekit.io
python scripts/quick_sync_to_notion.py 100ms.live
python scripts/quick_sync_to_notion.py daily.co
```

### Sync All Companies at Once

```bash
./scripts/sync_all_to_notion.sh
```

This will sync all three companies sequentially.

---

## Method 2: GitHub Actions (CI/CD)

**Best for:** Automated syncing via GitHub workflows

### Prerequisites

1. **NOTION_API_KEY must be added as GitHub Secret** (✅ Already done!)

2. **Workflow must be on main branch** (⚠️ Currently on Claude branch)

### How to Enable

#### Option A: Merge Claude Branch to Main

1. Go to GitHub repository
2. Create Pull Request from `claude/deep-dive-011CUsKDWjVFDEFTggnpgE4L` → `main`
3. Merge the PR
4. Workflow will appear in Actions tab

#### Option B: Temporarily Set Claude Branch as Default

1. Go to Settings → Branches
2. Change default branch to `claude/deep-dive-011CUsKDWjVFDEFTggnpgE4L`
3. Refresh Actions tab

### Run Workflow

Once visible in Actions tab:

1. Go to Actions → "Sync Research to Notion"
2. Click "Run workflow"
3. Enter company: `livekit.io`, `100ms.live`, or `daily.co`
4. Click "Run workflow"

---

## Data Being Synced

The following properties are synced to Notion:

| Property | Type | Description |
|----------|------|-------------|
| **Company_Name** | Title | Company name (e.g., "LiveKit") |
| **Website** | URL | Company website |
| **Linkedin Link** | URL | LinkedIn company page |
| **Status / Engagement** | Select | Set to "Ice Box" |
| **Vertical** | Select | Set to "Infrastructure" |
| **ICP** | Select | Ideal Customer Profile (set to "3") |
| **Product description** | Text | Short product summary |
| **ASR provider** | Multi-select | Speech-to-text providers used |
| **Nbr of AI/ML/Speech engineer** | Number | Estimated AI/ML team size |
| **Main Office Country** | Text | HQ location |

### Company Data Summary

#### LiveKit
- **Employees:** 37 total, ~18 AI/ML engineers
- **Funding:** $83M (Series B), $345M valuation
- **ASR Providers:** Deepgram, AssemblyAI, Speechmatics, Azure Speech, Google STT

#### 100ms
- **Employees:** 31 total, ~5 AI/ML engineers
- **Funding:** $24.5M (Series A)
- **ASR Providers:** None (no AI/speech partnerships)

#### Daily
- **Employees:** 116 total, ~22 AI/ML engineers
- **Funding:** $62.2M (Series B)
- **ASR Providers:** Deepgram, AssemblyAI, OpenAI Whisper, Google STT, Azure Speech

---

## Troubleshooting

### Error: NOTION_API_KEY not set

**Solution:** Create `config/.env` file with your API key, or export it:

```bash
export NOTION_API_KEY='secret_your_key_here'
```

### Error: Integration doesn't have access

**Solution:**
1. Open Notion database
2. Click "..." → "Add connections"
3. Select your integration (the one whose API key you're using)

### Error: Property type mismatch

**Solution:** Ensure your Notion database has these columns:
- Company_Name (Title)
- Website (URL)
- Linkedin Link (URL)
- Status / Engagement (Select)
- Vertical (Select)
- ICP (Select)
- Product description (Text)
- ASR provider (Multi-select)
- Nbr of AI/ML/Speech engineer (Number)
- Main Office Country (Text)

### GitHub Actions not visible

**Solution:** Workflows only appear on the default branch. Either:
1. Merge Claude branch to main (recommended)
2. Set Claude branch as default temporarily

---

## Quick Start (Fastest Path)

**On your laptop:**

```bash
# 1. Install dependency
pip install notion-client

# 2. Create API key config
echo "NOTION_API_KEY=secret_your_key_here" > config/.env

# 3. Sync all companies
./scripts/sync_all_to_notion.sh
```

Done! Check your Notion database: https://notion.so/2861bdff7e998000a14edb0bf56a75bf

---

## Security Notes

- ✅ `.env` files are gitignored (never committed)
- ✅ GitHub Secrets are encrypted (safe for CI/CD)
- ❌ Never commit API keys to the repository
- ✅ Local .env + .gitignore is the recommended pattern

---

## Related Files

- `scripts/quick_sync_to_notion.py` - Single company sync
- `scripts/sync_all_to_notion.sh` - Batch sync all companies
- `.github/workflows/sync-to-notion.yml` - GitHub Actions workflow
- `config/.env.example` - Template for API keys
- `logs/deep-dive-*.md` - Source research reports

---

## Need Help?

Check that:
1. ✅ `notion-client` is installed (`pip install notion-client`)
2. ✅ NOTION_API_KEY is set (in .env or environment)
3. ✅ Integration has access to the database
4. ✅ Database ID is correct: `2861bdff7e998000a14edb0bf56a75bf`
5. ✅ Database schema matches expected properties

For GitHub Actions issues:
- Verify NOTION_API_KEY is in Settings → Secrets
- Check workflow is on main/default branch
- Ensure workflow file is committed
