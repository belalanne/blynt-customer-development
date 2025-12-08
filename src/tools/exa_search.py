"""Exa AI web search integration - direct API calls for token efficiency."""

import os
from typing import Any, Optional

from ..logging_config import get_logger
from ..utils import RetryConfig, http_request
from ..models import ExaSearchInput, ExaFindSimilarInput

logger = get_logger("tools.exa")

EXA_API_URL = "https://api.exa.ai"

# Retry config for Exa API
EXA_RETRY_CONFIG = RetryConfig(
    max_retries=3,
    base_delay=1.0,
    max_delay=15.0,
    retryable_status_codes=(429, 500, 502, 503, 504),
)


async def exa_search(
    query: str,
    num_results: int = 10,
    use_autoprompt: bool = True,
    include_domains: Optional[list[str]] = None,
    exclude_domains: Optional[list[str]] = None,
    start_published_date: Optional[str] = None,
    category: Optional[str] = None,
    contents: bool = True,
) -> dict[str, Any]:
    """Search the web using Exa AI.

    Args:
        query: Search query
        num_results: Number of results (default 10)
        use_autoprompt: Let Exa optimize the query (default True)
        include_domains: Only include results from these domains
        exclude_domains: Exclude results from these domains
        start_published_date: Filter by publish date (ISO format)
        category: Filter by category (company, research_paper, news, etc.)
        contents: Include page contents in results

    Returns:
        Search results with URLs, titles, and optionally content
    """
    # Validate input
    try:
        validated = ExaSearchInput(
            query=query,
            num_results=num_results,
            use_autoprompt=use_autoprompt,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            start_published_date=start_published_date,
            category=category,
            contents=contents,
        )
    except ValueError as e:
        logger.warning(f"Invalid input for exa_search: {e}")
        return {"error": f"Invalid input: {e}"}

    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        logger.error("EXA_API_KEY not configured")
        return {"error": "EXA_API_KEY not configured"}

    logger.info(f"Exa search: '{validated.query[:50]}...' ({validated.num_results} results)")

    payload: dict[str, Any] = {
        "query": validated.query,
        "numResults": validated.num_results,
        "useAutoprompt": validated.use_autoprompt,
    }

    if validated.include_domains:
        payload["includeDomains"] = validated.include_domains
    if validated.exclude_domains:
        payload["excludeDomains"] = validated.exclude_domains
    if validated.start_published_date:
        payload["startPublishedDate"] = validated.start_published_date
    if validated.category:
        payload["category"] = validated.category

    # Request contents if needed
    if validated.contents:
        payload["contents"] = {"text": {"maxCharacters": 2000}}

    result = await http_request(
        method="POST",
        url=f"{EXA_API_URL}/search",
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30.0,
        retry_config=EXA_RETRY_CONFIG,
    )

    if "error" in result:
        logger.error(f"Exa search failed: {result['error']}")
        return {"error": result["error"], "detail": result.get("data")}

    data = result["data"]
    num_found = len(data.get("results", []))
    logger.info(f"Exa search returned {num_found} results")

    return data


async def exa_find_similar(
    url: str,
    num_results: int = 10,
    include_domains: Optional[list[str]] = None,
    exclude_domains: Optional[list[str]] = None,
    contents: bool = True,
) -> dict[str, Any]:
    """Find companies/pages similar to a given URL.

    Args:
        url: URL to find similar pages for
        num_results: Number of results (default 10)
        include_domains: Only include results from these domains
        exclude_domains: Exclude results from these domains
        contents: Include page contents in results

    Returns:
        Similar pages with URLs, titles, and optionally content
    """
    # Validate input
    try:
        validated = ExaFindSimilarInput(
            url=url,
            num_results=num_results,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            contents=contents,
        )
    except ValueError as e:
        logger.warning(f"Invalid input for exa_find_similar: {e}")
        return {"error": f"Invalid input: {e}"}

    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        logger.error("EXA_API_KEY not configured")
        return {"error": "EXA_API_KEY not configured"}

    logger.info(f"Exa find similar: {validated.url} ({validated.num_results} results)")

    payload: dict[str, Any] = {
        "url": validated.url,
        "numResults": validated.num_results,
    }

    if validated.include_domains:
        payload["includeDomains"] = validated.include_domains
    if validated.exclude_domains:
        payload["excludeDomains"] = validated.exclude_domains

    if validated.contents:
        payload["contents"] = {"text": {"maxCharacters": 2000}}

    result = await http_request(
        method="POST",
        url=f"{EXA_API_URL}/findSimilar",
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30.0,
        retry_config=EXA_RETRY_CONFIG,
    )

    if "error" in result:
        logger.error(f"Exa find similar failed: {result['error']}")
        return {"error": result["error"], "detail": result.get("data")}

    data = result["data"]
    num_found = len(data.get("results", []))
    logger.info(f"Exa find similar returned {num_found} results")

    return data
