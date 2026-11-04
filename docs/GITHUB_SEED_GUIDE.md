# Seed Guide Research Notes — GitHub

**Purpose:** Use GitHub as the first and most carefully validated example in the product. These notes summarize official documentation available on 4 November 2026. Re-open the source pages before deploying; provider docs can change.

## 1. Key product decision

Do not assume the correct product is always a GitHub OAuth App. GitHub's documentation says GitHub Apps are generally preferred because they offer fine-grained permissions, more control over repository access and short-lived tokens. GitHub Apps can act on behalf of a user or independently; OAuth Apps act on behalf of a user. Both use OAuth 2.0 in their user authorization flow.

**Guide UX:** Start with “Which GitHub app type should I create?” and ask what the integration needs to access/do. Only present the OAuth App registration path when it fits the use case. For installation-based access, repository-level permissions or app-initiated actions/webhooks, evaluate GitHub App first.

Sources:
- [GitHub: Building OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps)
- [GitHub: GitHub Apps vs OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps)
- [GitHub: Deciding when to build a GitHub App](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/deciding-when-to-build-a-github-app)
- [GitHub Apps overview](https://docs.github.com/en/apps/overview)

## 2. OAuth App registration path (when OAuth App is appropriate)

The current official registration guide describes this path:

1. Sign in to GitHub.
2. Open account Settings.
3. Open Developer settings.
4. Select OAuth Apps.
5. Select New OAuth App (or Register a new application for a first app).
6. Enter an application name.
7. Enter the homepage URL.
8. Optionally provide an application description.
9. Enter the authorization callback URL.
10. Register the application.

The guide documents up to 10 callback URLs. Device flow can optionally be enabled if the application needs it. Token expiration is enabled by default for newly created OAuth Apps; the developer must ensure their app supports expiring tokens/refresh behavior as documented.

Source: [Creating an OAuth app](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app)

## 3. Authorization flow and callback

GitHub's web application authorization flow redirects the user to request identity, redirects back to the application, and then the app uses the user's access token to access the API. GitHub documents `client_id` as required and recommends specifying `redirect_uri`; if omitted, the first configured callback URL is used.

Source: [Authorizing OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)

## 4. Scopes and permissions

OAuth scopes limit what an OAuth token can access; they do not grant permissions beyond what the authorizing user already has. The guide should tell the developer to request only the scopes needed for the intended integration. Do not invent a scope list without the developer's intended actions.

Source: [Building OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps)

## 5. Security notes

GitHub's OAuth App best practices warn that a public client cannot keep a client secret confidential and recommend PKCE for public clients. For a server-side web application, protect tokens on the backend. Avoid wildcard callback matching unless necessary because it can expand redirect targets and create risk.

Source: [Best practices for creating an OAuth app](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/best-practices-for-creating-an-oauth-app)

## 6. Approval / wait time

The standard OAuth App registration instructions above describe registering an app and configuring its OAuth details. They do not establish a universal provider review/approval SLA. Therefore:

- Do not claim a guaranteed approval time.
- Do not assert that every GitHub integration needs no approval whatsoever.
- Show “No separate review step identified in the registration documentation reviewed; confirm organization policies and the exact product/distribution requirements.”
- Set external wait time to `unknown` unless additional official evidence establishes otherwise.

## 7. Example readiness summary (safe wording)

- **Recommended product:** depends on the use case; evaluate GitHub App first for integrations needing fine-grained repository/organization permissions or installation-based operation.
- **OAuth App registration:** documented self-service registration flow if the OAuth App is the right product.
- **Active effort:** provide a clearly labeled prototype estimate only after manually walking the flow; don't call it a provider SLA.
- **External wait:** unknown / no universal wait window established by the reviewed source set.
- **Agent can:** discover docs, explain app-type tradeoffs, extract required registration fields, inspect public documentation and draft a checklist.
- **Developer must:** sign in, create/register the app, configure the actual callback URL and scopes, safeguard client secrets, test the integration and handle any organization/provider requirements.

## 8. Validation record template

Complete this after manually checking the guide:

| Check | Result | Notes |
|---|---|---|
| Official docs open | Not yet tested | Add date and outcome |
| Registration steps match current UI/docs | Not yet tested | Record any mismatch |
| GitHub App vs OAuth App distinction correct | Not yet tested | Check against comparison page |
| Callback URL facts correct | Not yet tested | Link exact source |
| Scope facts correct | Not yet tested | Avoid invented scopes |
| Approval/wait claim appropriately qualified | Not yet tested | Keep unknown if unproven |
| Public portal inspection attempted | Not yet tested | Record if login is required |
