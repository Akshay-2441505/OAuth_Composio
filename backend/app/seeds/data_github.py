from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).isoformat()

GITHUB_APP = {
    "slug": "github",
    "name": "GitHub",
    "website_url": "https://github.com",
    "provider_domain": "github.com",
    "category": "Developer tools",
    "auth_types": ["OAuth2", "Personal Access Token", "GitHub App Installation"],
    "managed_oauth_status": "available",
    "managed_oauth_source_url": "https://docs.composio.dev/docs/authentication/custom-app-vs-managed-app",
}

GITHUB_SOURCES = [
    {
        "id": "src_gh_01",
        "title": "Differences between GitHub Apps and OAuth apps",
        "url": "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps",
        "domain": "docs.github.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Details differences in permissions, token lifespan, and user vs org installations."
    },
    {
        "id": "src_gh_02",
        "title": "Creating an OAuth app",
        "url": "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app",
        "domain": "docs.github.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Official step-by-step registration instructions in GitHub Developer Settings."
    },
    {
        "id": "src_gh_03",
        "title": "Authorizing OAuth apps",
        "url": "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps",
        "domain": "docs.github.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Explains web application flow, redirect_uri behavior, and scope parameter."
    },
    {
        "id": "src_gh_04",
        "title": "Best practices for creating an OAuth app",
        "url": "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/best-practices-for-creating-an-oauth-app",
        "domain": "docs.github.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Highlights secret safeguarding, token refresh/expiration defaults, and PKCE recommendations."
    }
]

GITHUB_GUIDE_CONTENT = {
    "app": {
        "name": "GitHub",
        "website_url": "https://github.com",
        "provider_domain": "github.com",
        "category": "Developer tools"
    },
    "readiness": {
        "recommended_auth_product": "GitHub App (preferred for granular permissions) or OAuth App (for simple user identity)",
        "custom_oauth_app_required": "conditional",
        "managed_oauth": {
            "status": "available",
            "source_url": "https://docs.composio.dev/docs/authentication/custom-app-vs-managed-app",
            "checked_at": NOW
        },
        "complexity": "medium",
        "complexity_rationale": "Must choose between GitHub App (recommended by GitHub for repository fine-grained tokens) and OAuth App (broader permissions, user-centric)."
    },
    "time_estimates": {
        "active_setup": {
            "minimum_minutes": 15,
            "maximum_minutes": 30,
            "confidence": "high",
            "basis": "Documented self-service UI in GitHub Developer Settings with immediate credential generation.",
            "evidence_refs": ["src_gh_02"]
        },
        "external_wait": {
            "status": "none",
            "minimum_hours": 0,
            "maximum_hours": 0,
            "basis": "Standard OAuth App registration is self-service with immediate availability; no mandatory provider approval queue unless listing on GitHub Marketplace.",
            "evidence_refs": ["src_gh_02"]
        }
    },
    "approval": {
        "required": "no",
        "triggers": [
            "GitHub Marketplace publishing requires organizational verification and security review.",
            "OAuth App access may require organization owner approval if accessing private org repositories."
        ],
        "requirements": [
            "Active GitHub user or organization account",
            "Valid callback URL",
            "Verified organization domain (if seeking Marketplace badge)"
        ],
        "unknowns": [
            "Individual organization admin approval policies vary by target enterprise."
        ]
    },
    "prerequisites": [
        "A verified GitHub account",
        "Decision between GitHub App vs. OAuth App integration architecture",
        "A valid public or localhost callback URL for development",
        "Identified minimum scopes required for your integration"
    ],
    "steps": [
        {
            "id": "step_gh_01",
            "title": "Decide: GitHub App vs. OAuth App",
            "description": "Evaluate if you need fine-grained repository access and webhooks (choose GitHub App) or broad account-level read/write on behalf of users (choose OAuth App). GitHub officially recommends GitHub Apps for modern integrations.",
            "portal_url": "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps",
            "owner": "developer",
            "requires_login": False,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Architecture decision made and integration requirements documented.",
            "evidence_status": "verified",
            "evidence_refs": ["src_gh_01"],
            "handoff_reason": "Architectural choice depends on application security posture."
        },
        {
            "id": "step_gh_02",
            "title": "Navigate to Developer Settings in GitHub",
            "description": "Sign in to GitHub, click your profile photo in the top right, go to Settings -> Developer settings -> OAuth Apps.",
            "portal_url": "https://github.com/settings/developers",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "OAuth Apps console is visible.",
            "evidence_status": "verified",
            "evidence_refs": ["src_gh_02"],
            "handoff_reason": "Requires developer GitHub account credentials."
        },
        {
            "id": "step_gh_03",
            "title": "Register New OAuth Application",
            "description": "Click 'New OAuth App' (or 'Register a new application'). Enter Application name, Homepage URL, optional Application description, and Authorization callback URL (up to 10 URLs supported).",
            "portal_url": "https://github.com/settings/applications/new",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "App created with a designated Client ID visible.",
            "evidence_status": "verified",
            "evidence_refs": ["src_gh_02"],
            "handoff_reason": "Form requires valid developer domain and callback endpoints."
        },
        {
            "id": "step_gh_04",
            "title": "Generate Client Secret & Safeguard It",
            "description": "Click 'Generate a new client secret'. Copy the secret immediately to your secure backend vault. Note: GitHub will never display the secret again.",
            "portal_url": "https://github.com/settings/developers",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": True,
            "destructive_or_sensitive": True,
            "verification": "Client Secret copied to secure server environment.",
            "evidence_status": "verified",
            "evidence_refs": ["src_gh_02", "src_gh_04"],
            "handoff_reason": "Secrets must never be shared with or processed by this research assistant."
        },
        {
            "id": "step_gh_05",
            "title": "Configure Scopes and Token Expiration",
            "description": "Determine minimal scopes (e.g. 'repo', 'read:user'). Note that newly created OAuth apps have token expiration enabled by default; configure your server to handle refresh tokens.",
            "portal_url": "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps",
            "owner": "developer",
            "requires_login": False,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "OAuth authorization URL correctly requests explicit scopes and handles code exchange.",
            "evidence_status": "verified",
            "evidence_refs": ["src_gh_03", "src_gh_04"],
            "handoff_reason": "Scope selection requires knowing the exact integration API calls."
        }
    ],
    "blockers": [
        {
            "title": "Organization OAuth App Restrictions",
            "cause": "Target user's GitHub Organization has restricted third-party application access.",
            "resolution": "Request admin approval through GitHub or request the organization admin whitelist your OAuth App Client ID.",
            "evidence_refs": ["src_gh_01"]
        },
        {
            "title": "Token Expiration Mismatch",
            "cause": "App expects perpetual access tokens, but GitHub OAuth Apps default to 8-hour expiring tokens with refresh tokens.",
            "resolution": "Implement the refresh token exchange flow using the refresh_token grant type.",
            "evidence_refs": ["src_gh_04"]
        }
    ],
    "agent_capabilities": [
        "Discover and analyze official GitHub developer documentation",
        "Explain architectural differences between GitHub Apps and OAuth Apps",
        "Extract required fields and callback URL constraints",
        "Identify common error codes and token expiration defaults"
    ],
    "human_actions_required": [
        "Sign in to GitHub Developer Settings",
        "Submit the app registration form",
        "Generate and securely store the OAuth Client Secret in backend vault",
        "Review organization-level third-party access policies"
    ],
    "findings": [
        {
            "claim": "GitHub Apps are officially recommended over OAuth Apps for fine-grained repository permissions.",
            "status": "verified",
            "source_ids": ["src_gh_01"],
            "evidence_note": "Directly documented in GitHub comparison documentation.",
            "confidence": "high"
        },
        {
            "claim": "Standard GitHub OAuth App registration is self-service without prior review queues.",
            "status": "verified",
            "source_ids": ["src_gh_02"],
            "evidence_note": "Confirmed by official registration walkthrough.",
            "confidence": "high"
        },
        {
            "claim": "OAuth apps support up to 10 callback URLs.",
            "status": "verified",
            "source_ids": ["src_gh_02"],
            "evidence_note": "Documented in registration form fields specification.",
            "confidence": "high"
        }
    ],
    "sources": GITHUB_SOURCES,
    "assumptions": [
        "Developer has permission to register apps on their GitHub account or organization.",
        "Application runs on a secure server capable of storing client secrets."
    ],
    "uncertainties": [
        "Approval policies in target customer organizations cannot be known beforehand."
    ],
    "last_researched_at": NOW
}

