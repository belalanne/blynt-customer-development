"""Tests for utility functions."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from src.utils import (
    RetryConfig,
    calculate_delay,
    http_request,
)


class TestRetryConfig:
    """Tests for RetryConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 30.0
        assert config.exponential_base == 2.0
        assert config.jitter is True

    def test_custom_values(self):
        """Test custom configuration values."""
        config = RetryConfig(
            max_retries=5,
            base_delay=2.0,
            max_delay=60.0,
        )
        assert config.max_retries == 5
        assert config.base_delay == 2.0
        assert config.max_delay == 60.0


class TestCalculateDelay:
    """Tests for calculate_delay function."""

    def test_first_attempt(self):
        """Test delay for first attempt."""
        config = RetryConfig(base_delay=1.0, jitter=False)
        delay = calculate_delay(0, config)
        assert delay == 1.0

    def test_exponential_backoff(self):
        """Test exponential backoff without jitter."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=False)

        assert calculate_delay(0, config) == 1.0
        assert calculate_delay(1, config) == 2.0
        assert calculate_delay(2, config) == 4.0
        assert calculate_delay(3, config) == 8.0

    def test_max_delay_cap(self):
        """Test that delay is capped at max_delay."""
        config = RetryConfig(
            base_delay=1.0,
            exponential_base=2.0,
            max_delay=5.0,
            jitter=False,
        )

        # 2^10 = 1024, but should be capped at 5.0
        delay = calculate_delay(10, config)
        assert delay == 5.0

    def test_jitter_range(self):
        """Test that jitter keeps delay within expected range."""
        config = RetryConfig(
            base_delay=2.0,
            exponential_base=2.0,
            max_delay=100.0,
            jitter=True,
        )

        # Run multiple times to check jitter
        delays = [calculate_delay(1, config) for _ in range(100)]

        # Base delay at attempt 1 is 4.0
        # With jitter, should be between 2.0 (0.5 * 4) and 6.0 (1.5 * 4)
        for delay in delays:
            assert 2.0 <= delay <= 6.0


class TestHttpRequest:
    """Tests for http_request function."""

    @pytest.mark.asyncio
    async def test_successful_request(self):
        """Test successful HTTP request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await http_request(
                method="GET",
                url="https://api.example.com/test",
            )

            assert result["status_code"] == 200
            assert result["data"] == {"success": True}
            assert "error" not in result

    @pytest.mark.asyncio
    async def test_error_response(self):
        """Test HTTP error response."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not found"}

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await http_request(
                method="GET",
                url="https://api.example.com/notfound",
            )

            assert result["status_code"] == 404
            assert "error" in result
