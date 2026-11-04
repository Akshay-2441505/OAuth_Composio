import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ssrf_validator import is_safe_url
from app.services.fetch_service import fetch_service

def test_blocks_localhost_and_loopback():
    blocked_urls = [
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000/callback",
        "http://127.0.1.1",
        "http://[::1]",
    ]
    for url in blocked_urls:
        safe, reason = is_safe_url(url)
        assert not safe, f"Expected {url} to be blocked, but passed: {reason}"

def test_blocks_cloud_metadata_ip():
    metadata_urls = [
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254",
        "https://169.254.169.254/computeMetadata/v1/",
        "http://metadata.google.internal/computeMetadata/v1/",
        "http://instance-data/latest/meta-data/",
        "http://[fd00:ec2::254]/latest/meta-data/",
    ]
    for url in metadata_urls:
        safe, reason = is_safe_url(url)
        assert not safe, f"Expected metadata URL {url} to be blocked, but passed: {reason}"

def test_blocks_private_subnets():
    private_urls = [
        "http://10.0.0.1",
        "http://192.168.1.1/admin",
        "http://172.16.0.1",
    ]
    for url in private_urls:
        safe, reason = is_safe_url(url)
        assert not safe, f"Expected private IP {url} to be blocked, but passed: {reason}"

def test_blocks_non_http_schemes():
    invalid_schemes = [
        "file:///etc/passwd",
        "ftp://ftp.example.com",
        "gopher://example.com",
        "data:text/plain;base64,SGVsbG8=",
    ]
    for url in invalid_schemes:
        safe, reason = is_safe_url(url)
        assert not safe, f"Expected scheme {url} to be blocked"

def test_blocks_invalid_ports():
    safe, reason = is_safe_url("http://example.com:22")
    assert not safe
    assert "Port" in reason

def test_allows_valid_public_domain():
    safe, reason = is_safe_url("https://docs.github.com/en/apps/oauth-apps")
    assert safe, f"Expected public URL to be safe, but blocked: {reason}"

@pytest.mark.asyncio
async def test_fetch_service_blocks_redirect_to_private_ip():
    """Validates that fetch_service prevents SSRF redirect bypass to loopback/private IP."""
    # Create mock redirect response to 127.0.0.1
    redirect_resp = MagicMock()
    redirect_resp.is_redirect = True
    redirect_resp.headers = {"Location": "http://127.0.0.1:8000/admin"}

    with patch("httpx.AsyncClient.get", AsyncMock(return_value=redirect_resp)):
        result = await fetch_service.fetch_and_extract("https://docs.github.com/en/apps")
        assert result["fetch_status"] == "blocked"
        assert "Security check blocked" in result["error"]
