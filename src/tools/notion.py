"""Notion database integration - direct API calls for token efficiency."""

import os
import re
from typing import Any, Optional
from urllib.parse import urlparse

import httpx

from ..logging_config import get_logger
from ..utils import RetryConfig, http_request

logger = get_logger("tools.notion")

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

# Retry config for Notion API
NOTION_RETRY_CONFIG = RetryConfig(
    max_retries=3,
    base_delay=1.0,
    max_delay=15.0,
    retryable_status_codes=(429, 500, 502, 503, 504),
)


def _normalize_domain(url: str) -> str:
    """Extract and normalize domain from URL for comparison.

    Examples:
        https://www.volubile.ai -> volubile.ai
        volubile.ai -> volubile.ai
        http://spitch.ai/ -> spitch.ai
    """
    if not url:
        return ""

    # Add scheme if missing for proper parsing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]

        # Remove www. prefix
        if domain.startswith('www.'):
            domain = domain[4:]

        # Remove trailing slashes and lowercase
        return domain.lower().rstrip('/')
    except Exception:
        # Fallback: simple regex extraction
        match = re.search(r'(?:https?://)?(?:www\.)?([^/]+)', url.lower())
        return match.group(1) if match else url.lower()


def _get_url_variations(domain: str) -> list[str]:
    """Generate URL variations to search for.

    Args:
        domain: Normalized domain (e.g., volubile.ai)

    Returns:
        List of URL variations to check
    """
    return [
        f"https://{domain}",
        f"https://www.{domain}",
        f"http://{domain}",
        f"http://www.{domain}",
        domain,
        f"www.{domain}",
        f"https://{domain}/",
        f"https://www.{domain}/",
    ]


def _get_headers() -> dict[str, str]:
    """Get Notion API headers."""
    api_key = os.getenv("NOTION_API_KEY")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


async def notion_search(
    query: str,
    database_id: Optional[str] = None,
    filter_property: Optional[str] = None,
    filter_value: Optional[str] = None,
) -> dict[str, Any]:
    """Search Notion for pages matching a query.

    Args:
        query: Search query
        database_id: Limit search to a specific database (optional)
        filter_property: Property name to filter by (optional)
        filter_value: Value to filter for (optional)

    Returns:
        Matching pages with their properties
    """
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        logger.error("NOTION_API_KEY not configured")
        return {"error": "NOTION_API_KEY not configured"}

    logger.info(f"Notion search: '{query}'")

    db_id = database_id or os.getenv("NOTION_DATABASE_ID")

    # If we have a database ID, query that database
    if db_id:
        payload: dict[str, Any] = {}

        # Add text filter if query provided
        if query and filter_property:
            payload["filter"] = {
                "property": filter_property,
                "rich_text": {"contains": query},
            }
        elif filter_property and filter_value:
            payload["filter"] = {
                "property": filter_property,
                "rich_text": {"equals": filter_value},
            }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{NOTION_API_URL}/databases/{db_id}/query",
                json=payload,
                headers=_get_headers(),
                timeout=30.0,
            )

            if response.status_code != 200:
                return {"error": f"Notion API error: {response.status_code}", "detail": response.text}

            return response.json()

    # Otherwise, do a global search
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{NOTION_API_URL}/search",
            json={"query": query},
            headers=_get_headers(),
            timeout=30.0,
        )

        if response.status_code != 200:
            return {"error": f"Notion API error: {response.status_code}", "detail": response.text}

        return response.json()


async def notion_save_company(
    company_name: str,
    website: str,
    linkedin_url: Optional[str] = None,
    vertical: Optional[str] = None,
    icp: Optional[str] = None,
    product_description: Optional[str] = None,
    asr_providers: Optional[list[str]] = None,
    ai_ml_engineers: Optional[int] = None,
    country: Optional[str] = None,
    database_id: Optional[str] = None,
) -> dict[str, Any]:
    """Save a company to Notion database.

    Args:
        company_name: Company name (title)
        website: Company website URL (unique identifier)
        linkedin_url: LinkedIn company page URL
        vertical: Industry/sector
        icp: ICP classification ("1", "2", "3", "4", "N/A")
        product_description: Short product description (5 words)
        asr_providers: List of ASR providers used
        ai_ml_engineers: Number of AI/ML/Speech engineers
        country: Main office country
        database_id: Override default database ID

    Returns:
        Created page data
    """
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        logger.error("NOTION_API_KEY not configured")
        return {"error": "NOTION_API_KEY not configured"}

    db_id = database_id or os.getenv("NOTION_DATABASE_ID")
    if not db_id:
        logger.error("NOTION_DATABASE_ID not configured")
        return {"error": "NOTION_DATABASE_ID not configured"}

    logger.info(f"Saving company to Notion: {company_name} ({website})")

    # Build properties matching Blynt's Notion schema
    properties: dict[str, Any] = {
        "Company_Name": {"title": [{"text": {"content": company_name}}]},
        "Website": {"url": website},
    }

    if linkedin_url:
        properties["Linkedin Link"] = {"url": linkedin_url}

    if vertical:
        properties["Vertical"] = {"select": {"name": vertical}}

    if icp:
        properties["ICP"] = {"select": {"name": icp}}

    if product_description:
        properties["Product description"] = {
            "rich_text": [{"text": {"content": product_description}}]
        }

    if asr_providers:
        properties["ASR provider"] = {
            "multi_select": [{"name": provider} for provider in asr_providers]
        }

    if ai_ml_engineers is not None:
        properties["Nbr of AI/ML/Speech engineer"] = {"number": ai_ml_engineers}

    if country:
        properties["Main Office Country"] = {
            "rich_text": [{"text": {"content": country}}]
        }

    payload = {
        "parent": {"database_id": db_id},
        "properties": properties,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{NOTION_API_URL}/pages",
            json=payload,
            headers=_get_headers(),
            timeout=30.0,
        )

        if response.status_code not in (200, 201):
            return {"error": f"Notion API error: {response.status_code}", "detail": response.text}

        return response.json()


async def notion_update_company(
    page_id: str,
    updates: dict[str, Any],
) -> dict[str, Any]:
    """Update an existing company page in Notion.

    Args:
        page_id: Notion page ID to update
        updates: Dictionary of property updates

    Returns:
        Updated page data
    """
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        return {"error": "NOTION_API_KEY not configured"}

    # Convert updates to Notion property format
    properties: dict[str, Any] = {}

    for key, value in updates.items():
        if key == "company_name":
            properties["Company_Name"] = {"title": [{"text": {"content": value}}]}
        elif key == "website":
            properties["Website"] = {"url": value}
        elif key == "linkedin_url":
            properties["Linkedin Link"] = {"url": value}
        elif key == "vertical":
            properties["Vertical"] = {"select": {"name": value}}
        elif key == "icp":
            properties["ICP"] = {"select": {"name": value}}
        elif key == "product_description":
            properties["Product description"] = {
                "rich_text": [{"text": {"content": value}}]
            }
        elif key == "asr_providers":
            properties["ASR provider"] = {
                "multi_select": [{"name": p} for p in value]
            }
        elif key == "ai_ml_engineers":
            properties["Nbr of AI/ML/Speech engineer"] = {"number": value}
        elif key == "country":
            properties["Main Office Country"] = {
                "rich_text": [{"text": {"content": value}}]
            }

    payload = {"properties": properties}

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{NOTION_API_URL}/pages/{page_id}",
            json=payload,
            headers=_get_headers(),
            timeout=30.0,
        )

        if response.status_code != 200:
            return {"error": f"Notion API error: {response.status_code}", "detail": response.text}

        return response.json()


async def notion_find_by_website(
    website: str,
    database_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """Find a company by website URL (for duplicate checking).

    Uses domain normalization to match URLs regardless of format:
    - https://www.example.com == example.com == http://example.com/

    Args:
        website: Website URL to search for
        database_id: Database to search in

    Returns:
        Page data if found, None otherwise
    """
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        logger.error("NOTION_API_KEY not configured")
        return None

    db_id = database_id or os.getenv("NOTION_DATABASE_ID")
    if not db_id:
        logger.error("NOTION_DATABASE_ID not configured")
        return None

    # Normalize input domain
    normalized_domain = _normalize_domain(website)
    if not normalized_domain:
        logger.warning(f"Could not normalize domain: {website}")
        return None

    logger.debug(f"Checking for duplicate: {normalized_domain}")

    # Try multiple URL variations
    url_variations = _get_url_variations(normalized_domain)

    async with httpx.AsyncClient() as client:
        for url_variant in url_variations:
            payload = {
                "filter": {
                    "property": "Website",
                    "url": {"equals": url_variant},
                }
            }

            response = await client.post(
                f"{NOTION_API_URL}/databases/{db_id}/query",
                json=payload,
                headers=_get_headers(),
                timeout=30.0,
            )

            if response.status_code != 200:
                continue

            data = response.json()
            results = data.get("results", [])

            if results:
                logger.info(f"Found existing company by URL variation: {url_variant}")
                return results[0]

        # Also try "contains" search as fallback
        logger.debug(f"Trying 'contains' fallback search for: {normalized_domain}")
        payload = {
            "filter": {
                "property": "Website",
                "url": {"contains": normalized_domain},
            }
        }

        response = await client.post(
            f"{NOTION_API_URL}/databases/{db_id}/query",
            json=payload,
            headers=_get_headers(),
            timeout=30.0,
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                logger.info(f"Found existing company by contains search: {normalized_domain}")
                return results[0]

        logger.debug(f"No existing company found for: {normalized_domain}")
        return None


async def notion_save_company_if_not_exists(
    company_name: str,
    website: str,
    linkedin_url: Optional[str] = None,
    vertical: Optional[str] = None,
    icp: Optional[str] = None,
    product_description: Optional[str] = None,
    asr_providers: Optional[list[str]] = None,
    ai_ml_engineers: Optional[int] = None,
    country: Optional[str] = None,
    status: Optional[str] = None,
    database_id: Optional[str] = None,
) -> dict[str, Any]:
    """Save a company to Notion only if it doesn't already exist.

    Checks for existing company by domain before creating.

    Args:
        company_name: Company name (title)
        website: Company website URL (unique identifier)
        linkedin_url: LinkedIn company page URL
        vertical: Industry/sector
        icp: ICP classification ("1", "2", "3", "4", "N/A")
        product_description: Short product description
        asr_providers: List of ASR providers used
        ai_ml_engineers: Number of AI/ML/Speech engineers
        country: Main office country
        status: Status/Engagement value
        database_id: Override default database ID

    Returns:
        Dict with 'action' ('created', 'exists', 'error'), 'page' data, and 'message'
    """
    logger.info(f"Attempting to save company: {company_name} ({website})")

    # Check if company already exists
    existing = await notion_find_by_website(website, database_id)

    if existing:
        logger.info(f"Company already exists: {company_name}")
        # Extract existing page info
        existing_id = existing.get("id", "")
        existing_url = f"https://www.notion.so/{existing_id.replace('-', '')}"
        existing_name = ""
        try:
            title_prop = existing.get("properties", {}).get("Company_Name", {})
            title_content = title_prop.get("title", [])
            if title_content:
                existing_name = title_content[0].get("text", {}).get("content", "")
        except Exception:
            pass

        return {
            "action": "exists",
            "page": existing,
            "page_id": existing_id,
            "page_url": existing_url,
            "message": f"Company '{existing_name or company_name}' already exists at {existing_url}",
        }

    # Create new company
    result = await notion_save_company(
        company_name=company_name,
        website=website,
        linkedin_url=linkedin_url,
        vertical=vertical,
        icp=icp,
        product_description=product_description,
        asr_providers=asr_providers,
        ai_ml_engineers=ai_ml_engineers,
        country=country,
        database_id=database_id,
    )

    if "error" in result:
        return {
            "action": "error",
            "page": None,
            "message": result.get("error"),
            "detail": result.get("detail"),
        }

    page_id = result.get("id", "")
    page_url = f"https://www.notion.so/{page_id.replace('-', '')}"

    return {
        "action": "created",
        "page": result,
        "page_id": page_id,
        "page_url": page_url,
        "message": f"Company '{company_name}' created at {page_url}",
    }
