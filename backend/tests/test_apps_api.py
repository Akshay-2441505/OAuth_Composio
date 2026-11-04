from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_apps():
    response = client.get("/api/apps")
    assert response.status_code == 200
    apps = response.json()
    assert len(apps) >= 3
    slugs = [a["slug"] for a in apps]
    assert "github" in slugs
    assert "google" in slugs
    assert "slack" in slugs

def test_search_apps():
    # Search for GitHub
    response = client.get("/api/apps?q=git")
    assert response.status_code == 200
    apps = response.json()
    assert len(apps) == 1
    assert apps[0]["slug"] == "github"

    # Search for non-existent app
    response = client.get("/api/apps?q=nonexistentappxyz")
    assert response.status_code == 200
    apps = response.json()
    assert len(apps) == 0

def test_get_app_detail():
    response = client.get("/api/apps/github")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "github"
    assert data["name"] == "GitHub"
    assert data["managed_oauth_status"] == "available"
    assert data["guide_id"] == "guide_github"

def test_get_app_guide():
    response = client.get("/api/apps/github/guide")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "github"
    assert data["origin"] == "seeded"
    assert data["status"] == "validated"
    assert "content" in data
    assert data["content"]["app"]["name"] == "GitHub"

def test_get_guide_by_id():
    response = client.get("/api/guides/guide_github")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "guide_github"
    assert len(data["content"]["steps"]) > 0

def test_get_guide_sources():
    response = client.get("/api/guides/guide_github/sources")
    assert response.status_code == 200
    sources = response.json()
    assert len(sources) >= 4
    domains = [s["domain"] for s in sources]
    assert all("github.com" in d for d in domains)

