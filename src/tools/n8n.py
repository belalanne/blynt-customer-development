"""n8n workflow integration - trigger workflows via webhooks."""

import os
from typing import Any, Optional

import httpx

from ..logging_config import get_logger
from ..utils import RetryConfig, http_request
from ..models import N8nEnrichCompanyInput, N8nEnrichPersonInput, N8nTriggerWorkflowInput

logger = get_logger("tools.n8n")

# Retry config for n8n webhooks (longer timeout, more retries)
N8N_RETRY_CONFIG = RetryConfig(
    max_retries=3,
    base_delay=2.0,
    max_delay=30.0,
    retryable_status_codes=(429, 500, 502, 503, 504),
)


async def _call_webhook(
    url: str,
    data: dict[str, Any],
    timeout: int = 60,
) -> dict[str, Any]:
    """Internal helper to call n8n webhook with retry logic.

    Args:
        url: Webhook URL
        data: Data payload to send
        timeout: Request timeout in seconds

    Returns:
        Workflow response or error
    """
    logger.info(f"Calling n8n webhook: {url[:50]}...")
    logger.debug(f"Webhook payload: {data}")

    result = await http_request(
        method="POST",
        url=url,
        json=data,
        timeout=float(timeout),
        retry_config=N8N_RETRY_CONFIG,
    )

    if "error" in result:
        logger.error(f"n8n webhook failed: {result['error']}")
        return {"error": result["error"], "detail": result.get("data")}

    logger.info(f"n8n webhook succeeded (status {result['status_code']})")
    return result["data"]


async def n8n_enrich_company(
    domain: str,
    company_name: Optional[str] = None,
) -> dict[str, Any]:
    """Enrich company data via n8n workflow.

    Uses N8N_WEBHOOK_COMPANY environment variable.

    Args:
        domain: Company domain to enrich (e.g., "vapi.ai")
        company_name: Optional company name if known

    Returns:
        Enriched company data (firmographics, funding, contacts, etc.)
    """
    # Validate input
    try:
        validated = N8nEnrichCompanyInput(domain=domain, company_name=company_name)
    except ValueError as e:
        logger.warning(f"Invalid input for n8n_enrich_company: {e}")
        return {"error": f"Invalid input: {e}"}

    url = os.getenv("N8N_WEBHOOK_COMPANY")
    if not url:
        logger.error("N8N_WEBHOOK_COMPANY not configured")
        return {"error": "N8N_WEBHOOK_COMPANY not configured"}

    logger.info(f"Enriching company: {validated.domain}")

    data = {
        "domain": validated.domain,
        "source": "sales-assistant-agent",
    }
    if validated.company_name:
        data["company_name"] = validated.company_name

    return await _call_webhook(url, data)


async def n8n_enrich_person(
    linkedin_url: Optional[str] = None,
    email: Optional[str] = None,
    name: Optional[str] = None,
    company: Optional[str] = None,
) -> dict[str, Any]:
    """Enrich person/contact data via n8n workflow.

    Uses N8N_WEBHOOK_PEOPLE environment variable.

    Args:
        linkedin_url: LinkedIn profile URL
        email: Person's email address
        name: Person's full name
        company: Company they work at

    Returns:
        Enriched person data (title, contact info, social profiles, etc.)
    """
    # Validate input
    try:
        validated = N8nEnrichPersonInput(
            linkedin_url=linkedin_url,
            email=email,
            name=name,
            company=company,
        )
    except ValueError as e:
        logger.warning(f"Invalid input for n8n_enrich_person: {e}")
        return {"error": f"Invalid input: {e}"}

    url = os.getenv("N8N_WEBHOOK_PEOPLE")
    if not url:
        logger.error("N8N_WEBHOOK_PEOPLE not configured")
        return {"error": "N8N_WEBHOOK_PEOPLE not configured"}

    identifier = validated.linkedin_url or validated.email or validated.name
    logger.info(f"Enriching person: {identifier}")

    data = {
        "source": "sales-assistant-agent",
    }
    if validated.linkedin_url:
        data["linkedin_url"] = validated.linkedin_url
    if validated.email:
        data["email"] = validated.email
    if validated.name:
        data["name"] = validated.name
    if validated.company:
        data["company"] = validated.company

    return await _call_webhook(url, data)


async def n8n_trigger_workflow(
    workflow_name: str,
    data: dict[str, Any],
    webhook_url: Optional[str] = None,
) -> dict[str, Any]:
    """Trigger a generic n8n workflow via webhook.

    Args:
        workflow_name: Name/identifier of the workflow being triggered
        data: Data payload to send to the workflow
        webhook_url: Webhook URL (required)

    Returns:
        Workflow response or error
    """
    # Validate input
    if not webhook_url:
        logger.error("webhook_url is required for generic workflow trigger")
        return {"error": "webhook_url is required for generic workflow trigger"}

    try:
        validated = N8nTriggerWorkflowInput(
            workflow_name=workflow_name,
            data=data,
            webhook_url=webhook_url,
        )
    except ValueError as e:
        logger.warning(f"Invalid input for n8n_trigger_workflow: {e}")
        return {"error": f"Invalid input: {e}"}

    logger.info(f"Triggering workflow: {validated.workflow_name}")

    payload = {
        "workflow": validated.workflow_name,
        "data": validated.data,
        "source": "sales-assistant-agent",
    }

    return await _call_webhook(validated.webhook_url, payload)
