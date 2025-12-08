"""Shared utilities for the Sales Assistant."""

import asyncio
import functools
import random
from typing import Any, Callable, Optional, Type, TypeVar

import httpx

from .logging_config import get_logger

logger = get_logger("utils")

T = TypeVar("T")


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: tuple = (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
        ),
        retryable_status_codes: tuple = (429, 500, 502, 503, 504),
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions
        self.retryable_status_codes = retryable_status_codes


DEFAULT_RETRY_CONFIG = RetryConfig()


def calculate_delay(
    attempt: int,
    config: RetryConfig,
) -> float:
    """Calculate delay before next retry with exponential backoff.

    Args:
        attempt: Current attempt number (0-indexed)
        config: Retry configuration

    Returns:
        Delay in seconds
    """
    delay = config.base_delay * (config.exponential_base ** attempt)
    delay = min(delay, config.max_delay)

    if config.jitter:
        # Add random jitter (0.5x to 1.5x)
        delay = delay * (0.5 + random.random())

    return delay


def retry_async(
    config: Optional[RetryConfig] = None,
    on_retry: Optional[Callable[[int, Exception], None]] = None,
):
    """Decorator for async functions with retry logic.

    Args:
        config: Retry configuration
        on_retry: Optional callback when retry occurs

    Returns:
        Decorated function
    """
    if config is None:
        config = DEFAULT_RETRY_CONFIG

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e

                    # Check if HTTP status code is retryable
                    if isinstance(e, httpx.HTTPStatusError):
                        if e.response.status_code not in config.retryable_status_codes:
                            raise

                    if attempt < config.max_retries:
                        delay = calculate_delay(attempt, config)
                        logger.warning(
                            f"Retry {attempt + 1}/{config.max_retries} for {func.__name__} "
                            f"after {delay:.2f}s due to: {e}"
                        )

                        if on_retry:
                            on_retry(attempt, e)

                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {config.max_retries} retries exhausted for {func.__name__}"
                        )
                        raise

            raise last_exception

        return wrapper

    return decorator


class AsyncHTTPClient:
    """Async HTTP client with retry logic and logging."""

    def __init__(
        self,
        base_url: str = "",
        headers: Optional[dict[str, str]] = None,
        timeout: float = 30.0,
        retry_config: Optional[RetryConfig] = None,
    ):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
        self.retry_config = retry_config or DEFAULT_RETRY_CONFIG
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "AsyncHTTPClient":
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")

        last_exception = None
        config = self.retry_config

        for attempt in range(config.max_retries + 1):
            try:
                logger.debug(f"{method.upper()} {url} (attempt {attempt + 1})")
                response = await self._client.request(method, url, **kwargs)

                # Check for retryable status codes
                if response.status_code in config.retryable_status_codes:
                    if attempt < config.max_retries:
                        delay = calculate_delay(attempt, config)
                        logger.warning(
                            f"Retrying {method} {url} after {delay:.2f}s "
                            f"(status {response.status_code})"
                        )
                        await asyncio.sleep(delay)
                        continue
                    else:
                        response.raise_for_status()

                logger.debug(f"{method.upper()} {url} -> {response.status_code}")
                return response

            except config.retryable_exceptions as e:
                last_exception = e
                if attempt < config.max_retries:
                    delay = calculate_delay(attempt, config)
                    logger.warning(
                        f"Retrying {method} {url} after {delay:.2f}s due to: {e}"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Request failed after {config.max_retries} retries: {e}")
                    raise

        raise last_exception

    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self._request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        return await self._request("POST", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> httpx.Response:
        return await self._request("PATCH", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> httpx.Response:
        return await self._request("DELETE", url, **kwargs)


async def http_request(
    method: str,
    url: str,
    headers: Optional[dict[str, str]] = None,
    json: Optional[dict[str, Any]] = None,
    timeout: float = 30.0,
    retry_config: Optional[RetryConfig] = None,
) -> dict[str, Any]:
    """Make a single HTTP request with retry logic.

    Args:
        method: HTTP method
        url: Request URL
        headers: Request headers
        json: JSON body
        timeout: Request timeout
        retry_config: Retry configuration

    Returns:
        Response as dict with 'status_code', 'data', and optionally 'error'
    """
    config = retry_config or DEFAULT_RETRY_CONFIG
    last_exception = None

    for attempt in range(config.max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                logger.debug(f"{method.upper()} {url} (attempt {attempt + 1})")

                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    json=json,
                )

                # Check for retryable status codes
                if response.status_code in config.retryable_status_codes:
                    if attempt < config.max_retries:
                        delay = calculate_delay(attempt, config)
                        logger.warning(
                            f"Retrying {method} {url} after {delay:.2f}s "
                            f"(status {response.status_code})"
                        )
                        await asyncio.sleep(delay)
                        continue

                logger.debug(f"{method.upper()} {url} -> {response.status_code}")

                # Try to parse JSON
                try:
                    data = response.json()
                except Exception:
                    data = {"text": response.text}

                if response.status_code >= 400:
                    return {
                        "status_code": response.status_code,
                        "error": f"HTTP {response.status_code}",
                        "data": data,
                    }

                return {
                    "status_code": response.status_code,
                    "data": data,
                }

        except config.retryable_exceptions as e:
            last_exception = e
            if attempt < config.max_retries:
                delay = calculate_delay(attempt, config)
                logger.warning(f"Retrying {method} {url} after {delay:.2f}s due to: {e}")
                await asyncio.sleep(delay)
            else:
                logger.error(f"Request failed after {config.max_retries} retries: {e}")
                return {
                    "status_code": 0,
                    "error": str(e),
                    "data": None,
                }

    return {
        "status_code": 0,
        "error": str(last_exception),
        "data": None,
    }
