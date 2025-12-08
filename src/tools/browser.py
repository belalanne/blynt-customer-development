"""Playwright browser automation - for when APIs aren't available."""

import base64
import os
from typing import Any, Optional

# Playwright is imported lazily to avoid startup overhead
_browser = None
_playwright = None


async def _get_browser():
    """Lazily initialize Playwright browser."""
    global _browser, _playwright

    if _browser is None:
        from playwright.async_api import async_playwright

        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )

    return _browser


async def _close_browser():
    """Close the browser when done."""
    global _browser, _playwright

    if _browser:
        await _browser.close()
        _browser = None

    if _playwright:
        await _playwright.stop()
        _playwright = None


async def browser_screenshot(
    url: str,
    full_page: bool = False,
    selector: Optional[str] = None,
    wait_for: Optional[str] = None,
    wait_timeout: int = 10000,
) -> dict[str, Any]:
    """Take a screenshot of a webpage.

    Args:
        url: URL to screenshot
        full_page: Capture full scrollable page (default False)
        selector: CSS selector to screenshot specific element (optional)
        wait_for: CSS selector to wait for before screenshot (optional)
        wait_timeout: Max wait time in ms (default 10000)

    Returns:
        Base64 encoded screenshot and page title
    """
    try:
        browser = await _get_browser()
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)

        if wait_for:
            await page.wait_for_selector(wait_for, timeout=wait_timeout)

        title = await page.title()

        if selector:
            element = await page.query_selector(selector)
            if element:
                screenshot = await element.screenshot()
            else:
                return {"error": f"Selector '{selector}' not found"}
        else:
            screenshot = await page.screenshot(full_page=full_page)

        await context.close()

        return {
            "screenshot_base64": base64.b64encode(screenshot).decode(),
            "title": title,
            "url": url,
        }

    except Exception as e:
        return {"error": f"Screenshot failed: {str(e)}"}


async def browser_extract_text(
    url: str,
    selector: Optional[str] = None,
    wait_for: Optional[str] = None,
    wait_timeout: int = 10000,
) -> dict[str, Any]:
    """Extract text content from a webpage.

    Args:
        url: URL to extract text from
        selector: CSS selector to extract specific element (optional, defaults to body)
        wait_for: CSS selector to wait for before extraction (optional)
        wait_timeout: Max wait time in ms (default 10000)

    Returns:
        Extracted text content and metadata
    """
    try:
        browser = await _get_browser()
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)

        if wait_for:
            await page.wait_for_selector(wait_for, timeout=wait_timeout)

        title = await page.title()

        if selector:
            elements = await page.query_selector_all(selector)
            texts = []
            for el in elements:
                text = await el.inner_text()
                texts.append(text.strip())
            content = "\n\n".join(texts)
        else:
            content = await page.inner_text("body")

        await context.close()

        return {
            "text": content[:50000],  # Limit to 50k chars
            "title": title,
            "url": url,
            "truncated": len(content) > 50000,
        }

    except Exception as e:
        return {"error": f"Text extraction failed: {str(e)}"}


async def browser_extract_html(
    url: str,
    selector: Optional[str] = None,
    wait_for: Optional[str] = None,
    wait_timeout: int = 10000,
) -> dict[str, Any]:
    """Extract HTML/DOM from a webpage.

    Args:
        url: URL to extract HTML from
        selector: CSS selector to extract specific element (optional)
        wait_for: CSS selector to wait for before extraction (optional)
        wait_timeout: Max wait time in ms (default 10000)

    Returns:
        HTML content and metadata
    """
    try:
        browser = await _get_browser()
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)

        if wait_for:
            await page.wait_for_selector(wait_for, timeout=wait_timeout)

        title = await page.title()

        if selector:
            element = await page.query_selector(selector)
            if element:
                html = await element.inner_html()
            else:
                return {"error": f"Selector '{selector}' not found"}
        else:
            html = await page.content()

        await context.close()

        return {
            "html": html[:100000],  # Limit to 100k chars
            "title": title,
            "url": url,
            "truncated": len(html) > 100000,
        }

    except Exception as e:
        return {"error": f"HTML extraction failed: {str(e)}"}


async def browser_extract_links(
    url: str,
    selector: Optional[str] = None,
    filter_pattern: Optional[str] = None,
) -> dict[str, Any]:
    """Extract all links from a webpage.

    Args:
        url: URL to extract links from
        selector: CSS selector to limit link extraction scope (optional)
        filter_pattern: Regex pattern to filter links (optional)

    Returns:
        List of links with text and href
    """
    import re

    try:
        browser = await _get_browser()
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)

        title = await page.title()

        # Find all links
        if selector:
            links = await page.query_selector_all(f"{selector} a")
        else:
            links = await page.query_selector_all("a")

        results = []
        for link in links:
            href = await link.get_attribute("href")
            text = await link.inner_text()

            if href:
                # Make absolute URL
                if href.startswith("/"):
                    from urllib.parse import urljoin
                    href = urljoin(url, href)

                # Apply filter if provided
                if filter_pattern:
                    if not re.search(filter_pattern, href):
                        continue

                results.append({
                    "text": text.strip()[:200],
                    "href": href,
                })

        await context.close()

        return {
            "links": results[:500],  # Limit to 500 links
            "total_found": len(results),
            "title": title,
            "url": url,
        }

    except Exception as e:
        return {"error": f"Link extraction failed: {str(e)}"}


async def browser_fill_and_submit(
    url: str,
    form_data: dict[str, str],
    submit_selector: Optional[str] = None,
    wait_after_submit: int = 3000,
) -> dict[str, Any]:
    """Fill a form and optionally submit it.

    Args:
        url: URL with the form
        form_data: Dict mapping selectors to values to fill
        submit_selector: CSS selector for submit button (optional)
        wait_after_submit: Ms to wait after submit (default 3000)

    Returns:
        Page content after form submission
    """
    try:
        browser = await _get_browser()
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Fill form fields
        for selector, value in form_data.items():
            await page.fill(selector, value)

        # Submit if selector provided
        if submit_selector:
            await page.click(submit_selector)
            await page.wait_for_timeout(wait_after_submit)

        title = await page.title()
        current_url = page.url
        content = await page.inner_text("body")

        await context.close()

        return {
            "text": content[:20000],
            "title": title,
            "url": current_url,
            "submitted": submit_selector is not None,
        }

    except Exception as e:
        return {"error": f"Form fill failed: {str(e)}"}


async def browser_scroll_and_capture(
    url: str,
    scroll_count: int = 3,
    scroll_delay: int = 1000,
) -> dict[str, Any]:
    """Scroll page to load dynamic content and capture full text.

    Useful for infinite scroll pages like LinkedIn feeds.

    Args:
        url: URL to scroll
        scroll_count: Number of scroll iterations (default 3)
        scroll_delay: Ms to wait between scrolls (default 1000)

    Returns:
        Full page text after scrolling
    """
    try:
        browser = await _get_browser()
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Scroll down multiple times to load dynamic content
        for _ in range(scroll_count):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(scroll_delay)

        title = await page.title()
        content = await page.inner_text("body")

        # Take full page screenshot
        screenshot = await page.screenshot(full_page=True)

        await context.close()

        return {
            "text": content[:50000],
            "screenshot_base64": base64.b64encode(screenshot).decode(),
            "title": title,
            "url": url,
            "scroll_count": scroll_count,
        }

    except Exception as e:
        return {"error": f"Scroll capture failed: {str(e)}"}
