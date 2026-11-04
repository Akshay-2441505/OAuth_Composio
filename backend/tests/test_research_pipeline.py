from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.source_ranker import rank_source, is_domain_match
from app.services.search_service import search_service
from app.services.fetch_service import fetch_service
from app.services.llm.router import llm_router

from app.services.research_orchestrator import orchestrator

client = TestClient(app)

def test_source_ranking_official_vs_secondary():
    official = rank_source(
        url="https://docs.github.com/en/apps/creating-an-oauth-app",
        title="Creating an OAuth App",
        provider_domain="github.com"
    )
    assert official["is_official"] is True
    assert official["source_type"] == "official_documentation"
    assert official["priority"] >= 80

    secondary = rank_source(
        url="https://medium.com/some-blog/how-to-github-oauth",
        title="How to build GitHub OAuth",
        provider_domain="github.com"
    )
    assert secondary["is_official"] is False
    assert secondary["priority"] < official["priority"]

def test_domain_match_subdomain_handling():
    assert is_domain_match("docs.github.com", "github.com") is True
    assert is_domain_match("api.slack.com", "slack.com") is True
    assert is_domain_match("notion.so", "notion.so") is True
    assert is_domain_match("evilgithub.com", "github.com") is False
    assert is_domain_match("github.com.attacker.com", "github.com") is False

def test_create_research_run_requires_input():
    response = client.post("/api/research-runs", json={})
    assert response.status_code == 400
    assert "Either 'app_name' or 'website_url'" in response.json()["detail"]

def test_create_research_run_rejects_ssrf():
    response = client.post("/api/research-runs", json={
        "website_url": "http://169.254.169.254/latest/meta-data/"
    })
    assert response.status_code == 400
    assert "Invalid or restricted URL" in response.json()["detail"]

def test_create_research_run_success():
    mock_sources = [
        {
            "title": "Linear API Docs",
            "url": "https://linear.app/docs",
            "domain": "linear.app",
            "source_type": "official_documentation",
            "is_official": True,
            "snippet": "Linear API"
        }
    ]
    mock_fetch = {
        "url": "https://linear.app/docs",
        "http_status": 200,
        "fetch_status": "success",
        "content": "Linear OAuth 2.0 Docs",
        "error": None
    }

    with patch.object(search_service, "search_provider_docs", AsyncMock(return_value=mock_sources)), \
         patch.object(fetch_service, "fetch_and_extract", AsyncMock(return_value=mock_fetch)), \
         patch.object(llm_router, "generate_structured_guide", AsyncMock(return_value=(None, "heuristic", "offline", "mock"))):
        
        response = client.post("/api/research-runs", json={
            "app_name": "Linear",
            "website_url": "https://linear.app",
            "integration_intent": "Manage issues and sync pull requests"
        })
        assert response.status_code == 201
        data = response.json()
        assert "run_id" in data
        assert len(data["stages"]) > 0

        run_id = data["run_id"]
        get_res = client.get(f"/api/research-runs/{run_id}")
        assert get_res.status_code == 200
        run_data = get_res.json()
        assert run_data["run_id"] == run_id

def test_input_sanitization_strips_control_characters():
    with patch.object(orchestrator, "execute_research", AsyncMock()):
        response = client.post("/api/research-runs", json={
            "app_name": "Test\x00\x08App\x1f",
            "website_url": "https://example.com"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["input_name"] == "TestApp"

def test_list_research_runs():
    res = client.get("/api/research-runs")
    assert res.status_code == 200
    runs = res.json()
    assert isinstance(runs, list)
    assert len(runs) > 0

def test_input_validation_prohibits_secrets():
    """Validates that attempts to pass secrets or tokens are rejected with 422."""
    response = client.post("/api/research-runs", json={
        "app_name": "TestApp",
        "website_url": "https://example.com",
        "integration_intent": "Using client_secret=abcdef123456"
    })
    assert response.status_code == 422
    assert "prohibited credential pattern" in response.text

def test_input_validation_requires_alphanumeric_name():
    """Validates that purely symbolic or whitespace names are rejected."""
    response = client.post("/api/research-runs", json={
        "app_name": "???---!!!",
        "website_url": "https://example.com"
    })
    assert response.status_code == 422
    assert "must contain at least one alphanumeric character" in response.text

def test_duplicate_in_flight_run_returns_existing():
    """Validates that starting a second run for the same app while queued returns the existing run."""
    with patch.object(orchestrator, "execute_research", AsyncMock()), \
         patch("app.routers.research.is_safe_url", return_value=(True, "Safe")):
        res1 = client.post("/api/research-runs", json={
            "app_name": "UniqueAppTest1",
            "website_url": "https://example.com"
        })
        assert res1.status_code == 201
        run1_id = res1.json()["run_id"]

        # Duplicate immediate request
        res2 = client.post("/api/research-runs", json={
            "app_name": "UniqueAppTest1",
            "website_url": "https://example.com"
        })
        assert res2.status_code == 201
        assert res2.json()["run_id"] == run1_id

def test_retry_research_run_endpoint():
    """Validates the POST /api/research-runs/{run_id}/retry endpoint."""
    with patch.object(orchestrator, "execute_research", AsyncMock()), \
         patch("app.routers.research.is_safe_url", return_value=(True, "Safe")):
        # Create a run
        res = client.post("/api/research-runs", json={
            "app_name": "RetryTargetApp",
            "website_url": "https://example.com"
        })
        assert res.status_code == 201
        run_id = res.json()["run_id"]

        # Trigger retry
        retry_res = client.post(f"/api/research-runs/{run_id}/retry")
        assert retry_res.status_code == 200
        data = retry_res.json()
        assert data["run_id"] == run_id
        assert data["status"] == "queued"

def test_invalid_guide_id_and_slug_formats_return_400():
    """Validates that malformed IDs with suspicious characters are rejected with 400 Bad Request."""
    res_guide = client.get("/api/guides/../../etc/passwd")
    assert res_guide.status_code in (400, 404)

    res_guide2 = client.get("/api/guides/!invalid@guide#id$")
    assert res_guide2.status_code == 400
    assert "Invalid guide ID format" in res_guide2.json()["detail"]

    res_app = client.get("/api/apps/!invalid@slug#")
    assert res_app.status_code == 400
    assert "Invalid app slug format" in res_app.json()["detail"]
