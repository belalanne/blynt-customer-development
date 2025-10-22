"""
Email Discovery Utilities

Provides functions to discover and verify email addresses using multiple methods:
- Web search (free)
- Hunter.io API
- Apollo.io API
- Email pattern detection and verification
"""

import os
import re
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .logger import get_logger
from .config import get_config

logger = get_logger(__name__)


class EmailSource(Enum):
    """Source of email discovery"""
    WEB_SEARCH = "web_search"
    HUNTER = "hunter"
    APOLLO = "apollo"
    PATTERN_GUESS = "pattern_guess"
    MANUAL = "manual"


@dataclass
class EmailResult:
    """Result of email discovery"""
    email: Optional[str]
    source: EmailSource
    confidence: float  # 0-100
    verified: bool
    sources_urls: List[str]
    error: Optional[str] = None

    def __str__(self):
        if self.email:
            return f"{self.email} (Source: {self.source.value}, Confidence: {self.confidence}%)"
        return f"Not found ({self.error or 'No email discovered'})"


class EmailDiscovery:
    """Main class for email discovery"""

    def __init__(self):
        self.config = get_config()
        self.hunter_api_key = os.getenv('HUNTER_API_KEY')
        self.apollo_api_key = os.getenv('APOLLO_API_KEY')

    def discover_email(
        self,
        first_name: str,
        last_name: str,
        domain: str,
        company_name: Optional[str] = None,
        role: Optional[str] = None
    ) -> List[EmailResult]:
        """
        Discover email using multiple methods in order of priority:
        1. Web search (free)
        2. Hunter.io (if API key available)
        3. Apollo.io (if API key available)
        4. Pattern guessing + verification

        Args:
            first_name: First name of the person
            last_name: Last name of the person
            domain: Company domain (e.g., 'modjo.ai')
            company_name: Full company name (optional, improves accuracy)
            role: Job title (optional, improves accuracy)

        Returns:
            List of EmailResult objects, sorted by confidence (highest first)
        """
        results = []

        # Method 1: Web Search
        logger.info(f"Trying web search for {first_name} {last_name} @ {domain}")
        # Note: Web search would need to be implemented using WebSearch tool
        # For now, we'll focus on API methods

        # Method 2: Hunter.io
        if self.hunter_api_key:
            hunter_result = self._try_hunter(first_name, last_name, domain)
            if hunter_result.email:
                results.append(hunter_result)
        else:
            logger.warning("Hunter.io API key not set. Skipping Hunter.io.")

        # Method 3: Apollo.io
        if self.apollo_api_key:
            apollo_result = self._try_apollo(
                first_name, last_name, domain, company_name, role
            )
            if apollo_result.email:
                results.append(apollo_result)
        else:
            logger.warning("Apollo.io API key not set. Skipping Apollo.io.")

        # Method 4: Pattern guessing + verification
        if not results and self.hunter_api_key:
            pattern_result = self._try_pattern_guess(first_name, last_name, domain)
            if pattern_result.email:
                results.append(pattern_result)

        # Sort by confidence
        results.sort(key=lambda r: r.confidence, reverse=True)

        return results

    def _try_hunter(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> EmailResult:
        """
        Try to find email using Hunter.io Email Finder API

        API Docs: https://hunter.io/api/v2/docs#email-finder
        """
        try:
            url = "https://api.hunter.io/v2/email-finder"
            params = {
                "domain": domain,
                "first_name": first_name,
                "last_name": last_name,
                "api_key": self.hunter_api_key
            }

            logger.info(f"Calling Hunter.io API for {first_name} {last_name} @ {domain}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("data") and data["data"].get("email"):
                email_data = data["data"]
                return EmailResult(
                    email=email_data["email"],
                    source=EmailSource.HUNTER,
                    confidence=email_data.get("score", 50),
                    verified=email_data.get("verification", {}).get("status") == "valid",
                    sources_urls=[s["uri"] for s in email_data.get("sources", [])]
                )
            else:
                return EmailResult(
                    email=None,
                    source=EmailSource.HUNTER,
                    confidence=0,
                    verified=False,
                    sources_urls=[],
                    error="No email found by Hunter.io"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Hunter.io API error: {e}")
            return EmailResult(
                email=None,
                source=EmailSource.HUNTER,
                confidence=0,
                verified=False,
                sources_urls=[],
                error=str(e)
            )

    def _try_apollo(
        self,
        first_name: str,
        last_name: str,
        domain: str,
        company_name: Optional[str] = None,
        role: Optional[str] = None
    ) -> EmailResult:
        """
        Try to find email using Apollo.io People Match API

        API Docs: https://apolloio.github.io/apollo-api-docs/
        """
        try:
            url = "https://api.apollo.io/v1/people/match"
            headers = {
                "Content-Type": "application/json",
                "Cache-Control": "no-cache"
            }
            payload = {
                "api_key": self.apollo_api_key,
                "first_name": first_name,
                "last_name": last_name,
                "domain": domain
            }

            if company_name:
                payload["organization_name"] = company_name
            if role:
                payload["title"] = role

            logger.info(f"Calling Apollo.io API for {first_name} {last_name} @ {domain}")
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("person") and data["person"].get("email"):
                person = data["person"]
                email_status = person.get("email_status", "unknown")

                # Apollo confidence scoring
                confidence = 90 if email_status == "verified" else 70

                return EmailResult(
                    email=person["email"],
                    source=EmailSource.APOLLO,
                    confidence=confidence,
                    verified=email_status == "verified",
                    sources_urls=[person.get("linkedin_url", "")]
                )
            else:
                return EmailResult(
                    email=None,
                    source=EmailSource.APOLLO,
                    confidence=0,
                    verified=False,
                    sources_urls=[],
                    error="No email found by Apollo.io"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Apollo.io API error: {e}")
            return EmailResult(
                email=None,
                source=EmailSource.APOLLO,
                confidence=0,
                verified=False,
                sources_urls=[],
                error=str(e)
            )

    def _try_pattern_guess(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> EmailResult:
        """
        Guess email using common patterns and verify with Hunter.io
        """
        # Generate common email patterns
        patterns = self._generate_email_patterns(first_name, last_name, domain)

        # Try to verify each pattern
        for pattern in patterns:
            if self._verify_email_hunter(pattern):
                return EmailResult(
                    email=pattern,
                    source=EmailSource.PATTERN_GUESS,
                    confidence=60,  # Lower confidence for guessed emails
                    verified=True,
                    sources_urls=[]
                )

        return EmailResult(
            email=None,
            source=EmailSource.PATTERN_GUESS,
            confidence=0,
            verified=False,
            sources_urls=[],
            error="No valid pattern found"
        )

    def _generate_email_patterns(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> List[str]:
        """
        Generate common email patterns

        Returns list of possible emails sorted by likelihood
        """
        first = first_name.lower().strip()
        last = last_name.lower().strip()
        first_initial = first[0] if first else ""

        # Remove special characters and accents
        first = self._normalize_name(first)
        last = self._normalize_name(last)

        patterns = [
            f"{first}@{domain}",                    # paul@modjo.ai
            f"{first}.{last}@{domain}",            # paul.berloty@modjo.ai
            f"{first_initial}.{last}@{domain}",    # p.berloty@modjo.ai
            f"{first}{last}@{domain}",             # paulberloty@modjo.ai
            f"{first}_{last}@{domain}",            # paul_berloty@modjo.ai
            f"{last}.{first}@{domain}",            # berloty.paul@modjo.ai
            f"{first}-{last}@{domain}",            # paul-berloty@modjo.ai
        ]

        return patterns

    def _normalize_name(self, name: str) -> str:
        """Remove accents and special characters from name"""
        import unicodedata
        # Remove accents
        name = ''.join(
            c for c in unicodedata.normalize('NFD', name)
            if unicodedata.category(c) != 'Mn'
        )
        # Keep only alphanumeric and hyphen
        name = re.sub(r'[^a-z0-9-]', '', name.lower())
        return name

    def _verify_email_hunter(self, email: str) -> bool:
        """
        Verify if email exists using Hunter.io Email Verifier

        API Docs: https://hunter.io/api/v2/docs#email-verifier
        """
        if not self.hunter_api_key:
            return False

        try:
            url = "https://api.hunter.io/v2/email-verifier"
            params = {
                "email": email,
                "api_key": self.hunter_api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("data"):
                status = data["data"].get("status")
                # Consider valid or accept_all as potentially valid
                return status in ["valid", "accept_all"]

            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Hunter.io verification error: {e}")
            return False

    def get_company_email_pattern(self, domain: str) -> Optional[Dict]:
        """
        Get the most common email pattern for a company using Hunter.io Domain Search

        Returns:
            Dict with pattern info or None if not found
            Example: {"pattern": "{first}@{domain}", "confidence": 95}
        """
        if not self.hunter_api_key:
            logger.warning("Hunter.io API key not set")
            return None

        try:
            url = "https://api.hunter.io/v2/domain-search"
            params = {
                "domain": domain,
                "api_key": self.hunter_api_key,
                "limit": 1  # We only need the pattern, not all emails
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("data") and data["data"].get("pattern"):
                return {
                    "pattern": data["data"]["pattern"],
                    "confidence": data["data"].get("organization", {}).get("pattern_score", 0)
                }

            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Hunter.io domain search error: {e}")
            return None


def extract_domain_from_url(url: str) -> str:
    """
    Extract domain from URL

    Examples:
        https://www.modjo.ai/about -> modjo.ai
        modjo.ai -> modjo.ai
        www.modjo.ai -> modjo.ai
    """
    # Remove protocol
    domain = re.sub(r'https?://', '', url)
    # Remove path
    domain = domain.split('/')[0]
    # Remove www
    domain = re.sub(r'^www\.', '', domain)
    return domain


def split_full_name(full_name: str) -> Tuple[str, str]:
    """
    Split full name into first and last name

    Examples:
        "Paul Berloty" -> ("Paul", "Berloty")
        "Matthieu de la Fournière" -> ("Matthieu", "de la Fournière")
        "Jean-Pierre Dupont" -> ("Jean-Pierre", "Dupont")
    """
    parts = full_name.strip().split()

    if len(parts) == 0:
        return "", ""
    elif len(parts) == 1:
        return parts[0], ""
    elif len(parts) == 2:
        return parts[0], parts[1]
    else:
        # Handle compound last names (de la Fournière, van der Berg, etc.)
        # Assume everything after first word is last name
        return parts[0], " ".join(parts[1:])


# Example usage
if __name__ == "__main__":
    # Set up API keys
    os.environ['HUNTER_API_KEY'] = 'your_hunter_key'
    os.environ['APOLLO_API_KEY'] = 'your_apollo_key'

    # Initialize discovery
    discovery = EmailDiscovery()

    # Find email
    results = discovery.discover_email(
        first_name="Paul",
        last_name="Berloty",
        domain="modjo.ai",
        company_name="Modjo",
        role="CEO"
    )

    # Print results
    for result in results:
        print(result)
