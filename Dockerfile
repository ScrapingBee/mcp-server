# Local stdio launcher for the hosted ScrapingBee MCP server.
# The container only forwards MCP requests to https://mcp.scrapingbee.com/mcp.
# Newest Python version tested in CI.
FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir . \
 && useradd --create-home --uid 10001 app

USER app
# Pass the key at run time: docker run -i --rm -e SCRAPINGBEE_API_KEY scrapingbee-mcp
ENTRYPOINT ["scrapingbee-mcp"]
