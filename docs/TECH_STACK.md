# Technical Stack and Dependencies

## 1. Stack decision

Choose the stack that maximizes working product scope within 6–8 hours and fits the developer's existing React/FastAPI experience.

| Layer | Choice | Reason |
|---|---|---|
| IDE/agentic development | Google Antigravity | Build assistance, workspace rules and browser/tool workflows |
| Frontend | React + Vite + TypeScript | Familiar, fast local dev and static deployment |
| Styling | Tailwind CSS | Fast consistent layout |
| UI primitives | shadcn/ui or small custom components | Accessible dialogs, badges, forms and tables without overbuilding |
| Icons | lucide-react | Consistent interface icons |
| Backend | Python 3.12 + FastAPI | Simple JSON API and async-friendly endpoints |
| Validation | Pydantic v2 | Strong validation for model-generated guide data |
| Database | SQLite + SQLAlchemy 2.x | No hosted DB setup required for prototype; persists guides locally |
| HTTP | httpx | Async fetching of public provider documentation |
| Page extraction | Trafilatura, with BeautifulSoup fallback | Extract readable main content from documentation pages |
| Browser fallback | Playwright (optional) | Only for JS-rendered public pages that HTTP extraction cannot read |
| Search | Tavily Search API | Shared model-independent search layer |
| Primary LLM | OpenRouter | OpenAI-compatible endpoint and broad model selection |
| Fallback LLM | Groq | Separate provider endpoint for inference fallback |
| Tests | pytest + httpx TestClient; Vitest/React Testing Library if time | Verify schema, API and critical UI behavior |
| Deployment | Vercel (frontend) + Render/Fly.io/Railway (backend) | Simple split deployment; use a persistent disk for SQLite if supported |

## 2. Important architecture decision: search is not the model

Do **not** rely exclusively on OpenRouter's built-in web search if Groq is intended to be a true fallback. Provider-specific server tools differ. Instead, use a shared research layer:

1. Tavily searches for candidate URLs.
2. A source-ranking function prioritizes official provider/developer documentation.
3. HTTPX fetches public pages.
4. Trafilatura extracts readable content; Playwright is an optional fallback for dynamic pages.
5. The same normalized evidence package is sent to OpenRouter or Groq for analysis and guide generation.

This requires a `TAVILY_API_KEY` in addition to the two LLM API keys. It avoids coupling source discovery to one model vendor. Verify current Tavily plans/limits before using; do not assume a free quota is permanent.

Alternative: OpenRouter offers `openrouter:web_search` and `openrouter:web_fetch`, and Groq offers browser search for certain GPT-OSS models. Those can be used as provider-specific adapters, but the tool behavior and returned evidence differ; that is more work to make reliable for a 6–8 hour build.

## 3. Model provider adapter

Use the OpenAI Python SDK against each provider's OpenAI-compatible API endpoint, or their official SDKs if needed.

- OpenRouter base URL: `https://openrouter.ai/api/v1`
- Groq base URL: `https://api.groq.com/openai/v1`

Configuration:

- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`
- `GROQ_API_KEY`
- `GROQ_MODEL`
- `AI_PROVIDER_ORDER=openrouter,groq`

Use separate model IDs. Do not assume the same model ID is supported at both vendors. Set the model IDs after checking each provider's current model catalogue. Groq's current browser-search documentation lists `openai/gpt-oss-20b` and `openai/gpt-oss-120b` as supported browser-search models; however, the recommended architecture uses Tavily for search, so Groq's browser-search-specific limitation is not required.

## 4. Model fallback behavior

Implement a small `LLMProvider` interface with `generate_structured(...)`.

Recommended behavior:
1. Try providers in `AI_PROVIDER_ORDER`.
2. On timeout, network error, rate limit, transient 5xx, provider/model unavailable, or repeated invalid structured output, try the next configured provider.
3. On authentication/configuration errors (e.g., bad key), log a clear setup error and optionally try the next provider if configured; do not hide that the first key is misconfigured.
4. Validate response with Pydantic. If invalid, attempt one repair/retry with a compact validation error. Then fail over.
5. Record provider/model, elapsed time and failure category in the research run; never log key values or full sensitive headers.
6. If only one provider key is present, use that provider. If neither is present, disable live generation with an actionable setup message; seeded guides remain usable.

**Keys are not combined.** The app selects one provider per inference attempt. A fallback is a second independent API request, not a blended credential.

## 5. Suggested Python dependencies

Minimum backend:

```txt
fastapi
uvicorn[standard]
pydantic>=2
pydantic-settings
sqlalchemy>=2
httpx
trafilatura
beautifulsoup4
openai
python-dotenv
pytest
```

Optional:

```txt
playwright
```

Add Playwright browser binaries only if needed. Avoid adding LangChain, LlamaIndex, vector DBs or agent frameworks unless implementation demonstrates a concrete need; a transparent workflow/orchestrator is sufficient.

## 6. Suggested frontend dependencies

```txt
react
react-dom
react-router-dom
lucide-react
zod
```

Plus Vite, TypeScript, Tailwind and optionally shadcn/ui setup. Keep API calls in one typed client module.

## 7. API keys required

| Key | Required? | Purpose |
|---|---|---|
| `OPENROUTER_API_KEY` | One LLM key required; preferred | Primary guide-analysis/generation provider |
| `GROQ_API_KEY` | Optional but recommended | Fallback model provider |
| `TAVILY_API_KEY` | Recommended/required for selected search design | Find relevant public docs independently of LLM vendor |
| `COMPOSIO_API_KEY` | No | Only if later adding a Composio API lookup; not required for this MVP |
| GitHub OAuth client ID/secret | No | The product researches public docs; it does not register/use GitHub OAuth on behalf of users |
| GitHub PAT | No | Public GitHub docs do not require one for this use case |

Never place secrets in `VITE_*` environment variables or in the browser bundle. Keep them in backend `.env` locally and backend deployment environment settings remotely.

## 8. Hosting notes

- Vercel serves the React app.
- Deploy FastAPI separately.
- Set frontend API base URL to the backend URL.
- SQLite is acceptable for the prototype only if the hosting service provides persistent disk storage. Otherwise use a small managed PostgreSQL instance (e.g., Supabase) or another persistent DB.
- Configure CORS for the deployed frontend origin.
- Add a backend health check endpoint.
