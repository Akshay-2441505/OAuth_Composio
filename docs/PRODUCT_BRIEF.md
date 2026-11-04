# Product Brief — OAuth Compass

## Working name

**OAuth Compass** — working title only; rename if desired.

## One-line proposition

Help developers understand what it takes to make an app integration OAuth-ready, then turn provider-specific research into an actionable, source-backed setup guide they can follow and share.

## Problem

An agent developer wants to support an external app. Before end users can connect their accounts, the developer may need to register an OAuth application, configure callback URLs and scopes, prepare public app information, and satisfy provider verification or approval requirements. The process is distributed across documentation and provider consoles. Developers struggle to estimate effort, identify blockers and know which tasks can be automated.

## Product thesis

The product is a **readiness and research layer**, not another connector runtime. Existing infrastructure products offer useful reference patterns:

- Composio: managed OAuth versus custom credentials; help users avoid unnecessary app registration where managed auth fits.
- Nango: highlight provider-specific auth nuances rather than emitting generic OAuth boilerplate.
- Pipedream: make a broad catalogue searchable and filterable.
- Apideck: make connection/setup status visible.
- Paragon: show a practical integration setup sequence.
- WorkOS: account for providers with custom or unusual OAuth configuration.

These references inform design patterns only. We should not claim feature parity or copy their implementation.

## Primary users

1. **AI-agent developer:** wants an app connected to an agent and needs to understand OAuth prerequisites, scopes, redirects and approval.
2. **Integration engineer / technical operator:** manages multiple provider onboarding processes and needs a repeatable checklist and status.
3. **Founder / technical generalist:** needs to know whether setup is a quick task or a multi-week dependency before committing to an integration.

## Core jobs to be done

- When I decide to support an app, tell me whether I need my own OAuth app or whether a managed option is sufficient.
- Show me the provider-specific registration, scopes, redirect and verification steps.
- Give me a realistic split between hands-on setup and external waiting time.
- Tell me what an agent can research/prepare and where I must take over.
- Let me share the same researched guide with a teammate.
- When an app is missing, investigate it and create a guide from evidence.

## Scope decision

The submission should demonstrate the **complete core loop**:

`Discover app → understand readiness → follow guide → investigate new app → save/share generated guide`.

Seed three varied guides: GitHub, Google and Slack. GitHub is the first and most deeply validated demo guide. Google and Slack demonstrate that the same schema can represent different provider nuances. The system should be able to generate a guide for an unfamiliar app entered by name or URL.

## Non-goals for the take-home

- Registering OAuth apps automatically in provider consoles.
- Obtaining real provider approvals.
- Collecting/storing provider client secrets, access tokens or refresh tokens.
- Implementing the actual end-user OAuth connection flow.
- Building 100 fully researched guides.
- Building a production-grade crawler, SaaS authentication, billing, team workspaces, queue infrastructure or analytics suite.
- Claiming a guaranteed approval timeline.

## Differentiating product principles

1. **Readiness before instructions:** first explain whether a custom app is required and why.
2. **Provider-specific, not generic:** discover the correct OAuth product, scopes and portal for each provider.
3. **Evidence over confident prose:** show URLs, retrieval dates and confidence/evidence state.
4. **Time transparency:** separate active work from external review/wait time.
5. **Human/agent boundary:** make actions the agent can do and actions requiring user login/approval explicit.
6. **Freshness:** show when the guide was last researched; do not imply it is permanently current.

## Success definition

A developer who has not seen the product before can select a known app or submit a new one, understand the next steps and likely effort, inspect the supporting sources, and share the result without a verbal walkthrough.
