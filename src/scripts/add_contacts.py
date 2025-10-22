#!/usr/bin/env python3
"""
Add contacts from a company to Notion People database.
"""

import asyncio
import os
import sys
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
from notion_client import AsyncClient

# Load environment variables
config_dir = Path(__file__).parent.parent.parent / "config"
load_dotenv(config_dir / ".env")

# Database IDs
COMPANIES_DB_ID = "2861bdff7e998000a14edb0bf56a75bf"
PEOPLE_COLLECTION_ID = "collection://20a1bdff-7e99-81a7-8612-000b6f8a32f4"

# Extract actual database ID from collection ID for People database
# collection://20a1bdff-7e99-81a7-8612-000b6f8a32f4 -> 20a1bdff7e9981a78612000b6f8a32f4
PEOPLE_DB_ID = "20a1bdff7e9981a78612000b6f8a32f4"


class ContactAdder:
    """Handles adding contacts from a company to Notion."""

    def __init__(self, api_key: str):
        self.client = AsyncClient(auth=api_key)

    def normalize_domain(self, domain: str) -> str:
        """Normalize domain for consistent matching."""
        domain = domain.lower().strip()
        # Remove protocol
        domain = re.sub(r'^https?://', '', domain)
        # Remove www.
        domain = re.sub(r'^www\.', '', domain)
        # Remove trailing slash and path
        domain = domain.split('/')[0]
        return domain

    async def search_company(self, domain: str) -> Optional[Dict]:
        """
        Search for company in Notion database by domain.

        Args:
            domain: Company domain (e.g., "getvoiceline.com")

        Returns:
            Company page data if found, None otherwise
        """
        normalized = self.normalize_domain(domain)

        print(f"🔍 Searching for company with domain: {normalized}")

        try:
            # Query the database
            response = await self.client.databases.query(
                database_id=COMPANIES_DB_ID,
                filter={
                    "property": "Website",
                    "url": {
                        "contains": normalized
                    }
                }
            )

            if response["results"]:
                page = response["results"][0]
                print(f"✅ Found company: {page['url']}")
                return page
            else:
                # Try searching by title if URL search didn't work
                response = await self.client.databases.query(
                    database_id=COMPANIES_DB_ID
                )

                # Manual filtering (since Notion search can be limited)
                for page in response["results"]:
                    props = page.get("properties", {})
                    website_prop = props.get("Website", {})

                    if website_prop.get("type") == "url":
                        url = website_prop.get("url", "")
                        if url and normalized in self.normalize_domain(url):
                            print(f"✅ Found company: {page['url']}")
                            return page

                print(f"❌ Company not found in database")
                return None

        except Exception as e:
            print(f"❌ Error searching for company: {str(e)}")
            return None

    async def get_page_content(self, page_id: str) -> str:
        """Get page content as text."""
        try:
            blocks = await self.client.blocks.children.list(block_id=page_id)
            content = []

            for block in blocks["results"]:
                block_type = block["type"]
                if block_type == "paragraph":
                    text = self._extract_rich_text(block["paragraph"].get("rich_text", []))
                    content.append(text)
                elif block_type == "heading_1":
                    text = self._extract_rich_text(block["heading_1"].get("rich_text", []))
                    content.append(f"# {text}")
                elif block_type == "heading_2":
                    text = self._extract_rich_text(block["heading_2"].get("rich_text", []))
                    content.append(f"## {text}")
                elif block_type == "heading_3":
                    text = self._extract_rich_text(block["heading_3"].get("rich_text", []))
                    content.append(f"### {text}")
                elif block_type == "bulleted_list_item":
                    text = self._extract_rich_text(block["bulleted_list_item"].get("rich_text", []))
                    content.append(f"- {text}")

            return "\n".join(content)
        except Exception as e:
            print(f"⚠️ Error reading page content: {str(e)}")
            return ""

    def _extract_rich_text(self, rich_text: List[Dict]) -> str:
        """Extract plain text from Notion rich text."""
        return "".join([t.get("plain_text", "") for t in rich_text])

    def extract_property_value(self, page: Dict, prop_name: str) -> Optional[str]:
        """Extract property value from Notion page."""
        try:
            props = page.get("properties", {})
            prop = props.get(prop_name, {})
            prop_type = prop.get("type")

            if prop_type == "url":
                return prop.get("url")
            elif prop_type == "title":
                return self._extract_rich_text(prop.get("title", []))
            elif prop_type == "rich_text":
                return self._extract_rich_text(prop.get("rich_text", []))
            elif prop_type == "select":
                select = prop.get("select")
                return select.get("name") if select else None
            elif prop_type == "number":
                return prop.get("number")
            elif prop_type == "email":
                return prop.get("email")

        except Exception as e:
            print(f"⚠️ Error extracting property {prop_name}: {str(e)}")

        return None

    def extract_linkedin_urls(self, text: str) -> List[str]:
        """Extract LinkedIn URLs from text."""
        pattern = r'https?://(?:www\.)?linkedin\.com/in/[\w-]+'
        return re.findall(pattern, text)

    async def search_people_by_linkedin(self, linkedin_url: str) -> Optional[Dict]:
        """Search People database for existing contact by LinkedIn URL."""
        try:
            response = await self.client.databases.query(
                database_id=PEOPLE_DB_ID,
                filter={
                    "property": "LinkedIn URL",
                    "url": {
                        "equals": linkedin_url
                    }
                }
            )

            if response["results"]:
                return response["results"][0]
            return None

        except Exception as e:
            print(f"⚠️ Error searching people database: {str(e)}")
            return None

    async def add_contact(self, contact_data: Dict, company_page_url: str, company_icp: str) -> Optional[str]:
        """
        Add contact to People database.

        Args:
            contact_data: Contact information
            company_page_url: Notion URL of the company page
            company_icp: Company ICP value (1, 2, 3, or N/A)

        Returns:
            Page URL if successful, None otherwise
        """
        try:
            # Map ICP to Campaign
            campaign_map = {
                "1": "ICP#1",
                "2": "ICP#2",
                "3": "ICP#3",
            }
            campaign = campaign_map.get(company_icp)

            # Build properties
            properties = {
                "Contact_Name": {
                    "title": [{"text": {"content": contact_data["name"]}}]
                },
                "Role": {
                    "rich_text": [{"text": {"content": contact_data.get("role", "")}}]
                },
                "Company name": {
                    "url": company_page_url
                },
                "Decision_Level": {
                    "select": {"name": contact_data.get("decision_level", "Influencer")}
                },
                "Type": {
                    "select": {"name": "Customer"}
                },
                "Status Contact": {
                    "select": {"name": "🥶 Ice Box"}
                },
                "Source of contacts": {
                    "select": {"name": "Outreach"}
                },
                "Owner / Assigned To": {
                    "rich_text": [{"text": {"content": "Benjamin Lalanne"}}]
                }
            }

            # Add LinkedIn URL if available
            if contact_data.get("linkedin"):
                properties["LinkedIn URL"] = {
                    "url": contact_data["linkedin"]
                }

            # Add Email if available
            if contact_data.get("email"):
                properties["Email"] = {
                    "email": contact_data["email"]
                }

            # Add Campaign if ICP is valid
            if campaign:
                properties["Campaign"] = {
                    "select": {"name": campaign}
                }

            # Create the page
            response = await self.client.pages.create(
                parent={"database_id": PEOPLE_DB_ID},
                properties=properties
            )

            return response["url"]

        except Exception as e:
            print(f"❌ Error adding contact {contact_data.get('name')}: {str(e)}")
            return None


async def main():
    """Main execution."""
    if len(sys.argv) < 2:
        print("Usage: python add_contacts.py <company_domain>")
        sys.exit(1)

    domain = sys.argv[1]

    # Get API key
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        print("❌ NOTION_API_KEY not found in environment")
        sys.exit(1)

    adder = ContactAdder(api_key)

    # Step 1: Find company
    print(f"\n🔍 Step 1: Searching for company {domain}...")
    company = await adder.search_company(domain)

    if not company:
        print(f"\n❌ Company '{domain}' not found in Notion database")
        print(f"💡 Please run `/enrich-company {domain}` first to add the company")
        sys.exit(1)

    company_url = company["url"]
    company_name = adder.extract_property_value(company, "Company_Name") or "Unknown"
    company_website = adder.extract_property_value(company, "Website")
    company_icp = adder.extract_property_value(company, "ICP") or "N/A"

    print(f"✅ Found company: {company_name}")
    print(f"📧 Company domain: {company_website}")
    print(f"🎯 ICP: {company_icp}")
    print(f"🔗 Notion URL: {company_url}")

    # Step 2: Check existing contacts mentioned in company page
    print(f"\n📋 Step 2: Checking for already mentioned contacts...")
    page_content = await adder.get_page_content(company["id"])
    existing_linkedin_urls = adder.extract_linkedin_urls(page_content)

    if existing_linkedin_urls:
        print(f"Found {len(existing_linkedin_urls)} LinkedIn URLs in company page:")
        for url in existing_linkedin_urls:
            print(f"  - {url}")
    else:
        print("No LinkedIn URLs found in company page")

    print(f"\n✅ Setup complete. Company data ready for contact research.")
    campaign_map = {'1': 'ICP#1', '2': 'ICP#2', '3': 'ICP#3'}
    campaign = campaign_map.get(company_icp, 'None')

    print(f"\n📊 Summary:")
    print(f"  - Company: {company_name}")
    print(f"  - Domain: {company_website}")
    print(f"  - ICP: {company_icp}")
    print(f"  - Campaign: {campaign}")
    print(f"  - Existing LinkedIn URLs: {len(existing_linkedin_urls)}")

    # Return data for further processing
    return {
        "company": company,
        "company_name": company_name,
        "company_url": company_url,
        "company_domain": company_website,
        "company_icp": company_icp,
        "existing_linkedin_urls": existing_linkedin_urls
    }


if __name__ == "__main__":
    result = asyncio.run(main())
