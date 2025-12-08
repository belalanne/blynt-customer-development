"""Tavily web search integration - direct API calls for token efficiency."""

import os
from typing import Any, Optional

import httpx


TAVILY_API_URL = "https://api.tavily.com"


async def tavily_search(
    query: str,
    search_depth: str = "basic",
    max_results: int = 10,
    include_domains: Optional[list[str]] = None,
    exclude_domains: Optional[list[str]] = None,
    include_answer: bool = True,
    include_raw_content: bool = False,
) -> dict[str, Any]:
    """Search the web using Tavily AI.

    Args:
        query: Search query
        search_depth: "basic" (faster) or "advanced" (more thorough)
        max_results: Number of results (default 10)
        include_domains: Only include results from these domains
        exclude_domains: Exclude results from these domains
        include_answer: Include AI-generated answer (default True)
        include_raw_content: Include raw page content (default False)

    Returns:
        Search results with URLs, titles, content snippets, and optional answer
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY not configured"}

    payload: dict[str, Any] = {
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

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TAVILY_API_URL}/search",
            json=payload,
            timeout=30.0,
        )

        if response.status_code != 200:
            return {"error": f"Tavily API error: {response.status_code}", "detail": response.text}

        return response.json()


async def tavily_extract(
    urls: list[str],
) -> dict[str, Any]:
    """Extract content from specific URLs using Tavily.

    Args:
        urls: List of URLs to extract content from

    Returns:
        Extracted content from each URL
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY not configured"}

    payload = {
        "api_key": api_key,
        "urls": urls,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TAVILY_API_URL}/extract",
            json=payload,
            timeout=60.0,
        )

        if response.status_code != 200:
            return {"error": f"Tavily API error: {response.status_code}", "detail": response.text}

        return response.json()


async def tavily_qna(
    query: str,
    search_depth: str = "advanced",
) -> dict[str, Any]:
    """Get a direct answer to a question using Tavily QnA.

    Optimized for AI agent tool use - returns a concise answer.

    Args:
        query: Question to answer
        search_depth: "basic" or "advanced" (default)

    Returns:
        Direct answer with sources
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY not configured"}

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "include_answer": True,
        "max_results": 5,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TAVILY_API_URL}/search",
            json=payload,
            timeout=30.0,
        )

        if response.status_code != 200:
            return {"error": f"Tavily API error: {response.status_code}", "detail": response.text}

        data = response.json()
        return {
            "answer": data.get("answer", ""),
            "sources": [
                {"title": r.get("title"), "url": r.get("url")}
                for r in data.get("results", [])[:5]
            ],
        }
