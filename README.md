# ScrapingBee MCP Server


<p align="center">
  <a href="https://mcp.scrapingbee.com/">
<img src="https://github.com/user-attachments/assets/7a07376f-cdda-4e3e-8056-15095ca80054" alt="scrapingbee-mcp" />
  </a>
</p>

[![CI](https://github.com/ScrapingBee/mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/ScrapingBee/mcp-server/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-com.scrapingbee%2Fmcp-blue)](https://registry.modelcontextprotocol.io/v0/servers?search=com.scrapingbee/mcp)
[![ScrapingBee/mcp-server MCP server](https://glama.ai/mcp/servers/ScrapingBee/mcp-server/badges/score.svg)](https://glama.ai/mcp/servers/ScrapingBee/mcp-server)

Official MCP server for [ScrapingBee](https://www.scrapingbee.com), maintained by the ScrapingBee team.
Connect to the hosted endpoint `https://mcp.scrapingbee.com/mcp`, or run the `scrapingbee-mcp`
launcher from this repository as a local stdio server.

A production-ready Model Context Protocol (MCP) server that enables AI agents to access structured web data using ScrapingBee as a tool.

This project demonstrates how to transform [ScrapingBee](https://mcp.scrapingbee.com/) into an AI-native data layer. Instead of embedding scraping logic directly inside prompts, AI agents register ScrapingBee as a tool and request structured web data on demand.

If you are building:

• AI agents that require live web access  
• Autonomous research systems  
• Ecommerce intelligence bots  
• Market monitoring agents  
• LLM workflows with tool execution  
• AI-powered web scraping infrastructure  

This repository provides a complete MCP integration blueprint.


### Quick start

The server is hosted by ScrapingBee at **`https://mcp.scrapingbee.com/mcp`** (Streamable HTTP) —
there is nothing to install. You need a ScrapingBee API key
([get one here](https://app.scrapingbee.com/account/manage/api_key); trial credits included).
Registry name: `com.scrapingbee/mcp`.

Clients that support MCP sign-in (OAuth) only need the URL: they open a ScrapingBee sign-in page
where you paste your API key once, and the key never appears in the client or in the URL. Other
clients send the key as the header `Authorization: Bearer <key>`.

**Claude (claude.ai and Claude Desktop)**

Settings → Connectors → Add custom connector → URL `https://mcp.scrapingbee.com/mcp` → Add, then
Connect and sign in.

**Claude Code**

```bash
claude mcp add --transport http scrapingbee https://mcp.scrapingbee.com/mcp
```

Claude Code opens the sign-in page in your browser. To use a header instead, add
`--header "Authorization: Bearer YOUR_API_KEY"`.

**Codex CLI**

```bash
codex mcp add scrapingbee --url https://mcp.scrapingbee.com/mcp \
  --bearer-token-env-var SCRAPINGBEE_API_KEY
```

**Gemini CLI**

```bash
gemini extensions install https://github.com/ScrapingBee/mcp-server
```

You'll be asked for your ScrapingBee API key, which is stored in your system keychain. Change it
later with `gemini extensions config scrapingbee`. If you skip the prompt, export
`SCRAPINGBEE_API_KEY` in your shell instead.

**Cursor, VS Code and other clients with a JSON config**

```json
{
  "mcpServers": {
    "scrapingbee": {
      "url": "https://mcp.scrapingbee.com/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

**Clients that only run local (stdio) servers**

The `scrapingbee-mcp` launcher in this repository runs as a local stdio server and forwards every
call to the hosted endpoint. Requires [uv](https://docs.astral.sh/uv/) (or Python 3.10+ and pip).

```json
{
  "mcpServers": {
    "scrapingbee": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/ScrapingBee/mcp-server", "scrapingbee-mcp"],
      "env": { "SCRAPINGBEE_API_KEY": "YOUR_API_KEY" }
    }
  }
}
```

With Docker:

```bash
docker build -t scrapingbee-mcp https://github.com/ScrapingBee/mcp-server.git
docker run -i --rm -e SCRAPINGBEE_API_KEY scrapingbee-mcp
```

Also available through [Glama](https://glama.ai/mcp/connectors/com.scrapingbee.mcp/scraping-bee)
and the [MCP Registry](https://registry.modelcontextprotocol.io).


### Tools

| Tool | What it does |
|------|--------------|
| `get_page_text` | Fetch a URL and return its content as text or markdown (JavaScript rendered) |
| `get_page_html` | Fetch a URL and return the rendered HTML |
| `get_screenshot` | Fetch a URL and return a screenshot |
| `get_file` | Download a file (PDF, image, …) from a URL |
| `extract_page_data` | Fetch a URL and extract specific data with CSS or XPath selectors |
| `fast_search` | Fast web search returning organic results and top stories |
| `get_google_search_results` | Google SERP as JSON for specialised searches: news, maps, Lens, shopping, images, AI mode |
| `get_amazon_search_results` | Amazon search results as JSON |
| `get_amazon_product_details` | Amazon product details by ASIN |
| `get_amazon_pricing` | Current Amazon price and seller offers by ASIN |
| `get_walmart_search_results` | Walmart search results as JSON |
| `get_walmart_product_details` | Walmart product details by ID |
| `get_youtube_search_results` | YouTube search results |
| `get_youtube_video_metadata` | Title, description, stats and more for a video |
| `get_youtube_video_subtitles` | Subtitles / transcript for a video |
| `ask_chatgpt` | Send a prompt to ChatGPT, optionally with web search |
| `ask_gemini` | Send a prompt to Gemini, with citations when available |
| `get_scrapingbee_usage` | Remaining credits and concurrency for your account |

Each call consumes API credits exactly as the equivalent ScrapingBee API request would
(see [pricing](https://www.scrapingbee.com/pricing/) and the
[API documentation](https://www.scrapingbee.com/documentation/)). The server handles one page or
query per call; for hundreds of URLs, crawling a site, writing results to files or scheduling
recurring jobs, use the [ScrapingBee CLI](https://github.com/ScrapingBee/scrapingbee-cli).

### Authentication

The hosted server accepts either:

- **OAuth 2.1**: clients that support MCP authorization discover it from
  `https://mcp.scrapingbee.com/.well-known/oauth-protected-resource/mcp`, register themselves
  with Dynamic Client Registration, and send you to a ScrapingBee sign-in page where you paste your
  API key once.
- **API key**: send `Authorization: Bearer <SCRAPINGBEE_API_KEY>`. Never put the key in a URL.

`initialize` and `tools/list` work without credentials, so clients and directories can list the
tools before you sign in; every tool call needs a key or an OAuth token and uses credits.

Relevant keywords:
scrapingbee mcp  
model context protocol server  
mcp scraping  
ai agent web scraping  
mcp web scraping tool  


### What Is Model Context Protocol (MCP)?

Model Context Protocol (MCP) defines how AI systems interact with external tools in a structured way.

Instead of letting a language model guess how to scrape or browse the web, MCP allows it to:

1. Discover available tools  
2. Call a tool using structured parameters  
3. Receive normalized JSON responses  
4. Inject results back into the reasoning loop  

The ScrapingBee MCP server exposes web scraping capabilities as a formally registered tool that AI systems can use safely and predictably.


### Why Use ScrapingBee with MCP?

AI models cannot reliably:

• Bypass anti-bot protections  
• Manage proxy rotation  
• Render JavaScript-heavy pages  
• Handle CAPTCHA challenges  
• Maintain scraping infrastructure  

ScrapingBee handles all of that.

The MCP server acts as a bridge between your AI agent and ScrapingBee’s managed scraping infrastructure.

This enables true AI agent web scraping without fragile prompt-based hacks.


### Architecture Overview

AI Agent  
→ MCP Client  
→ ScrapingBee MCP Server  
→ ScrapingBee API  
→ Target Website  
→ Structured JSON Response  
→ Injected Back Into Agent Context  

The AI agent never scrapes directly.  
It calls tools.  
The MCP server executes them.


### Installation

There is nothing to install or run: the server is operated by ScrapingBee at
`https://mcp.scrapingbee.com/mcp`. The only setup is your API key, which every client below
sends as a `Authorization: Bearer` header:

```bash
export SCRAPINGBEE_API_KEY=your_api_key
```


### Connecting to the ScrapingBee MCP Server

You can connect in two ways:

1. Via Claude Desktop (remote MCP)
2. Via a custom Python MCP client


## Option 1: Connect to Claude Desktop

Add it as a custom connector (Settings → Connectors → Add custom connector →
`https://mcp.scrapingbee.com/mcp`) and sign in, or add the `scrapingbee-mcp` launcher config from
[Quick start](#quick-start) to your `claude_desktop_config.json` file.

This registers ScrapingBee as an MCP tool provider inside Claude Desktop.

After restarting Claude, the tools become available automatically.


### Option 2: Custom Python MCP Client

For advanced AI workflows, you can build a minimal async MCP client using Python.

Below is a complete working example.


### custom_mcp_client.py

```python
import os
import re
import json
import asyncio
import httpx
import google.generativeai as genai
from typing import Dict, Any, List

MCP_SERVER_URL = "https://mcp.scrapingbee.com/mcp"
SCRAPINGBEE_API_KEY = os.environ.get("SCRAPINGBEE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
```


### MCP Client Implementation

```python
class MCPClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session_id = None
        self.http_client = httpx.AsyncClient(timeout=300)
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "Minimal-MCP-Client/1.0",
        }

    async def _send_request(self, payload: Dict[str, Any]):
        headers = self.headers.copy()
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        response = await self.http_client.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()

        text = (await response.aread()).decode("utf-8")

        if "data:" in text:
            match = re.search(r"data:\s*({.*})", text, re.DOTALL)
            if match:
                return json.loads(match.group(1))

        if response.status_code in [202, 204] or not text:
            return {"status": "ok"}

        return json.loads(text)

    async def initialize(self):
        init_payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "MinimalClient"},
            },
        }

        async with self.http_client.stream(
            "POST", self.base_url, json=init_payload, headers=self.headers
        ) as response:
            self.session_id = response.headers.get("Mcp-Session-Id")

        notify_payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }

        await self._send_request(notify_payload)

        list_payload = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/list",
            "params": {}
        }

        return await self._send_request(list_payload)

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        payload = {
            "jsonrpc": "2.0",
            "id": "3",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        return await self._send_request(payload)
```


### Converting MCP Tools for Gemini

```python
def format_tools_for_gemini(tools: List[Dict[str, Any]]):
    type_map = {
        "string": genai.protos.Type.STRING,
        "integer": genai.protos.Type.INTEGER,
        "number": genai.protos.Type.NUMBER,
        "boolean": genai.protos.Type.BOOLEAN,
    }

    gemini_tools = []

    for tool in tools:
        properties = {}
        input_schema = tool.get("inputSchema", {})

        if "properties" in input_schema:
            for name, prop in input_schema["properties"].items():
                properties[name] = genai.protos.Schema(
                    type=type_map.get(prop.get("type", "string")),
                    description=prop.get("description", "")
                )

        func = genai.protos.FunctionDeclaration(
            name=tool["name"],
            description=tool["description"],
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties=properties,
                required=input_schema.get("required", [])
            ),
        )

        gemini_tools.append(
            genai.protos.Tool(function_declarations=[func])
        )

    return gemini_tools
```


### Full AI → MCP → Tool Execution Flow

```python
async def main():
    mcp_client = MCPClient(MCP_SERVER_URL, SCRAPINGBEE_API_KEY)
    tools_response = await mcp_client.initialize()

    genai.configure(api_key=GEMINI_API_KEY)
    gemini_tools = format_tools_for_gemini(tools_response["result"]["tools"])

    model = genai.GenerativeModel(
        model_name="gemini-2.5-pro",
        tools=gemini_tools
    )

    user_prompt = input("Ask the AI to perform a task:\n> ")

    response = model.generate_content(user_prompt)
    function_call = response.candidates[0].content.parts[0].function_call

    tool_name = function_call.name
    tool_args = dict(function_call.args)

    result = await mcp_client.call_tool(tool_name, tool_args)

    print(json.dumps(result, indent=2))
```

### What This Enables

With this architecture you can:

• Build AI agents that reason about available tools  
• Allow LLMs to dynamically choose scraping actions  
• Execute structured web data extraction  
• Inject real-world data into model context  
• Create scalable AI-native web scraping systems  


### Conclusion

The [ScrapingBee MCP Server](https://mcp.scrapingbee.com/) transforms web scraping into a structured, tool-driven data layer for AI systems.

Instead of brittle prompt scraping, you get:

• Model Context Protocol compliance  
• JSON-RPC structured execution  
• AI agent web scraping  
• Scalable tool orchestration  

This is AI-native web data access.

To start building AI-powered agents today, [Get your free API key](https://app.scrapingbee.com/account/register) and connect to the ScrapingBee MCP server in minutes.


### What is in this repository

| Path | What it is |
|------|------------|
| `src/scrapingbee_mcp/` | The `scrapingbee-mcp` stdio launcher (MIT). It proxies MCP requests to the hosted server; nothing is scraped locally. |
| `Dockerfile` | Container image for the launcher. |
| `server.json` | Copy of the [MCP Registry](https://registry.modelcontextprotocol.io) entry `com.scrapingbee/mcp`. |
| `glama.json` | Maintainers of the [Glama](https://glama.ai/mcp/servers/ScrapingBee/mcp-server) listing. |
| `gemini-extension.json`, `GEMINI.md` | Gemini CLI extension manifest and context. |
| `lhm.plugin.json` | Manifest for the [LobeHub](https://lobehub.com/mcp) MCP marketplace. |
| `tests/` | Unit tests and a smoke test that lists the hosted server's tools without a key. |

The hosted server runs on ScrapingBee's infrastructure and is operated by ScrapingBee; its source
is not published. The MIT license covers the contents of this repository.

### Security

Please report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

### Development

```bash
uv venv && uv pip install -e . pytest
pytest -q tests                 # unit tests
python tests/smoke_stdio.py     # lists the hosted tools through the launcher (no key, no credits)
```
