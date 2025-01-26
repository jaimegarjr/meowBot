import pytest
import aiohttp
from unittest.mock import AsyncMock, MagicMock, patch
from meowbot.application.models.http_client import HttpClient, HttpMethod


@pytest.mark.asyncio
async def test_http_client_initialization():
    """Test the initialization of HttpClient."""
    base_url = "https://api.example.com"
    client = HttpClient(base_url=base_url)

    assert client.base_url == base_url
    assert client.default_headers == {"User-Agent": "HttpClient/1.0"}
    assert client.timeout.total == 10
    assert client.session is None


# @pytest.mark.asyncio
# async def test_http_client_request():
#     """Test the request method of HttpClient."""
#     # Create a mock response
#     mock_response = AsyncMock()
#     mock_response.json.return_value = {"key": "value"}
#     mock_response.__aenter__.return_value = mock_response
#     mock_response.__aexit__.return_value = None

#     # Mock the ClientSession
#     mock_session = AsyncMock()
#     # This is the key change: return_value becomes a coroutine
#     mock_session.request = AsyncMock(return_value=mock_response)

#     with patch("aiohttp.ClientSession", return_value=mock_session):
#         client = HttpClient(base_url="https://api.example.com")
#         async with client:
#             response = await client.request(HttpMethod.GET, "/endpoint")
#             assert response == {"key": "value"}

#             # Update the assertion to match the actual call
#             mock_session.request.assert_called_once_with(
#                 "GET",  # Note: we use the string value, not the enum
#                 "https://api.example.com/endpoint",
#                 timeout=client.timeout,
#                 headers={},
#             )
