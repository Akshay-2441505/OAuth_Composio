# Competitive References and Product Patterns

This document records inspiration for the assignment. These products solve adjacent integration/authentication problems; OAuth Compass should not attempt to rebuild their connector runtime.

## 1. Composio — managed OAuth vs custom auth

Reference: https://docs.composio.dev/docs/authentication/custom-app-vs-managed-app

Useful patterns:
- Explain when a developer can use a managed OAuth application and avoid registering their own.
- Explain when custom credentials are needed (e.g. consent branding, custom scopes, quota needs or custom provider instances).
- Make the managed/custom decision part of the readiness summary, with the evidence and date it was checked.

Product decision:
- Show managed OAuth status as `available`, `not_available`, `unknown` or `not_checked`.
- Do not imply that Composio-managed auth exists for every app. Look it up and cite the current directory/docs.

## 2. Nango — provider-specific authentication details

Reference: https://nango.dev/

Useful patterns:
- Provider auth implementations differ; a generic OAuth checklist will miss real-world nuances.
- Explain scopes, refresh behavior, token types and provider-specific setup.
- Distinguish credentials provided by an integration platform from credentials owned by the developer.

Product decision:
- The guide schema has provider-specific requirements and explicit uncertainties.
- Avoid hardcoded universal OAuth assumptions.

## 3. Pipedream Connect — searchable app catalogue

Reference: https://pipedream.com/apps

Useful patterns:
- Searchable directory.
- App category and auth metadata.
- Clear app-level navigation and discovery.

Product decision:
- Build a small searchable library first, but design data records so the catalogue can grow. A 100-app library is the long-term direction, not the take-home content requirement.

## 4. Apideck Vault — connection state clarity

Reference: https://www.apideck.com/vault

Useful patterns:
- Make setup/connection status visible.
- Separate what the platform can handle from what the developer/customer must do.

Product decision:
- Show setup progress and human handoff points in the guide. This is not a live provider approval tracker.

## 5. Paragon — concrete integration setup sequence

Reference: https://docs.useparagon.com/

Useful patterns:
- Walk the developer through selecting an integration, registering/configuring an app with the provider, then entering credentials/configuration in the integration platform.
- Explain callback URL and scope requirements at the point they matter.

Product decision:
- Use explicit numbered steps with location/portal, required fields, verification check and source link.

## 6. WorkOS — custom and unfamiliar providers

Reference: https://workos.com/docs

Useful patterns:
- Some platforms support custom provider definitions because not every application has a prebuilt configuration.
- Provider-specific authorization/token URLs and scope configuration matter.

Product decision:
- Live research must accept an unfamiliar app and discover its auth product and configuration rather than relying on a fixed app catalogue.

## 7. What we are not building

- Not a unified API connector runtime.
- Not an OAuth token vault.
- Not an OAuth client library.
- Not a provider approval submission service.
- Not another generic AI chat interface.

## 8. Our specific gap/opportunity

Existing integration/auth products primarily help developers connect apps, store/refresh credentials or manage integrations. This take-home is narrower and upstream: help the developer understand the readiness path before a provider-side application is usable. The product should turn fragmented docs and console requirements into an actionable, evidence-backed plan.

## Source hierarchy

The competitor docs above are product-design references only. For provider-specific OAuth facts, use the provider's own official documentation as the primary evidence. For example:

- GitHub requirements → `docs.github.com`.
- Google requirements → official Google Identity / Cloud documentation.
- Slack requirements → `api.slack.com`.

Never use GitHub docs as a generic source for non-GitHub apps.
