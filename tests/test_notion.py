"""Tests for Notion tools."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from src.tools.notion import (
    _normalize_domain,
    _get_url_variations,
    notion_find_by_website,
    notion_save_company_if_not_exists,
)


class TestNormalizeDomain:
    """Tests for domain normalization."""

    def test_full_url(self):
        """Test normalizing full URL."""
        assert _normalize_domain("https://www.example.com") == "example.com"

    def test_url_with_path(self):
        """Test normalizing URL with path."""
        assert _normalize_domain("https://example.com/about") == "example.com"

    def test_bare_domain(self):
        """Test normalizing bare domain."""
        assert _normalize_domain("example.com") == "example.com"

    def test_www_prefix(self):
        """Test removing www prefix."""
        assert _normalize_domain("www.example.com") == "example.com"

    def test_http_protocol(self):
        """Test http protocol."""
        assert _normalize_domain("http://example.com") == "example.com"

    def test_trailing_slash(self):
        """Test removing trailing slash."""
        assert _normalize_domain("https://example.com/") == "example.com"

    def test_uppercase(self):
        """Test lowercase conversion."""
        assert _normalize_domain("EXAMPLE.COM") == "example.com"

    def test_empty_string(self):
        """Test empty string."""
        assert _normalize_domain("") == ""


class TestGetUrlVariations:
    """Tests for URL variations generator."""

    def test_generates_variations(self):
        """Test that variations are generated."""
        variations = _get_url_variations("example.com")

        assert "https://example.com" in variations
        assert "https://www.example.com" in variations
        assert "http://example.com" in variations
        assert "http://www.example.com" in variations
        assert "example.com" in variations
        assert "www.example.com" in variations

    def test_number_of_variations(self):
        """Test number of variations generated."""
        variations = _get_url_variations("test.com")
        assert len(variations) == 8


class TestNotionFindByWebsite:
    """Tests for notion_find_by_website function."""

    @pytest.mark.asyncio
    async def test_returns_none_without_api_key(self):
        """Test returns None when API key not configured."""
        with patch.dict("os.environ", {}, clear=True):
            result = await notion_find_by_website("example.com")
            assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_without_database_id(self, mock_env_vars):
        """Test returns None when database ID not configured."""
        env = mock_env_vars.copy()
        del env["NOTION_DATABASE_ID"]

        with patch.dict("os.environ", env, clear=True):
            result = await notion_find_by_website("example.com")
            assert result is None


class TestNotionSaveCompanyIfNotExists:
    """Tests for notion_save_company_if_not_exists function."""

    @pytest.mark.asyncio
    async def test_returns_exists_when_duplicate(self, mock_env_vars, sample_notion_page):
        """Test returns 'exists' when company already exists."""
        with patch.dict("os.environ", mock_env_vars):
            with patch(
                "src.tools.notion.notion_find_by_website",
                return_value=sample_notion_page,
            ):
                result = await notion_save_company_if_not_exists(
                    company_name="Test Company",
                    website="https://test.com",
                )

                assert result["action"] == "exists"
                assert "page" in result
                assert "already exists" in result["message"]
