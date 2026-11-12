from scrapingbee_mcp.__main__ import DEFAULT_URL, build_headers


def test_bearer_header_from_key():
    assert build_headers("abc") == {"Authorization": "Bearer abc"}


def test_no_header_without_key():
    assert build_headers(None) == {}
    assert build_headers("   ") == {}


def test_default_url_is_hosted_endpoint():
    assert DEFAULT_URL == "https://mcp.scrapingbee.com/mcp"
