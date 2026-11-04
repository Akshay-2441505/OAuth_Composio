# Data Model and API Contract

This is a deliberately small schema for the take-home. Prefer JSON stored in SQLite columns for flexible guide content, with separate rows for apps, guides, sources and research runs.

## 1. Core entities

### App

| Field | Type | Notes |
|---|---|---|
| `id` | UUID/string | Primary key |
| `slug` | string | Unique human-readable URL key |
| `name` | string | Display name |
| `website_url` | string | Canonical public homepage |
| `provider_domain` | string | Provider domain used for source ranking |
| `category` | string | Developer tools, productivity, etc. |
| `auth_types` | string[]/JSON | OAuth2, OAuth1, API key, etc. |
| `managed_oauth_status` | enum | available / not_available / unknown / not_checked |
| `managed_oauth_source_url` | nullable string | Evidence URL if status was checked |
| `created_at`, `updated_at` | datetime | Timestamps |

### Guide

| Field | Type | Notes |
|---|---|---|
| `id` | UUID/string | Stable shareable ID |
| `app_id` | nullable FK | Null for newly discovered provider if no app row yet |
| `slug` | string | Optional human-readable share slug |
| `origin` | enum | seeded / generated |
| `status` | enum | researched / validated / partial / needs_review |
| `content_json` | JSON | Validated GuideSchema payload |
| `version` | integer | Start at 1 |
| `created_at`, `updated_at` | datetime | Timestamps |
| `last_researched_at` | nullable datetime | When sources were last fetched |
| `is_public` | boolean | MVP defaults true for shareable guide |

### Source

| Field | Type | Notes |
|---|---|---|
| `id` | string | Source ID referenced by guide findings |
| `guide_id` | FK | Parent guide |
| `title`, `url`, `domain` | string | Source metadata |
| `source_type` | string | official_documentation / official_portal / support / secondary |
| `is_official` | boolean | Determined by provider domain allowlist/review |
| `retrieved_at` | datetime | When fetched |
| `http_status` | nullable integer | Fetch outcome |
| `fetch_status` | string | success / blocked / failed / partial |
| `relevance_note` | string | Why source is included |

### ResearchRun

| Field | Type | Notes |
|---|---|---|
| `id` | UUID/string | Run ID |
| `input_name` | nullable string | Original name input |
| `input_url` | nullable string | Original URL input |
| `normalized_domain` | nullable string | Resolved domain |
| `status` | enum | queued / identifying / searching / fetching / analyzing / validating / completed / partial / failed |
| `stage_log_json` | JSON | Timestamped actual events |
| `provider_used` | nullable string | openrouter / groq |
| `model_used` | nullable string | Model ID |
| `fallback_reason` | nullable string | Sanitized error category |
| `guide_id` | nullable FK | Created guide |
| `error_message` | nullable string | User-safe failure reason |
| `started_at`, `completed_at` | datetime | Timestamps |

## 2. Guide JSON schema (conceptual)

Use Pydantic models as the actual validator. This is a readable contract; implementation can refine optional fields while preserving meaning.

```json
{
  "app": {
    "name": "GitHub",
    "website_url": "https://github.com",
    "provider_domain": "github.com",
    "category": "Developer tools"
  },
  "readiness": {
    "recommended_auth_product": "GitHub App or OAuth App depending on requirements",
    "custom_oauth_app_required": "conditional",
    "managed_oauth": {
      "status": "unknown",
      "source_url": null,
      "checked_at": null
    },
    "complexity": "medium",
    "complexity_rationale": "The correct GitHub app type depends on access and installation needs."
  },
  "time_estimates": {
    "active_setup": {
      "minimum_minutes": 30,
      "maximum_minutes": 60,
      "confidence": "low",
      "basis": "Prototype estimate based on documented registration/configuration steps.",
      "evidence_refs": []
    },
    "external_wait": {
      "status": "unknown",
      "minimum_hours": null,
      "maximum_hours": null,
      "basis": "No reliable provider review window established by sources reviewed.",
      "evidence_refs": []
    }
  },
  "approval": {
    "required": "unknown",
    "triggers": [],
    "requirements": [],
    "unknowns": []
  },
  "prerequisites": [],
  "steps": [
    {
      "id": "step_01",
      "title": "Choose the correct GitHub app type",
      "description": "Compare GitHub App and OAuth App based on access requirements.",
      "portal_url": "https://docs.github.com/en/apps/overview",
      "owner": "developer",
      "requires_login": false,
      "requires_secret": false,
      "verification": "Decision recorded before registration.",
      "evidence_status": "verified",
      "evidence_refs": []
    }
  ],
  "blockers": [],
  "agent_capabilities": [],
  "human_actions_required": [],
  "findings": [],
  "sources": [],
  "assumptions": [],
  "uncertainties": [],
  "last_researched_at": "ISO-8601 timestamp"
}
```

For MVP time estimates, do not use the example numbers as validated GitHub estimates. Treat them as placeholder values until tested and reviewed. If no defensible estimate exists, return `unknown`.

## 3. REST endpoints

### Directory

- `GET /api/apps?q=&category=&auth_type=` — list/search apps.
- `GET /api/apps/{slug}` — app metadata and summary.
- `GET /api/apps/{slug}/guide` — latest seeded/saved guide for app.

### Research

- `POST /api/research-runs`
  - Body: `{ "app_name": "Example", "website_url": "https://example.com", "integration_intent": "optional" }`
  - Response: `{ "run_id": "...", "status": "queued" }`
- `GET /api/research-runs/{run_id}` — current status, stage log and guide ID when complete.

### Guides

- `GET /api/guides/{guide_id}` — persisted public guide.
- `GET /api/guides/{guide_id}/sources` — optional separate source list endpoint.
- `POST /api/guides/{guide_id}/refresh` — defer unless time permits.

### Health

- `GET /api/health` — simple health status.

## 4. Example research run response

```json
{
  "run_id": "run_abc123",
  "status": "fetching",
  "stages": [
    {"name": "identify", "status": "completed", "message": "Resolved provider domain."},
    {"name": "search", "status": "completed", "message": "Found official developer documentation."},
    {"name": "fetch", "status": "running", "message": "Reading OAuth setup and verification pages."}
  ],
  "guide_id": null,
  "error": null
}
```

## 5. Error states

- Invalid URL/scheme: `400` with explanation.
- Private/localhost/metadata host: reject before fetch.
- Research provider not configured: `503` with environment setup instructions.
- No relevant official docs: return partial guide or a clear research failure; do not invent.
- LLM provider failure: attempt fallback; if all fail, mark run failed and retain collected sources.
- Invalid schema after repair: mark run partial/failed and preserve diagnostics without exposing stack traces.
