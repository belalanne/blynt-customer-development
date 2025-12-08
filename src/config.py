"""Configuration management for the sales assistant."""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration."""

    # API Keys
    anthropic_api_key: str
    exa_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    notion_api_key: Optional[str] = None

    # Notion
    notion_database_id: Optional[str] = None

    # n8n webhooks
    n8n_webhook_company: Optional[str] = None
    n8n_webhook_people: Optional[str] = None

    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "Config":
        """Load configuration from environment variables.

        Args:
            env_file: Path to .env file (optional)

        Returns:
            Config instance
        """
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to load from multiple locations
            for path in [".env", "../config/.env", "config/.env"]:
                if Path(path).exists():
                    load_dotenv(path)
                    break

        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        return cls(
            anthropic_api_key=anthropic_key,
            exa_api_key=os.getenv("EXA_API_KEY"),
            tavily_api_key=os.getenv("TAVILY_API_KEY"),
            notion_api_key=os.getenv("NOTION_API_KEY"),
            notion_database_id=os.getenv("NOTION_DATABASE_ID"),
            n8n_webhook_company=os.getenv("N8N_WEBHOOK_COMPANY"),
            n8n_webhook_people=os.getenv("N8N_WEBHOOK_PEOPLE"),
        )

    def validate(self) -> list[str]:
        """Validate configuration and return list of warnings."""
        warnings = []

        if not self.exa_api_key and not self.tavily_api_key:
            warnings.append("No search API configured (EXA_API_KEY or TAVILY_API_KEY)")

        if not self.notion_api_key:
            warnings.append("NOTION_API_KEY not set - Notion sync disabled")

        if not self.n8n_webhook_company:
            warnings.append("N8N_WEBHOOK_COMPANY not set - company enrichment disabled")

        if not self.n8n_webhook_people:
            warnings.append("N8N_WEBHOOK_PEOPLE not set - people enrichment disabled")

        return warnings
