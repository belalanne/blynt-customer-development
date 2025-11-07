#!/usr/bin/env python3
"""
Direct Notion sync script - Run on your laptop with local .env file
Usage: python scripts/quick_sync_to_notion.py livekit.io
"""
import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from notion_client import AsyncClient
except ImportError:
    print("❌ notion-client not installed")
    print("Run: pip install notion-client")
    sys.exit(1)

# Load .env if available
env_file = Path(__file__).parent.parent / "config" / ".env"
if env_file.exists():
    print(f"✅ Loading {env_file}")
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

# Configuration
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "2861bdff7e998000a14edb0bf56a75bf")
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
COMPANY = sys.argv[1] if len(sys.argv) > 1 else "livekit.io"

# Company data mapping (extracted from deep dive analyses)
COMPANY_DATA = {
    "livekit.io": {
        "Company_Name": "LiveKit",
        "Website": "https://livekit.io",
        "Linkedin Link": "https://www.linkedin.com/company/livekitco",
        "Status / Engagement": "Ice Box",
        "Vertical": "Infrastructure",
        "ICP": "3",
        "Product description": "Open-source WebRTC infrastructure for real-time voice-video-AI",
        "ASR provider": ["Deepgram", "AssemblyAI", "Speechmatics", "Azure Speech", "Google STT"],
        "Nbr of AI/ML/Speech engineer": 18,
        "Main Office Country": "United States",
        "Employee Count": 37,
        "Funding Raised": "$83M",
        "Funding Stage": "Series B",
        "Valuation": "$345M",
    },
    "100ms.live": {
        "Company_Name": "100ms",
        "Website": "https://www.100ms.live",
        "Linkedin Link": "https://www.linkedin.com/company/100mslive",
        "Status / Engagement": "Ice Box",
        "Vertical": "Infrastructure",
        "ICP": "3",
        "Product description": "Live video API infrastructure for developers",
        "ASR provider": ["None"],  # No AI/speech partnerships identified
        "Nbr of AI/ML/Speech engineer": 5,
        "Main Office Country": "United States",
        "Employee Count": 31,
        "Funding Raised": "$24.5M",
        "Funding Stage": "Series A",
        "Valuation": "Not disclosed",
    },
    "daily.co": {
        "Company_Name": "Daily",
        "Website": "https://www.daily.co",
        "Linkedin Link": "https://www.linkedin.com/company/daily-co",
        "Status / Engagement": "Ice Box",
        "Vertical": "Infrastructure",
        "ICP": "3",
        "Product description": "WebRTC platform with Pipecat voice AI framework",
        "ASR provider": ["Deepgram", "AssemblyAI", "OpenAI Whisper", "Google STT", "Azure Speech"],
        "Nbr of AI/ML/Speech engineer": 22,
        "Main Office Country": "United States",
        "Employee Count": 116,
        "Funding Raised": "$62.2M",
        "Funding Stage": "Series B",
        "Valuation": "Not disclosed",
    },
}

async def sync_to_notion():
    """Sync company data to Notion database."""
    if not NOTION_API_KEY:
        print("❌ NOTION_API_KEY not set")
        print("\nPlease set it in config/.env or export it:")
        print("export NOTION_API_KEY='secret_your_key_here'")
        sys.exit(1)

    if COMPANY not in COMPANY_DATA:
        print(f"❌ Unknown company: {COMPANY}")
        print(f"Available: {', '.join(COMPANY_DATA.keys())}")
        sys.exit(1)

    data = COMPANY_DATA[COMPANY]
    client = AsyncClient(auth=NOTION_API_KEY)

    print(f"\n{'='*60}")
    print(f"  Syncing {data['Company_Name']} to Notion")
    print(f"{'='*60}\n")

    # Step 1: Search for existing page
    print(f"🔍 Searching for existing page by URL: {data['Website']}")
    try:
        query = await client.databases.query(
            database_id=DATABASE_ID,
            filter={
                "property": "Website",
                "url": {"equals": data["Website"]}
            }
        )
    except Exception as e:
        print(f"❌ Error querying database: {e}")
        print("\nTroubleshooting:")
        print("1. Check NOTION_API_KEY is correct")
        print("2. Check integration has access to the database")
        print("3. Go to Notion DB → ... → Add connections → Select your integration")
        sys.exit(1)

    # Step 2: Prepare properties
    properties = {
        "Company_Name": {"title": [{"text": {"content": data["Company_Name"]}}]},
        "Website": {"url": data["Website"]},
        "Linkedin Link": {"url": data["Linkedin Link"]},
        "Status / Engagement": {"select": {"name": data["Status / Engagement"]}},
        "Vertical": {"select": {"name": data["Vertical"]}},
        "ICP": {"select": {"name": data["ICP"]}},
        "Product description": {"rich_text": [{"text": {"content": data["Product description"]}}]},
        "ASR provider": {"multi_select": [{"name": name} for name in data["ASR provider"]]},
        "Nbr of AI/ML/Speech engineer": {"number": data["Nbr of AI/ML/Speech engineer"]},
        "Main Office Country": {"rich_text": [{"text": {"content": data["Main Office Country"]}}]},
    }

    # Step 3: Create or update page
    if query["results"]:
        page_id = query["results"][0]["id"]
        print(f"✅ Found existing page")
        print(f"   Page ID: {page_id}")

        try:
            response = await client.pages.update(
                page_id=page_id,
                properties=properties
            )
            print(f"✅ Updated page properties")
        except Exception as e:
            print(f"❌ Error updating page: {e}")
            sys.exit(1)
    else:
        print(f"📝 No existing page found, creating new...")

        try:
            response = await client.pages.create(
                parent={"database_id": DATABASE_ID},
                properties=properties
            )
            page_id = response["id"]
            print(f"✅ Created new page")
            print(f"   Page ID: {page_id}")
        except Exception as e:
            print(f"❌ Error creating page: {e}")
            print("\nTroubleshooting:")
            print("1. Check database schema matches expected properties")
            print("2. Check 'Vertical' and 'ICP' values exist as options")
            sys.exit(1)

    # Step 4: Add content reference
    report_path = f"logs/deep-dive-{COMPANY}-2025-11-06.md"
    try:
        await client.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{"type": "text", "text": {"content": f"📊 Full research report: {report_path}"}}],
                        "icon": {"emoji": "📊"}
                    }
                }
            ]
        )
        print(f"✅ Added report reference")
    except Exception as e:
        print(f"⚠️  Could not add content block: {e}")

    # Success!
    page_url = f"https://notion.so/{page_id.replace('-', '')}"
    print(f"\n{'='*60}")
    print(f"✅ SUCCESS! {data['Company_Name']} synced to Notion")
    print(f"{'='*60}")
    print(f"\n🔗 Notion Page: {page_url}")
    print(f"\n📊 Properties Updated:")
    print(f"   • Company: {data['Company_Name']}")
    print(f"   • Website: {data['Website']}")
    print(f"   • ICP: {data['ICP']}")
    print(f"   • ASR Providers: {', '.join(data['ASR provider'])}")
    print(f"   • Engineers: {data['Nbr of AI/ML/Speech engineer']}")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/quick_sync_to_notion.py <company>")
        print("\nAvailable companies:")
        for company in COMPANY_DATA.keys():
            print(f"  - {company}")
        print("\nExample:")
        print("  python scripts/quick_sync_to_notion.py livekit.io")
        sys.exit(1)

    asyncio.run(sync_to_notion())
