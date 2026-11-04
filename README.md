# OAuth Compass — Integration Readiness & Research Layer

**OAuth Compass** is a developer intelligence tool built for the Composio APM Integrations assignment. It helps developers understand what it takes to make an external service OAuth-ready *before* writing integration code or setting up connection runtimes.

The product combines a searchable library of verified guides with a live AI research agent that can investigate unfamiliar apps using public official developer documentation.

---

## 1. Key Value Proposition & Problem Solved

When AI-agent builders and integration engineers want to connect external applications (like GitHub, Google, Slack, Notion, or Linear), they face:
- Dispersed developer documentation and opaque console workflows.
- Ambiguous architectural choices (e.g. GitHub Apps vs. GitHub OAuth Apps).
- Hidden review/verification requirements (e.g. Google CASA security reviews for restricted scopes).
- Conflated active setup time vs. third-party review waiting time.
- Security concerns regarding how OAuth client credentials and tokens should be handled.

**OAuth Compass solves this upstream**:
1. **Readiness Before Implementation:** Tells developers whether custom app registration is necessary or if Composio managed auth is available.
2. **Provider-Specific Guidance:** Discovers the exact portal URLs, scope requirements, and approval triggers from official docs.
3. **Time Transparency:** Keeps active hands-on setup time (minutes) strictly separate from external review waiting time (days/weeks).
4. **Evidence & Truthfulness:** Every claim is categorized as `verified`, `attempted`, `estimated`, or `unknown` and linked to its source.
5. **Zero Secret Storage:** Never collects, logs, or stores client secrets, user access tokens, or refresh tokens.
6. **Shareable & Persistent:** Every guide is stored in SQLite and accessible at a permanent URL (e.g., `/guides/:id`).

---

## 2. System Architecture

```text
┌────────────────────────────────────────────────────────┐
│               React + Vite + TypeScript UI             │
│   (/ Explore Directory, /apps/:slug, /generate, /guides/:id)│
└───────────────────────────┬────────────────────────────┘
                            │ REST API (JSON)
┌───────────────────────────▼────────────────────────────┐
│                  FastAPI Backend Server                │
│    (SSRF Validation, SQLite/SQLAlchemy 2.x Persistence) │
└──────┬────────────────────┬────────────────────┬───────┘
       │                    │                    │
┌──────▼───────┐     ┌──────▼───────┐     ┌──────▼────────┐
│ Search Layer │     │ Fetch Engine │     │ LLM Fallback  │
│ Tavily API / │     │ HTTPX +      │     │ Router:       │
│ Heuristic    │     │ Trafilatura  │     │ 1. OpenRouter │
│ Discovery    │     │ (SSRF Safe)  │     │ 2. Groq       │
└──────────────┘     └──────────────┘     └───────────────┘
```

---

## 3. Seeded Demo Guides & Verified Nuances

The system seeds three verified guides demonstrating varied provider architectures:

| Provider | Recommended Product | Key Nuance & Decision | External Approval SLA | Primary Source |
|---|---|---|---|---|
| **GitHub** | **GitHub App** (for granular repo/org permissions) or **OAuth App** (for simple user identity) | Explains why GitHub Apps are preferred over legacy OAuth Apps; highlights default 8-hour token expiration with refresh tokens and 10 callback URL limit. | **Instant / None** (self-service; only Marketplace listings require review) | [GitHub Building OAuth Apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps) |
| **Google Workspace & Cloud** | **OAuth 2.0 Web Client** | Explains OAuth Consent Screen User Types (Internal vs. External), 100 test-user caps, and mandatory CASA Tier 2 security assessment for restricted scopes (Gmail/Drive). | **Conditional** (Instant for testing; 3–6 weeks for restricted scopes) | [Google Identity OAuth 2.0](https://developers.google.com/identity/protocols/oauth2) |
| **Slack** | **Slack App with OAuth 2.0 (v2)** | Differentiates Bot Token Scopes (`chat:write`) from User Token Scopes; explains Slack App Manifest imports. | **Instant** for workspace installs; 2–4 weeks only for public App Directory | [Slack OAuth v2 Docs](https://api.slack.com/authentication/oauth-v2) |

---

## 4. Evidence State Model

OAuth Compass avoids fabricated AI claims by tagging every fact and requirement:
- **`verified`**: Directly established by an official provider documentation URL or empirical test.
- **`attempted`**: Public inspection or HTTP fetch performed by the system; does not imply provider approval.
- **`estimated`**: Engineering estimate with transparent rationale and confidence level.
- **`unknown`**: Information not published or unconfirmed in available documentation.

---

## 5. Security Invariants & Safe Crawling

1. **SSRF Guard:** All submitted URLs and redirect targets are resolved via DNS. IP addresses matching loopback (`127.0.0.0/8`, `::1`), private networks (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), or cloud metadata IPs (`169.254.169.254`) are immediately rejected.
2. **Prompt Injection Mitigation:** All fetched web documentation is treated as untrusted reference material. System prompts explicitly forbid the model from executing commands found inside scraped pages.
3. **No Credential Storage:** The product is a research layer, not an OAuth token vault. Client secrets, personal access tokens, and end-user passwords are never requested or persisted.

---

## 6. Quickstart: Running Locally

### Prerequisites
- Python 3.12+ (tested on Python 3.13)
- Node.js 18+ & npm

### Step 1: Backend Setup
```powershell
# Navigate to backend directory
cd backend

# Create virtual environment and activate
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# (Optional) Copy .env and configure your keys
cp .env.example .env
# Configure OPENROUTER_API_KEY, GROQ_API_KEY, or TAVILY_API_KEY if available.
# (If unconfigured, the app falls back to offline heuristic research mode).

# Run backend server
uvicorn app.main:app --reload --port 8000
```
*Backend will start on `http://localhost:8000` and automatically seed GitHub, Google, and Slack into SQLite.*

### Step 2: Frontend Setup
```powershell
# In a new terminal, navigate to frontend directory
cd frontend

# Install packages
npm install

# Start Vite dev server
npm run dev
```
*Frontend will open on `http://localhost:5173` with an automatic proxy forwarding `/api` calls to port 8000.*

---

## 7. Running the Automated Test Suite

The backend includes 26 pytest tests covering API endpoints, schema validation, SSRF security, LLM provider fallback, and live research generation:

```powershell
cd backend
.venv\Scripts\pytest -v
```

**Test Coverage Summary:**
- `test_apps_api.py`: App directory listing, search queries, and guide fetching.
- `test_health.py`: Health endpoint and provider configuration status.
- `test_schemas.py`: Pydantic validation of seed guides and referential integrity of source IDs.
- `test_ssrf_safety.py`: Rejection of loopback, AWS/GCP metadata IP, private subnets, non-HTTP schemes, and invalid ports.
- `test_llm_fallback.py`: Provider fallback from OpenRouter to Groq on simulated 429/timeout, schema repair loop, and end-to-end research generation with SQLite persistence.
- `test_research_pipeline.py`: Source domain ranking and background research run execution.

---

## 8. Disclosed Prototype Limitations

- **In-Process Job Execution:** Background research runs execute using FastAPI `BackgroundTasks` persisted to SQLite. A production deployment would use a durable distributed queue (e.g. Celery or BullMQ).
- **Public Documentation Only:** The agent inspects publicly accessible developer portals and documentation; it does not log in to provider accounts or submit apps for review on the user's behalf.
- **Dynamic JS-Rendered Pages:** The fetcher uses HTTPX and Trafilatura. SPAs requiring heavy client-side JavaScript rendering without static fallback are skipped to avoid long headless browser wait times.
