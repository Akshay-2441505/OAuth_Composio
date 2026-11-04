import time
from unittest.mock import patch, AsyncMock
import pytest
from app.services.llm.base import LLMProvider
from app.services.llm.router import LLMRouter, llm_router
from app.services.llm.heuristic_fallback import generate_heuristic_guide
from app.services.search_service import search_service
from app.services.fetch_service import fetch_service
from app.schemas.guide import GuideSchema
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class MockFailingProvider(LLMProvider):
    def __init__(self, name: str, error_message: str):
        self._name = name
        self._error = error_message

    @property
    def provider_name(self) -> str:
        return self._name

    @property
    def model_name(self) -> str:
        return f"{self._name}-mock-model"

    def is_configured(self) -> bool:
        return True

    async def generate_guide_json(self, evidence_package, repair_feedback=None):
        return None, self._error

class MockWorkingProvider(LLMProvider):
    def __init__(self, name: str, payload: dict):
        self._name = name
        self._payload = payload

    @property
    def provider_name(self) -> str:
        return self._name

    @property
    def model_name(self) -> str:
        return f"{self._name}-working-model"

    def is_configured(self) -> bool:
        return True

    async def generate_guide_json(self, evidence_package, repair_feedback=None):
        return self._payload, None

@pytest.mark.asyncio
async def test_llm_router_fallback_on_primary_failure():
    """Validates that when primary provider (OpenRouter) fails with 429/timeout, Groq is invoked."""
    router = LLMRouter()
    
    # Configure primary failing, secondary working
    sample_guide = generate_heuristic_guide({
        "app_name": "TestApp",
        "provider_domain": "testapp.com",
        "sources": [{"id": "src_01", "title": "Test Doc", "url": "https://testapp.com/docs"}]
    }).model_dump()

    router.providers["openrouter"] = MockFailingProvider("openrouter", "Rate limit 429: Too Many Requests")
    router.providers["groq"] = MockWorkingProvider("groq", sample_guide)

    guide, provider_used, model_used, fallback_reason = await router.generate_structured_guide({
        "app_name": "TestApp",
        "provider_domain": "testapp.com",
    })

    assert guide is not None
    assert provider_used == "groq"
    assert "Rate limit 429" in fallback_reason
    assert guide.app.name == "TestApp"

def test_heuristic_fallback_produces_valid_guide():
    """Validates heuristic fallback synthesizes schema-compliant GuideSchema when keys unconfigured."""
    evidence = {
        "app_name": "Linear",
        "provider_domain": "linear.app",
        "sources": [
            {
                "id": "src_01",
                "title": "Linear API OAuth Documentation",
                "url": "https://linear.app/docs/oauth",
                "domain": "linear.app",
                "source_type": "official_documentation",
                "is_official": True,
            }
        ]
    }
    guide = generate_heuristic_guide(evidence)
    assert isinstance(guide, GuideSchema)
    assert guide.app.name == "Linear"
    assert guide.time_estimates.active_setup.confidence == "medium"
    assert len(guide.steps) > 0
    assert len(guide.sources) == 1

def test_end_to_end_research_run_and_guide_retrieval():
    """Validates full pipeline: research-run creation, execution, guide generation and retrieval."""
    mock_sources = [
        {
            "title": "Linear OAuth 2.0 Authentication Documentation",
            "url": "https://linear.app/docs/oauth-authentication",
            "domain": "linear.app",
            "source_type": "official_documentation",
            "is_official": True,
            "snippet": "Register OAuth application, define scopes, and exchange authorization codes."
        }
    ]
    mock_fetch = {
        "url": "https://linear.app/docs/oauth-authentication",
        "http_status": 200,
        "fetch_status": "success",
        "content": "Linear OAuth 2.0 Documentation. To connect your application, register at linear.app/settings/api. Requires HTTPS redirect URI. Scopes: read, write, issues:create.",
        "error": None
    }

    sample_guide = generate_heuristic_guide({
        "app_name": "Linear",
        "provider_domain": "linear.app",
        "sources": mock_sources,
    })

    with patch.object(search_service, "search_provider_docs", AsyncMock(return_value=mock_sources)), \
         patch.object(fetch_service, "fetch_and_extract", AsyncMock(return_value=mock_fetch)), \
         patch.object(llm_router, "generate_structured_guide", AsyncMock(return_value=(sample_guide, "mock_llm", "mock_model", None))):
        
        response = client.post("/api/research-runs", json={
            "app_name": "Linear",
            "website_url": "https://linear.app",
            "integration_intent": "Read issues and sync pull requests"
        })
        assert response.status_code == 201
        run_id = response.json()["run_id"]

        # Poll status until completed (near-instant with mocked network)
        run_data = None
        for _ in range(30):
            res = client.get(f"/api/research-runs/{run_id}")
            assert res.status_code == 200
            run_data = res.json()
            if run_data["status"] in ("completed", "failed"):
                break
            time.sleep(0.1)

        assert run_data is not None
        assert run_data["status"] == "completed", f"Run failed with error: {run_data.get('error')}"
        assert run_data["guide_id"] is not None

        # Fetch generated guide by ID
        guide_id = run_data["guide_id"]
        guide_res = client.get(f"/api/guides/{guide_id}")
        assert guide_res.status_code == 200
        guide_payload = guide_res.json()
        assert guide_payload["id"] == guide_id
        assert guide_payload["content"]["app"]["name"] == "Linear"
        assert len(guide_payload["content"]["steps"]) > 0

        # Verify newly generated app appears in directory listing
        apps_res = client.get("/api/apps?q=linear")
        assert apps_res.status_code == 200
        apps = apps_res.json()
        assert any(a["name"] == "Linear" for a in apps)

def test_all_llm_providers_failing_marks_run_failed_without_heuristic_fake():
    """Validates that when all LLM providers fail, the orchestrator returns an explicit incomplete/failed state without creating a fake validated guide."""
    mock_sources = [
        {
            "title": "Doc",
            "url": "https://example.com/docs",
            "domain": "example.com",
            "source_type": "official_documentation",
            "is_official": True,
            "snippet": "OAuth"
        }
    ]
    mock_fetch = {
        "url": "https://example.com/docs",
        "http_status": 200,
        "fetch_status": "success",
        "content": "Sample Documentation",
        "error": None
    }

    # Simulate both providers failing
    with patch.object(search_service, "search_provider_docs", AsyncMock(return_value=mock_sources)), \
         patch.object(fetch_service, "fetch_and_extract", AsyncMock(return_value=mock_fetch)), \
         patch.object(llm_router, "generate_structured_guide", AsyncMock(return_value=(None, None, None, "OpenRouter 429 | Groq 503"))):
        
        response = client.post("/api/research-runs", json={
            "app_name": "FailingLLMApp",
            "website_url": "https://example.com"
        })
        assert response.status_code == 201
        run_id = response.json()["run_id"]

        run_data = None
        for _ in range(30):
            res = client.get(f"/api/research-runs/{run_id}")
            run_data = res.json()
            if run_data["status"] in ("completed", "failed"):
                break
            time.sleep(0.1)

        assert run_data["status"] == "failed"
        assert run_data["guide_id"] is None
        assert "AI synthesis incomplete" in run_data["error"]

def test_enforce_evidence_grounding_downgrades_unsupported_claims():
    """Validates that claims without official fetched sources are downgraded from verified to estimated/unknown."""
    from app.services.research_orchestrator import enforce_evidence_grounding

    evidence = {
        "app_name": "TestGrounding",
        "provider_domain": "testgrounding.com",
        "sources": [
            {
                "id": "src_01",
                "title": "Secondary Blog",
                "url": "https://blog.com/test",
                "domain": "blog.com",
                "source_type": "secondary",
                "is_official": False,
            }
        ]
    }
    guide = generate_heuristic_guide(evidence)
    # Artificially set step 1 to verified with only secondary source ref
    guide.steps[0].evidence_status = "verified"
    guide.steps[0].evidence_refs = ["src_01"]

    fetched_evidence = [
        {
            "id": "src_01",
            "fetch_status": "success",
            "http_status": 200,
            "is_official": False,
        }
    ]

    grounded_guide = enforce_evidence_grounding(guide, fetched_evidence)
    # Must be downgraded from verified to estimated because source is secondary
    assert grounded_guide.steps[0].evidence_status == "estimated"
