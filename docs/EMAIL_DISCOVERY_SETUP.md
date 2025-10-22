# Email Discovery Setup Guide

Complete guide to setting up and using email discovery for contact enrichment.

## Overview

The email discovery system finds email addresses for contacts using three methods:
1. **Web Search** (Free) - Searches publicly available sources
2. **Hunter.io** (Freemium) - Email finder with verification
3. **Apollo.io** (Freemium) - B2B contact database

## Quick Start

### 1. Get API Keys

#### Hunter.io Setup (Recommended)
1. Go to https://hunter.io/users/sign_up
2. Create a free account
3. Navigate to https://hunter.io/api-keys
4. Copy your API key
5. Free tier includes:
   - 25 email searches/month
   - 50 email verifications/month
   - Domain search

**Pricing:**
- Free: 25 searches/month
- Starter: $49/month - 100 searches
- Growth: $99/month - 500 searches
- Business: $199/month - 1,500 searches

#### Apollo.io Setup (Optional but recommended)
1. Go to https://www.apollo.io/sign-up
2. Create a free account
3. Navigate to Settings → Integrations → API
4. Copy your API key
5. Free tier includes:
   - 50 email credits/month
   - Better B2B coverage
   - Phone numbers included

**Pricing:**
- Free: 50 credits/month
- Basic: $49/month - Unlimited
- Professional: $79/month - Unlimited + advanced features

### 2. Configure API Keys

Add API keys to your environment:

```bash
cd /Users/benja/Projects/blynt-customer-development

# Copy example env file if you haven't already
cp config/.env.example config/.env

# Edit the .env file
nano config/.env
```

Add your keys:
```bash
# Email Discovery APIs
HUNTER_API_KEY=your_hunter_key_here
APOLLO_API_KEY=your_apollo_key_here
```

### 3. Test the Setup

Test if your API keys work:

```python
from src.utils.email_discovery import EmailDiscovery

# Initialize
discovery = EmailDiscovery()

# Test with a known contact
results = discovery.discover_email(
    first_name="Paul",
    last_name="Berloty",
    domain="modjo.ai",
    company_name="Modjo",
    role="CEO"
)

# Print results
for result in results:
    print(result)
```

## Usage

### Method 1: During Contact Addition

Use `/add-contact` command with automatic email discovery:

```bash
/add-contact modjo.ai
```

This will:
1. Find contacts from the company
2. Automatically discover emails for each contact
3. Add contacts with emails to Notion

### Method 2: Enrich Existing Contacts

Use `/find-email` command to add emails to existing contacts:

```bash
# Find email for specific person
/find-email Paul Berloty

# Find emails for all contacts at a company
/find-email Modjo

# Find emails for contacts missing emails
/find-email --missing-emails
```

### Method 3: Programmatic Usage

Use the Python module directly:

```python
from src.utils.email_discovery import EmailDiscovery, split_full_name, extract_domain_from_url

# Initialize discovery
discovery = EmailDiscovery()

# Discover email
results = discovery.discover_email(
    first_name="John",
    last_name="Doe",
    domain="example.com",
    company_name="Example Inc",
    role="CTO"
)

# Get best result
if results:
    best = results[0]  # Sorted by confidence
    print(f"Found: {best.email}")
    print(f"Source: {best.source.value}")
    print(f"Confidence: {best.confidence}%")
    print(f"Verified: {best.verified}")
```

## How It Works

### Email Discovery Flow

```
┌─────────────────────────────────────────────────┐
│ Input: Name, Company Domain, Role (optional)    │
└──────────────────┬──────────────────────────────┘
                   │
                   v
┌─────────────────────────────────────────────────┐
│ Step 1: Web Search (Free)                       │
│ - Search "[Name] [Company] email"               │
│ - Check company website, press releases         │
│ - Look for public email addresses               │
└──────────────────┬──────────────────────────────┘
                   │
                   v
         ┌─────────┴─────────┐
         │ Email found?      │
         └─────────┬─────────┘
                   │ No
                   v
┌─────────────────────────────────────────────────┐
│ Step 2: Hunter.io API                           │
│ - Email Finder API                              │
│ - Returns email + confidence score              │
│ - Includes source URLs                          │
└──────────────────┬──────────────────────────────┘
                   │
                   v
         ┌─────────┴─────────┐
         │ Email found?      │
         └─────────┬─────────┘
                   │ No
                   v
┌─────────────────────────────────────────────────┐
│ Step 3: Apollo.io API                           │
│ - People Match API                              │
│ - Better B2B coverage                           │
│ - Returns verified emails                       │
└──────────────────┬──────────────────────────────┘
                   │
                   v
         ┌─────────┴─────────┐
         │ Email found?      │
         └─────────┬─────────┘
                   │ No
                   v
┌─────────────────────────────────────────────────┐
│ Step 4: Pattern Guessing + Verification         │
│ - Get company email pattern                     │
│ - Generate possible emails:                     │
│   • first@domain.com                            │
│   • first.last@domain.com                       │
│   • f.last@domain.com                           │
│ - Verify each with Hunter.io                    │
└──────────────────┬──────────────────────────────┘
                   │
                   v
┌─────────────────────────────────────────────────┐
│ Output: List of EmailResult                     │
│ - Sorted by confidence (highest first)          │
│ - Includes source, verification status          │
└─────────────────────────────────────────────────┘
```

### Confidence Scoring

The system assigns confidence scores (0-100%) based on:

- **90-100%**: Multiple sources confirm, verified
  - Example: Found in Hunter + Apollo + company website

- **70-89%**: Single reliable source, verified
  - Example: Hunter.io with high score + verification

- **50-69%**: Pattern-guessed but verified
  - Example: Generated from pattern, verified as deliverable

- **<50%**: Low confidence, use with caution
  - Example: Pattern guess, not verified

### Email Pattern Detection

Common patterns the system uses:

| Pattern | Example | Frequency |
|---------|---------|-----------|
| `{first}@{domain}` | paul@modjo.ai | 35% |
| `{first}.{last}@{domain}` | paul.berloty@modjo.ai | 30% |
| `{f}.{last}@{domain}` | p.berloty@modjo.ai | 15% |
| `{first}{last}@{domain}` | paulberloty@modjo.ai | 10% |
| `{first}_{last}@{domain}` | paul_berloty@modjo.ai | 5% |
| `{last}.{first}@{domain}` | berloty.paul@modjo.ai | 3% |
| `{first}-{last}@{domain}` | paul-berloty@modjo.ai | 2% |

The system:
1. Fetches the company's most common pattern from Hunter.io
2. Generates emails using all common patterns
3. Verifies each generated email
4. Returns the first valid one

## Best Practices

### Rate Limiting

Be mindful of API quotas:

```python
# Check remaining quota before bulk operations
from src.utils.email_discovery import EmailDiscovery

discovery = EmailDiscovery()

# For Hunter.io - track manually or use their Account Info endpoint
# GET https://api.hunter.io/v2/account?api_key=YOUR_KEY

# For Apollo.io - they have generous free tier but track usage
```

**Recommended approach:**
- Use web search first (free)
- Reserve API calls for high-value contacts
- Batch process during off-peak hours
- Add delays between requests (1-2 seconds)

### Email Verification

Always verify emails before cold outreach:

```python
from src.utils.email_discovery import EmailDiscovery

discovery = EmailDiscovery()

# Verify single email
is_valid = discovery._verify_email_hunter("paul@modjo.ai")

if is_valid:
    print("Email is deliverable")
else:
    print("Email may not be valid")
```

### GDPR Compliance

**Important legal considerations:**

1. **Legitimate Interest**
   - Only use emails for B2B business purposes
   - Keep records of why you're contacting someone
   - Provide easy opt-out mechanisms

2. **Data Storage**
   - Store email source and confidence
   - Record when email was discovered
   - Delete emails upon request

3. **Email Usage**
   - Include unsubscribe links in all emails
   - Honor opt-out requests immediately
   - Don't share emails with third parties

4. **Anti-Spam Laws**
   - CAN-SPAM (US): Include physical address, unsubscribe
   - GDPR (EU): Legitimate interest or consent required
   - CASL (Canada): Express or implied consent

### Error Handling

The system handles common errors gracefully:

```python
results = discovery.discover_email(...)

for result in results:
    if result.email:
        print(f"✓ Found: {result.email}")
    elif result.error:
        if "rate limit" in result.error.lower():
            print("⚠ Rate limit exceeded - try again later")
        elif "api key" in result.error.lower():
            print("⚠ API key invalid or not set")
        else:
            print(f"✗ Error: {result.error}")
```

## Troubleshooting

### Problem: "Hunter.io API key not set"

**Solution:**
1. Check if `HUNTER_API_KEY` is in your `.env` file
2. Ensure `.env` file is in the `config/` directory
3. Restart your application to load new env vars

```bash
# Check if key is loaded
python -c "import os; print(os.getenv('HUNTER_API_KEY'))"
```

### Problem: "Rate limit exceeded"

**Solution:**
- Wait until next month for quota reset
- Upgrade to paid plan
- Use alternative method (Apollo or web search)

**Check remaining quota:**
```bash
curl "https://api.hunter.io/v2/account?api_key=YOUR_KEY"
```

### Problem: "No email found"

**Possible reasons:**
1. Person doesn't have a public email
2. Email uses uncommon pattern
3. API databases don't have this contact

**Solutions:**
- Try LinkedIn direct message
- Use company general contact form
- Check if email is on their personal website
- Look for them on GitHub, Twitter, conference sites

### Problem: Low confidence emails

**What to do:**
1. Manually verify on company website
2. Use email verification services
3. Send test email (carefully)
4. Use LinkedIn InMail instead

## API Documentation

### Hunter.io API

**Endpoints used:**
- Email Finder: `GET /v2/email-finder`
- Email Verifier: `GET /v2/email-verifier`
- Domain Search: `GET /v2/domain-search`

**Docs:** https://hunter.io/api/v2/docs

**Response format:**
```json
{
  "data": {
    "email": "paul@modjo.ai",
    "score": 95,
    "verification": {
      "status": "valid",
      "date": "2024-01-15"
    },
    "sources": [
      {
        "domain": "modjo.ai",
        "uri": "https://modjo.ai/team",
        "extracted_on": "2024-01-15"
      }
    ]
  }
}
```

### Apollo.io API

**Endpoints used:**
- People Match: `POST /v1/people/match`

**Docs:** https://apolloio.github.io/apollo-api-docs/

**Response format:**
```json
{
  "person": {
    "email": "paul@modjo.ai",
    "email_status": "verified",
    "first_name": "Paul",
    "last_name": "Berloty",
    "linkedin_url": "https://www.linkedin.com/in/paul-berloty/",
    "phone_numbers": [],
    "organization": {
      "name": "Modjo",
      "website_url": "https://modjo.ai"
    }
  }
}
```

## Advanced Usage

### Custom Email Patterns

Add company-specific patterns:

```python
from src.utils.email_discovery import EmailDiscovery

discovery = EmailDiscovery()

# Override pattern generation
def custom_patterns(first, last, domain):
    # Add your custom patterns
    return [
        f"{first[0]}{last}@{domain}",  # pberloty@modjo.ai
        f"{first}.{last}@{domain}",
    ]

discovery._generate_email_patterns = custom_patterns
```

### Batch Processing

Process multiple contacts efficiently:

```python
import time
from src.utils.email_discovery import EmailDiscovery

discovery = EmailDiscovery()

contacts = [
    ("Paul", "Berloty", "modjo.ai"),
    ("Matthieu", "de la Fournière", "modjo.ai"),
    # ... more contacts
]

results_all = []

for first, last, domain in contacts:
    results = discovery.discover_email(first, last, domain)
    results_all.append((f"{first} {last}", results))

    # Rate limiting: wait between requests
    time.sleep(2)

# Process results
for name, results in results_all:
    if results and results[0].email:
        print(f"✓ {name}: {results[0].email}")
    else:
        print(f"✗ {name}: No email found")
```

### Logging and Monitoring

Track email discovery operations:

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)

# The EmailDiscovery class already logs operations
# View logs in your application's log file

# To adjust log level:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## FAQ

**Q: Which service should I use first?**
A: Always start with web search (free), then Hunter.io (better coverage), then Apollo (B2B focus).

**Q: How accurate are the results?**
A: Hunter.io typically 85-95% accurate for verified emails. Apollo similar. Pattern guessing lower at 60-70%.

**Q: Can I use this for mass email campaigns?**
A: Technically yes, but ensure GDPR compliance and use proper email marketing tools with unsubscribe features.

**Q: What if email bounces?**
A: Mark as invalid in your database. Don't retry. Bounces hurt your sender reputation.

**Q: Can I find personal emails (Gmail, etc.)?**
A: This is designed for business emails only. Personal emails are harder to find and ethically questionable to use.

**Q: How do I export found emails?**
A: Use the `/find-email` command which automatically updates Notion, or export from Notion database.

## Support

For issues or questions:
1. Check this guide first
2. Review API documentation (Hunter.io, Apollo.io)
3. Check application logs for errors
4. Open an issue in the project repository

## Updates

Last updated: 2025-10-17
Version: 1.0.0
