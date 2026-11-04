import os
import re
import time
from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.database import SessionLocal
from app.models.app import App
from app.models.guide import Guide
from app.models.source import Source
from app.models.research_run import ResearchRun
from app.services.ssrf_validator import is_safe_url
from app.services.fetch_service import fetch_service
from app.services.search_service import search_service
from app.services.llm.router import LLMRouter, llm_router
from app.services.llm.base import LLMProvider
from app.services.research_orchestrator import orchestrator, enforce_evidence_grounding
from app.schemas.guide import GuideSchema
from app.services.llm.heuristic_fallback import generate_heuristic_guide

client = TestClient(app)

# ==========================================
# 1. DIRECTORY TESTS
# ==========================================

def test_qa_directory_search_exact():
    res = client.get("/api/apps?q=GitHub")
    assert res.status_code == 200
    apps = res.json()
    assert len(apps) == 1
    assert apps[0]["slug"] == "github"

def test_qa_directory_search_partial():
    res = client.get("/api/apps?q=git")
    assert res.status_code == 200
    apps = res.json()
    assert len(apps) >= 1
    assert any(a["slug"] == "github" for a in apps)

def test_qa_directory_search_invalid_characters():
    # Test control chars and SQL injection patterns
    res = client.get("/api/apps?q=%00%1f%27%20OR%201=1--")
    assert res.status_code == 200
    # SQL injection should not return all apps unexpectedly or crash
    apps = res.json()
    assert isinstance(apps, list)

def test_qa_directory_search_nonexistent():
    res = client.get("/api/apps?q=NonExistentPlatform999xyz")
    assert res.status_code == 200
    apps = res.json()
    assert len(apps) == 0

def test_qa_directory_category_and_auth_filters():
    # Filter by category
    res = client.get("/api/apps?category=Developer+tools")
    assert res.status_code == 200
    apps = res.json()
    assert all(a["category"] == "Developer tools" for a in apps)

    # Filter by auth_type
    res_auth = client.get("/api/apps?auth_type=OAuth2")
    assert res_auth.status_code == 200
    assert len(res_auth.json()) >= 3


# ==========================================
# 2. OAUTH GUIDES TESTS
# ==========================================

def test_qa_guides_seeded_all_open():
    seeded_slugs = ["github", "google", "slack"]
    for slug in seeded_slugs:
        # Test app endpoint
        app_res = client.get(f"/api/apps/{slug}")
        assert app_res.status_code == 200
        app_data = app_res.json()
        assert app_data["slug"] == slug
        guide_id = app_data["guide_id"]
        assert guide_id is not None

        # Test guide endpoint
        guide_res = client.get(f"/api/guides/{guide_id}")
        assert guide_res.status_code == 200
        guide_data = guide_res.json()
        assert guide_data["status"] == "validated"
        assert guide_data["is_public"] is True

        content = guide_data["content"]
        assert len(content["steps"]) > 0
        assert len(content["sources"]) > 0

        # Validate step requirements
        for step in content["steps"]:
            assert step["title"]
            assert step["description"]
            assert step["verification"]
            assert step["evidence_status"] in ("verified", "attempted", "estimated", "unknown")

        # Check source links
        for src in content["sources"]:
            assert src["url"].startswith("http")
            assert src["is_official"] in (True, False)
            assert src["domain"]

def test_qa_guides_invalid_ids():
    # Malformed ID with invalid characters -> 400 Bad Request
    res_malformed = client.get("/api/guides/!@#$invalid_id%")
    assert res_malformed.status_code == 400
    assert "Invalid guide ID format" in res_malformed.json()["detail"]

    # Nonexistent safe ID -> 404 Not Found
    res_notfound = client.get("/api/guides/guide_nonexistent_999")
    assert res_notfound.status_code == 404


# ==========================================
# 3. AI RESEARCH TESTS
# ==========================================

def test_qa_research_search_by_url_and_persistence():
    mock_sources = [
        {
            "title": "Airtable OAuth Documentation",
            "url": "https://airtable.com/developers/web/api/oauth-reference",
            "domain": "airtable.com",
            "source_type": "official_documentation",
            "is_official": True,
            "snippet": "Airtable OAuth 2.0 allows third-party applications to access Airtable data."
        }
    ]
    mock_fetch = {
        "url": "https://airtable.com/developers/web/api/oauth-reference",
        "http_status": 200,
        "fetch_status": "success",
        "content": "Airtable OAuth 2.0 reference. Endpoints: https://airtable.com/oauth/authorize, https://airtable.com/oauth/token. Scopes: data.records:read, data.records:write.",
        "error": None
    }
    sample_guide = generate_heuristic_guide({
        "app_name": "Airtable",
        "provider_domain": "airtable.com",
        "sources": mock_sources,
    })

    with patch.object(search_service, "search_provider_docs", AsyncMock(return_value=mock_sources)), \
         patch.object(fetch_service, "fetch_and_extract", AsyncMock(return_value=mock_fetch)), \
         patch.object(llm_router, "generate_structured_guide", AsyncMock(return_value=(sample_guide, "mock_llm", "mock_model", None))):
        
        # Test creation by URL
        res = client.post("/api/research-runs", json={
            "app_name": "Airtable",
            "website_url": "https://airtable.com",
            "integration_intent": "Read and write records via OAuth"
        })
        assert res.status_code == 201
        run_id = res.json()["run_id"]

        # Poll run
        completed = False
        run_data = None
        for _ in range(20):
            r = client.get(f"/api/research-runs/{run_id}")
            assert r.status_code == 200
            run_data = r.json()
            if run_data["status"] == "completed":
                completed = True
                break
            time.sleep(0.1)

        assert completed is True
        assert run_data["guide_id"] is not None

        # Verify guide is queryable
        guide_res = client.get(f"/api/guides/{run_data['guide_id']}")
        assert guide_res.status_code == 200
        assert guide_res.json()["content"]["app"]["name"] == "Airtable"

def test_qa_research_nonexistent_application_fails_truthfully():
    # If no docs discovered, search fails truthfully
    with patch.object(search_service, "search_provider_docs", AsyncMock(return_value=[])):
        res = client.post("/api/research-runs", json={
            "app_name": "GhostPlatformNonExistentXYZ",
            "website_url": None
        })
        assert res.status_code == 201
        run_id = res.json()["run_id"]

        failed = False
        run_data = None
        for _ in range(20):
            r = client.get(f"/api/research-runs/{run_id}")
            run_data = r.json()
            if run_data["status"] == "failed":
                failed = True
                break
            time.sleep(0.1)

        assert failed is True
        assert run_data["guide_id"] is None
        assert "Could not locate developer documentation" in run_data["error"]


# ==========================================
# 4. LLM RELIABILITY & FALLBACK
# ==========================================

class MockProvider(LLMProvider):
    def __init__(self, name: str, response: dict = None, error: str = None):
        self._name = name
        self._resp = response
        self._err = error

    @property
    def provider_name(self) -> str:
        return self._name

    @property
    def model_name(self) -> str:
        return f"{self._name}-test"

    def is_configured(self) -> bool:
        return True

    async def generate_guide_json(self, evidence_package, repair_feedback=None):
        return self._resp, self._err

@pytest.mark.asyncio
async def test_qa_llm_timeout_triggers_groq_fallback():
    router = LLMRouter()
    sample_guide = generate_heuristic_guide({
        "app_name": "TestApp",
        "provider_domain": "testapp.com",
        "sources": [{"id": "src_01", "title": "Doc", "url": "https://testapp.com/docs"}]
    }).model_dump()

    primary_name = settings.provider_order[0]
    secondary_name = settings.provider_order[1] if len(settings.provider_order) > 1 else "openrouter"

    router.providers[primary_name] = MockProvider(primary_name, error="Request timed out after 25s")
    router.providers[secondary_name] = MockProvider(secondary_name, response=sample_guide)

    guide, provider_used, model_used, fallback_reason = await router.generate_structured_guide({
        "app_name": "TestApp",
        "provider_domain": "testapp.com",
    })
    assert guide is not None
    assert provider_used == secondary_name
    assert "Request timed out" in fallback_reason

@pytest.mark.asyncio
async def test_qa_llm_both_failing_returns_none_without_hallucinating():
    router = LLMRouter()
    router.providers["openrouter"] = MockProvider("openrouter", error="Rate limit 429")
    router.providers["groq"] = MockProvider("groq", error="Service unavailable 503")

    guide, provider_used, model_used, fallback_reason = await router.generate_structured_guide({
        "app_name": "TestApp",
        "provider_domain": "testapp.com",
    })
    assert guide is None
    assert "Rate limit 429" in fallback_reason
    assert "Service unavailable 503" in fallback_reason


# ==========================================
# 5. SECURITY & SSRF TESTS
# ==========================================

def test_qa_security_ssrf_comprehensive():
    blocked_test_urls = [
        "http://localhost",
        "http://localhost:8000/api",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://[::1]",
        "http://10.0.0.1",
        "http://192.168.1.1",
        "http://172.16.0.1",
        "http://169.254.169.254",
        "http://metadata.google.internal",
        "http://instance-data",
        "http://[fd00:ec2::254]",
        "file:///etc/passwd",
        "ftp://ftp.example.com",
        "gopher://evil.com",
        "http://example.com:22",
    ]
    for url in blocked_test_urls:
        safe, reason = is_safe_url(url)
        assert not safe, f"Expected {url} to be blocked! Reason: {reason}"

def test_qa_security_credentials_prohibited():
    prohibited_payloads = [
        {"app_name": "App", "website_url": "https://example.com", "integration_intent": "client_secret=12345"},
        {"app_name": "App", "website_url": "https://example.com", "integration_intent": "access_token=abcdef"},
        {"app_name": "App", "website_url": "https://example.com", "integration_intent": "bearer eyJhbGciOi..."},
    ]
    for payload in prohibited_payloads:
        res = client.post("/api/research-runs", json=payload)
        assert res.status_code == 422


# ==========================================
# 6. DATABASE PERSISTENCE TESTS
# ==========================================

def test_qa_database_entities_and_relations():
    db = SessionLocal()
    try:
        # Check Apps
        apps = db.query(App).all()
        assert len(apps) >= 3
        
        # Check Guides
        guides = db.query(Guide).all()
        assert len(guides) >= 3

        # Check Sources
        sources = db.query(Source).all()
        assert len(sources) > 0

        # Check Research Runs
        runs = db.query(ResearchRun).all()
        assert len(runs) > 0
    finally:
        db.close()
