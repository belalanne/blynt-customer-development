#!/usr/bin/env python3
"""Sales Assistant - Entry point for the AI-powered sales research agent."""

import asyncio
import sys
from pathlib import Path

# Ensure the project root is in the path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config import Config
from src.agent import SalesAssistant


async def interactive_mode():
    """Run the sales assistant in interactive mode."""
    print("=" * 60)
    print("Sales Assistant - AI-powered Sales Research")
    print("=" * 60)
    print()

    # Load and validate config
    try:
        config = Config.from_env()
        warnings = config.validate()
        if warnings:
            print("Configuration warnings:")
            for warning in warnings:
                print(f"  - {warning}")
            print()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please copy .env.example to .env and set your API keys.")
        return

    print("Type 'quit' or 'exit' to stop.")
    print("Type 'help' for available commands.")
    print()

    async with SalesAssistant() as assistant:
        while True:
            try:
                prompt = input("You: ").strip()

                if not prompt:
                    continue

                if prompt.lower() in ("quit", "exit"):
                    print("Goodbye!")
                    break

                if prompt.lower() == "help":
                    print_help()
                    continue

                print("\nAssistant: ", end="", flush=True)
                response = await assistant.query(prompt)
                print(response)
                print()

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print()


def print_help():
    """Print help message."""
    print("""
Available commands:
  help              - Show this help message
  quit/exit         - Exit the assistant

Example queries:
  "Research the company vapi.ai"
  "Find 10 companies similar to otter.ai"
  "What ASR providers does fireflies.ai use?"
  "Save this company to Notion: ..."
  "Trigger the enrichment workflow for bland.ai"

ICP Classification:
  ICP 1 - Speech/Dictation Products
  ICP 2 - Meeting AI Assistants
  ICP 3 - Voice Agents Platforms
  ICP 4 - Custom Speech/Voice Solutions
  N/A   - Not a fit
""")


async def research_company(domain: str):
    """Research a single company."""
    async with SalesAssistant() as assistant:
        result = await assistant.research_company(domain)
        print(result)


async def find_lookalikes(domain: str, count: int = 10):
    """Find lookalike companies."""
    async with SalesAssistant() as assistant:
        result = await assistant.find_lookalikes(domain, count)
        print(result)


def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # Interactive mode
        asyncio.run(interactive_mode())
    elif sys.argv[1] == "research" and len(sys.argv) >= 3:
        # Research a specific company
        domain = sys.argv[2]
        asyncio.run(research_company(domain))
    elif sys.argv[1] == "lookalikes" and len(sys.argv) >= 3:
        # Find lookalike companies
        domain = sys.argv[2]
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        asyncio.run(find_lookalikes(domain, count))
    else:
        print("Usage:")
        print("  python main.py              - Interactive mode")
        print("  python main.py research <domain>")
        print("  python main.py lookalikes <domain> [count]")


if __name__ == "__main__":
    main()
