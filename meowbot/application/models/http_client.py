import aiohttp
import asyncio
import logging
from enum import Enum
from typing import Any, Dict, Optional, Union


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HttpClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        """
        Initialize the HttpClient.

        Args:
            base_url (str): The base URL for all requests.
            headers (dict): Default headers for requests.
            timeout (int): Timeout for requests in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.default_headers = headers or {"User-Agent": "HttpClient/1.0"}
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Set up the client session when entering async context."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the client session when exiting async context."""
        await self.close()

    async def _ensure_session(self):
        """Ensure a session exists, creating it if necessary."""
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=self.timeout, headers=self.default_headers)

    async def close(self):
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None

    def _format_url(self, endpoint: str) -> str:
        """Format the full URL for the request."""
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    async def request(
        self, method: HttpMethod, endpoint: str, **kwargs
    ) -> Union[Dict[str, Any], str]:
        """
        Perform an HTTP request.

        Args:
            method (HttpMethod): The HTTP method to use.
            endpoint (str): The API endpoint (relative to base_url).
            **kwargs: Additional arguments to pass to aiohttp (e.g., params, json, headers).

        Returns:
            Response JSON or text.
        """
        await self._ensure_session()
        url = self._format_url(endpoint)

        # Merge default headers with per-request headers
        headers = kwargs.pop("headers", {})
        headers = {**self.default_headers, **headers}

        try:
            async with self.session.request(
                method.value, url, headers=headers, **kwargs
            ) as response:
                response.raise_for_status()
                if "application/json" in response.headers.get("Content-Type", ""):
                    return await response.json()
                return await response.text()
        except aiohttp.ClientResponseError as e:
            logging.error(f"HTTP Error {e.status} for {method.value} {url}: {e.message}")
            raise
        except asyncio.TimeoutError:
            logging.error(f"Request timed out for {method.value} {url}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during {method.value} {url}: {e}")
            raise

    async def get(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        """Perform a GET request."""
        return await self.request(HttpMethod.GET, endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        """Perform a POST request."""
        return await self.request(HttpMethod.POST, endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        """Perform a PUT request."""
        return await self.request(HttpMethod.PUT, endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        """Perform a DELETE request."""
        return await self.request(HttpMethod.DELETE, endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        """Perform a PATCH request."""
        return await self.request(HttpMethod.PATCH, endpoint, **kwargs)
