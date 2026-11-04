# 6–8 Hour Build Plan

## Priority rule

Complete one working vertical slice before adding polish. The live research/generation path and evidence quality are more important than a large static directory.

## Milestone 0 — Workspace and decisions (20–30 min)

- Open the bundle in Antigravity.
- Read `AGENTS.md` and core docs.
- Confirm the workspace plan and folder structure.
- Create `.env` from `.env.example` (do not commit `.env`).
- Confirm at least one LLM key and search key are available.

**Exit:** agreed scaffold, environment verified and no unresolved architecture contradiction.

## Milestone 1 — Backend foundation (45–60 min)

- Create FastAPI app, CORS and `/api/health`.
- Add SQLite/SQLAlchemy models.
- Add seed records for GitHub, Google and Slack.
- Add directory and guide read endpoints.
- Add schema tests.

**Exit:** frontend or curl can read seeded apps and guides.

## Milestone 2 — Frontend library and guide (60–75 min)

- Build header, directory search and cards.
- Build guide page with readiness summary, steps and sources.
- Add loading/empty/error states.
- Add copy link.

**Exit:** user can browse seeded guides and a guide URL reloads.

## Milestone 3 — Research pipeline (90–120 min)

- Add input validation and safe URL normalization.
- Implement Tavily search adapter.
- Implement HTTPX + Trafilatura fetch/extraction.
- Add official-source ranking.
- Persist research run stage updates.

**Exit:** backend collects normalized sources for an unfamiliar public provider.

## Milestone 4 — LLM and structured guide (60–90 min)

- Implement OpenRouter adapter.
- Implement Groq adapter.
- Add ordered fallback and error classification.
- Create Pydantic guide schema.
- Generate, validate and persist a guide.

**Exit:** unfamiliar app produces a guide with sources and unknowns.

## Milestone 5 — Live research UI and shareability (45–60 min)

- Build generator form and real run progress display.
- Poll research-run endpoint.
- Link to saved guide on completion.
- Add copy/share action.

**Exit:** complete end-to-end generation flow works from browser.

## Milestone 6 — Validation, polish and deployment (60–90 min)

- Manually validate GitHub guide against official docs.
- Validate one Google/Slack sample and one generated guide.
- Test fallback, no-key error, invalid URL and share URL.
- Fix highest-impact UX issues.
- Deploy frontend/backend and set environment variables.
- Update submission README with limitations and sources.

**Exit:** reviewer can access and operate the deployed prototype.

## Cut list if time runs short

Cut in this order:
1. Dark mode.
2. Category filters beyond search.
3. Automatic guide refresh.
4. Playwright (keep HTTPX/Trafilatura and disclose dynamic-page limits).
5. Fancy animated progress UI.

Do not cut:
- Real live research for an unfamiliar app.
- Persisted shareable guide.
- Source URLs and evidence status.
- Clear active-time vs approval-wait distinction.
- Human/agent boundary.
- Manual validation of the GitHub guide.
