"""HTTP client utilities and factories."""

import httpx
from typing import Optional, Dict, Any
from loguru import logger


class HTTPClientConfig:
    """Configuration for HTTP clients."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 60.0,
        auth: Optional[tuple] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.auth = auth
        self.headers = headers or {}


def create_http_client(config: HTTPClientConfig) -> httpx.AsyncClient:
    """Create a configured async HTTP client."""
    return httpx.AsyncClient(
        base_url=config.base_url,
        timeout=config.timeout,
        auth=config.auth,
        headers=config.headers,
    )


def create_sync_http_client(config: HTTPClientConfig) -> httpx.Client:
    """Create a configured synchronous HTTP client."""
    return httpx.Client(
        base_url=config.base_url,
        timeout=config.timeout,
        auth=config.auth,
        headers=config.headers,
    )


async def safe_http_request(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    **kwargs: Any,
) -> Optional[Dict[str, Any]]:
    """
    Make an HTTP request with error handling and logging.

    Args:
        client: AsyncClient instance
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        **kwargs: Additional arguments to pass to client.request()

    Returns:
        Response JSON or None if request failed
    """
    try:
        response = await client.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        logger.error(f"HTTP request failed: {method} {url}: {e}")
        return None
    except Exception:
        logger.exception(f"Unexpected error during HTTP request: {method} {url}")
        return None
