# UX / Design Specification

## 1. Design goal

Make OAuth readiness understandable at a glance, while keeping technical detail available to developers. The product should feel like a focused developer tool—not a generic chatbot and not a marketing landing page.

## 2. Information architecture

### Routes

- `/` — Explore / app directory.
- `/apps/:slug` — Seeded or known app guide.
- `/generate` — Submit app name or website and follow research.
- `/guides/:id` — Persisted shareable guide (works after reload).

Avoid user login for the MVP.

## 3. Main page: Explore

### Header
- Product mark and name: OAuth Compass.
- Primary action: “Research an app”.
- Optional small explanation: “Understand the path to OAuth readiness”.

### Search and filters
- Search input accepts provider/app name.
- Small filters: category, auth type and difficulty (filters can be deferred if they slow implementation).
- Directory cards show:
  - App name and category.
  - Authentication type(s), not assumed OAuth-only.
  - Guide status and last-researched date.
  - Managed OAuth status as `Available`, `Not available` or `Unknown` only when evidence exists.
  - Complexity label with a short reason.
  - “View guide” action.

### Empty state
“No guide yet. Research this app” should lead to `/generate` with the search text prefilled.

## 4. App guide page

Use a structured document layout. Top summary should contain:

- Provider/app name and website.
- Guide status (Seeded / AI-generated; Researched / Validated / Needs review).
- “Last researched” timestamp.
- Complexity (Low / Medium / High / Unknown) plus one-line rationale.
- Whether custom OAuth app is required/optional/unknown for the use case.
- Managed OAuth availability and source, if assessed.
- Active setup effort and external approval wait in separate fields.
- Share/copy-link control.

### Guide sections

1. **Start here** — recommended path and key decision.
2. **Before you start** — provider account, company/domain, app URL, privacy policy, callback URL, required scopes, prerequisites.
3. **Step-by-step setup** — numbered steps with action, location/portal, what to enter, how to verify completion and source.
4. **Approval and verification** — `Not identified`, `Conditional`, `Required` or `Unknown`; list trigger and requirements separately.
5. **Potential blockers** — blocker, why it occurs, how to resolve and source.
6. **What the agent can do** — research docs, extract fields, inspect public setup pages, draft checklist.
7. **What you must do** — sign in, provide business/legal information, create secrets in provider console, submit for review, accept provider terms.
8. **Evidence and sources** — grouped by official / secondary source; show title, domain, retrieved date and evidence status.
9. **Assumptions and unknowns** — explicit list.

### Evidence labels

Use text labels plus icon, not color alone:
- Verified
- Attempted
- Estimated
- Unknown

Provide a tooltip or short explanatory note for each. Never use “Verified” just because an LLM returned a confident answer.

## 5. Live guide generation page

### Input
- One text field: app name or website URL.
- Optional intent field: “What do you want to do with this app?” It helps identify relevant scopes. Do not make it mandatory in the MVP.
- CTA: “Research and generate guide”.

### Progress UI
Display a vertical timeline of the actual pipeline steps:
- Identify application.
- Search for official developer docs.
- Read OAuth setup pages.
- Extract registration/scopes/approval requirements.
- Check for setup blockers.
- Validate evidence and generate guide.

Each item can be `queued`, `running`, `completed`, `partial` or `failed`. Use backend-reported stage events or polling state; do not animate fake steps.

### Completion
- Show summary card and CTA “Open guide”.
- Copy shareable URL.
- Show count of official sources and any unresolved research items.
- If the research failed, provide a useful failure reason and allow retry.

## 6. Visual direction

- Style: calm, precise, technical, high information density with generous spacing.
- Light theme by default; dark mode optional only if quick.
- Neutral backgrounds, restrained accent color, strong typography and clear dividers.
- Prefer compact tables/checklists for configuration data.
- Avoid dashboard clutter, fake metrics and decorative charts.
- Use a consistent icon set such as Lucide.
- Keep complexity labels neutral; reserve strong color for actual warnings and completion.
- All cards and controls must be functional.

## 7. Important interaction details

- “Copy guide link” copies the canonical URL, not an internal API endpoint.
- Source links open the original provider docs in a new tab.
- Long pages use a sticky in-page table of contents if implementation time permits.
- Unknown values should not be rendered as zero or false.
- When `approval_required = conditional`, show the condition prominently.
- When time is unknown, write “Not published / not confirmed” rather than omitting the field.
- Guide updates should show a version or last-researched time so the user knows when the research was performed.

## 8. Mobile behavior

- Single-column app cards.
- Search full width.
- Guide sections collapse into accordions only where helpful; keep the readiness summary visible near the top.
- Source URLs wrap safely and controls remain tappable.
