"""Pytest configuration and fixtures."""

import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def mock_env_vars():
    """Set up mock environment variables for testing."""
    env_vars = {
        "ANTHROPIC_API_KEY": "test-anthropic-key",
        "EXA_API_KEY": "test-exa-key",
        "TAVILY_API_KEY": "test-tavily-key",
        "NOTION_API_KEY": "test-notion-key",
        "NOTION_DATABASE_ID": "test-database-id",
        "N8N_WEBHOOK_COMPANY": "https://n8n.example.com/webhook/company",
        "N8N_WEBHOOK_PEOPLE": "https://n8n.example.com/webhook/people",
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx response."""
    def _make_response(status_code: int, json_data: dict):
        response = MagicMock()
        response.status_code = status_code
        response.json.return_value = json_data
        response.text = str(json_data)
        return response
    return _make_response


@pytest.fixture
def mock_httpx_client(mock_httpx_response):
    """Create a mock httpx AsyncClient."""
    async def _make_client(responses: list[tuple[int, dict]]):
        client = AsyncMock()

        # Set up responses for sequential calls
        response_queue = [
            mock_httpx_response(status, data)
            for status, data in responses
        ]

        client.post.side_effect = response_queue
        client.get.side_effect = response_queue
        client.patch.side_effect = response_queue

        return client

    return _make_client


@pytest.fixture
def sample_company_data():
    """Sample company data for testing."""
    return {
        "company_name": "Test Company",
        "website": "https://test.com",
        "linkedin_url": "https://linkedin.com/company/test",
        "vertical": "SaaS",
        "icp": "3",
        "product_description": "Voice AI platform",
        "asr_providers": ["Deepgram", "Gladia"],
        "ai_ml_engineers": 10,
        "country": "USA",
    }


@pytest.fixture
def sample_exa_response():
    """Sample Exa search response."""
    return {
        "results": [
            {
                "url": "https://example1.com",
                "title": "Example Company 1",
                "text": "Example company building voice AI...",
            },
            {
                "url": "https://example2.com",
                "title": "Example Company 2",
                "text": "Another voice AI company...",
            },
        ]
    }


@pytest.fixture
def sample_notion_page():
    """Sample Notion page response."""
    return {
        "id": "test-page-id-1234",
        "object": "page",
        "properties": {
            "Company_Name": {
                "title": [{"text": {"content": "Test Company"}}]
            },
            "Website": {"url": "https://test.com"},
            "ICP": {"select": {"name": "3"}},
        },
        "url": "https://notion.so/test-page",
    }
