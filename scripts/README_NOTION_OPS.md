# Notion Contact Operations - Lightweight Script

## Purpose
This script provides **token-optimized** Notion operations for the `/add-contact` workflow. It reduces token usage by ~20-30k tokens per operation by:

- Using direct database queries instead of semantic search
- Returning minimal JSON responses
- Avoiding verbose MCP tool results

## Token Savings Comparison

| Operation | MCP Tools | This Script | Savings |
|-----------|-----------|-------------|---------|
| Check duplicate | 15k tokens | 2k tokens | 87% |
| Get company | 12k tokens | 2k tokens | 83% |
| Add contact | 10k tokens | 3k tokens | 70% |
| **Total /add-contact** | **37k tokens** | **~7k tokens** | **81%** |
| | | | |
| Create/update company | 15k tokens | 2k tokens | 87% |
| **Total /sync-to-notion** | **~20k tokens** | **~3k tokens** | **85%** |
| | | | |
| Search contacts | 12k tokens | 2k tokens | 83% |
| Update contact email | 10k tokens | 3k tokens | 70% |
| **Total /find-email** | **~22k tokens** | **~5k tokens** | **77%** |
| | | | |
| Get company + Update ICP | 15k tokens | 3k tokens | 80% |
| **Total /map-icp** | **~15k tokens** | **~3k tokens** | **80%** |
| | | | |
| **Batch: 10 companies** | **150k tokens** | **~5k tokens** | **97%** |
| **Total /batch-process (10)** | **~150k tokens** | **~5k tokens** | **97%** |

## Setup

### 1. Install Dependencies
```bash
# Activate virtual environment
source .venv/bin/activate

# Install notion-client (specific version)
pip install notion-client==2.2.1
```

### 2. Configure API Key
```bash
# Add to config/.env
NOTION_API_KEY=secret_your_integration_key_here
```

### 3. Share Databases with Integration
In Notion:
1. Open the **People** database
2. Click `...` → **Add connections** → Select your integration
3. Repeat for **Companies** database

## Usage

### Contact Operations

#### Check for Duplicate Contact
```bash
python scripts/notion_contact_ops.py check-duplicate \
  --linkedin "https://www.linkedin.com/in/m-ullah/"

# Output:
{
  "exists": true,
  "page_id": "2bc1bdff-7e99-81e4-a9b9-f42fb9234628",
  "name": "Michaël Ullah",
  "url": "https://notion.so/2bc1bdff7e9981e4a9b9f42fb9234628"
}
```

#### Add New Contact
```bash
python scripts/notion_contact_ops.py add-contact \
  --name "Michaël Ullah" \
  --role "Chief Technology Officer" \
  --company-id "https://notion.so/2ae1bdff7e998108b43ae2bef1c335a6" \
  --linkedin "https://www.linkedin.com/in/m-ullah/" \
  --email "michael.ullah@rcpt.ai" \
  --campaign "ICP #3"

# Output:
{
  "success": true,
  "page_id": "2bc1bdff-7e99-81e4-a9b9-f42fb9234628",
  "url": "https://notion.so/2bc1bdff7e9981e4a9b9f42fb9234628",
  "name": "Michaël Ullah",
  "role": "Chief Technology Officer"
}
```

#### Search Contacts by Name
```bash
python scripts/notion_contact_ops.py search-contacts \
  --name "Paul Berloty"

# Output:
{
  "found": true,
  "count": 1,
  "contacts": [
    {
      "page_id": "xxx-xxx-xxx",
      "name": "Paul Berloty",
      "email": "paul@modjo.ai",
      "role": "CEO",
      "url": "https://notion.so/xxxxx"
    }
  ]
}
```

#### Get Contacts Without Email
```bash
python scripts/notion_contact_ops.py get-contacts-without-email --limit 50

# Output:
{
  "count": 12,
  "contacts": [
    {
      "page_id": "xxx-xxx-xxx",
      "name": "John Doe",
      "role": "CTO",
      "linkedin": "https://www.linkedin.com/in/johndoe/",
      "url": "https://notion.so/xxxxx"
    }
  ]
}
```

#### Update Contact Email
```bash
python scripts/notion_contact_ops.py update-email \
  --contact-id "2bc1bdff-7e99-81e4-a9b9-f42fb9234628" \
  --email "new.email@company.com" \
  --source "Hunter.io (95% confidence)"

# Output:
{
  "success": true,
  "page_id": "2bc1bdff-7e99-81e4-a9b9-f42fb9234628",
  "email": "new.email@company.com",
  "source": "Hunter.io (95% confidence)",
  "url": "https://notion.so/xxxxx"
}
```

### Company Operations

#### Get Company by Domain
```bash
python scripts/notion_contact_ops.py get-company \
  --domain "recept.ai"

# Output:
{
  "found": true,
  "page_id": "2ae1bdff-7e99-8108-b43a-e2bef1c335a6",
  "page_url": "https://notion.so/2ae1bdff7e998108b43ae2bef1c335a6",
  "icp": "3",
  "name": "Recept AI",
  "domain": "rcpt.ai"
}
```

#### Create or Update Company
```bash
python scripts/notion_contact_ops.py create-or-update-company \
  --name "Krisp" \
  --website "https://krisp.ai" \
  --linkedin "https://www.linkedin.com/company/krisp-technologies" \
  --vertical "Voice AI" \
  --icp "3" \
  --product-desc "AI noise cancellation for calls" \
  --asr-providers "Deepgram,Assembly AI" \
  --ai-engineers 25 \
  --country "United States"

# Output:
{
  "success": true,
  "page_id": "xxx-xxx-xxx",
  "url": "https://notion.so/xxxxx",
  "action": "created",
  "company_name": "Krisp"
}
```

#### Update Company ICP
```bash
python scripts/notion_contact_ops.py update-icp \
  --company-id "2ae1bdff-7e99-8108-b43a-e2bef1c335a6" \
  --icp "2"

# Output:
{
  "success": true,
  "page_id": "2ae1bdff-7e99-8108-b43a-e2bef1c335a6",
  "icp": "2",
  "url": "https://notion.so/xxxxx"
}
```

#### Batch Create/Update Companies
```bash
python scripts/notion_contact_ops.py batch-create-companies \
  --file data/batch-companies.json

# Output:
{
  "success": true,
  "total": 10,
  "created": 7,
  "updated": 3,
  "failed": 0,
  "results": [
    {
      "company": "Krisp",
      "action": "created",
      "page_id": "xxx-xxx-xxx",
      "url": "https://notion.so/xxxxx"
    },
    {
      "company": "Modjo",
      "action": "updated",
      "page_id": "yyy-yyy-yyy",
      "url": "https://notion.so/yyyyy"
    }
  ]
}
```

**JSON File Format (data/batch-companies.json):**
```json
{
  "companies": [
    {
      "name": "Krisp",
      "website": "https://krisp.ai",
      "linkedin": "https://www.linkedin.com/company/krisp-technologies",
      "vertical": "Voice AI",
      "icp": "3",
      "product_description": "AI noise cancellation for calls",
      "asr_providers": ["Deepgram", "Assembly AI"],
      "ai_engineers": 25,
      "main_office_country": "United States"
    },
    {
      "name": "Modjo",
      "website": "https://modjo.ai",
      "linkedin": "https://www.linkedin.com/company/modjo",
      "vertical": "Sales Intelligence",
      "icp": "2",
      "product_description": "Conversation intelligence for sales teams",
      "asr_providers": ["Deepgram"],
      "ai_engineers": 12,
      "main_office_country": "France"
    }
  ]
}
```

**Note:** You can also pass a plain array instead of `{"companies": [...]}` format.

## Integration with Claude Code

### Option 1: Direct Script Execution
From within Claude Code, execute the script directly:
```bash
.venv/bin/python3 scripts/notion_contact_ops.py check-duplicate --linkedin "..."
```

### Option 2: Create Wrapper Slash Command
Create `.claude/commands/add-contact-fast.md`:
```markdown
Use the lightweight Python script instead of MCP tools to save tokens:

1. Run: `.venv/bin/python3 scripts/notion_contact_ops.py check-duplicate --linkedin "{{arg}}"`
2. If not duplicate, gather contact info
3. Run: `.venv/bin/python3 scripts/notion_contact_ops.py add-contact ...`

This approach uses ~7k tokens instead of ~37k tokens.
```

## Database IDs

| Database | ID |
|----------|-----|
| **People** | `20a1bdff-7e99-80fb-9d3c-dfbfa7a8bd70` |
| **Companies** | `20a1bdff-7e99-80c4-8f85-c663fa70c2f2` |

## Error Handling

### Permission Error
```json
{
  "error": "Could not find database with ID: ..."
}
```
**Solution:** Share the database with your Notion integration (see Setup step 3)

### User Not Found
```json
{
  "error": "Could not find user: Benjamin Lalanne"
}
```
**Solution:** Check the user name exactly matches in Notion, or update the script's default owner

### API Key Missing
```json
{
  "error": "NOTION_API_KEY not set"
}
```
**Solution:** Add `NOTION_API_KEY` to `config/.env`

## Maintenance

### Update Database IDs
If database IDs change, update in `scripts/notion_contact_ops.py`:
```python
PEOPLE_DB = "your-new-people-db-id"
COMPANIES_DB = "your-new-companies-db-id"
```

### Add New Operations
Extend the `NotionContactManager` class with new methods following the same pattern:
- Use direct `client.databases.query()` with filters
- Return minimal JSON (only essential fields)
- Cache common lookups (e.g., user IDs)

## Troubleshooting

### Script can't find notion-client
```bash
# Check if using correct Python
which python3

# Use venv Python explicitly
.venv/bin/python3 scripts/notion_contact_ops.py ...
```

### ModuleNotFoundError
```bash
# Install dependencies in venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Wrong notion-client version
```bash
# Install specific version
pip install notion-client==2.2.1
```
