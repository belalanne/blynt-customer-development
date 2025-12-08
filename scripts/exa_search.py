#!/usr/bin/env python3
"""Exa AI Search - Standalone CLI tool for web search and finding similar companies.

Usage:
    # Search for companies
    python scripts/exa_search.py search "voice AI company customer service"

    # Find similar companies
    python scripts/exa_search.py similar "https://vapi.ai"

    # Search with options
    python scripts/exa_search.py search "AI transcription" --num-results 5 --category company

Environment:
    EXA_API_KEY: Your Exa API key (from .env or environment)
"""

import argparse
import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

EXA_API_URL = "https://api.exa.ai"


def get_api_key() -> str:
    """Get Exa API key from environment."""
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        print("Error: EXA_API_KEY not set. Add it to .env or export it.", file=sys.stderr)
        sys.exit(1)
    return api_key


def exa_search(
    query: str,
    num_results: int = 10,
    use_autoprompt: bool = True,
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    category: str | None = None,
    include_text: bool = True,
) -> dict:
    """Search the web using Exa AI.

    Args:
        query: Search query
        num_results: Number of results to return
        use_autoprompt: Let Exa optimize the query
        include_domains: Only include results from these domains
        exclude_domains: Exclude results from these domains
        category: Filter by category (company, news, research_paper, etc.)
        include_text: Include page text content in results

    Returns:
        Search results dict
    """
    api_key = get_api_key()

    payload = {
        "query": query,
        "numResults": num_results,
        "useAutoprompt": use_autoprompt,
    }

    if include_domains:
        payload["includeDomains"] = include_domains
    if exclude_domains:
        payload["excludeDomains"] = exclude_domains
    if category:
        payload["category"] = category
    if include_text:
        payload["contents"] = {"text": {"maxCharacters": 2000}}

    with httpx.Client() as client:
        response = client.post(
            f"{EXA_API_URL}/search",
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

        if response.status_code != 200:
            return {"error": f"API error {response.status_code}", "detail": response.text}

        return response.json()


def exa_find_similar(
    url: str,
    num_results: int = 10,
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    include_text: bool = True,
) -> dict:
    """Find companies/pages similar to a given URL.

    Args:
        url: URL to find similar pages for
        num_results: Number of results to return
        include_domains: Only include results from these domains
        exclude_domains: Exclude results from these domains
        include_text: Include page text content in results

    Returns:
        Similar pages dict
    """
    api_key = get_api_key()

    payload = {
        "url": url,
        "numResults": num_results,
    }

    if include_domains:
        payload["includeDomains"] = include_domains
    if exclude_domains:
        payload["excludeDomains"] = exclude_domains
    if include_text:
        payload["contents"] = {"text": {"maxCharacters": 500}}

    with httpx.Client() as client:
        response = client.post(
            f"{EXA_API_URL}/findSimilar",
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

        if response.status_code != 200:
            return {"error": f"API error {response.status_code}", "detail": response.text}

        return response.json()


def format_results(data: dict, verbose: bool = False) -> str:
    """Format search results for display."""
    if "error" in data:
        return f"Error: {data['error']}\n{data.get('detail', '')}"

    lines = []
    results = data.get("results", [])

    lines.append(f"Found {len(results)} results")
    if "costDollars" in data:
        lines.append(f"Cost: ${data['costDollars'].get('total', 0):.4f}")
    lines.append("")

    for i, result in enumerate(results, 1):
        lines.append(f"{i}. {result.get('title', 'No title')}")
        lines.append(f"   URL: {result.get('url', '')}")

        if result.get("publishedDate"):
            lines.append(f"   Published: {result['publishedDate'][:10]}")

        if verbose and result.get("text"):
            text = result["text"][:200].replace("\n", " ")
            lines.append(f"   Preview: {text}...")

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Exa AI Search - Search the web and find similar companies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic search
    python scripts/exa_search.py search "AI voice agent company"

    # Find lookalike companies
    python scripts/exa_search.py similar "https://vapi.ai" --num-results 5

    # Search with category filter
    python scripts/exa_search.py search "transcription API" --category company

    # Output as JSON
    python scripts/exa_search.py search "speech recognition" --json
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search the web")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--num-results", "-n", type=int, default=10, help="Number of results")
    search_parser.add_argument("--category", "-c", help="Category filter (company, news, research_paper)")
    search_parser.add_argument("--include-domains", nargs="+", help="Only include these domains")
    search_parser.add_argument("--exclude-domains", nargs="+", help="Exclude these domains")
    search_parser.add_argument("--no-autoprompt", action="store_true", help="Disable query optimization")
    search_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    search_parser.add_argument("--verbose", "-v", action="store_true", help="Show text previews")

    # Similar command
    similar_parser = subparsers.add_parser("similar", help="Find similar companies/pages")
    similar_parser.add_argument("url", help="URL to find similar pages for")
    similar_parser.add_argument("--num-results", "-n", type=int, default=10, help="Number of results")
    similar_parser.add_argument("--include-domains", nargs="+", help="Only include these domains")
    similar_parser.add_argument("--exclude-domains", nargs="+", help="Exclude these domains")
    similar_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    similar_parser.add_argument("--verbose", "-v", action="store_true", help="Show text previews")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "search":
        result = exa_search(
            query=args.query,
            num_results=args.num_results,
            use_autoprompt=not args.no_autoprompt,
            include_domains=args.include_domains,
            exclude_domains=args.exclude_domains,
            category=args.category,
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_results(result, verbose=args.verbose))

    elif args.command == "similar":
        result = exa_find_similar(
            url=args.url,
            num_results=args.num_results,
            include_domains=args.include_domains,
            exclude_domains=args.exclude_domains,
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_results(result, verbose=args.verbose))


if __name__ == "__main__":
    main()
