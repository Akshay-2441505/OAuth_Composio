# First Antigravity Prompt

Paste the following into Antigravity after opening this folder as the workspace:

---

You are the senior full-stack engineer implementing **OAuth Compass**, a focused working prototype for the Composio APM Integrations take-home assignment.

First read `AGENTS.md` and the relevant documents in `docs/`. Then:

1. Summarize the user problem and the agreed MVP in your own words.
2. Propose a concrete folder structure for the React/Vite frontend and FastAPI backend.
3. Identify any conflicts or missing decisions in the docs before writing code. Do not invent provider-specific OAuth requirements.
4. Produce a milestone plan that fits a 6–8 hour prototype build.
5. Start with Milestone 1 only: scaffold the frontend/backend, add a health endpoint, add SQLite persistence, and seed the GitHub/Google/Slack directory records. Run the app and tests before moving on.

Important constraints:
- Build a functional MVP, not static mock screens.
- GitHub is the first demo guide, but its official docs are authoritative only for GitHub. Other providers must use their own official docs.
- For GitHub, explicitly distinguish GitHub OAuth Apps from GitHub Apps and explain the choice.
- Use separate OpenRouter and Groq API keys in a model-provider fallback chain. Do not merge keys.
- Keep search/fetch independent of the model vendor (Tavily + HTTPX/Trafilatura; Playwright only when needed), so model failover does not remove research capability.
- Validate generated guide JSON with Pydantic; preserve source URLs and evidence status.
- Never claim that an OAuth app was registered or approved unless that actually happened.
- Do not store provider OAuth secrets or end-user tokens.
- Do not expose API keys in frontend code.

Before each milestone, state exactly what you will implement. After each milestone, report changed files, commands/tests run, results, known issues and the next milestone. Do not skip validation.

---
