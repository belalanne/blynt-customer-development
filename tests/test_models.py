"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from src.models import (
    ExaSearchInput,
    ExaFindSimilarInput,
    TavilySearchInput,
    NotionCompanyInput,
    N8nEnrichCompanyInput,
    N8nEnrichPersonInput,
)


class TestExaSearchInput:
    """Tests for ExaSearchInput model."""

    def test_valid_input(self):
        """Test valid search input."""
        input_data = ExaSearchInput(query="voice AI companies")
        assert input_data.query == "voice AI companies"
        assert input_data.num_results == 10  # default
        assert input_data.use_autoprompt is True  # default

    def test_custom_num_results(self):
        """Test custom number of results."""
        input_data = ExaSearchInput(query="test", num_results=50)
        assert input_data.num_results == 50

    def test_invalid_num_results_too_high(self):
        """Test that num_results over 100 raises error."""
        with pytest.raises(ValidationError):
            ExaSearchInput(query="test", num_results=150)

    def test_invalid_num_results_too_low(self):
        """Test that num_results under 1 raises error."""
        with pytest.raises(ValidationError):
            ExaSearchInput(query="test", num_results=0)

    def test_empty_query(self):
        """Test that empty query raises error."""
        with pytest.raises(ValidationError):
            ExaSearchInput(query="")


class TestNotionCompanyInput:
    """Tests for NotionCompanyInput model."""

    def test_valid_input(self):
        """Test valid company input."""
        input_data = NotionCompanyInput(
            company_name="Test Co",
            website="test.com",
        )
        assert input_data.company_name == "Test Co"
        assert input_data.website == "https://test.com"  # auto-prefixed

    def test_website_with_https(self):
        """Test website already has https."""
        input_data = NotionCompanyInput(
            company_name="Test Co",
            website="https://test.com",
        )
        assert input_data.website == "https://test.com"

    def test_valid_icp_values(self):
        """Test all valid ICP values."""
        for icp in ["1", "2", "3", "4", "N/A"]:
            input_data = NotionCompanyInput(
                company_name="Test",
                website="test.com",
                icp=icp,
            )
            assert input_data.icp == icp

    def test_invalid_icp(self):
        """Test invalid ICP value raises error."""
        with pytest.raises(ValidationError):
            NotionCompanyInput(
                company_name="Test",
                website="test.com",
                icp="5",
            )

    def test_empty_company_name(self):
        """Test empty company name raises error."""
        with pytest.raises(ValidationError):
            NotionCompanyInput(
                company_name="",
                website="test.com",
            )


class TestN8nEnrichCompanyInput:
    """Tests for N8nEnrichCompanyInput model."""

    def test_domain_normalization(self):
        """Test domain is normalized."""
        input_data = N8nEnrichCompanyInput(domain="https://www.test.com/")
        assert input_data.domain == "test.com"

    def test_domain_lowercase(self):
        """Test domain is lowercased."""
        input_data = N8nEnrichCompanyInput(domain="TEST.COM")
        assert input_data.domain == "test.com"


class TestN8nEnrichPersonInput:
    """Tests for N8nEnrichPersonInput model."""

    def test_valid_with_linkedin(self):
        """Test valid input with LinkedIn URL."""
        input_data = N8nEnrichPersonInput(
            linkedin_url="https://linkedin.com/in/test"
        )
        assert input_data.linkedin_url == "https://linkedin.com/in/test"

    def test_valid_with_email(self):
        """Test valid input with email."""
        input_data = N8nEnrichPersonInput(email="test@example.com")
        assert input_data.email == "test@example.com"

    def test_valid_with_name(self):
        """Test valid input with name."""
        input_data = N8nEnrichPersonInput(name="John Doe")
        assert input_data.name == "John Doe"

    def test_missing_all_identifiers(self):
        """Test that missing all identifiers raises error."""
        with pytest.raises(ValidationError):
            N8nEnrichPersonInput()

    def test_invalid_email(self):
        """Test invalid email raises error."""
        with pytest.raises(ValidationError):
            N8nEnrichPersonInput(email="not-an-email")
