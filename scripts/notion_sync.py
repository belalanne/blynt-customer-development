#!/usr/bin/env python3
"""Notion Sync - Standalone CLI tool for saving companies to Notion.

Usage:
    # Save a company
    python scripts/notion_sync.py save "Olivya" "olivya.io" --icp 3 --vertical "AI Voice Agents"

    # Check if company exists
    python scripts/notion_sync.py check "olivya.io"

    # Search for companies
    python scripts/notion_sync.py search "voice"

Environment:
    NOTION_API_KEY: Your Notion API key (from .env or environment)
    NOTION_DATABASE_ID: Target database ID (from .env or environment)
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def get_config() -> tuple[str, str]:
    """Get Notion API key and database ID from environment."""
    api_key = os.getenv("NOTION_API_KEY")
    db_id = os.getenv("NOTION_DATABASE_ID")

    if not api_key:
        print("Error: NOTION_API_KEY not set. Add it to .env or export it.", file=sys.stderr)
        sys.exit(1)
    if not db_id:
        print("Error: NOTION_DATABASE_ID not set. Add it to .env or export it.", file=sys.stderr)
        sys.exit(1)

    return api_key, db_id


def get_headers() -> dict[str, str]:
    """Get Notion API headers."""
    api_key, _ = get_config()
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def normalize_domain(url: str) -> str:
    """Extract and normalize domain from URL."""
    if not url:
        return ""

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain.lower().rstrip('/')
    except Exception:
        return url.lower()


def notion_find_by_website(website: str) -> dict | None:
    """Find a company by website URL.

    Args:
        website: Website URL to search for

    Returns:
        Page data if found, None otherwise
    """
    _, db_id = get_config()
    domain = normalize_domain(website)

    # Try multiple URL variations
    variations = [
        f"https://{domain}",
        f"https://www.{domain}",
        domain,
    ]

    with httpx.Client() as client:
        for url_variant in variations:
            payload = {
                "filter": {
                    "property": "Website",
                    "url": {"equals": url_variant},
                }
            }

            response = client.post(
                f"{NOTION_API_URL}/databases/{db_id}/query",
                json=payload,
                headers=get_headers(),
                timeout=30.0,
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    return results[0]

        # Fallback: contains search
        payload = {
            "filter": {
                "property": "Website",
                "url": {"contains": domain},
            }
        }

        response = client.post(
            f"{NOTION_API_URL}/databases/{db_id}/query",
            json=payload,
            headers=get_headers(),
            timeout=30.0,
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                return results[0]

    return None


def notion_save_company(
    company_name: str,
    website: str,
    linkedin_url: str | None = None,
    vertical: str | None = None,
    icp: str | None = None,
    product_description: str | None = None,
    asr_providers: list[str] | None = None,
    ai_ml_engineers: int | None = None,
    country: str | None = None,
    skip_duplicate_check: bool = False,
) -> dict:
    """Save a company to Notion database.

    Args:
        company_name: Company name
        website: Company website URL
        linkedin_url: LinkedIn company page
        vertical: Industry/sector
        icp: ICP classification (1, 2, 3, 4, N/A)
        product_description: Short description (5 words)
        asr_providers: List of ASR providers
        ai_ml_engineers: Number of AI/ML engineers
        country: HQ country
        skip_duplicate_check: Skip checking for existing company

    Returns:
        Result dict with action and page data
    """
    _, db_id = get_config()

    # Check for duplicates unless skipped
    if not skip_duplicate_check:
        existing = notion_find_by_website(website)
        if existing:
            page_id = existing.get("id", "")
            page_url = f"https://www.notion.so/{page_id.replace('-', '')}"
            return {
                "action": "exists",
                "page_id": page_id,
                "page_url": page_url,
                "message": f"Company already exists at {page_url}",
            }

    # Build properties
    properties = {
        "Company_Name": {"title": [{"text": {"content": company_name}}]},
        "Website": {"url": f"https://{normalize_domain(website)}"},
    }

    if linkedin_url:
        properties["Linkedin Link"] = {"url": linkedin_url}
    if vertical:
        properties["Vertical"] = {"select": {"name": vertical}}
    if icp:
        properties["ICP"] = {"select": {"name": icp}}
    if product_description:
        properties["Product description"] = {"rich_text": [{"text": {"content": product_description}}]}
    if asr_providers:
        properties["ASR provider"] = {"multi_select": [{"name": p} for p in asr_providers]}
    if ai_ml_engineers is not None:
        properties["Nbr of AI/ML/Speech engineer"] = {"number": ai_ml_engineers}
    if country:
        properties["Main Office Country"] = {"rich_text": [{"text": {"content": country}}]}

    payload = {
        "parent": {"database_id": db_id},
        "properties": properties,
    }

    with httpx.Client() as client:
        response = client.post(
            f"{NOTION_API_URL}/pages",
            json=payload,
            headers=get_headers(),
            timeout=30.0,
        )

        if response.status_code not in (200, 201):
            return {
                "action": "error",
                "message": f"API error {response.status_code}",
                "detail": response.text,
            }

        data = response.json()
        page_id = data.get("id", "")
        page_url = f"https://www.notion.so/{page_id.replace('-', '')}"

        return {
            "action": "created",
            "page_id": page_id,
            "page_url": page_url,
            "message": f"Company '{company_name}' created at {page_url}",
        }


def notion_search(query: str) -> dict:
    """Search for companies in Notion.

    Args:
        query: Search query

    Returns:
        Search results
    """
    _, db_id = get_config()

    payload = {}
    if query:
        payload["filter"] = {
            "or": [
                {"property": "Company_Name", "title": {"contains": query}},
                {"property": "Website", "url": {"contains": query}},
            ]
        }

    with httpx.Client() as client:
        response = client.post(
            f"{NOTION_API_URL}/databases/{db_id}/query",
            json=payload,
            headers=get_headers(),
            timeout=30.0,
        )

        if response.status_code != 200:
            return {"error": f"API error {response.status_code}", "detail": response.text}

        return response.json()


def format_page(page: dict) -> str:
    """Format a Notion page for display."""
    props = page.get("properties", {})

    # Extract company name
    name = ""
    try:
        name = props.get("Company_Name", {}).get("title", [{}])[0].get("text", {}).get("content", "")
    except (IndexError, KeyError):
        pass

    # Extract website
    website = props.get("Website", {}).get("url", "")

    # Extract ICP
    icp = props.get("ICP", {}).get("select", {})
    icp_value = icp.get("name", "") if icp else ""

    # Extract vertical
    vertical = props.get("Vertical", {}).get("select", {})
    vertical_value = vertical.get("name", "") if vertical else ""

    page_id = page.get("id", "")
    page_url = f"https://www.notion.so/{page_id.replace('-', '')}"

    return f"- {name} | {website} | ICP: {icp_value} | {vertical_value}\n  {page_url}"


def main():
    parser = argparse.ArgumentParser(
        description="Notion Sync - Save and manage companies in Notion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Save a new company
    python scripts/notion_sync.py save "Olivya" "olivya.io" --icp 3 --vertical "AI Voice Agents"

    # Check if company exists
    python scripts/notion_sync.py check "olivya.io"

    # Search for companies
    python scripts/notion_sync.py search "voice"

    # Save with full details
    python scripts/notion_sync.py save "Vapi" "vapi.ai" \\
        --icp 3 \\
        --vertical "Voice AI Platform" \\
        --linkedin "https://linkedin.com/company/vapi-ai" \\
        --description "Voice AI development platform" \\
        --country "USA" \\
        --asr Deepgram "Assembly AI"
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Save command
    save_parser = subparsers.add_parser("save", help="Save a company to Notion")
    save_parser.add_argument("name", help="Company name")
    save_parser.add_argument("website", help="Company website")
    save_parser.add_argument("--linkedin", help="LinkedIn company URL")
    save_parser.add_argument("--vertical", help="Industry/sector")
    save_parser.add_argument("--icp", choices=["1", "2", "3", "4", "N/A"], help="ICP classification")
    save_parser.add_argument("--description", help="Short product description (5 words)")
    save_parser.add_argument("--asr", nargs="+", help="ASR providers used")
    save_parser.add_argument("--engineers", type=int, help="Number of AI/ML/Speech engineers")
    save_parser.add_argument("--country", help="HQ country")
    save_parser.add_argument("--force", action="store_true", help="Skip duplicate check")
    save_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Check command
    check_parser = subparsers.add_parser("check", help="Check if company exists")
    check_parser.add_argument("website", help="Company website to check")
    check_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for companies")
    search_parser.add_argument("query", nargs="?", default="", help="Search query (optional)")
    search_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "save":
        result = notion_save_company(
            company_name=args.name,
            website=args.website,
            linkedin_url=args.linkedin,
            vertical=args.vertical,
            icp=args.icp,
            product_description=args.description,
            asr_providers=args.asr,
            ai_ml_engineers=args.engineers,
            country=args.country,
            skip_duplicate_check=args.force,
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Action: {result['action']}")
            print(result['message'])

    elif args.command == "check":
        existing = notion_find_by_website(args.website)

        if args.json:
            print(json.dumps(existing, indent=2) if existing else "null")
        else:
            if existing:
                print(f"Found: {format_page(existing)}")
            else:
                print(f"Not found: {args.website}")

    elif args.command == "search":
        result = notion_search(args.query)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                results = result.get("results", [])
                print(f"Found {len(results)} companies\n")
                for page in results:
                    print(format_page(page))


if __name__ == "__main__":
    main()
