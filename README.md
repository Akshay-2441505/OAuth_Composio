# OAuth Compass — Developer Integration Readiness & Research Layer

**OAuth Compass** is a developer intelligence tool built for the **Composio APM Integrations** assignment. It empowers developers and AI-agent builders to evaluate integration complexity, review registration steps, and verify managed OAuth availability *before* writing integration code or setting up runtime connections.

The product combines a searchable catalog of verified reference guides with an autonomous AI research agent that inspects unfamiliar platforms using official developer documentation.

---

## 1. Key Architectural & Product Decisions

### 1. Dual-Provider LLM Fallback (Groq $\rightarrow$ OpenRouter)
* **Primary LLM:** Groq routing to `llama-3.3-70b-versatile` on ultra-fast LPU inference hardware ($\approx$10–15s structured synthesis).
* **Secondary LLM (Automatic Failover):** OpenRouter routing to `meta-llama/llama-3.3-70b-instruct` for high-fidelity fallback.
* **Resilience Behavior:** The router catches HTTP 429 rate limits, connection timeouts, and provider downtime. If an LLM returns malformed JSON, a targeted repair attempt is executed before failing safely. The system never fabricates unverified data if both models fail.

### 2. Tavily Search & Deterministic Documentation Discovery
* Uses the **Tavily Search API** specialized for developer documentation discovery.
* Official domains are ranked using a relevance scoring engine (`source_ranker.py`) that prioritizes official documentation portals (e.g., `docs.github.com`, `developers.google.com`) over forums or blog posts.

### 3. Pre-Seeded Verified Reference Guides
The catalog includes out-of-the-box verified guides that highlight real-world architectural trade-offs:
* **GitHub:** Detailed comparison between **GitHub Apps** (fine-grained repository permissions, 8-hour token expiration) and **OAuth Apps** (coarse account-wide scopes).
* **Google Workspace & Cloud:** Clarifies internal vs. external consent screens, test user quotas (100 cap), and mandatory CASA Tier 2 third-party security assessments for restricted scopes (Gmail/Drive).
* **Slack:** Demarcates Bot Token Scopes (`chat:write`) from User Token Scopes and provides App Manifest YAML import instructions.

### 4. Zero-Credential Security Principle
* OAuth Compass is strictly a **pre-integration research layer**.
* It never requests, accepts, logs, or stores OAuth client secrets, access tokens, refresh tokens, or developer passwords.

### 5. Unified Zero-Latency Deployment
* Built with a multi-stage `Dockerfile` that builds the React/Vite SPA and embeds it directly into FastAPI.
* Eliminates CORS preflight overhead (`OPTIONS` requests), eliminates 50-second serverless cold starts, and allows background research runs to complete without timeout interruptions.

---

## 2. Architecture & Evidence Model

```text
┌────────────────────────────────────────────────────────┐
│               React + Vite + TypeScript UI             │
│    Dark Developer Workspace: #0A0E17 / #141C2E / #A3E635│
└───────────────────────────┬────────────────────────────┘
                            │ REST API (/api)
┌───────────────────────────▼────────────────────────────┐
│                  FastAPI Backend Server                │
│    (SSRF DNS Validation, SQLite/SQLAlchemy 2.x Store)  │
└──────┬────────────────────┬────────────────────┬───────┘
       │                    │                    │
┌──────▼───────┐     ┌──────▼───────┐     ┌──────▼────────┐
│ Search Layer │     │ Fetch Engine │     │ LLM Router:   │
│ Tavily API / │     │ HTTPX +      │     │ 1. OpenRouter │
│ Domain Scout │     │ Trafilatura  │     │ 2. Groq       │
└──────────────┘     └──────────────┘     └───────────────┘
```

Every claim is attributed using a standardized evidence model:
* **`verified`**: Supported directly by an official provider URL or deterministic test.
* **`attempted`**: Public inspection or HTTP fetch performed by the system; does not imply provider approval.
* **`estimated`**: Engineering estimate with transparent rationale and confidence level.
* **`unknown`**: Information not established in available public documentation.

---

## 3. Quickstart & Setup Instructions

### Option A: Running Locally (Fastest)

#### Prerequisites
* Python 3.10+ (tested on Python 3.12 and 3.13)
* Node.js 18+ & npm

#### 1. Configure Environment Variables
Copy `.env.example` to `.env` in the root directory:
```bash
cp .env.example .env
```
Add your API keys (the app gracefully falls back to offline heuristic research mode if keys are omitted):
```env
OPENROUTER_API_KEY=sk-or-v1-xxxx
GROQ_API_KEY=gsk_xxxx
TAVILY_API_KEY=tvly-xxxx
```

#### 2. Start Both Services with One Command (Windows PowerShell)
```powershell
.\run_app.ps1
```

#### Or Run Manually:
```bash
# Terminal 1 - Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

* **Frontend:** `http://localhost:5173`
* **Backend API Docs:** `http://localhost:8000/docs`
* **Health Check:** `http://localhost:8000/api/health`

---

### Option B: Cloud Deployment (Railway / Docker)

The repository includes a production-grade multi-stage `Dockerfile` and `railway.toml`:
1. Push your repository to GitHub.
2. In [Railway](https://railway.app), click **New Project** $\rightarrow$ **Deploy from GitHub repo**.
3. Select `OAuth_Composio`.
4. In **Variables**, add:
   * `OPENROUTER_API_KEY`
   * `GROQ_API_KEY`
   * `TAVILY_API_KEY`
5. In **Settings** $\rightarrow$ **Networking**, click **Generate Domain**.

---

## 4. Automated Test Suite (50 Passing Tests)

OAuth Compass includes a 50-test automated suite covering security, schemas, provider failover, and API endpoints:

```bash
cd backend
pytest -v
```

### Test Coverage Highlights
* `test_ssrf_safety.py`: Validates strict DNS-level rejection of IPv4 loopback, IPv6 loopback, link-local addresses, private subnets, cloud metadata IPs (`169.254.169.254`), and non-HTTP protocols.
* `test_llm_fallback.py`: Tests automatic failover from OpenRouter to Groq on simulated HTTP 429 and connection timeouts.
* `test_qa_audit.py`: Validates input length boundaries, malformed path sanitization, case-insensitive provider search, and Pydantic schema validation.
* `test_apps_api.py` & `test_research_pipeline.py`: Verifies app directory search filters, background task execution, and SQLite guide persistence.

---

## 5. Disclosed Prototype Limitations

1. **In-Process Task Execution:** Autonomous research runs execute via FastAPI `BackgroundTasks`. In a production scale deployment with hundreds of concurrent runs, this would be replaced with a durable distributed task queue like Celery or BullMQ with Redis.
2. **Public Documentation Inspection:** The agent analyzes publicly available developer documentation; it does not automatically register developer accounts or submit OAuth apps for provider review on the user's behalf.
3. **Static DOM Extraction:** Scraping utilizes HTTPX and Trafilatura. Complex single-page apps (SPAs) that require heavy JavaScript hydration or canvas rendering without fallback are skipped to maintain fast runtimes and avoid headless browser overhead.
4. **Local SQLite Persistence:** The prototype uses SQLite with SQLAlchemy for simplicity and zero-configuration setup. For multi-region serverless deployments, this would be migrated to PostgreSQL (e.g. Supabase or Neon).
