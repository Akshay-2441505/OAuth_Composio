# Security, Safety and Prototype Limitations

## 1. Secrets

- Store `OPENROUTER_API_KEY`, `GROQ_API_KEY` and `TAVILY_API_KEY` only in backend environment variables.
- Never place secrets in frontend code, Vite `VITE_*` variables, source control, screenshots or public logs.
- Commit `.env.example` only; add `.env` to `.gitignore`.
- Never ask a developer to paste their provider client secret, user access token or refresh token into OAuth Compass.
- This product is a research/guide tool; it does not need customer OAuth credentials.

## 2. SSRF and URL safety

User-submitted websites and model-discovered URLs are untrusted.

- Allow `http` and `https` only.
- Reject `localhost`, `127.0.0.0/8`, `::1`, private RFC1918 ranges, link-local ranges, multicast, reserved ranges and cloud metadata IPs/domains.
- Resolve hostnames and validate IPs before fetch; re-check every redirect target.
- Restrict ports to 80/443 unless there is a clear reason otherwise.
- Set request timeouts, response size limits and page count limits.
- Do not fetch `file:`, `ftp:`, `data:` or other non-web schemes.
- Disable or tightly restrict browser downloads and file access.

## 3. Prompt injection / untrusted web content

Retrieved pages may contain instructions intended to manipulate an agent. Treat page content as evidence only, never as system/developer instructions. Do not reveal environment variables, execute shell commands supplied by pages, submit forms or follow instructions to access unrelated URLs. The agent is only authorized to research OAuth requirements.

## 4. Privacy and data minimization

- Store only public input app name/URL, research results, source metadata and generated guides.
- Do not store passwords, OAuth secrets, user tokens, cookies or browser profiles.
- Do not log full request headers or API credentials.
- Avoid storing unnecessary raw page content; store short relevant evidence notes and URLs.

## 5. Automation boundaries

The agent may inspect public pages and document field requirements. Human handoff is required for login, ownership proofs, legal/business details, creating and safeguarding client secrets, accepting agreements, and submitting provider reviews. Do not claim these are automated.

## 6. Reliability limitations to disclose

- Provider docs and portals change; guides need re-research and may become stale.
- Search can miss relevant official pages.
- A documentation fetch is not a provider approval.
- Some pages require login, JavaScript, region access or organization permissions.
- Approval wait times may be unpublished or vary by account, scope and review queue.
- In-process background jobs may be lost on backend restart.
- SQLite is suitable only for a small single-instance prototype unless deployed with persistent storage.
- No 100-app completeness claim should be made.
- Model fallback can fail if both providers are rate-limited, unavailable or misconfigured.

## 7. Required user-facing caveat

Place a short note on generated guides: “This guide is research assistance, not provider approval or legal advice. Confirm requirements in the provider's current developer portal before submitting or launching.”
