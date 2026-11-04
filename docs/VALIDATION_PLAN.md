# Validation and Demo Plan

## 1. Validation objective

Show that the product gives developers actionable, trustworthy setup guidance and that its agent performs real research rather than generating a plausible-looking generic OAuth checklist.

## 2. Test matrix

| Test | App/type | What it validates |
|---|---|---|
| Seeded guide | GitHub | OAuth App vs GitHub App nuance; registration steps and sources |
| Seeded guide | Google | Scope-dependent consent-screen/verification complexity |
| Seeded guide | Slack | Scope types and provider-specific app configuration |
| Live generation | An unfamiliar public app selected during demo | Search, official-doc discovery, extraction, structured generation, persistence and sharing |
| Fallback | Simulate OpenRouter timeout/429 | Groq generates from same evidence package |
| Single provider | Configure only one key | App still works with available provider |
| No API key | Remove LLM key | Seeded guides work; live generation gives actionable configuration message |
| SSRF safety | Submit localhost/private IP URL | URL is rejected before fetch |
| Prompt injection | A fetched page contains “ignore previous instructions” | Agent treats it as untrusted content and does not obey |
| Shareability | Open generated URL in fresh browser | Saved guide loads without the original run state |

## 3. Source validation checklist

For every seeded guide and at least one generated guide:

- Open all cited URLs manually.
- Confirm the source belongs to the provider or is clearly labeled secondary.
- Compare every critical claim against the page.
- Confirm the app/product type is correctly identified.
- Confirm callback/redirect requirements are stated accurately.
- Confirm scope names and verification triggers are not invented.
- Confirm approval wait time is unknown unless a reliable published window exists.
- Check whether the provider recommends an alternative to OAuth (e.g., a provider-specific app type).
- Record any correction made after manual review.

## 4. What counts as an actual setup attempt?

Valid attempted evidence includes:
- Navigating to a public developer portal landing page.
- Inspecting visible registration form labels without submission.
- Confirming that a page requires sign-in before deeper inspection.
- Fetching an official doc and recording HTTP status.

Not equivalent to a completed setup:
- Reading a tutorial.
- Opening a login page.
- Finding a “Create app” button.
- Generating a client ID in a hypothetical example.

If credentials/sign-in are required, stop and record a human handoff. Do not fabricate a successful registration.

## 5. Heuristic checks

A guide is review-ready only if:
- It has a named app/provider and primary official source(s).
- It states the auth product or clearly marks ambiguity.
- It includes a useful ordered setup path.
- It separates active setup from external wait.
- It has source references for critical requirements.
- It says what the agent attempted and what it could not test.
- It identifies human-only steps.
- It lists unknowns rather than filling gaps with guesses.

## 6. Manual acceptance test

1. Launch frontend and backend.
2. Search GitHub and open the guide.
3. Check the guide explains OAuth App vs GitHub App and links to official docs.
4. Navigate to Google and Slack guides.
5. Enter a new provider by name or URL.
6. Observe actual research stages and source discovery.
7. Open generated guide and inspect evidence/source links.
8. Copy the guide URL and open it in another browser tab/session.
9. Trigger model fallback and verify the guide is still produced.
10. Test invalid/private URL rejection.

## 7. What to include in submission README/demo

- Live deployed URL.
- GitHub repository URL.
- How to run locally.
- Which apps are seeded.
- One unfamiliar app used in live-generation demo.
- Which sources were manually checked.
- What was actually attempted in provider portals.
- Which requirements remain unknown.
- Known limitations (in-process job runner, limited app set, no logged-in setup, no provider submission).

## 8. Evaluation-aligned narrative

Explain that the prototype is intentionally narrow but demonstrates both parts of the assignment: a small library with real guides, and on-demand agent research that can extend beyond the library. Emphasize evidence quality and transparent human handoff over number of screens or complexity of the agent framework.
