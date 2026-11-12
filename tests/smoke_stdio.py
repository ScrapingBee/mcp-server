"""Smoke test: start the launcher over stdio and list tools (no API key, no credits)."""

import asyncio
import os
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport


async def main() -> int:
    env = {k: v for k, v in os.environ.items() if k != "SCRAPINGBEE_API_KEY"}
    transport = StdioTransport(
        command=sys.executable, args=["-m", "scrapingbee_mcp"], env=env
    )
    async with Client(transport) as client:
        tools = await client.list_tools()
    names = sorted(t.name for t in tools)
    print(len(names), names)
    return (
        0
        if {"get_page_text", "fast_search", "get_scrapingbee_usage"} <= set(names)
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
