# Blynt Customer Development

Go-to-Market intelligence platform for discovering lookalike companies, enriching company data, mapping subprocessors, and syncing to Notion.

## Features

- **Company Enrichment**: Gather firmographics, tech stack, funding, and contact info
- **Lookalike Discovery**: Find similar companies based on multiple attributes
- **Subprocessor Mapping**: Discover and map vendor relationships
- **Notion Integration**: Sync all data to Notion databases with proper relationships
- **Batch Processing**: Process multiple companies efficiently
- **Claude Code Integration**: Powerful slash commands for common workflows

## Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (for web scraping)
playwright install
```

### 2. Configuration

```bash
# Copy example environment file
cp config/.env.example config/.env

# Edit config/.env and add your API keys
```

Required API keys:
- `NOTION_API_KEY` - Notion integration token
- `NOTION_DATABASE_ID` - Your Notion database ID

Optional API keys (for enrichment):
- `CLEARBIT_API_KEY`, `APOLLO_API_KEY`, `LINKEDIN_API_KEY`
- `OPENAI_API_KEY` - For AI-powered analysis

### 3. Set up Notion Database

Create a Notion database with these properties:
- **Name** (Title)
- **Domain** (URL)
- **Industry** (Select)
- **Employee Count** (Number)
- **Location** (Text)
- **Tech Stack** (Multi-select)
- **LinkedIn** (URL)
- **Lookalikes** (Relation to same database)
- **Subprocessors** (Relation to Subprocessors database)

Copy the database ID from the URL and add to `.env`.

## Usage

### Using Claude Code Slash Commands

This project is optimized for use with Claude Code. Use these slash commands:

```bash
# Enrich a single company
/enrich-company example.com

# Find lookalike companies
/find-lookalikes example.com 20 0.7

# Discover subprocessors
/discover-subprocessors example.com

# Sync data to Notion
/sync-to-notion example.com all

# Complete deep dive (all operations)
/deep-dive example.com

# Batch process multiple companies
/batch-process companies.csv all
```

### Using Python Modules Directly

```python
import asyncio
from src.enrichment import CompanyEnricher
from src.lookalike import LookalikeFinder
from src.subprocessors import SubprocessorDiscoverer
from src.notion import NotionClient
from src.utils import load_config

async def main():
    # Load configuration
    config = load_config()

    # Enrich a company
    enricher = CompanyEnricher(config)
    company_data = await enricher.enrich("example.com")
    print(f"Enriched: {company_data.name}")

    # Find lookalikes
    finder = LookalikeFinder()
    lookalikes = await finder.find_lookalikes("example.com", limit=10)
    print(f"Found {len(lookalikes)} lookalikes")

    # Discover subprocessors
    discoverer = SubprocessorDiscoverer()
    subprocessors = await discoverer.discover("example.com")
    print(f"Found {len(subprocessors)} subprocessors")

    # Sync to Notion
    notion = NotionClient(
        api_key=config["notion_api_key"],
        database_id=config["notion_database_id"]
    )
    page_id = await notion.sync_company(company_data.to_dict())
    print(f"Synced to Notion: {page_id}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Structure

```
blynt-customer-development/
├── claude.md                    # Project context for Claude Code
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore
│
├── config/
│   ├── .env.example            # Example environment configuration
│   └── .env                    # Your actual configuration (not in git)
│
├── src/
│   ├── enrichment/             # Company data enrichment
│   │   ├── __init__.py
│   │   └── enricher.py
│   │
│   ├── lookalike/              # Lookalike company discovery
│   │   ├── __init__.py
│   │   └── finder.py
│   │
│   ├── subprocessors/          # Vendor/subprocessor mapping
│   │   ├── __init__.py
│   │   └── discoverer.py
│   │
│   ├── notion/                 # Notion integration
│   │   ├── __init__.py
│   │   └── client.py
│   │
│   └── utils/                  # Shared utilities
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
│
├── .claude/
│   └── commands/               # Slash commands for Claude Code
│       ├── enrich-company.md
│       ├── find-lookalikes.md
│       ├── discover-subprocessors.md
│       ├── sync-to-notion.md
│       ├── deep-dive.md
│       └── batch-process.md
│
├── data/
│   ├── raw/                    # Raw input data
│   └── processed/              # Processed output data
│
└── logs/                       # Application logs
```

## Workflows

### 1. Single Company Analysis

```bash
# Complete analysis of one company
/deep-dive acme-corp.com
```

This will:
1. Enrich company data
2. Find 20 similar companies
3. Discover all subprocessors
4. Sync everything to Notion
5. Generate a summary report

### 2. Lookalike Campaign

```bash
# Find lookalikes for existing customers
/find-lookalikes customer1.com 50
/find-lookalikes customer2.com 50
/find-lookalikes customer3.com 50

# Batch enrich the results
/batch-process lookalikes.csv enrich
```

### 3. Vendor Mapping

```bash
# Map out vendor ecosystem
/discover-subprocessors target-company.com
/sync-to-notion target-company.com subprocessors
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_enrichment.py
```

### Code Quality

```bash
# Format code
black src/

# Lint
flake8 src/

# Type checking
mypy src/
```

## API Rate Limits

Be mindful of API rate limits:
- Notion: 3 requests/second
- Clearbit/Apollo: Varies by plan
- LinkedIn: Very restrictive

The project includes built-in rate limiting and retry logic.

## Data Storage

- **Raw data**: `data/raw/` - Unprocessed API responses
- **Processed data**: `data/processed/` - Cleaned and enriched data
- **Logs**: `logs/` - Application logs with daily rotation

## Troubleshooting

### Common Issues

**Import errors**: Make sure you've activated the virtual environment
```bash
source venv/bin/activate
```

**Notion API errors**: Verify your integration has access to the database

**Rate limit errors**: Add delays between requests or use batch processing

**Missing dependencies**: Reinstall requirements
```bash
pip install -r requirements.txt --force-reinstall
```

## Contributing

This is an internal tool for Blynt customer development. See claude.md for architecture details.

## License

Proprietary - Blynt Internal Use Only
