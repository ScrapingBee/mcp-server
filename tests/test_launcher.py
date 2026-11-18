import asyncio

from fastmcp import Client

from scrapingbee_mcp.__main__ import (
    DEFAULT_URL,
    MISSING_KEY,
    build_headers,
    build_proxy,
)


def test_bearer_header_from_key():
    assert build_headers("abc") == {"Authorization": "Bearer abc"}


def test_no_header_without_key():
    assert build_headers(None) == {}
    assert build_headers("   ") == {}


def test_default_url_is_hosted_endpoint():
    assert DEFAULT_URL == "https://mcp.scrapingbee.com/mcp"


def test_tool_call_without_key_explains_missing_key():
    async def call():
        async with Client(build_proxy(DEFAULT_URL, None)) as client:
            return await client.call_tool(
                "get_scrapingbee_usage", {}, raise_on_error=False
            )

    result = asyncio.run(call())
    assert result.is_error
    assert result.content[0].text == MISSING_KEY
