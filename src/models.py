"""Pydantic models for input validation."""

from typing import Any, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator
import re


# ====================
# Exa Search Models
# ====================


class ExaSearchInput(BaseModel):
    """Input validation for Exa web search."""

    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    num_results: int = Field(default=10, ge=1, le=100, description="Number of results")
    use_autoprompt: bool = Field(default=True, description="Let Exa optimize the query")
    include_domains: Optional[list[str]] = Field(
        default=None, description="Only include results from these domains"
    )
    exclude_domains: Optional[list[str]] = Field(
        default=None, description="Exclude results from these domains"
    )
    start_published_date: Optional[str] = Field(
        default=None, description="Filter by publish date (ISO format)"
    )
    category: Optional[str] = Field(
        default=None, description="Filter by category (company, research_paper, news)"
    )
    contents: bool = Field(default=True, description="Include page contents")

    @field_validator("include_domains", "exclude_domains", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        """Convert empty strings to None for optional list fields."""
        if v == "" or v == []:
            return None
        return v

    @field_validator("start_published_date", "category", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty strings to None for optional string fields."""
        if v == "":
            return None
        return v


class ExaFindSimilarInput(BaseModel):
    """Input validation for Exa find similar."""

    url: str = Field(..., min_length=1, description="URL to find similar pages for")
    num_results: int = Field(default=10, ge=1, le=100, description="Number of results")
    include_domains: Optional[list[str]] = None
    exclude_domains: Optional[list[str]] = None
    contents: bool = Field(default=True)

    @field_validator("include_domains", "exclude_domains", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        """Convert empty strings to None for optional list fields."""
        if v == "" or v == []:
            return None
        return v


# ====================
# Tavily Search Models
# ====================


class TavilySearchInput(BaseModel):
    """Input validation for Tavily search."""

    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    search_depth: str = Field(
        default="basic",
        description="Search depth: basic or advanced",
    )
    max_results: int = Field(default=10, ge=1, le=20, description="Number of results")
    include_answer: bool = Field(default=True, description="Include AI-generated answer")
    include_domains: Optional[list[str]] = None
    exclude_domains: Optional[list[str]] = None

    @field_validator("include_domains", "exclude_domains", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        """Convert empty strings to None for optional list fields."""
        if v == "" or v == []:
            return None
        return v

    @field_validator("search_depth")
    @classmethod
    def validate_search_depth(cls, v: str) -> str:
        if v not in ("basic", "advanced"):
            raise ValueError("search_depth must be 'basic' or 'advanced'")
        return v


class TavilyExtractInput(BaseModel):
    """Input validation for Tavily content extraction."""

    urls: list[str] = Field(..., min_length=1, max_length=10, description="URLs to extract")


# ====================
# Notion Models
# ====================


class NotionSearchInput(BaseModel):
    """Input validation for Notion search."""

    query: str = Field(..., min_length=1, max_length=500)
    database_id: Optional[str] = None
    filter_property: Optional[str] = None
    filter_value: Optional[str] = None


class NotionCompanyInput(BaseModel):
    """Input validation for saving a company to Notion."""

    company_name: str = Field(..., min_length=1, max_length=200)
    website: str = Field(..., min_length=1)
    linkedin_url: Optional[str] = None
    vertical: Optional[str] = Field(default=None, max_length=100)
    icp: Optional[str] = Field(default=None)
    product_description: Optional[str] = Field(default=None, max_length=50)
    asr_providers: Optional[list[str]] = None
    ai_ml_engineers: Optional[int] = Field(default=None, ge=0)
    country: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = None
    database_id: Optional[str] = None

    @field_validator("asr_providers", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        """Convert empty strings to None for optional list fields."""
        if v == "" or v == []:
            return None
        return v

    @field_validator("linkedin_url", "vertical", "product_description", "country", "status", "database_id", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty strings to None for optional string fields."""
        if v == "":
            return None
        return v

    @field_validator("icp")
    @classmethod
    def validate_icp(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("1", "2", "3", "4", "N/A"):
            raise ValueError("ICP must be '1', '2', '3', '4', or 'N/A'")
        return v

    @field_validator("website")
    @classmethod
    def validate_website(cls, v: str) -> str:
        # Ensure it has a scheme
        if not v.startswith(("http://", "https://")):
            v = f"https://{v}"
        return v


class NotionUpdateInput(BaseModel):
    """Input validation for updating a company in Notion."""

    page_id: str = Field(..., min_length=1)
    updates: dict[str, Any] = Field(..., min_length=1)


# ====================
# n8n Models
# ====================


class N8nEnrichCompanyInput(BaseModel):
    """Input validation for n8n company enrichment."""

    domain: str = Field(..., min_length=1, max_length=255)
    company_name: Optional[str] = Field(default=None, max_length=200)

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, v: str) -> str:
        # Remove protocol if present
        v = re.sub(r"^https?://", "", v)
        # Remove www. prefix
        v = re.sub(r"^www\.", "", v)
        # Remove trailing slash
        v = v.rstrip("/")
        return v.lower()


class N8nEnrichPersonInput(BaseModel):
    """Input validation for n8n person enrichment."""

    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = Field(default=None, max_length=200)
    company: Optional[str] = Field(default=None, max_length=200)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            # Basic email validation
            if "@" not in v or "." not in v.split("@")[-1]:
                raise ValueError("Invalid email format")
        return v

    def model_post_init(self, __context: Any) -> None:
        """Validate that at least one identifier is provided."""
        if not any([self.linkedin_url, self.email, self.name]):
            raise ValueError("At least one of linkedin_url, email, or name is required")


class N8nTriggerWorkflowInput(BaseModel):
    """Input validation for generic n8n workflow trigger."""

    workflow_name: str = Field(..., min_length=1, max_length=100)
    data: dict[str, Any] = Field(default_factory=dict)
    webhook_url: str = Field(..., min_length=1)


# ====================
# Browser Models
# ====================


class BrowserScreenshotInput(BaseModel):
    """Input validation for browser screenshot."""

    url: str = Field(..., min_length=1)
    full_page: bool = Field(default=False)
    selector: Optional[str] = None
    wait_for: Optional[str] = None


class BrowserExtractTextInput(BaseModel):
    """Input validation for browser text extraction."""

    url: str = Field(..., min_length=1)
    selector: Optional[str] = None
    wait_for: Optional[str] = None


class BrowserExtractHtmlInput(BaseModel):
    """Input validation for browser HTML extraction."""

    url: str = Field(..., min_length=1)
    selector: Optional[str] = None
    wait_for: Optional[str] = None


class BrowserExtractLinksInput(BaseModel):
    """Input validation for browser link extraction."""

    url: str = Field(..., min_length=1)
    selector: Optional[str] = None
    filter_pattern: Optional[str] = None


class BrowserScrollCaptureInput(BaseModel):
    """Input validation for browser scroll and capture."""

    url: str = Field(..., min_length=1)
    scroll_count: int = Field(default=3, ge=1, le=20)
    scroll_delay: int = Field(default=1000, ge=100, le=10000)
