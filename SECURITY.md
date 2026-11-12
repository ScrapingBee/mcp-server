# Security policy

## Scope

This policy covers:

- the hosted ScrapingBee MCP server at `https://mcp.scrapingbee.com/mcp`, including its OAuth
  endpoints and `/.well-known/` metadata;
- the `scrapingbee-mcp` stdio launcher and Docker image in this repository.

Vulnerabilities in the ScrapingBee API itself are also welcome at the same address.

## Reporting a vulnerability

Email **contact@scrapingbee.com** with the subject `SECURITY: mcp-server`. Please include
the affected endpoint or file, steps to reproduce, and the impact you observed. Do not open a
public issue for a suspected vulnerability, and never include a real API key in a report.

We acknowledge reports within 3 business days and keep you updated until the issue is resolved.

## Supported versions

| Component | Supported |
|-----------|-----------|
| Hosted server (`mcp.scrapingbee.com`) | Always the deployed version |
| `scrapingbee-mcp` launcher | Latest release on `master` |

## How credentials are handled

- Your ScrapingBee API key is sent only as the `Authorization: Bearer` header over TLS to
  `mcp.scrapingbee.com`. Never put it in a URL.
- The launcher reads the key from the `SCRAPINGBEE_API_KEY` environment variable, never logs it,
  and sends it to no other host.
- With OAuth 2.1 sign-in, the client never sees your API key.
