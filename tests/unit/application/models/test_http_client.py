import pytest
import asyncio
from aioresponses import aioresponses
from meowbot.application.models.http_client import HttpClient


@pytest.mark.asyncio
async def test_http_client_initialization():
    """Test the initialization of HttpClient."""
    base_url = "https://api.example.com"
    client = HttpClient(base_url=base_url)

    assert client.base_url == base_url
    assert client.default_headers == {"User-Agent": "HttpClient/1.0"}
    assert client.timeout.total == 10
    assert client.session is None


@pytest.mark.asyncio
async def test_get_request():
    base_url = "https://api.example.com"
    endpoint = "/test"
    expected_response = {"success": True}

    with aioresponses() as mock:
        mock.get(f"{base_url}{endpoint}", payload=expected_response, status=200)

        async with HttpClient(base_url) as client:
            response = await client.get(endpoint)

    assert response == expected_response


@pytest.mark.asyncio
async def test_post_request():
    base_url = "https://api.example.com"
    endpoint = "/submit"
    payload = {"key": "value"}
    expected_response = {"message": "Created"}

    with aioresponses() as mock:
        mock.post(f"{base_url}{endpoint}", payload=expected_response, status=201)

        async with HttpClient(base_url) as client:
            response = await client.post(endpoint, json=payload)

    assert response == expected_response


@pytest.mark.asyncio
async def test_timeout():
    base_url = "https://api.example.com"
    endpoint = "/timeout"

    with aioresponses() as mock:
        mock.get(f"{base_url}{endpoint}", exception=asyncio.TimeoutError)

        async with HttpClient(base_url) as client:
            with pytest.raises(asyncio.TimeoutError):
                await client.get(endpoint)


@pytest.mark.asyncio
async def test_404_error():
    base_url = "https://api.example.com"
    endpoint = "/not-found"

    with aioresponses() as mock:
        mock.get(f"{base_url}{endpoint}", status=404)

        async with HttpClient(base_url) as client:
            with pytest.raises(Exception) as excinfo:
                await client.get(endpoint)

    assert "404" in str(excinfo.value)


@pytest.mark.asyncio
async def test_custom_headers():
    base_url = "https://api.example.com"
    endpoint = "/headers-test"
    custom_headers = {"Authorization": "Bearer token"}
    expected_response = {"authorized": True}

    with aioresponses() as mock:
        mock.get(
            f"{base_url}{endpoint}",
            payload=expected_response,
            status=200,
            headers=custom_headers,
        )

        async with HttpClient(base_url) as client:
            response = await client.get(endpoint, headers=custom_headers)

    assert response == expected_response


@pytest.mark.asyncio
async def test_session_closing():
    base_url = "https://api.example.com"

    async with HttpClient(base_url) as client:
        with aioresponses() as mock:
            mock.get(f"{base_url}/", payload={}, status=200)
            await client.get("/")

    assert client.session is None


@pytest.mark.asyncio
async def test_http_client_error_handling():
    base_url = "https://api.example.com"
    endpoint = "/error"

    with aioresponses() as mock:
        mock.get(f"{base_url}{endpoint}", exception=Exception("Server error"))

        async with HttpClient(base_url) as client:
            with pytest.raises(Exception) as excinfo:
                await client.get(endpoint)

    assert "Server error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_all_http_methods():
    base_url = "https://api.example.com"
    endpoint = "/all-methods"
    data = {"key": "value"}

    with aioresponses() as mock:
        mock.get(f"{base_url}{endpoint}", payload=data, status=200)
        mock.post(f"{base_url}{endpoint}", payload=data, status=201)
        mock.put(f"{base_url}{endpoint}", payload=data, status=200)
        mock.delete(f"{base_url}{endpoint}", payload=data, status=204)
        mock.patch(f"{base_url}{endpoint}", payload=data, status=200)

        async with HttpClient(base_url) as client:
            get_response = await client.get(endpoint)
            post_response = await client.post(endpoint, json=data)
            put_response = await client.put(endpoint, json=data)
            delete_response = await client.delete(endpoint)
            patch_response = await client.patch(endpoint, json=data)

    assert get_response == data
    assert post_response == data
    assert put_response == data
    assert delete_response == data
    assert patch_response == data


@pytest.mark.asyncio
async def test_response_text_format():
    base_url = "https://api.example.com"
    endpoint = "/text"
    expected_response = "Hello, world!"
    response_headers = {"Content-Type": "text/plain"}

    with aioresponses() as mock:
        mock.get(
            f"{base_url}{endpoint}", body=expected_response, headers=response_headers, status=200
        )

        async with HttpClient(base_url) as client:
            response = await client.get(endpoint)

    assert response == expected_response
