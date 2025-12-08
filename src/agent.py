"""Sales Assistant Agent - AI-powered sales research using Claude Agent SDK."""

import json
import os
from typing import Any, Optional
from pathlib import Path

from claude_agent_sdk import (
    AgentDefinition,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError,
    create_sdk_mcp_server,
    tool,
)

from .tools import (
    exa_search,
    exa_find_similar,
    tavily_search,
    tavily_extract,
    notion_save_company,
    notion_search,
    notion_update_company,
    n8n_trigger_workflow,
    n8n_enrich_company,
    n8n_enrich_person,
    browser_screenshot,
    browser_extract_text,
    browser_extract_html,
    browser_extract_links,
    browser_scroll_and_capture,
)
from .tools.notion import notion_find_by_website, notion_save_company_if_not_exists


# System prompt for the sales assistant
SALES_ASSISTANT_PROMPT = """You are a Sales Research Assistant for Blynt, a company that provides real-time transcription APIs with advanced features like natural turn-taking, keyword boosting, and interruption handling.

## Your Role
Help the sales team research companies that might benefit from Blynt's products. You can:
1. Trigger n8n workflows for enrichment (fastest, uses integrated data sources)
2. Search for company information using web search (Exa or Tavily)
3. Find lookalike companies similar to existing customers
4. Discover what voice/speech infrastructure companies use (ASR, TTS, LLM providers)
5. Save research findings to Notion
6. Use browser automation (Playwright) when APIs don't provide enough data

## Tool Priority Strategy (IMPORTANT)

When researching a company, **always follow this priority order**:

### Priority 1: n8n Workflows (Try First)
- Use `n8n_enrich_company` for company data (domain required)
- Use `n8n_enrich_person` for people/contacts (linkedin_url, email, or name required)
- n8n has integrations with Apollo, Clearbit, and other data providers
- This is the fastest and most reliable source for firmographics, contacts, funding
- **Check the response**: If data is complete (name, industry, size, contacts), you may skip lower priorities

### Priority 2: Web Search (Fill Gaps)
- Use `exa_web_search` for technical content, job postings, news
- Use `tavily_search` for general company info with AI-summarized answers
- Use `exa_find_lookalikes` to find similar companies
- **When to use**: n8n returned incomplete data, or you need tech stack / voice infrastructure details

### Priority 3: Playwright Browser (Last Resort)
- Use `browser_extract_text` for JavaScript-heavy pages (LinkedIn, SPAs)
- Use `browser_screenshot` for visual proof or pricing pages
- Use `browser_scroll_capture` for infinite-scroll content
- Use `browser_extract_links` to find careers pages, documentation
- **When to use**: Web search APIs couldn't access the content (LinkedIn profiles, gated pages, heavy JS rendering)

### Decision Flow Example
```
User: "Research vapi.ai and find key contacts"

1. First: n8n_enrich_company(domain="vapi.ai")
   → Got: name, funding, employee count, location
   → Missing: tech stack, ASR providers

2. Then: exa_web_search("vapi.ai voice AI technology stack ASR")
   → Got: Uses Deepgram, ElevenLabs, WebRTC
   → Found: CEO name "Jordan Dearsley"

3. Then: n8n_enrich_person(name="Jordan Dearsley", company="Vapi")
   → Got: Email, LinkedIn, title
   → Missing: LinkedIn details

4. Finally: browser_extract_text("https://linkedin.com/in/jordandearsley")
   → Got: Full profile, background
   → Complete!
```

### Skip Rules
- Skip n8n if user explicitly says "search the web" or "use Exa/Tavily"
- Skip Playwright if APIs already returned complete data
- Go directly to Playwright if user asks for "screenshot" or "scrape"

## Target Market (ICP Classification)
When researching companies, classify them into one of these ICPs:

- **ICP 1**: Speech/Dictation Products - Companies adding speech or dictation to their product (healthcare documentation, legal transcription, note-taking apps)
- **ICP 2**: Meeting AI Assistants - Companies building meeting transcription or conversation intelligence (like Otter.ai, Gong, Fireflies)
- **ICP 3**: Voice Agents Platforms - Companies building voice agent platforms or AI phone assistants (like Vapi, Bland AI)
- **ICP 4**: Custom Speech/Voice Solutions - Companies building proprietary voice infrastructure
- **N/A**: Not a fit for Blynt's products

## Research Focus
When analyzing a company's tech stack, focus on:

**Priority 1 - Transport & Framework:**
- Transport protocol: WebRTC, WebSockets, SIP
- Real-time framework: LiveKit, Pipecat, Daily, Agora, Twilio
- Agentic framework: Vapi, LiveKit Agents, Retell, Vocode

**Priority 2 - Speech Stack:**
- ASR provider: Deepgram, Gladia, Assembly AI, Azure Speech, Whisper
- LLM provider: OpenAI, Anthropic, Google Gemini, Azure OpenAI
- TTS provider: ElevenLabs, Play.ht, Deepgram Aura, Azure TTS

**Ignore:** General hosting (AWS, GCP), CDN, analytics, marketing tools

## Guidelines
- Always cite your sources with URLs
- Distinguish between confirmed facts and inferences
- Check for duplicates before saving to Notion
- Keep product descriptions to 5 words or less
- Be concise and focus on actionable intelligence

## Interactive Clarifications
Use the AskUserQuestion tool to clarify when:
- Multiple companies match a search (ask which one to research)
- Unclear ICP classification (ask user to confirm)
- Before saving to Notion (confirm data is correct)
- Multiple possible approaches (ask user preference)
- Missing critical information (ask user to provide it)

Example situations to ask:
- "I found 3 companies named 'Olivya'. Which one?" → AskUserQuestion with options
- "This company could be ICP 2 or ICP 3. Which fits better?" → AskUserQuestion
- "Ready to save to Notion. Confirm these details?" → AskUserQuestion
"""


# Subagent definitions for specialized tasks
SUBAGENTS = {
    "company-researcher": AgentDefinition(
        description="Researches companies using enrichment APIs and web search",
        prompt="""You are a Company Research Specialist. Gather company information using:
1. n8n_enrich_company (try first - fastest)
2. exa_web_search (for additional context)
3. tavily_search (for AI-summarized answers)

Return structured data: company_name, website, industry, employee_count, country, funding, description (5 words max), sources.""",
        tools=[
            "mcp__sales__n8n_enrich_company",
            "mcp__sales__exa_web_search",
            "mcp__sales__tavily_search",
        ],
        model="haiku",
    ),
    "stack-discoverer": AgentDefinition(
        description="Discovers voice/speech technology stack for companies",
        prompt="""You are a Voice Technology Stack Analyst. Find what ASR, TTS, LLM, and real-time infrastructure a company uses.

Look for: Deepgram, Gladia, Assembly AI (ASR); ElevenLabs, Play.ht (TTS); WebRTC, LiveKit, Pipecat (frameworks).

Search: privacy policies, subprocessor lists, job postings, technical docs, GitHub repos.
IGNORE: AWS, GCP, Cloudflare, analytics, payment processors.""",
        tools=[
            "mcp__sales__exa_web_search",
            "mcp__sales__tavily_search",
            "mcp__sales__tavily_extract_content",
            "mcp__sales__browser_extract_text",
        ],
        model="sonnet",
    ),
    "notion-syncer": AgentDefinition(
        description="Syncs company data to Notion database",
        prompt="""You are a Notion Database Manager. Handle Notion operations:
1. ALWAYS check for duplicates by website domain first
2. Only create if no duplicate exists
3. Required fields: company_name, website, vertical, icp (1-4 or N/A), product_description (5 words max)

Report: action taken, Notion page URL, fields updated.""",
        tools=[
            "mcp__sales__notion_search_companies",
            "mcp__sales__notion_save_company",
            "mcp__sales__notion_update_company",
        ],
        model="haiku",
    ),
    "contact-finder": AgentDefinition(
        description="Finds and enriches contact information for key people",
        prompt="""You are a Contact Research Specialist. Find decision makers:
Priority: CTO, VP Engineering, Head of AI, Founder/CEO.

1. Search for names/LinkedIn URLs with exa_web_search
2. Enrich with n8n_enrich_person
3. Browser fallback for LinkedIn profiles

Return: name, title, email, linkedin, source.""",
        tools=[
            "mcp__sales__n8n_enrich_person",
            "mcp__sales__exa_web_search",
            "mcp__sales__browser_extract_text",
        ],
        model="haiku",
    ),
    "lookalike-finder": AgentDefinition(
        description="Finds companies similar to a given company",
        prompt="""You are a Lookalike Company Researcher. Find similar companies:
1. Use exa_find_lookalikes with target company URL
2. Filter for voice/speech AI companies
3. Classify each by ICP (1=Dictation, 2=Meeting AI, 3=Voice Agents, 4=Custom Voice)

Return ranked list with: company, domain, description, icp, fit_score, reasoning.""",
        tools=[
            "mcp__sales__exa_find_lookalikes",
            "mcp__sales__exa_web_search",
        ],
        model="haiku",
    ),
}


# Define tools using the @tool decorator
@tool(
    "exa_web_search",
    "Search the web for company information, news, and technical content using Exa AI",
    {
        "query": str,
        "num_results": int,
        "category": str,
        "include_domains": list,
    },
)
async def tool_exa_search(args: dict[str, Any]) -> dict[str, Any]:
    """Execute Exa web search."""
    result = await exa_search(
        query=args["query"],
        num_results=args.get("num_results", 10),
        category=args.get("category"),
        include_domains=args.get("include_domains"),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "exa_find_lookalikes",
    "Find companies similar to a given company URL",
    {"url": str, "num_results": int},
)
async def tool_exa_find_similar(args: dict[str, Any]) -> dict[str, Any]:
    """Find similar companies using Exa."""
    result = await exa_find_similar(
        url=args["url"],
        num_results=args.get("num_results", 10),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "tavily_search",
    "Search the web using Tavily AI with AI-generated answers",
    {
        "query": str,
        "search_depth": str,
        "max_results": int,
    },
)
async def tool_tavily_search(args: dict[str, Any]) -> dict[str, Any]:
    """Execute Tavily search."""
    result = await tavily_search(
        query=args["query"],
        search_depth=args.get("search_depth", "basic"),
        max_results=args.get("max_results", 10),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "tavily_extract_content",
    "Extract content from specific URLs using Tavily",
    {"urls": list},
)
async def tool_tavily_extract(args: dict[str, Any]) -> dict[str, Any]:
    """Extract content from URLs."""
    result = await tavily_extract(urls=args["urls"])
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "notion_search_companies",
    "Search the Notion database for existing companies",
    {"query": str, "filter_property": str},
)
async def tool_notion_search(args: dict[str, Any]) -> dict[str, Any]:
    """Search Notion for companies."""
    result = await notion_search(
        query=args["query"],
        filter_property=args.get("filter_property"),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "notion_save_company",
    "Save a company to Notion database. Check for duplicates first using the website URL.",
    {
        "company_name": str,
        "website": str,
        "linkedin_url": str,
        "vertical": str,
        "icp": str,
        "product_description": str,
        "asr_providers": list,
        "ai_ml_engineers": int,
        "country": str,
    },
)
async def tool_notion_save(args: dict[str, Any]) -> dict[str, Any]:
    """Save company to Notion."""
    # Check for duplicates first
    existing = await notion_find_by_website(args["website"])
    if existing:
        return {
            "content": [{
                "type": "text",
                "text": f"Company already exists in Notion: {existing.get('id')}",
            }]
        }

    result = await notion_save_company(
        company_name=args["company_name"],
        website=args["website"],
        linkedin_url=args.get("linkedin_url"),
        vertical=args.get("vertical"),
        icp=args.get("icp"),
        product_description=args.get("product_description"),
        asr_providers=args.get("asr_providers"),
        ai_ml_engineers=args.get("ai_ml_engineers"),
        country=args.get("country"),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "notion_update_company",
    "Update an existing company in Notion",
    {"page_id": str, "updates": dict},
)
async def tool_notion_update(args: dict[str, Any]) -> dict[str, Any]:
    """Update company in Notion."""
    result = await notion_update_company(
        page_id=args["page_id"],
        updates=args["updates"],
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "n8n_enrich_company",
    "Enrich company data via n8n workflow. Returns firmographics, funding, contacts from Apollo/Clearbit.",
    {
        "domain": str,
        "company_name": str,
    },
)
async def tool_n8n_enrich_company(args: dict[str, Any]) -> dict[str, Any]:
    """Enrich company via n8n."""
    result = await n8n_enrich_company(
        domain=args["domain"],
        company_name=args.get("company_name"),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "n8n_enrich_person",
    "Enrich person/contact data via n8n workflow. Returns email, title, social profiles.",
    {
        "linkedin_url": str,
        "email": str,
        "name": str,
        "company": str,
    },
)
async def tool_n8n_enrich_person(args: dict[str, Any]) -> dict[str, Any]:
    """Enrich person via n8n."""
    result = await n8n_enrich_person(
        linkedin_url=args.get("linkedin_url"),
        email=args.get("email"),
        name=args.get("name"),
        company=args.get("company"),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


# Browser automation tools (Playwright)
@tool(
    "browser_screenshot",
    "Take a screenshot of a webpage. Use when you need visual proof or the page uses heavy JS rendering.",
    {
        "url": str,
        "full_page": bool,
        "selector": str,
        "wait_for": str,
    },
)
async def tool_browser_screenshot(args: dict[str, Any]) -> dict[str, Any]:
    """Take webpage screenshot."""
    result = await browser_screenshot(
        url=args["url"],
        full_page=args.get("full_page", False),
        selector=args.get("selector"),
        wait_for=args.get("wait_for"),
    )
    if "error" in result:
        return {"content": [{"type": "text", "text": json.dumps(result)}]}

    return {
        "content": [
            {"type": "text", "text": f"Screenshot of {result['title']} ({result['url']})"},
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": result["screenshot_base64"],
                },
            },
        ]
    }


@tool(
    "browser_extract_text",
    "Extract text content from a webpage. Use for JS-heavy pages that APIs can't scrape.",
    {
        "url": str,
        "selector": str,
        "wait_for": str,
    },
)
async def tool_browser_extract_text(args: dict[str, Any]) -> dict[str, Any]:
    """Extract text from webpage."""
    result = await browser_extract_text(
        url=args["url"],
        selector=args.get("selector"),
        wait_for=args.get("wait_for"),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "browser_extract_html",
    "Extract raw HTML/DOM from a webpage. Use when you need structured data from the page.",
    {
        "url": str,
        "selector": str,
        "wait_for": str,
    },
)
async def tool_browser_extract_html(args: dict[str, Any]) -> dict[str, Any]:
    """Extract HTML from webpage."""
    result = await browser_extract_html(
        url=args["url"],
        selector=args.get("selector"),
        wait_for=args.get("wait_for"),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "browser_extract_links",
    "Extract all links from a webpage. Useful for finding subpages, careers pages, etc.",
    {
        "url": str,
        "selector": str,
        "filter_pattern": str,
    },
)
async def tool_browser_extract_links(args: dict[str, Any]) -> dict[str, Any]:
    """Extract links from webpage."""
    result = await browser_extract_links(
        url=args["url"],
        selector=args.get("selector"),
        filter_pattern=args.get("filter_pattern"),
    )
    return {
        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
    }


@tool(
    "browser_scroll_capture",
    "Scroll a page to load dynamic content (infinite scroll) then capture text and screenshot.",
    {
        "url": str,
        "scroll_count": int,
        "scroll_delay": int,
    },
)
async def tool_browser_scroll_capture(args: dict[str, Any]) -> dict[str, Any]:
    """Scroll and capture webpage."""
    result = await browser_scroll_and_capture(
        url=args["url"],
        scroll_count=args.get("scroll_count", 3),
        scroll_delay=args.get("scroll_delay", 1000),
    )
    if "error" in result:
        return {"content": [{"type": "text", "text": json.dumps(result)}]}

    return {
        "content": [
            {"type": "text", "text": f"Scrolled {result['scroll_count']}x: {result['title']}\n\n{result['text'][:5000]}"},
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": result["screenshot_base64"],
                },
            },
        ]
    }


def create_sales_tools_server():
    """Create MCP server with all sales assistant tools."""
    return create_sdk_mcp_server(
        name="sales-tools",
        version="1.0.0",
        tools=[
            # Search tools
            tool_exa_search,
            tool_exa_find_similar,
            tool_tavily_search,
            tool_tavily_extract,
            # Notion tools
            tool_notion_search,
            tool_notion_save,
            tool_notion_update,
            # n8n enrichment tools
            tool_n8n_enrich_company,
            tool_n8n_enrich_person,
            # Browser tools (Playwright)
            tool_browser_screenshot,
            tool_browser_extract_text,
            tool_browser_extract_html,
            tool_browser_extract_links,
            tool_browser_scroll_capture,
        ],
    )


def create_agent_options(
    system_prompt: str | None = None,
    permission_mode: str | None = None,
    include_subagents: bool = True,
    setting_sources: list[str] | None = None,
) -> ClaudeAgentOptions:
    """Create agent options with sales tools.

    Args:
        system_prompt: Custom system prompt (uses default if None)
        permission_mode: Permission mode for tool execution (default from env or "default")
        include_subagents: Whether to include subagent definitions
        setting_sources: Settings sources to load (default: ["project"])

    Returns:
        Configured ClaudeAgentOptions
    """
    sales_server = create_sales_tools_server()

    # Get permission mode from env or use default
    mode = permission_mode or os.getenv("AGENT_PERMISSION_MODE", "default")

    # Get project root for setting sources
    project_root = Path(__file__).parent.parent

    options = ClaudeAgentOptions(
        system_prompt=system_prompt or SALES_ASSISTANT_PROMPT,
        mcp_servers={"sales": sales_server},
        allowed_tools=[
            # Search tools
            "mcp__sales__exa_web_search",
            "mcp__sales__exa_find_lookalikes",
            "mcp__sales__tavily_search",
            "mcp__sales__tavily_extract_content",
            # Notion tools
            "mcp__sales__notion_search_companies",
            "mcp__sales__notion_save_company",
            "mcp__sales__notion_update_company",
            # n8n enrichment tools
            "mcp__sales__n8n_enrich_company",
            "mcp__sales__n8n_enrich_person",
            # Browser tools (Playwright)
            "mcp__sales__browser_screenshot",
            "mcp__sales__browser_extract_text",
            "mcp__sales__browser_extract_html",
            "mcp__sales__browser_extract_links",
            "mcp__sales__browser_scroll_capture",
            # Task tool for subagents
            "Task",
            # Interactive tools
            "AskUserQuestion",
        ],
        permission_mode=mode,
        setting_sources=setting_sources if setting_sources is not None else ["project"],
        cwd=str(project_root),
        agents=SUBAGENTS if include_subagents else None,
    )

    return options


class SalesAssistantError(Exception):
    """Base exception for Sales Assistant errors."""
    pass


class CLINotInstalledError(SalesAssistantError):
    """Raised when Claude Code CLI is not installed."""
    pass


class AgentExecutionError(SalesAssistantError):
    """Raised when agent execution fails."""

    def __init__(self, message: str, exit_code: int = None, stderr: str = None):
        super().__init__(message)
        self.exit_code = exit_code
        self.stderr = stderr


class SalesAssistant:
    """High-level interface for the Sales Assistant agent."""

    def __init__(
        self,
        system_prompt: str | None = None,
        permission_mode: str | None = None,
        include_subagents: bool = True,
        session_id: str | None = None,
    ):
        """Initialize the Sales Assistant.

        Args:
            system_prompt: Custom system prompt
            permission_mode: Permission mode for tool execution
            include_subagents: Whether to include subagent definitions
            session_id: Resume a previous session by ID
        """
        self.options = create_agent_options(
            system_prompt=system_prompt,
            permission_mode=permission_mode,
            include_subagents=include_subagents,
        )
        self._client: ClaudeSDKClient | None = None
        self._session_id = session_id
        self._current_session_id: str | None = None

    @property
    def session_id(self) -> str | None:
        """Get the current session ID for resuming conversations."""
        return self._current_session_id

    async def __aenter__(self) -> "SalesAssistant":
        """Enter async context."""
        try:
            if self._session_id:
                # Resume existing session
                self._client = ClaudeSDKClient(
                    options=self.options,
                    resume=self._session_id,
                )
            else:
                self._client = ClaudeSDKClient(options=self.options)
            await self._client.__aenter__()
            return self
        except CLINotFoundError as e:
            raise CLINotInstalledError(
                "Claude Code CLI not found. Please install it first: "
                "https://docs.claude.com/en/api/agent-sdk/overview"
            ) from e

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context."""
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def query(self, prompt: str) -> str:
        """Send a query to the assistant and get a response.

        Args:
            prompt: User query

        Returns:
            Assistant response text

        Raises:
            RuntimeError: If not used as async context manager
            AgentExecutionError: If agent execution fails
        """
        if not self._client:
            raise RuntimeError("SalesAssistant must be used as async context manager")

        try:
            await self._client.query(prompt)

            response_parts = []
            async for message in self._client.receive_response():
                if isinstance(message, dict):
                    if message.get("type") == "text":
                        response_parts.append(message.get("text", ""))
                    # Capture session ID if provided
                    if "session_id" in message:
                        self._current_session_id = message["session_id"]
                elif isinstance(message, str):
                    response_parts.append(message)

            return "".join(response_parts)

        except ProcessError as e:
            raise AgentExecutionError(
                f"Agent execution failed: {e}",
                exit_code=getattr(e, "exit_code", None),
                stderr=getattr(e, "stderr", None),
            ) from e
        except CLIJSONDecodeError as e:
            raise AgentExecutionError(
                f"Failed to parse agent response: {e}"
            ) from e

    async def interrupt(self) -> None:
        """Interrupt the current operation."""
        if self._client:
            await self._client.interrupt()

    async def research_company(self, domain: str) -> str:
        """Research a company by domain.

        Args:
            domain: Company domain to research

        Returns:
            Research findings
        """
        prompt = f"""Research the company at {domain}:
1. Find basic company information (name, industry, size, location)
2. Identify their voice/speech technology stack if applicable
3. Determine ICP classification (1-4 or N/A)
4. Find key contacts if available

Provide a summary with sources."""
        return await self.query(prompt)

    async def find_lookalikes(self, domain: str, count: int = 10) -> str:
        """Find companies similar to the given domain.

        Args:
            domain: Company domain to find lookalikes for
            count: Number of lookalikes to find

        Returns:
            Lookalike companies
        """
        prompt = f"""Find {count} companies similar to {domain}:
1. Use Exa to find lookalike companies
2. For each company, provide: name, domain, brief description
3. Rate their potential fit for Blynt's products

Focus on companies in the voice/speech AI space."""
        return await self.query(prompt)

    async def save_to_notion(self, company_data: dict[str, Any]) -> str:
        """Save company data to Notion.

        Args:
            company_data: Company data to save

        Returns:
            Save result
        """
        prompt = f"""Save this company to Notion:
{json.dumps(company_data, indent=2)}

Check for duplicates first using the website URL."""
        return await self.query(prompt)

    async def discover_stack(self, domain: str) -> str:
        """Discover a company's voice/speech technology stack.

        Args:
            domain: Company domain to analyze

        Returns:
            Technology stack findings
        """
        prompt = f"""Use the stack-discoverer subagent to analyze {domain}'s voice technology stack.

Focus on:
- ASR providers (Deepgram, Gladia, Assembly AI, etc.)
- TTS providers (ElevenLabs, Play.ht, etc.)
- Real-time frameworks (LiveKit, Pipecat, WebRTC)
- LLM providers

Search their privacy policy, subprocessor list, job postings, and technical docs."""
        return await self.query(prompt)

    async def deep_dive(self, domain: str) -> str:
        """Perform a complete deep-dive analysis on a company.

        Args:
            domain: Company domain to analyze

        Returns:
            Complete analysis including research, stack, contacts, and Notion sync
        """
        prompt = f"""Perform a complete deep-dive analysis on {domain}:

1. Use company-researcher subagent for firmographics
2. Use stack-discoverer subagent for voice tech stack
3. Use contact-finder subagent for key decision makers
4. Classify ICP (1-4 or N/A)
5. Use notion-syncer subagent to save all findings

Provide a comprehensive report with all findings and the Notion page URL."""
        return await self.query(prompt)
