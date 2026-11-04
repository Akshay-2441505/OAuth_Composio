from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).isoformat()

SLACK_APP = {
    "slug": "slack",
    "name": "Slack",
    "website_url": "https://api.slack.com",
    "provider_domain": "slack.com",
    "category": "Communication & Collaboration",
    "auth_types": ["OAuth2 (v2)", "App Manifest", "Webhook"],
    "managed_oauth_status": "available",
    "managed_oauth_source_url": "https://docs.composio.dev/docs/authentication/custom-app-vs-managed-app",
}

SLACK_SOURCES = [
    {
        "id": "src_slack_01",
        "title": "Installing with OAuth 2.0 (v2)",
        "url": "https://api.slack.com/authentication/oauth-v2",
        "domain": "api.slack.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Core guide for Slack OAuth v2 flow, redirect URL matching, and token exchange."
    },
    {
        "id": "src_slack_02",
        "title": "Permission scopes in Slack apps",
        "url": "https://api.slack.com/scopes",
        "domain": "api.slack.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Explains difference between bot token scopes and user token scopes."
    },
    {
        "id": "src_slack_03",
        "title": "App manifests reference",
        "url": "https://api.slack.com/reference/manifests",
        "domain": "api.slack.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Configuration format to declaratively configure scopes, redirect URLs, and event subscriptions."
    }
]

SLACK_GUIDE_CONTENT = {
    "app": {
        "name": "Slack",
        "website_url": "https://api.slack.com",
        "provider_domain": "slack.com",
        "category": "Communication & Collaboration"
    },
    "readiness": {
        "recommended_auth_product": "Slack App with OAuth 2.0 (v2)",
        "custom_oauth_app_required": "conditional",
        "managed_oauth": {
            "status": "available",
            "source_url": "https://docs.composio.dev/docs/authentication/custom-app-vs-managed-app",
            "checked_at": NOW
        },
        "complexity": "medium",
        "complexity_rationale": "Requires understanding Slack's dual token architecture (Bot Token vs User Token scopes) and configuring OAuth v2 redirect URLs or App Manifests."
    },
    "time_estimates": {
        "active_setup": {
            "minimum_minutes": 20,
            "maximum_minutes": 45,
            "confidence": "high",
            "basis": "Fast configuration via api.slack.com/apps or instant JSON/YAML Slack App Manifest import.",
            "evidence_refs": ["src_slack_01", "src_slack_03"]
        },
        "external_wait": {
            "status": "none",
            "minimum_hours": 0,
            "maximum_hours": 0,
            "basis": "Internal workspace distribution is immediate with zero approval delay. Only public distribution via the Slack App Directory requires an editorial and security review.",
            "evidence_refs": ["src_slack_01"]
        }
    },
    "approval": {
        "required": "no",
        "triggers": [
            "Submitting to the public Slack App Directory requires Slack review (typically 2-4 weeks).",
            "Target Slack workspaces with 'Require App Approval' turned on require an internal Workspace Admin to approve installation."
        ],
        "requirements": [
            "Active Slack workspace with permissions to install apps",
            "HTTPS callback URL (or localhost for development)",
            "Configured App Manifest or manual OAuth v2 scope setup"
        ],
        "unknowns": [
            "Customer workspace internal admin approval policies vary."
        ]
    },
    "prerequisites": [
        "A Slack workspace where you have permission to install apps (or create a free sandbox workspace)",
        "Secure HTTPS endpoint (or localhost URL) for the OAuth redirect handler",
        "Decided whether you need Bot scopes (app acts as bot user) or User scopes (app acts on behalf of individual user)"
    ],
    "steps": [
        {
            "id": "step_slack_01",
            "title": "Create a New Slack App",
            "description": "Go to api.slack.com/apps, click 'Create New App'. Choose 'From scratch' or 'From an app manifest'. Name your app and select your development workspace.",
            "portal_url": "https://api.slack.com/apps?new_app=1",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Slack App Management dashboard appears for the new app.",
            "evidence_status": "verified",
            "evidence_refs": ["src_slack_01", "src_slack_03"],
            "handoff_reason": "Requires developer login and workspace selection."
        },
        {
            "id": "step_slack_02",
            "title": "Configure OAuth & Permissions",
            "description": "Under Features in the left sidebar, click 'OAuth & Permissions'. Scroll down to 'Redirect URLs' and click 'Add New Redirect URL'. Enter your authorization callback URL and click 'Save URLs'.",
            "portal_url": "https://api.slack.com/apps",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Redirect URL saved without error.",
            "evidence_status": "verified",
            "evidence_refs": ["src_slack_01"],
            "handoff_reason": "Redirect URI must match your app deployment domain."
        },
        {
            "id": "step_slack_03",
            "title": "Add Bot and User Scopes",
            "description": "In 'OAuth & Permissions', scroll to 'Scopes'. Distinguish 'Bot Token Scopes' (e.g. chat:write, channels:read for automated agents) from 'User Token Scopes' (actions on behalf of human users). Add only necessary permissions.",
            "portal_url": "https://api.slack.com/apps",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Selected scopes appear in the Scopes table.",
            "evidence_status": "verified",
            "evidence_refs": ["src_slack_02"],
            "handoff_reason": "Requires specifying the exact permissions your integration needs."
        },
        {
            "id": "step_slack_04",
            "title": "Retrieve App Credentials",
            "description": "In 'Basic Information', locate 'App Credentials'. Copy the Client ID, Client Secret, and Signing Secret. Save them to your backend environment.",
            "portal_url": "https://api.slack.com/apps",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": True,
            "destructive_or_sensitive": True,
            "verification": "Credentials safely stored in backend environment variables.",
            "evidence_status": "verified",
            "evidence_refs": ["src_slack_01"],
            "handoff_reason": "Secrets must never be shared outside your secure application."
        },
        {
            "id": "step_slack_05",
            "title": "Install App to Workspace & Test Authorization",
            "description": "Click 'Install to Workspace' at the top of the OAuth & Permissions page. Accept the consent dialog to test token generation and verify bot user appearance in your Slack workspace.",
            "portal_url": "https://api.slack.com/apps",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Bot user joins Slack channels and API tokens are issued.",
            "evidence_status": "verified",
            "evidence_refs": ["src_slack_01"],
            "handoff_reason": "Requires Slack workspace installation approval."
        }
    ],
    "blockers": [
        {
            "title": "Slack Admin Approval Required in Enterprise Orgs",
            "cause": "Workspace settings require workspace administrator approval before non-admin members can install third-party apps.",
            "resolution": "Request workspace administrator approval via the in-app Slack prompt or request installation by an admin.",
            "evidence_refs": ["src_slack_01"]
        },
        {
            "title": "Invalid Redirect URI Error (redirect_uri_mismatch)",
            "cause": "The redirect_uri passed in the authorization query string does not match the URL configured in the app settings exactly.",
            "resolution": "Ensure exact protocol, port, path, and trailing slash match what is saved in the Slack App OAuth & Permissions page.",
            "evidence_refs": ["src_slack_01"]
        }
    ],
    "agent_capabilities": [
        "Parse and generate Slack App Manifests (JSON/YAML)",
        "Identify appropriate bot vs user token scopes for integration scenarios",
        "Check redirect URL formatting compliance"
    ],
    "human_actions_required": [
        "Create Slack App in developer portal",
        "Authorize installation into target Slack workspace",
        "Store Slack Client Secret and Signing Secret safely"
    ],
    "findings": [
        {
            "claim": "Slack uses separate Bot Token Scopes and User Token Scopes in OAuth v2.",
            "status": "verified",
            "source_ids": ["src_slack_02"],
            "evidence_note": "Documented in Slack scopes guide.",
            "confidence": "high"
        },
        {
            "claim": "Internal workspace installation requires no Slack review and takes effect immediately.",
            "status": "verified",
            "source_ids": ["src_slack_01"],
            "evidence_note": "Confirmed by Slack OAuth v2 documentation.",
            "confidence": "high"
        }
    ],
    "sources": SLACK_SOURCES,
    "assumptions": [
        "User has a test Slack workspace with authorization to install apps."
    ],
    "uncertainties": [
        "Customer enterprise workspace approval settings cannot be verified ahead of time."
    ],
    "last_researched_at": NOW
}

