# Exa AI Integration Setup

Exa AI provides enhanced search capabilities for company research and contact discovery.

## Why Use Exa?

### Benefits
- ✅ **Faster company research** - Structured data in seconds
- ✅ **Better LinkedIn access** - Direct professional search
- ✅ **Higher quality results** - AI-optimized search
- ✅ **Token efficient** - Reduced context usage
- ✅ **Fewer hallucinations** - Verified sources

### Impact on Your Workflows
- **`/enrich-company`**: Get company data 3x faster with better accuracy
- **`/add-contact`**: LinkedIn search returns profiles with URLs automatically
- **`/exa-search`**: Standalone AI search for any query

## Setup Instructions

### Step 1: Get Exa API Key

1. Sign up at [https://exa.ai](https://exa.ai)
2. Navigate to your dashboard
3. Generate an API key
4. Copy the key (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### Step 2: Add to Environment

Add your Exa API key to `config/.env`:

```bash
# Exa AI Search
EXA_API_KEY=your_exa_api_key_here
```

### Step 3: Configure MCP Server

Your `.mcp.json` should already be configured with:

```json
{
  "mcpServers": {
    "Notion": {
      "url": "https://mcp.notion.com/mcp"
    },
    "Exa": {
      "url": "https://mcp.exa.ai/mcp",
      "headers": {
        "x-api-key": "your_exa_api_key_here"
      }
    }
  }
}
```

### Step 4: Restart Claude Code

**IMPORTANT:** You must restart Claude Code for the MCP server to load.

1. Quit Claude Code completely
2. Restart Claude Code
3. Verify Exa tools are available

## Verify Installation

### Test with `/exa-search`

Try the test command to verify Exa is working:

```bash
/exa-search gladia.io
```

Expected output:
- Tool used: `company_research`
- Structured company data
- Sources with URLs

### Check Available Tools

After restarting, these Exa MCP tools should be available:
- `mcp__exa__company_research` - Company intelligence
- `mcp__exa__linkedin_search` - Professional search
- `mcp__exa__web_search_exa` - General web search
- `mcp__exa__deep_researcher_start` - Complex research
- `mcp__exa__deep_researcher_check` - Research status

## Usage in Commands

### Enhanced `/enrich-company`

The command now automatically:
1. **Tries Exa first** - Uses `company_research` tool
2. **Falls back gracefully** - Uses web search if Exa unavailable
3. **Better results** - Structured firmographics, tech stack, funding

Example:
```bash
/enrich-company deepgram.com
```

### Enhanced `/add-contact`

The command now automatically:
1. **Uses Exa LinkedIn search** - Direct professional data
2. **Gets LinkedIn URLs** - Perfect for duplicate detection
3. **Falls back** - Uses traditional methods if needed

Example:
```bash
/add-contact assembly.ai
```

### Standalone Exa Search

Use `/exa-search` for any research:

```bash
# Company research
/exa-search modjo.ai

# LinkedIn search
/exa-search "CTO at Gladia"

# General search
/exa-search "best speech recognition APIs 2024"
```

## Available Exa Tools

### 1. Company Research
**Tool:** `mcp__exa__company_research`

**Best for:**
- Company firmographics
- Business intelligence
- Funding and team size
- Tech stack detection

**Example query:** `gladia.io`

**Returns:**
- Company name, description
- Headquarters, employee count
- Funding stage and amount
- Technology stack
- Recent news

### 2. LinkedIn Search
**Tool:** `mcp__exa__linkedin_search`

**Best for:**
- Finding professionals by role
- Company employee research
- Contact discovery

**Example query:** `"CEO at Deepgram"`

**Returns:**
- Name, current role
- LinkedIn profile URL
- Company information
- Experience highlights

### 3. Web Search
**Tool:** `mcp__exa__web_search_exa`

**Best for:**
- General research
- Technical documentation
- News and articles

**Example query:** `speech recognition API comparison`

**Returns:**
- Relevant web pages
- Summaries and key points
- Source URLs

### 4. Deep Research
**Tools:** `deep_researcher_start` + `deep_researcher_check`

**Best for:**
- Complex multi-source analysis
- Comprehensive reports
- Cross-reference validation

**Use case:** Market research, competitive analysis

## Pricing

Check [https://exa.ai/pricing](https://exa.ai/pricing) for current pricing.

Typical plans:
- **Free tier**: Limited searches for testing
- **Starter**: $X/month for regular use
- **Pro**: $X/month for high volume

## Troubleshooting

### Issue: Exa tools not available

**Solution:**
1. Check `.mcp.json` is configured correctly
2. Verify API key in `config/.env`
3. **Restart Claude Code completely** (quit and reopen)
4. Try `/exa-search test` to verify

### Issue: Authentication errors

**Solution:**
1. Verify API key is correct (no extra spaces)
2. Check key hasn't expired
3. Ensure key is in both `.mcp.json` and `config/.env`

### Issue: Rate limiting

**Solution:**
- Check your Exa plan limits
- Space out requests
- Consider upgrading plan

### Issue: Empty results

**Solution:**
- Try different query phrasing
- Check if company/person exists
- Fall back to traditional web search

## Fallback Behavior

All commands are designed to work **with or without** Exa:

- **If Exa available:** Uses Exa for faster, better results
- **If Exa unavailable:** Falls back to WebSearch, LinkedIn scraping, etc.
- **Graceful degradation:** No errors, just different data sources

This means you can:
- Test without Exa first
- Add Exa later for enhancement
- Remove Exa if budget constrained

## Best Practices

1. **Use Exa for high-value searches** - Company research, contact discovery
2. **Fall back for bulk operations** - Save API credits
3. **Verify results** - Always check sources provided
4. **Cache results** - Store Exa data to avoid repeat queries
5. **Monitor usage** - Track API consumption

## Example Workflow

### Complete Company Analysis with Exa

```bash
# 1. Enrich company (uses Exa automatically)
/enrich-company gladia.io

# 2. Map to ICP
/map-icp gladia.io

# 3. Discover subprocessors
/discover-subprocessors gladia.io

# 4. Add contacts (uses Exa LinkedIn search)
/add-contact gladia.io

# 5. Sync everything to Notion
/sync-to-notion gladia.io all
```

With Exa, this workflow is:
- ⚡ **3x faster** than web scraping
- 🎯 **More accurate** with structured data
- 📊 **Better LinkedIn coverage** with direct search
- 💰 **Token efficient** with optimized responses

## Migration Notes

### Already Using Commands Without Exa?

No changes needed! Commands automatically detect and use Exa when available.

### Want to Disable Exa Temporarily?

Remove from `.mcp.json` and restart Claude Code. Commands will fall back to traditional methods.

### Want to Add Exa to Existing Workflows?

Just follow the setup steps above. Existing commands will automatically benefit.

## Support

- **Exa Documentation:** https://docs.exa.ai
- **Exa MCP Guide:** https://docs.exa.ai/reference/exa-mcp
- **Issues:** Check logs in Claude Code for error messages
