"""
Configuration management utilities.
"""

import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv


def load_config(env_file: str = ".env") -> Dict[str, str]:
    """
    Load configuration from environment file.

    Args:
        env_file: Path to .env file (relative to config directory)

    Returns:
        Dictionary of configuration values
    """
    # Load from config/.env
    config_dir = Path(__file__).parent.parent.parent / "config"
    env_path = config_dir / env_file

    if env_path.exists():
        load_dotenv(env_path)

    return {
        # Data Enrichment APIs
        "clearbit_api_key": os.getenv("CLEARBIT_API_KEY", ""),
        "apollo_api_key": os.getenv("APOLLO_API_KEY", ""),
        "linkedin_api_key": os.getenv("LINKEDIN_API_KEY", ""),

        # Notion
        "notion_api_key": os.getenv("NOTION_API_KEY", ""),
        "notion_database_id": os.getenv("NOTION_DATABASE_ID", ""),

        # Optional
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    }
