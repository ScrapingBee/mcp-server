"""Run the hosted ScrapingBee MCP server as a local stdio MCP server.

ScrapingBee operates the MCP server at https://mcp.scrapingbee.com/mcp
(Streamable HTTP). Clients that only speak stdio, and sandboxes that build a
server from a repository, can run this launcher instead: it forwards every
MCP request to the hosted endpoint and sends the API key as
``Authorization: Bearer <key>``. No scraping happens on this machine.
"""

from __future__ import annotations

import os
import sys

from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.server import create_proxy

from scrapingbee_mcp import __version__

DEFAULT_URL = "https://mcp.scrapingbee.com/mcp"


def build_headers(api_key: str | None) -> dict[str, str]:
    """Return the upstream headers; no Authorization header without a key."""
    key = (api_key or "").strip()
    return {"Authorization": f"Bearer {key}"} if key else {}


def build_proxy(url: str, api_key: str | None):
    transport = StreamableHttpTransport(url, headers=build_headers(api_key))
    return create_proxy(
        transport,
        name="ScrapingBee",
        version=__version__,
        website_url="https://www.scrapingbee.com/documentation/remote-mcp/",
    )


def main() -> None:
    api_key = os.environ.get("SCRAPINGBEE_API_KEY")
    if not (api_key or "").strip():
        # Listing tools works without a key; calling one needs it.
        print(
            "SCRAPINGBEE_API_KEY is not set: tools can be listed but not called. "
            "Get a key at https://app.scrapingbee.com/account/manage/api_key",
            file=sys.stderr,
        )
    build_proxy(DEFAULT_URL, api_key).run(transport="stdio", show_banner=False)


if __name__ == "__main__":
    main()
