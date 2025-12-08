#!/usr/bin/env python3
"""Tavily Search - Standalone CLI tool for web search and content extraction.

Usage:
    # Search for companies
    python scripts/tavily_search.py search "voice AI company customer service"

    # Extract content from URLs
    python scripts/tavily_search.py extract "https://vapi.ai/about" "https://vapi.ai/pricing"

    # Advanced search with more results
    python scripts/tavily_search.py search "AI transcription" --depth advanced

Environment:
    TAVILY_API_KEY: Your Tavily API key (from .env or environment)
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

TAVILY_API_URL = "https://api.tavily.com"


def get_api_key() -> str:
    """Get Tavily API key from environment."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("Error: TAVILY_API_KEY not set. Add it to .env or export it.", file=sys.stderr)
        sys.exit(1)
    return api_key


def tavily_search(
    query: str,
    search_depth: str = "basic",
    max_results: int = 10,
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    include_answer: bool = True,
    include_raw_content: bool = False,
) -> dict:
    """Search the web using Tavily AI.

    Args:
        query: Search query
        search_depth: "basic" (faster) or "advanced" (more thorough)
        max_results: Number of results to return
        include_domains: Only include results from these domains
        exclude_domains: Exclude results from these domains
        include_answer: Include AI-generated answer
        include_raw_content: Include raw page content

    Returns:
        Search results dict with answer and results
    """
    api_key = get_api_key()

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "max_results": max_results,
        "include_answer": include_answer,
        "include_raw_content": include_raw_content,
    }

    if include_domains:
        payload["include_domains"] = include_domains
    if exclude_domains:
        payload["exclude_domains"] = exclude_domains

    with httpx.Client() as client:
        response = client.post(
            f"{TAVILY_API_URL}/search",
            json=payload,
            timeout=30.0,
        )

        if response.status_code != 200:
            return {"error": f"API error {response.status_code}", "detail": response.text}

        return response.json()


def tavily_extract(urls: list[str]) -> dict:
    """Extract content from specific URLs.

    Args:
        urls: List of URLs to extract content from

    Returns:
        Extracted content dict
    """
    api_key = get_api_key()

    payload = {
        "api_key": api_key,
        "urls": urls,
    }

    with httpx.Client() as client:
        response = client.post(
            f"{TAVILY_API_URL}/extract",
            json=payload,
            timeout=60.0,
        )

        if response.status_code != 200:
            return {"error": f"API error {response.status_code}", "detail": response.text}

        return response.json()


def format_search_results(data: dict, verbose: bool = False) -> str:
    """Format search results for display."""
    if "error" in data:
        return f"Error: {data['error']}\n{data.get('detail', '')}"

    lines = []

    # Show AI answer if available
    if data.get("answer"):
        lines.append("## AI Answer")
        lines.append(data["answer"])
        lines.append("")

    # Show response time
    if data.get("response_time"):
        lines.append(f"Response time: {data['response_time']:.2f}s")
        lines.append("")

    # Show results
    results = data.get("results", [])
    lines.append(f"## Results ({len(results)} found)")
    lines.append("")

    for i, result in enumerate(results, 1):
        score = result.get("score", 0)
        lines.append(f"{i}. [{score:.2f}] {result.get('title', 'No title')}")
        lines.append(f"   URL: {result.get('url', '')}")

        if verbose and result.get("content"):
            content = result["content"][:300].replace("\n", " ")
            lines.append(f"   Content: {content}...")

        lines.append("")

    return "\n".join(lines)


def format_extract_results(data: dict, verbose: bool = False) -> str:
    """Format extract results for display."""
    if "error" in data:
        return f"Error: {data['error']}\n{data.get('detail', '')}"

    lines = []

    # Show response time
    if data.get("response_time"):
        lines.append(f"Response time: {data['response_time']:.2f}s")
        lines.append("")

    # Show results
    results = data.get("results", [])
    failed = data.get("failed_results", [])

    lines.append(f"## Extracted Content ({len(results)} successful, {len(failed)} failed)")
    lines.append("")

    for result in results:
        lines.append(f"### {result.get('title', 'No title')}")
        lines.append(f"URL: {result.get('url', '')}")
        lines.append("")

        if result.get("raw_content"):
            content = result["raw_content"]
            if not verbose:
                content = content[:1000] + "..." if len(content) > 1000 else content
            lines.append(content)

        lines.append("")
        lines.append("---")
        lines.append("")

    if failed:
        lines.append("## Failed URLs")
        for url in failed:
            lines.append(f"- {url}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Tavily Search - AI-powered web search and content extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic search
    python scripts/tavily_search.py search "AI voice agent company"

    # Advanced search with more thorough results
    python scripts/tavily_search.py search "speech recognition API" --depth advanced

    # Extract content from specific pages
    python scripts/tavily_search.py extract "https://vapi.ai/about" "https://bland.ai/about"

    # Search with domain filter
    python scripts/tavily_search.py search "pricing" --include-domains vapi.ai bland.ai

    # Output as JSON
    python scripts/tavily_search.py search "voice AI" --json
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search the web")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--max-results", "-n", type=int, default=10, help="Number of results")
    search_parser.add_argument("--depth", "-d", choices=["basic", "advanced"], default="basic",
                               help="Search depth (advanced is slower but more thorough)")
    search_parser.add_argument("--include-domains", nargs="+", help="Only include these domains")
    search_parser.add_argument("--exclude-domains", nargs="+", help="Exclude these domains")
    search_parser.add_argument("--no-answer", action="store_true", help="Disable AI answer generation")
    search_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    search_parser.add_argument("--verbose", "-v", action="store_true", help="Show content previews")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract content from URLs")
    extract_parser.add_argument("urls", nargs="+", help="URLs to extract content from")
    extract_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    extract_parser.add_argument("--verbose", "-v", action="store_true", help="Show full content")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "search":
        result = tavily_search(
            query=args.query,
            search_depth=args.depth,
            max_results=args.max_results,
            include_domains=args.include_domains,
            exclude_domains=args.exclude_domains,
            include_answer=not args.no_answer,
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_search_results(result, verbose=args.verbose))

    elif args.command == "extract":
        result = tavily_extract(urls=args.urls)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_extract_results(result, verbose=args.verbose))


if __name__ == "__main__":
    main()
