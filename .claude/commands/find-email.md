---
description: Find and add email addresses for contacts in the People database
argument-hint: <contact_name or company_name>
---

# Find Email for Contacts

Discover email addresses for existing contacts in the People database using multiple methods: web search, Hunter.io, and Apollo.io.

**Token Optimization:** Use the Python script for all Notion operations (search, query, update) to save ~10-15k tokens per operation.

## Input
{{arg}}

## Task Instructions

This command enriches existing contacts with email addresses:
1. **Search for contacts** - Use Python script instead of MCP tools (~2k tokens vs 12k)
2. **Extract contact details** - Name, role, company, LinkedIn
3. **Discover emails** - Web search, Hunter.io, Apollo.io
4. **Update contact records** - Use Python script to save emails (~3k tokens vs 10k)

## Usage Modes

### Mode 1: Find email for specific person
```bash
/find-email Paul Berloty
/find-email "Matthieu de la Fournière"
```

### Mode 2: Find emails for all contacts at a company
```bash
/find-email Modjo
/find-email modjo.ai
```

### Mode 3: Batch process contacts without emails
```bash
/find-email --missing-emails
/find-email --all  # Process all contacts (use with caution due to API limits)
```

## Workflow Steps

### 1. Find Contacts in Notion (Using Python Script)

**Option A: Search by name**
```bash
.venv/bin/python3 scripts/notion_contact_ops.py search-contacts --name "Paul Berloty"
```

**Option B: Get all contacts without emails**
```bash
.venv/bin/python3 scripts/notion_contact_ops.py get-contacts-without-email --limit 50
```

**Response Format:**
```json
{
  "found": true,
  "count": 2,
  "contacts": [
    {
      "page_id": "xxx-xxx-xxx",
      "name": "Paul Berloty",
      "email": null,
      "role": "CEO",
      "linkedin": "https://www.linkedin.com/in/paul-berloty/",
      "url": "https://notion.so/xxxxx"
    }
  ]
}
```

- Display contacts found and ask for confirmation before processing
- Skip contacts that already have emails

### 2. Extract Contact Details
For each contact from the script response:
```
- Name (split into first/last)
- Current email (if any)
- Company name and domain (from Company relation)
- Role/title
- LinkedIn URL
- Contact page ID and URL
```

### 3. Email Discovery Process

#### Step 1: Web Search (Free)
```
Search queries:
- "[Full Name] [Company] email"
- "[Full Name] email site:[company_domain]"
- "[Full Name] contact [Company]"

Check sources:
- Company team/about pages
- Press releases and news articles
- Blog author bios
- Conference speaker pages
- LinkedIn "Contact Info" (if visible)
- GitHub profile (if tech role)
```

#### Step 2: Hunter.io Email Finder
```
Prerequisites:
- HUNTER_API_KEY set in config/.env
- Free tier: 25 requests/month

API Call:
GET https://api.hunter.io/v2/email-finder
  ?domain={company_domain}
  &first_name={firstName}
  &last_name={lastName}
  &api_key={HUNTER_API_KEY}

Response:
{
  "data": {
    "email": "paul@modjo.ai",
    "score": 95,
    "sources": [
      {"uri": "https://modjo.ai/team", "extracted_on": "2024-01-15"}
    ],
    "verification": {
      "status": "valid",
      "date": "2024-01-15"
    }
  }
}

Store:
- Email address
- Confidence score
- Source URLs
- Verification status
```

#### Step 3: Apollo.io People Match
```
Prerequisites:
- APOLLO_API_KEY set in config/.env
- Free tier: 50 credits/month

API Call:
POST https://api.apollo.io/v1/people/match
{
  "first_name": "Paul",
  "last_name": "Berloty",
  "organization_name": "Modjo",
  "domain": "modjo.ai"
}

Response:
{
  "person": {
    "email": "paul@modjo.ai",
    "email_status": "verified",
    "phone_numbers": ["+33 1 23 45 67 89"],
    "linkedin_url": "https://www.linkedin.com/in/paul-berloty/"
  }
}

Store:
- Email address
- Verification status
- Phone number (if found)
- LinkedIn (verify against existing)
```

#### Step 4: Email Pattern Guessing + Verification
```
If no email found yet:

1. Get company email pattern:
   - Use Hunter.io Domain Search API
   - Analyze existing emails from same company in database

2. Generate likely emails:
   - {first}@{domain}
   - {first}.{last}@{domain}
   - {f}.{last}@{domain}
   - {first}{last}@{domain}

3. Verify each guess:
   - Use Hunter.io Email Verifier
   - Stop at first valid email

API Call:
GET https://api.hunter.io/v2/email-verifier
  ?email={guessed_email}
  &api_key={HUNTER_API_KEY}

Response:
{
  "data": {
    "status": "valid",  // or "invalid", "accept_all", "unknown"
    "score": 80,
    "regexp": true,
    "gibberish": false,
    "disposable": false,
    "webmail": false,
    "mx_records": true,
    "smtp_server": true,
    "smtp_check": true,
    "accept_all": false
  }
}
```

### 4. Update Contact in Notion (Using Python Script)

Use the Python script to update the contact's email:

```bash
.venv/bin/python3 scripts/notion_contact_ops.py update-email \
  --contact-id "PAGE_ID_FROM_STEP_1" \
  --email "paul@modjo.ai" \
  --source "Hunter.io (95% confidence, verified)"
```

**Response Format:**
```json
{
  "success": true,
  "page_id": "xxx-xxx-xxx",
  "email": "paul@modjo.ai",
  "source": "Hunter.io (95% confidence, verified)",
  "url": "https://notion.so/xxxxx"
}
```

**Token Savings:** ~7k tokens per update (70% reduction) compared to MCP tools

The script automatically updates:
- Email address
- Source information (stored for tracking)

For additional details (verification status, confidence score, date found), you can optionally use Notion MCP to append to "Notes / Bio" field.

## Output Format

```
🔍 Finding emails for contacts...

📋 Contacts to process:
1. Paul Berloty - CEO @ Modjo (Email: Not set)
2. Matthieu de la Fournière - CTO @ Modjo (Email: Not set)
3. Thomas Beylot - CPO @ Modjo (Email: thomas@modjo.ai) ⚠ Already has email

Process 2 contacts without emails? [y/n]

📧 Email Discovery Results:

1. **Paul Berloty** - CEO @ Modjo
   ✓ Web Search: Found "paul@modjo.ai" in team page
   ✓ Hunter.io: Confirmed "paul@modjo.ai" (Score: 95%, Verified)
   ✓ Apollo.io: Matched "paul@modjo.ai" (Status: verified)
   → Best match: paul@modjo.ai (Multiple sources, high confidence)
   → Updated in Notion: https://www.notion.so/...

2. **Matthieu de la Fournière** - CTO @ Modjo
   ✗ Web Search: Not found
   ✓ Hunter.io: Found "matthieu@modjo.ai" (Score: 85%)
   ✓ Apollo.io: Not found
   → Best match: matthieu@modjo.ai (Hunter.io, 85% confidence)
   → Updated in Notion: https://www.notion.so/...

3. **Thomas Beylot** - CPO @ Modjo
   ⏭ Skipped: Already has email (thomas@modjo.ai)

📊 Summary:
- Processed: 2 contacts
- Emails found: 2
- Success rate: 100%
- Skipped: 1 (already has email)

⚠ API Usage:
- Hunter.io: 4 requests used (21 remaining this month)
- Apollo.io: 2 credits used (48 remaining this month)

💡 Next steps:
- Verify emails before outreach
- Update contact notes with additional context
- Set up email sequences
```

## API Setup Instructions

### Hunter.io Setup
1. Sign up at https://hunter.io/
2. Get API key from https://hunter.io/api-keys
3. Add to `config/.env`:
   ```
   HUNTER_API_KEY=your_api_key_here
   ```
4. Free tier: 25 requests/month
5. Paid plans start at $49/month (100 requests)

### Apollo.io Setup
1. Sign up at https://www.apollo.io/
2. Get API key from Settings → Integrations → API
3. Add to `config/.env`:
   ```
   APOLLO_API_KEY=your_api_key_here
   ```
4. Free tier: 50 credits/month
5. Paid plans start at $49/month (unlimited credits)

## Important Notes

### Email Discovery Best Practices
- **Always try web search first** - Free and respects public data
- **Check API quotas** before bulk operations
- **Verify emails** before cold outreach
- **Store sources** for transparency
- **Respect privacy** - Don't harvest emails aggressively

### Data Quality
- **Confidence scoring:**
  - 90-100%: Very reliable (multiple sources)
  - 70-89%: Good (single source, verified)
  - 50-69%: Moderate (pattern-guessed, verified)
  - <50%: Low confidence (use with caution)
- **Skip contacts** that already have verified emails
- **Update carefully** - Don't overwrite good data with guesses

### GDPR & Compliance
- Only use emails for legitimate business purposes
- Include unsubscribe links in all emails
- Respect opt-out requests
- Keep records of email sources
- Don't spam or harass

### Rate Limiting
- Hunter.io free: 25/month, Paid: 100-500/month
- Apollo.io free: 50/month, Paid: unlimited
- Add delays between API calls (1-2 seconds)
- Monitor usage to avoid hitting limits

### Error Handling
1. **API key not set:** Warn user, skip that method
2. **Rate limit exceeded:** Stop processing, show remaining contacts
3. **Invalid email format:** Flag for manual review
4. **No email found:** Store as "Not Found" with date attempted
5. **Multiple emails found:** Choose highest confidence, note alternatives

## Examples

```bash
# Find email for one person
/find-email Paul Berloty

# Find emails for all Modjo contacts
/find-email Modjo

# Find emails for contacts missing emails
/find-email --missing-emails

# Find emails with specific source preference
/find-email Modjo --prefer-hunter

# Batch process with confirmation
/find-email --all --confirm
```

## Follow-up Actions

After finding emails:
- Verify high-confidence emails with Hunter.io Verifier
- Add personalized notes based on web search findings
- Update contact status from "Ice Box" to "To Contact"
- Create email sequences in your outreach tool
- Set reminders for follow-up
