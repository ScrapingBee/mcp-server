# ScrapingBee MCP Server


<p align="center">
  <a href="[https://dashboard.scrapingbee.com/account/google_login](https://mcp.scrapingbee.com/)">
<img width="2047" height="824" alt="image" src="https://github.com/user-attachments/assets/1232c689-5a4c-4554-ab8d-cc74520d3a87" />
  </a>
</p>

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


## Why Use ScrapingBee with MCP?

AI models cannot reliably:

• Bypass anti-bot protections  
• Manage proxy rotation  
• Render JavaScript-heavy pages  
• Handle CAPTCHA challenges  
• Maintain scraping infrastructure  

ScrapingBee handles all of that.

The MCP server acts as a bridge between your AI agent and ScrapingBee’s managed scraping infrastructure.

This enables true AI agent web scraping without fragile prompt-based hacks.


## Architecture Overview

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


## Installation

Clone the repository:

```bash
git clone https://github.com/your-org/scrapingbee-mcp-server.git
cd scrapingbee-mcp-server
```

Install dependencies:

```bash
npm install
```

Set your API key:

```bash
export SCRAPINGBEE_API_KEY=your_api_key
```

Start the MCP server:

```bash
npm start
```


## Connecting to the ScrapingBee MCP Server

You can connect in two ways:

1. Via Claude Desktop (remote MCP)
2. Via a custom Python MCP client


## Option 1: Connect to Claude Desktop

Add the ScrapingBee MCP server to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "scrapingbee": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.scrapingbee.com/mcp?api_key=YOUR_API_KEY"
      ]
    }
  }
}
```

This registers ScrapingBee as an MCP tool provider inside Claude Desktop.

After restarting Claude, the tools become available automatically.


## Option 2: Custom Python MCP Client

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
        self.base_url = f"{base_url}?api_key={api_key}"
        self.session_id = None
        self.http_client = httpx.AsyncClient(timeout=300)
        self.headers = {
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

## What This Enables

With this architecture you can:

• Build AI agents that reason about available tools  
• Allow LLMs to dynamically choose scraping actions  
• Execute structured web data extraction  
• Inject real-world data into model context  
• Create scalable AI-native web scraping systems  


## Conclusion

The [ScrapingBee MCP Server](https://mcp.scrapingbee.com/) transforms web scraping into a structured, tool-driven data layer for AI systems.

Instead of brittle prompt scraping, you get:

• Model Context Protocol compliance  
• JSON-RPC structured execution  
• AI agent web scraping  
• Scalable tool orchestration  

This is AI-native web data access.

To start building AI-powered agents today, [Get your free API key](https://app.scrapingbee.com/account/register) and connect to the ScrapingBee MCP server in minutes.
