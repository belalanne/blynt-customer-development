---
description: Research and add key contacts from a company to the People database
argument-hint: <company_name or domain>
---

# Add Contacts from Company Research

Research key people from a target company and add them to the Notion People database with "Status Contact" set to "🥶 Ice Box".

## Input
{{arg}}

## Task Instructions

This command performs research-based contact discovery:
1. **Search for the company** in the Notion Companies database
2. **Check existing mentions** - Review the company's Notion page for already mentioned contacts
3. **Research key people** - Find decision makers and relevant contacts from the web
4. **Add new contacts** - Create entries in the People database for contacts not already tracked

### Target Roles to Research:
- **C-Level:** CEO, CTO, CIO, CPO, CMO
- **Engineering Leadership:** VP Engineering, Head of ML/AI, Director of Engineering
- **Product Leadership:** VP Product, Head of Product
- **Sales/Rev Ops:** CRO, VP Sales, Head of Revenue Operations
- **Decision Makers:** Anyone with budget authority for speech/AI tools

### Research Sources:
1. **Company website** - About page, Team page, Leadership section
2. **LinkedIn** - Company page employees, especially recent hires in key roles
3. **Crunchbase** - Founders and key executives
4. **News/press releases** - Recent announcements of new hires
5. **Company blog/engineering blog** - Authors of technical content

## Database Details
- **People Database Collection ID:** `collection://20a1bdff-7e99-81a7-8612-000b6f8a32f4`
- **Companies Database Collection ID:** `collection://20a1bdff-7e99-81b9-badb-000bc5d45f78`

## Duplicate Detection Keys

**CRITICAL**: To avoid duplicates, use these unique identifiers:
- **Companies**: Website URL/domain (e.g., "modjo.ai", "https://www.modjo.ai")
- **People**: LinkedIn URL (e.g., "https://www.linkedin.com/in/paul-berloty/")

## Workflow Steps

### 1. Find Company in Notion (Using Website URL as Key)
```
Search Strategy:
1. Normalize input to domain format:
   - "modjo.ai" → "modjo.ai"
   - "https://www.modjo.ai" → "modjo.ai"
   - "Modjo" → search by name, then verify domain

2. Search Companies database by Website property:
   - Use Notion search with domain/URL
   - Match against "Website" field (unique identifier)

3. If found:
   - Note the company page URL
   - Fetch the page content
   - Extract company domain for email discovery
   - **IMPORTANT:** Extract the company's ICP value (1, 2, 3, or N/A)

4. If NOT found:
   - Show: "Company not found in database"
   - Ask if user wants to run `/enrich-company [domain]` first
   - Do NOT proceed without company in database
```

### 2. Extract Already Mentioned Contacts from Company Page
```
Check company page content for:
- Names of people mentioned
- Roles/titles
- LinkedIn URLs (IMPORTANT: this is our duplicate detection key)
- Emails if listed

Keep track of these contacts to:
1. Avoid re-adding them
2. Compare against People database
3. Show user what's already tracked
```

### 3. Check for Duplicates in People Database (Using LinkedIn URL as Key)
```
CRITICAL STEP - Before adding any contact:

For each contact found in research:
1. Extract their LinkedIn URL
2. Search People database for existing contact with same LinkedIn URL
3. Check results:
   - If LinkedIn URL matches → SKIP this contact (duplicate)
   - If LinkedIn URL not found → Safe to add
   - If no LinkedIn URL available → Check by name + company (less reliable)

Search Methods:
a) Primary: Search by LinkedIn URL property
   - Most reliable unique identifier
   - Example: https://www.linkedin.com/in/paul-berloty/

b) Fallback: Search by Contact_Name + Company
   - Only if no LinkedIn URL available
   - Less reliable (name variations)

Duplicate Handling:
- ✓ Skip duplicates: Do NOT create new contact
- ℹ Inform user: "Already in database: [Name] - [Role]"
- 🔄 Optional: Offer to update existing contact with new info (email, role change)
```

### 4. Research New Contacts

**PRIORITY: Use Exa LinkedIn Search (If Available)**

1. **Try Exa LinkedIn Search First:**
   ```
   Tool: mcp__exa__linkedin_search

   Search queries to try:
   - "[Company Name] CEO"
   - "[Company Name] CTO"
   - "[Company Name] VP Engineering"
   - "[Company Name] Head of Product"

   Benefits:
   - ✅ Direct LinkedIn data access
   - ✅ Automatically includes LinkedIn URLs (for duplicate detection)
   - ✅ More accurate role/title information
   - ✅ Recent employment data
   ```

2. **If Exa succeeds:**
   - Extract: Name, Role, LinkedIn URL, Company
   - LinkedIn URL is automatically included (perfect for duplicate detection!)
   - Proceed to duplicate checking (Step 3)

3. **Fallback to Traditional Methods (if Exa unavailable):**
   ```
   - Use WebSearch to find:
     - "[Company] leadership team"
     - "[Company] CEO CTO"
     - "[Company] LinkedIn employees"
   - Visit company website /about, /team pages
   - Check LinkedIn company page for recent hires in target roles
   - Gather: Name, Role, LinkedIn URL (CRITICAL for duplicate detection)
   ```

**IMPORTANT: LinkedIn URL is mandatory for reliable duplicate detection**
- Exa automatically provides LinkedIn URLs
- If using fallback methods, always try to get LinkedIn URL
- If not available, use alternative search methods
```

### 5. Discover Email Addresses
For each contact found, attempt to find their email using multiple methods:

#### Method 1: Web Search (Free, always try first)
```
- Search: "[Name] [Company] email"
- Search: "[Name] email site:[company_domain]"
- Check: Company team page, press releases, blog author bios
- Check: LinkedIn "Contact Info" section (if visible)
- Look for email patterns in existing known emails
```

#### Method 2: Hunter.io (Freemium - 25 searches/month free)
```
Prerequisites:
- Set HUNTER_API_KEY in config/.env
- Free tier: 25 requests/month
- Paid: $49+/month for more volume

Steps:
1. Extract domain from company website (e.g., "modjo.ai")
2. Use Email Finder API:
   - Input: First name, Last name, Domain
   - Output: Likely email + confidence score
3. Use Email Verifier to validate if needed
4. Learn company email pattern (e.g., first@domain.com)

API Example:
GET https://api.hunter.io/v2/email-finder
  ?domain={domain}
  &first_name={firstName}
  &last_name={lastName}
  &api_key={HUNTER_API_KEY}

Response includes:
- email: "paul@modjo.ai"
- score: 95 (confidence)
- sources: [list of where found]
```

#### Method 3: Apollo.io (Freemium - 50 credits/month free)
```
Prerequisites:
- Set APOLLO_API_KEY in config/.env
- Free tier: 50 email credits/month
- Better coverage for tech companies

Steps:
1. Use People Search API with:
   - Name
   - Company domain
   - Job title (optional, for accuracy)
2. Returns: Email, phone, LinkedIn, validation status

API Example:
POST https://api.apollo.io/v1/people/match
{
  "first_name": "Paul",
  "last_name": "Berloty",
  "organization_name": "Modjo",
  "domain": "modjo.ai"
}

Response includes:
- email: "paul@modjo.ai"
- email_status: "verified"
- phone_numbers: []
- linkedin_url: "..."
```

#### Email Discovery Priority
```
1. Try Web Search first (free, sometimes finds emails in public content)
2. If no email found, try Hunter.io (good for pattern detection)
3. If still not found, try Apollo.io (better B2B coverage)
4. If none work, use pattern guessing + verification:
   - Guess: first@domain, first.last@domain, f.last@domain
   - Verify with Hunter.io Email Verifier
5. Store confidence level with email
```

#### Email Pattern Detection
```
If you find any emails for a company, detect the pattern:
- paul@modjo.ai → pattern: {first}@{domain}
- paul.berloty@modjo.ai → pattern: {first}.{last}@{domain}
- p.berloty@modjo.ai → pattern: {f}.{last}@{domain}

Use this pattern to guess other emails from same company
Always verify guessed emails before using
```

### 6. Add Contacts to People Database
For each NEW contact (verified as non-duplicate via LinkedIn URL check):

```json
{
  "Contact_Name": "Full Name",
  "Role": "Job Title",
  "Company name": "<company_page_url>",  // Use the Notion page URL from Step 1
  "Email": "email@example.com",  // if found via email discovery
  "LinkedIn URL": "https://linkedin.com/in/username",  // REQUIRED for duplicate detection
  "Decision_Level": "Decision Maker",  // based on role (string, not array)
  "Type": "Customer",  // string, not array
  "Status Contact": "🥶 Ice Box",
  "Source of contacts": "Outreach",  // valid values: Outreach, Inbound, Event, Referral, Personal
  "Owner / Assigned To": "Benjamin Lalanne",  // default owner
  "Campaign": "ICP#1"  // Map from company ICP: "1" → "ICP#1", "2" → "ICP#2", "3" → "ICP#3", "N/A" → null
}
```

**Campaign Mapping:**
- If company ICP = "1" → Set Campaign = "ICP#1"
- If company ICP = "2" → Set Campaign = "ICP#2"
- If company ICP = "3" → Set Campaign = "ICP#3"
- If company ICP = "N/A" or not set → Leave Campaign empty/null

**Pre-creation check:**
1. Search People database for this LinkedIn URL
2. If found → Skip (log as duplicate)
3. If not found → Proceed with creation

**Post-creation:**
- Log the contact URL for reporting
- Track email discovery success/failure
- Note any missing information

### 7. Update Company Page (Optional)
```
- Add a section with contacts found (if not already present)
- Format: "## Key Contacts\n- [Name] - [Role] - [Email] - [LinkedIn]"
```

## Decision Level Mapping

Automatically infer Decision_Level based on role:
- **Decision Maker:** CEO, CTO, CIO, VP-level
- **Influencer:** Director-level, Head of, Senior Manager
- **Buyer:** Manager-level positions with procurement influence

## Output Format

```
🔍 Researching contacts for [Company Name]...

✅ Found company in database: [Notion URL]
📧 Company domain: [domain] (for email discovery)
🔑 Using Website URL as unique key for company matching

📋 Already tracked contacts in People database:
- [Name] - [Role] - LinkedIn: [url] ✓ (already in database)
- [Name] - [Role] - No LinkedIn ⚠ (mentioned in company page)

🌐 Researching new contacts...
Found [X] potential contacts

🔍 Checking for duplicates (using LinkedIn URL as key)...
- [Name]: Checking LinkedIn [url]... ✓ New contact
- [Name]: Checking LinkedIn [url]... ⚠ DUPLICATE - Skipping
- [Name]: No LinkedIn URL found... ⚠ Checking by name + company... ✓ New contact

📧 Discovering email addresses for new contacts...
- Trying web search for [Name]... [✓ Found / ✗ Not found]
- Trying Hunter.io... [✓ Found: email@domain.com (95% confidence) / ✗ Not found / ⚠ API key not set]
- Trying Apollo.io... [✓ Found: email@domain.com (verified) / ✗ Not found / ⚠ API key not set]
- Email pattern detected: {first}@{domain}

✅ Added [X] new contacts to People Database:

1. **[Name]** - [Role]
   - LinkedIn: [url] ✓
   - Email: [email@domain.com] ✓ (Source: Hunter.io, 95% confidence)
   - Decision Level: [level]
   - Owner: Benjamin Lalanne
   - Campaign: ICP#[1/2/3]
   - Source: Outreach
   - Notion: [page_url]

2. **[Name]** - [Role]
   - LinkedIn: [url] ✓
   - Email: [Not found] ⚠ (Suggested: first@domain, first.last@domain)
   - Decision Level: [level]
   - Owner: Benjamin Lalanne
   - Campaign: ICP#[1/2/3]
   - Source: Outreach
   - Notion: [page_url]

⏭️ Skipped [X] duplicates:
- [Name] - [Role] (Already in database: [notion_url])
- [Name] - [Role] (Already in database: [notion_url])

📊 Summary:
- Contacts found: [total]
- New contacts added: [X]
- Duplicates skipped: [X]
- Emails discovered: [X]/[new contacts]

💡 Next steps:
- Review and enrich contact information
- Verify email addresses before cold outreach
- Set up outreach sequence for new contacts
- Update engagement status as needed
```

## Examples

```bash
# Research contacts from a domain
/add-contact gladia.io

# Research from company name
/add-contact Deepgram

# Research from company with guidance
/add-contact Assembly AI - focus on engineering leadership
```

## Important Notes

### Duplicate Detection (CRITICAL)
- **Company uniqueness:** Website URL/domain is the unique identifier
  - Always search by domain when looking for companies
  - "modjo.ai" and "https://www.modjo.ai" should match the same company
  - Normalize URLs before searching (remove www, protocol, paths)

- **People uniqueness:** LinkedIn URL is the unique identifier
  - ALWAYS try to get LinkedIn URL for each contact
  - Search People database by LinkedIn URL before adding
  - If LinkedIn URL matches existing contact → SKIP (duplicate)
  - If no LinkedIn URL: fallback to name + company check (less reliable)

- **Duplicate handling workflow:**
  1. Search People DB by LinkedIn URL
  2. If found → Skip and log as duplicate
  3. If not found → Verify by name + company
  4. Only add if confirmed as new contact

### General Guidelines
- **Prioritize quality over quantity:** Focus on decision makers and influencers
- **LinkedIn URL is mandatory:** For reliable duplicate detection
- **Cite sources:** Include source URLs for each contact found
- **Status Contact** is ALWAYS set to "🥶 Ice Box" by default
- **Decision_Level** should be a string: "Buyer", "Decision Maker", or "Influencer"
- **Type** defaults to "Customer" (string, not array)
- **Source of contacts** is ALWAYS set to "Outreach" (valid values: "Outreach", "Inbound", "Event", "Referral", "Personal")
- **Owner / Assigned To** is ALWAYS set to "Benjamin Lalanne"
- **Campaign** is automatically set based on company ICP:
  - ICP "1" → "ICP#1"
  - ICP "2" → "ICP#2"
  - ICP "3" → "ICP#3"
  - ICP "N/A" or missing → Leave empty

### Email Discovery Notes
- **Always try web search first** - It's free and sometimes emails are publicly listed
- **API Keys Required:**
  - Hunter.io: Set `HUNTER_API_KEY` in `config/.env`
  - Apollo.io: Set `APOLLO_API_KEY` in `config/.env`
  - Without API keys, only web search will work
- **Rate Limits:**
  - Hunter.io free: 25 searches/month
  - Apollo.io free: 50 credits/month
  - Pace requests appropriately to avoid hitting limits
- **Email Confidence:**
  - Store confidence score with emails
  - Verify emails before cold outreach
  - Pattern-guessed emails should be verified
- **GDPR Compliance:**
  - Only use emails for legitimate business purposes
  - Respect opt-outs and unsubscribe requests
  - Follow anti-spam laws (CAN-SPAM, GDPR)
- **Email Storage:**
  - Store email source (Web, Hunter, Apollo, Pattern)
  - Store confidence level if available
  - Note verification status

## Error Handling

1. **Company not found by URL:**
   - Normalize the domain (remove www, protocol, trailing slash)
   - Search again with normalized domain
   - If still not found: Prompt user to run `/enrich-company [domain]` first
   - Do NOT proceed without company in database

2. **All contacts are duplicates:**
   - Report: "All [X] contacts found are already in database"
   - List the existing contacts with Notion URLs
   - Suggest: Review existing contacts or look for additional team members

3. **No LinkedIn URL found for contact:**
   - Warning: "Cannot reliably check for duplicates without LinkedIn URL"
   - Fallback: Search by Contact_Name + Company name
   - If match found: Skip (likely duplicate)
   - If no match: Add with warning note

4. **Duplicate detection ambiguity:**
   - Multiple contacts with similar names at same company
   - No LinkedIn URL to verify uniqueness
   - Action: Ask user to manually verify before adding

5. **No new contacts found:**
   - Report already tracked contacts only
   - Check company page, team page, news
   - Suggest alternative sources (Crunchbase, press releases)

6. **Rate limiting:**
   - Pace web searches appropriately (1-2 seconds between requests)
   - For API limits: Show remaining quota
   - Suggest: Process high-priority contacts first

## Follow-up Actions

After adding contacts:
- Consider running `/enrich-company` if company needs more data
- Set up outreach campaign in your CRM
- Map company to ICP with `/map-icp` if not done
