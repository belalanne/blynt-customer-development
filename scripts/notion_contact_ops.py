#!/usr/bin/env python3
"""
Lightweight Notion contact operations - Optimized for minimal token usage
Usage:
  python scripts/notion_contact_ops.py check-duplicate --linkedin "https://linkedin.com/in/example"
  python scripts/notion_contact_ops.py get-company --domain "recept.ai"
  python scripts/notion_contact_ops.py add-contact --linkedin "..." --name "..." --role "..." --company-id "..."
"""
import os
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from notion_client import Client
except ImportError:
    print(json.dumps({"error": "notion-client not installed", "message": "Run: pip install notion-client"}))
    sys.exit(1)

# Load .env if available
env_file = Path(__file__).parent.parent / "config" / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

# Database IDs
PEOPLE_DB = "20a1bdff-7e99-80fb-9d3c-dfbfa7a8bd70"
COMPANIES_DB = "20a1bdff-7e99-80c4-8f85-c663fa70c2f2"
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")


class NotionContactManager:
    """Lightweight Notion contact operations with minimal responses."""

    def __init__(self, api_key: str):
        self.client = Client(auth=api_key)
        self.people_db = PEOPLE_DB
        self.companies_db = COMPANIES_DB
        self._user_cache = {}

    def check_duplicate_by_linkedin(self, linkedin_url: str) -> Dict[str, Any]:
        """
        Check if contact exists by LinkedIn URL.
        Returns: {"exists": bool, "page_id": str|None, "name": str|None}
        """
        try:
            result = self.client.databases.query(
                **{
                    "database_id": self.people_db,
                    "filter": {
                        "property": "LinkedIn URL",
                        "url": {"equals": linkedin_url}
                    },
                    "page_size": 1
                }
            )

            if result["results"]:
                page = result["results"][0]
                name = page["properties"].get("Contact_Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown")
                return {
                    "exists": True,
                    "page_id": page["id"],
                    "name": name,
                    "url": f"https://notion.so/{page['id'].replace('-', '')}"
                }
            else:
                return {"exists": False, "page_id": None, "name": None}
        except Exception as e:
            return {"error": str(e)}

    def get_company_by_domain(self, domain: str) -> Dict[str, Any]:
        """
        Get company by website domain (normalized).
        Returns: {"found": bool, "page_id": str, "icp": str, "name": str}
        """
        # Normalize domain (remove http://, https://, www.)
        normalized = domain.lower().replace("http://", "").replace("https://", "").replace("www.", "").rstrip("/")

        try:
            # Try exact match first
            result = self.client.databases.query(
                **{
                    "database_id": self.companies_db,
                    "filter": {
                        "property": "Website",
                        "url": {"contains": normalized}
                    },
                    "page_size": 5  # Get a few results to find best match
                }
            )

            if result["results"]:
                # Find best match
                for page in result["results"]:
                    website = page["properties"].get("Website", {}).get("url", "")
                    if normalized in website.lower():
                        name = page["properties"].get("Company_Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown")
                        icp_value = page["properties"].get("ICP", {}).get("select")
                        icp = icp_value.get("name", "N/A") if icp_value else "N/A"

                        return {
                            "found": True,
                            "page_id": page["id"],
                            "page_url": f"https://notion.so/{page['id'].replace('-', '')}",
                            "icp": icp,
                            "name": name,
                            "domain": website
                        }

            return {"found": False, "message": f"No company found with domain: {normalized}"}
        except Exception as e:
            return {"error": str(e)}

    def get_user_id(self, name: str) -> Optional[str]:
        """Get user ID by name (cached)."""
        if name in self._user_cache:
            return self._user_cache[name]

        try:
            result = self.client.users.list()
            for user in result["results"]:
                if user.get("name") == name:
                    user_id = user["id"]
                    self._user_cache[name] = user_id
                    return user_id
            return None
        except Exception:
            return None

    def create_or_update_company(
        self,
        company_name: str,
        website: str,
        linkedin: Optional[str] = None,
        vertical: Optional[str] = None,
        icp: str = "3",
        product_description: Optional[str] = None,
        asr_providers: Optional[list] = None,
        ai_engineers: Optional[int] = None,
        main_office_country: Optional[str] = None,
        status: str = "Ice Box"
    ) -> Dict[str, Any]:
        """
        Create or update company in Companies database.
        Returns: {"success": bool, "page_id": str, "url": str, "action": "created"|"updated"}
        """
        try:
            # Check if company exists
            existing = self.get_company_by_domain(website)

            # Build properties
            properties = {
                "Company_Name": {"title": [{"text": {"content": company_name}}]},
                "Website": {"url": website if website.startswith("http") else f"https://{website}"},
                "ICP": {"select": {"name": str(icp)}}
            }

            # Add optional fields
            if linkedin:
                properties["Linkedin Link"] = {"url": linkedin}
            if vertical:
                properties["Vertical"] = {"select": {"name": vertical}}
            if product_description:
                properties["Product description"] = {"rich_text": [{"text": {"content": product_description}}]}
            if asr_providers:
                properties["ASR provider"] = {"multi_select": [{"name": p} for p in asr_providers]}
            if ai_engineers is not None:
                properties["Nbr of AI/ML/Speech engineer"] = {"number": ai_engineers}
            if main_office_country:
                properties["Main Office Country"] = {"rich_text": [{"text": {"content": main_office_country}}]}

            # Only set status if creating new (don't overwrite existing)
            if not existing.get("found"):
                properties["Status / Engagement"] = {"select": {"name": status}}

            if existing.get("found"):
                # Update existing page
                response = self.client.pages.update(
                    page_id=existing["page_id"],
                    properties=properties
                )
                action = "updated"
                page_id = existing["page_id"]
            else:
                # Create new page
                response = self.client.pages.create(
                    parent={"database_id": self.companies_db},
                    properties=properties
                )
                action = "created"
                page_id = response["id"]

            page_url = f"https://notion.so/{page_id.replace('-', '')}"

            return {
                "success": True,
                "page_id": page_id,
                "url": page_url,
                "action": action,
                "company_name": company_name
            }
        except Exception as e:
            return {"error": str(e), "success": False}

    def update_company_icp(self, company_id: str, icp: str) -> Dict[str, Any]:
        """
        Update company ICP field.
        Returns: {"success": bool, "page_id": str, "icp": str}
        """
        try:
            response = self.client.pages.update(
                page_id=company_id,
                properties={
                    "ICP": {"select": {"name": str(icp)}}
                }
            )

            return {
                "success": True,
                "page_id": company_id,
                "icp": icp,
                "url": f"https://notion.so/{company_id.replace('-', '')}"
            }
        except Exception as e:
            return {"error": str(e), "success": False}

    def search_contacts_by_name(self, name: str) -> Dict[str, Any]:
        """
        Search for contacts by name.
        Returns: {"found": bool, "contacts": [list of contact dicts]}
        """
        try:
            result = self.client.databases.query(
                **{
                    "database_id": self.people_db,
                    "filter": {
                        "property": "Contact_Name",
                        "title": {"contains": name}
                    },
                    "page_size": 20
                }
            )

            contacts = []
            for page in result["results"]:
                name_val = page["properties"].get("Contact_Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown")
                email = page["properties"].get("Email", {}).get("email")
                role = page["properties"].get("Role", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")

                contacts.append({
                    "page_id": page["id"],
                    "name": name_val,
                    "email": email,
                    "role": role,
                    "url": f"https://notion.so/{page['id'].replace('-', '')}"
                })

            return {
                "found": len(contacts) > 0,
                "count": len(contacts),
                "contacts": contacts
            }
        except Exception as e:
            return {"error": str(e)}

    def get_contacts_without_email(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get all contacts without email addresses.
        Returns: {"count": int, "contacts": [list]}
        """
        try:
            result = self.client.databases.query(
                **{
                    "database_id": self.people_db,
                    "filter": {
                        "property": "Email",
                        "email": {"is_empty": True}
                    },
                    "page_size": limit
                }
            )

            contacts = []
            for page in result["results"]:
                name_val = page["properties"].get("Contact_Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown")
                role = page["properties"].get("Role", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
                linkedin = page["properties"].get("LinkedIn URL", {}).get("url")

                contacts.append({
                    "page_id": page["id"],
                    "name": name_val,
                    "role": role,
                    "linkedin": linkedin,
                    "url": f"https://notion.so/{page['id'].replace('-', '')}"
                })

            return {
                "count": len(contacts),
                "contacts": contacts
            }
        except Exception as e:
            return {"error": str(e)}

    def update_contact_email(
        self,
        contact_id: str,
        email: str,
        source: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update contact email address.
        Returns: {"success": bool, "page_id": str, "email": str}
        """
        try:
            properties = {
                "Email": {"email": email}
            }

            response = self.client.pages.update(
                page_id=contact_id,
                properties=properties
            )

            return {
                "success": True,
                "page_id": contact_id,
                "email": email,
                "source": source,
                "url": f"https://notion.so/{contact_id.replace('-', '')}"
            }
        except Exception as e:
            return {"error": str(e), "success": False}

    def batch_create_or_update_companies(self, companies_data: list) -> Dict[str, Any]:
        """
        Create or update multiple companies in batch.

        Args:
            companies_data: List of dicts, each containing company data:
                {
                    "name": "Company Name",
                    "website": "https://company.com",
                    "linkedin": "https://linkedin.com/company/...",
                    "vertical": "Voice AI",
                    "icp": "3",
                    "product_description": "Brief description",
                    "asr_providers": ["Deepgram", "Assembly AI"],
                    "ai_engineers": 25,
                    "main_office_country": "United States"
                }

        Returns: {
            "success": bool,
            "total": int,
            "created": int,
            "updated": int,
            "failed": int,
            "results": [
                {
                    "company": str,
                    "action": "created|updated|failed",
                    "page_id": str,
                    "url": str,
                    "error": str (if failed)
                }
            ]
        }
        """
        results = []
        created_count = 0
        updated_count = 0
        failed_count = 0

        for company_data in companies_data:
            try:
                # Call the existing create_or_update_company method
                result = self.create_or_update_company(
                    company_name=company_data.get("name", ""),
                    website=company_data.get("website", ""),
                    linkedin=company_data.get("linkedin"),
                    vertical=company_data.get("vertical"),
                    icp=company_data.get("icp", "3"),
                    product_description=company_data.get("product_description"),
                    asr_providers=company_data.get("asr_providers"),
                    ai_engineers=company_data.get("ai_engineers"),
                    main_office_country=company_data.get("main_office_country"),
                    status=company_data.get("status", "Ice Box")
                )

                if result.get("success"):
                    action = result.get("action", "unknown")
                    if action == "created":
                        created_count += 1
                    elif action == "updated":
                        updated_count += 1

                    results.append({
                        "company": company_data.get("name", "Unknown"),
                        "action": action,
                        "page_id": result.get("page_id"),
                        "url": result.get("url")
                    })
                else:
                    failed_count += 1
                    results.append({
                        "company": company_data.get("name", "Unknown"),
                        "action": "failed",
                        "error": result.get("error", "Unknown error")
                    })
            except Exception as e:
                failed_count += 1
                results.append({
                    "company": company_data.get("name", "Unknown"),
                    "action": "failed",
                    "error": str(e)
                })

        return {
            "success": failed_count == 0,
            "total": len(companies_data),
            "created": created_count,
            "updated": updated_count,
            "failed": failed_count,
            "results": results
        }

    def add_contact(
        self,
        name: str,
        role: str,
        company_page_url: str,
        linkedin_url: str,
        email: Optional[str] = None,
        decision_level: str = "Decision Maker",
        campaign: Optional[str] = None,
        owner: str = "Benjamin Lalanne"
    ) -> Dict[str, Any]:
        """
        Add contact to People database.
        Returns: {"success": bool, "page_id": str, "url": str}
        """
        try:
            # Get owner user ID
            owner_id = self.get_user_id(owner)
            if not owner_id:
                return {"error": f"Could not find user: {owner}"}

            # Extract page ID from URL if it's a full URL
            if company_page_url.startswith("http"):
                # Extract ID from URLs like https://notion.so/xxxxx or https://www.notion.so/xxxxx
                company_id = company_page_url.split("/")[-1].replace("-", "")
                # Add dashes back in UUID format
                if len(company_id) == 32:
                    company_id = f"{company_id[:8]}-{company_id[8:12]}-{company_id[12:16]}-{company_id[16:20]}-{company_id[20:]}"
            else:
                company_id = company_page_url

            # Build properties
            properties = {
                "Contact_Name": {"title": [{"text": {"content": name}}]},
                "Role": {"rich_text": [{"text": {"content": role}}]},
                "Company name": {"relation": [{"id": company_id}]},
                "LinkedIn URL": {"url": linkedin_url},
                "Decision_Level": {"multi_select": [{"name": decision_level}]},
                "Type": {"multi_select": [{"name": "Customer"}]},
                "Status Contact": {"select": {"name": "🥶 Ice Box"}},
                "Source of contacts": {"select": {"name": "Outreach"}},
                "Owner / Assigned To": {"people": [{"id": owner_id}]}
            }

            # Add email if provided
            if email:
                properties["Email"] = {"email": email}

            # Add campaign if provided
            if campaign:
                properties["Campaign"] = {"multi_select": [{"name": campaign}]}

            # Create page
            response = self.client.pages.create(
                parent={"database_id": self.people_db},
                properties=properties
            )

            page_id = response["id"]
            page_url = f"https://notion.so/{page_id.replace('-', '')}"

            return {
                "success": True,
                "page_id": page_id,
                "url": page_url,
                "name": name,
                "role": role
            }
        except Exception as e:
            return {"error": str(e), "success": False}


def main():
    """CLI interface for contact operations."""
    if not NOTION_API_KEY:
        print(json.dumps({"error": "NOTION_API_KEY not set"}))
        sys.exit(1)

    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Missing command",
            "usage": "python scripts/notion_contact_ops.py <command> [options]",
            "commands": {
                "check-duplicate": "--linkedin <url>",
                "get-company": "--domain <domain>",
                "add-contact": "--name <name> --role <role> --company-id <id> --linkedin <url> [--email <email>] [--campaign <campaign>]",
                "create-or-update-company": "--name <name> --website <url> [--linkedin <url>] [--vertical <vertical>] [--icp <1-4>] [--product-desc <desc>] [--asr-providers <list>] [--ai-engineers <num>] [--country <country>]",
                "batch-create-companies": "--file <json_file>",
                "update-icp": "--company-id <id> --icp <1-4|N/A>",
                "search-contacts": "--name <name>",
                "get-contacts-without-email": "[--limit <num>]",
                "update-email": "--contact-id <id> --email <email> [--source <source>]"
            }
        }))
        sys.exit(1)

    command = sys.argv[1]
    manager = NotionContactManager(NOTION_API_KEY)

    # Parse arguments
    args = {}
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith("--"):
            key = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
                args[key] = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        else:
            i += 1

    # Execute command
    if command == "check-duplicate":
        if "linkedin" not in args:
            print(json.dumps({"error": "Missing --linkedin argument"}))
            sys.exit(1)
        result = manager.check_duplicate_by_linkedin(args["linkedin"])
        print(json.dumps(result, indent=2))

    elif command == "get-company":
        if "domain" not in args:
            print(json.dumps({"error": "Missing --domain argument"}))
            sys.exit(1)
        result = manager.get_company_by_domain(args["domain"])
        print(json.dumps(result, indent=2))

    elif command == "add-contact":
        required = ["name", "role", "company-id", "linkedin"]
        missing = [arg for arg in required if arg not in args]
        if missing:
            print(json.dumps({"error": f"Missing arguments: {', '.join(missing)}"}))
            sys.exit(1)

        result = manager.add_contact(
            name=args["name"],
            role=args["role"],
            company_page_url=args["company-id"],
            linkedin_url=args["linkedin"],
            email=args.get("email"),
            campaign=args.get("campaign")
        )
        print(json.dumps(result, indent=2))

    elif command == "create-or-update-company":
        required = ["name", "website"]
        missing = [arg for arg in required if arg not in args]
        if missing:
            print(json.dumps({"error": f"Missing arguments: {', '.join(missing)}"}))
            sys.exit(1)

        # Parse ASR providers list (comma-separated)
        asr_providers = None
        if "asr-providers" in args:
            asr_providers = [p.strip() for p in args["asr-providers"].split(",")]

        result = manager.create_or_update_company(
            company_name=args["name"],
            website=args["website"],
            linkedin=args.get("linkedin"),
            vertical=args.get("vertical"),
            icp=args.get("icp", "3"),
            product_description=args.get("product-desc"),
            asr_providers=asr_providers,
            ai_engineers=int(args["ai-engineers"]) if "ai-engineers" in args else None,
            main_office_country=args.get("country")
        )
        print(json.dumps(result, indent=2))

    elif command == "update-icp":
        required = ["company-id", "icp"]
        missing = [arg for arg in required if arg not in args]
        if missing:
            print(json.dumps({"error": f"Missing arguments: {', '.join(missing)}"}))
            sys.exit(1)

        result = manager.update_company_icp(args["company-id"], args["icp"])
        print(json.dumps(result, indent=2))

    elif command == "search-contacts":
        if "name" not in args:
            print(json.dumps({"error": "Missing --name argument"}))
            sys.exit(1)

        result = manager.search_contacts_by_name(args["name"])
        print(json.dumps(result, indent=2))

    elif command == "get-contacts-without-email":
        limit = int(args.get("limit", 50))
        result = manager.get_contacts_without_email(limit)
        print(json.dumps(result, indent=2))

    elif command == "update-email":
        required = ["contact-id", "email"]
        missing = [arg for arg in required if arg not in args]
        if missing:
            print(json.dumps({"error": f"Missing arguments: {', '.join(missing)}"}))
            sys.exit(1)

        result = manager.update_contact_email(
            args["contact-id"],
            args["email"],
            args.get("source")
        )
        print(json.dumps(result, indent=2))

    elif command == "batch-create-companies":
        if "file" not in args:
            print(json.dumps({"error": "Missing --file argument"}))
            sys.exit(1)

        # Load JSON file with company data
        try:
            file_path = Path(args["file"])
            if not file_path.exists():
                print(json.dumps({"error": f"File not found: {args['file']}"}))
                sys.exit(1)

            with open(file_path) as f:
                data = json.load(f)

            # Handle both formats: list directly or {"companies": [...]}
            if isinstance(data, list):
                companies_data = data
            elif isinstance(data, dict) and "companies" in data:
                companies_data = data["companies"]
            else:
                print(json.dumps({"error": "Invalid JSON format. Expected list or {\"companies\": [...]}"}))
                sys.exit(1)

            result = manager.batch_create_or_update_companies(companies_data)
            print(json.dumps(result, indent=2))

        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON file: {str(e)}"}))
            sys.exit(1)
        except Exception as e:
            print(json.dumps({"error": f"Error processing file: {str(e)}"}))
            sys.exit(1)

    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
