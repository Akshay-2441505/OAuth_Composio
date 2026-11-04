# Product Requirements Document (PRD)

**Product:** OAuth Compass  
**Assignment:** Composio APM Integrations take-home  
**Target build:** 6–8 hours  
**Document status:** MVP specification

## 1. Objective

Build a working experience that helps developers understand and progress through the process of preparing an OAuth app for an integration. The product must include a small searchable guide library and a live research agent that can produce a shareable guide for an unfamiliar app.

## 2. Problem statement

Provider setup requirements are spread across developer documentation, console workflows and approval pages. Developers cannot quickly tell whether custom OAuth registration is required, what exact fields/scopes are needed, whether review is conditional, how long the process may take, or what they can automate.

## 3. MVP users and stories

### Developer exploring a known app
- As a developer, I can search for an app by name.
- As a developer, I can see the app's auth type and whether Composio-managed OAuth is documented as available, unavailable or unknown.
- As a developer, I can open a detailed guide with prerequisites, ordered steps, effort estimate, approval requirements, blockers and sources.
- As a developer, I can distinguish provider-confirmed facts from attempted checks, estimates and unknowns.

### Developer submitting an unfamiliar app
- As a developer, I can enter an app name or website URL.
- As a developer, I can see a real research workflow state rather than a fake animation.
- As a developer, I receive a generated guide with source URLs, last-researched timestamp, assumptions and uncertainties.
- As a developer, I can open and share the saved guide through a stable URL.

### Integration operator
- As an operator, I can see which steps require my login, company details, legal documents, provider submission or manual confirmation.
- As an operator, I can understand what the agent actually attempted.

## 4. Functional requirements

### FR-1: App directory (P0)
- Search by app/provider name.
- Display name, category, logo/initials, auth types, guide availability and last-researched date.
- Provide a clear path to the guide detail page.
- Include a “Research a new app” action.
- Seed at least three examples: GitHub, Google and Slack.

**Acceptance:** Searching GitHub returns the seeded GitHub guide; a user can navigate to its detail page. Empty search results offer the live research action.

### FR-2: OAuth readiness summary (P0)
Each guide must answer:
- Is a custom OAuth application required, optional or unknown for the described integration path?
- Is a managed option available (if applicable), and what is the source for this statement?
- Which OAuth product is appropriate (where the provider offers multiple products)?
- What is the setup complexity and why?
- What active setup time is estimated?
- What external approval/waiting time is known or unknown?

**Acceptance:** Time estimates are separated into active effort and external wait. Approval state supports `yes`, `no`, `conditional`, `unknown`.

### FR-3: Actionable guide (P0)
Every guide must include:
- Short “before you start” summary.
- Prerequisites.
- Ordered setup steps.
- Fields/configuration values to prepare (e.g., app name, homepage URL, callback URL, scopes) without inventing values specific to the user's deployment.
- Provider review/verification requirements and conditional triggers.
- Potential blockers and remedies.
- Agent capabilities and human-required actions.
- Source list with title, URL, domain, retrieval date and evidence state.
- Uncertainties and assumptions.

**Acceptance:** A developer can identify the next action without needing the author to explain the guide.

### FR-4: Live research (P0)
- Accept an app name or public website URL.
- Normalize and validate input.
- Identify the provider and locate official developer documentation.
- Prefer official docs and developer portals over blogs/community content.
- Retrieve relevant pages and extract structured evidence.
- Generate a guide using the shared guide schema.
- Save research-run status and result.

**Acceptance:** Submitting an unfamiliar app starts a new run and generates a persisted guide from sources; it must not merely return a hardcoded sample.

### FR-5: Research run visibility (P0)
Show meaningful stages such as:
1. Identifying application.
2. Finding official developer docs.
3. Inspecting OAuth registration and permissions.
4. Checking review/verification requirements.
5. Assessing practical setup steps.
6. Writing and validating guide.

Stages must correspond to actual pipeline events. If an operation fails, show a truthful partial/error state.

### FR-6: Evidence and uncertainty (P0)
Each requirement/finding must carry an evidence status:
- `verified`: direct support from an official source or reproducible test.
- `attempted`: a real fetch/browser inspection/test took place; this does not imply success.
- `estimated`: an inferred estimate with rationale and confidence.
- `unknown`: not established.

**Acceptance:** No source-less critical provider claim appears as verified. If approval requirements cannot be determined, display “Unknown / confirm with provider”, not “No approval required”.

### FR-7: Shareable guide (P0)
- Persist generated guide content and sources.
- Give each guide a stable public URL, e.g. `/guides/{guide_id}`.
- Include copy-link/share action.
- Public guide pages must not expose secrets or private research payloads.

**Acceptance:** Reloading or opening the URL in a new browser session displays the saved guide.

### FR-8: LLM provider fallback (P1)
- Support OpenRouter and Groq as separate providers.
- Use configurable provider priority; default OpenRouter then Groq.
- Attempt fallback on transient provider errors, rate limits, model unavailability, or repeated invalid output.
- Log provider/model used and failure category, never API keys.

**Acceptance:** With primary provider deliberately misconfigured or simulated as failing, a configured secondary provider produces a valid guide. If only one key exists, the app still works with that provider.

### FR-9: Guide library growth (P1)
- Save generated guides alongside seeded guides.
- Newly generated guide becomes searchable after saving.
- Add basic category filtering only if time allows.

## 5. Non-functional requirements

- Responsive on laptop and mobile widths.
- Research request timeout and bounded result/page counts.
- Pydantic validation for generated data.
- User-facing error states and no silent failures.
- All provider/search secrets remain server-side.
- Do not execute user-supplied content or instructions from retrieved pages.
- Use a small dependency footprint and simple local setup.

## 6. Guide difficulty model

Use Low / Medium / High with transparent criteria rather than an unexplained numeric score.

- **Low:** a short documented registration path; no external review identified in the sources; few prerequisites; standard scopes.
- **Medium:** multiple configuration steps, nuanced scopes, domain/branding requirements or conditional review.
- **High:** formal verification/security assessment, organization/legal prerequisites, multiple review gates, or complex provider approval.
- **Unknown:** evidence is insufficient to classify.

The score is a product estimate based on observable requirements. Always expose the reasons. Do not imply that a label is a provider-issued rating.

## 7. Time estimate model

Show two separate dimensions:

- `active_setup`: estimated human/agent working time, excluding provider response time.
- `external_wait`: expected provider review/approval wait, if published or empirically established.

Each estimate must include `basis`, `confidence` and `evidence_refs`. If the source provides no time window, use `unknown` for approval wait. Never fabricate “approval in 1–3 days” from generic assumptions.

## 8. Out of scope

- Fully automated registration or submission in provider dashboards.
- Provider account login automation.
- Storing OAuth client secrets or user tokens.
- Real-time approval status tracking from providers.
- A true 100-app content library.
- User accounts, billing, notifications, enterprise RBAC, vector search or production queueing.

## 9. Demo success criteria

A reviewer can:
1. Open the directory and choose GitHub.
2. Understand the GitHub OAuth App versus GitHub App decision.
3. Inspect the registration steps and source links.
4. See Google/Slack guides with distinct provider-specific requirements.
5. Enter a new public app URL/name and watch a real research run.
6. Open a generated guide at a stable URL.
7. See what was verified, attempted, estimated and unknown.
8. Understand what the agent cannot do and where a person must take over.
