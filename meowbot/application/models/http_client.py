import aiohttp
import asyncio
import logging
from enum import Enum


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HttpClient:
    def __init__(self, base_url: str, headers: dict = None, timeout: int = 10):
        """
        Initialize the HttpClient.

        Args:
            base_url (str): The base URL for all requests.
            headers (dict): Default headers for requests.
            timeout (int): Timeout for requests in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = aiohttp.ClientSession(timeout=self.timeout, headers=self.headers)

    async def request(self, method: HttpMethod, endpoint: str, **kwargs):
        """
        Perform an HTTP request.

        Args:
            method (HttpMethod): The HTTP method to use.
            endpoint (str): The API endpoint (relative to base_url).
            **kwargs: Additional arguments to pass to aiohttp (e.g., params, json, headers).

        Returns:
            Response JSON or text.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            async with self.session.request(method.value, url, **kwargs) as response:
                response.raise_for_status()
                if "application/json" in response.headers.get("Content-Type", ""):
                    return await response.json()
                return await response.text()
        except aiohttp.ClientResponseError as e:
            logging.error(f"HTTP Error: {e.status} {e.message}")
            raise
        except asyncio.TimeoutError:
            logging.error("Request timed out")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

    async def close(self):
        """Close the aiohttp session."""
        await self.session.close()

    async def get(self, endpoint: str, **kwargs):
        """Perform a GET request."""
        return await self.request(HttpMethod.GET, endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs):
        """Perform a POST request."""
        return await self.request(HttpMethod.POST, endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs):
        """Perform a PUT request."""
        return await self.request(HttpMethod.PUT, endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs):
        """Perform a DELETE request."""
        return await self.request(HttpMethod.DELETE, endpoint, **kwargs)
