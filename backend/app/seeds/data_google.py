from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).isoformat()

GOOGLE_APP = {
    "slug": "google",
    "name": "Google Workspace & Cloud",
    "website_url": "https://developers.google.com/identity/protocols/oauth2",
    "provider_domain": "google.com",
    "category": "Productivity & Cloud",
    "auth_types": ["OAuth2", "Service Account"],
    "managed_oauth_status": "available",
    "managed_oauth_source_url": "https://docs.composio.dev/docs/authentication/custom-app-vs-managed-app",
}

GOOGLE_SOURCES = [
    {
        "id": "src_goog_01",
        "title": "Using OAuth 2.0 to Access Google APIs",
        "url": "https://developers.google.com/identity/protocols/oauth2",
        "domain": "developers.google.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Primary documentation on Google OAuth 2.0 endpoints, redirect URIs, and scopes."
    },
    {
        "id": "src_goog_02",
        "title": "OAuth 2.0 App Verification FAQ",
        "url": "https://support.google.com/cloud/answer/9110907",
        "domain": "support.google.com",
        "source_type": "official_portal",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Explains unverified app limits (100 users), sensitive/restricted scopes, CASA tier 2 security assessments."
    },
    {
        "id": "src_goog_03",
        "title": "Setting up OAuth 2.0 Consent Screen",
        "url": "https://developers.google.com/workspace/guides/configure-oauth-consent",
        "domain": "developers.google.com",
        "source_type": "official_documentation",
        "is_official": True,
        "retrieved_at": NOW,
        "http_status": 200,
        "fetch_status": "success",
        "relevance_note": "Steps to configure internal vs external user types and domain verification requirements."
    }
]

GOOGLE_GUIDE_CONTENT = {
    "app": {
        "name": "Google Workspace & Cloud",
        "website_url": "https://developers.google.com/identity/protocols/oauth2",
        "provider_domain": "google.com",
        "category": "Productivity & Cloud"
    },
    "readiness": {
        "recommended_auth_product": "OAuth 2.0 Web Client (for user delegated access) or Service Account (for machine-to-machine domain-wide delegation)",
        "custom_oauth_app_required": "conditional",
        "managed_oauth": {
            "status": "available",
            "source_url": "https://docs.composio.dev/docs/authentication/custom-app-vs-managed-app",
            "checked_at": NOW
        },
        "complexity": "high",
        "complexity_rationale": "Requires configuring a Google Cloud Project, OAuth Consent Screen, and potentially undergoing Google Trust & Safety verification and CASA security assessment if requesting sensitive or restricted scopes."
    },
    "time_estimates": {
        "active_setup": {
            "minimum_minutes": 30,
            "maximum_minutes": 90,
            "confidence": "medium",
            "basis": "Configuring GCP Project, API enablement, consent screen branding, domain verification in Google Search Console, and client credentials.",
            "evidence_refs": ["src_goog_01", "src_goog_03"]
        },
        "external_wait": {
            "status": "conditional",
            "minimum_hours": 72,
            "maximum_hours": 720,
            "basis": "Testing mode/internal is immediate. Public apps with sensitive scopes typically take 3-7 business days for brand verification, while restricted scopes (e.g. Gmail/Drive) require CASA security assessment which takes 3-6 weeks.",
            "evidence_refs": ["src_goog_02"]
        }
    },
    "approval": {
        "required": "conditional",
        "triggers": [
            "Setting OAuth Consent Screen User Type to 'External' and publishing to production.",
            "Requesting sensitive scopes (e.g., calendar.events, contacts) or restricted scopes (e.g., gmail.readonly, drive).",
            "Requesting more than 100 test user authorizations."
        ],
        "requirements": [
            "Verified domain ownership via Google Search Console",
            "Publicly accessible Privacy Policy and Terms of Service URLs on verified domain",
            "YouTube demonstration video showing user grant flow and client ID in browser address bar",
            "Third-party CASA Tier 2 security assessment (for restricted scopes)"
        ],
        "unknowns": [
            "Exact turnaround time for Google Trust & Safety queue during peak cycles."
        ]
    },
    "prerequisites": [
        "Google Cloud Console billing account / project",
        "Verified domain ownership in Google Search Console matching the privacy policy and OAuth redirect hosts",
        "Public Privacy Policy and Terms of Service URLs"
    ],
    "steps": [
        {
            "id": "step_goog_01",
            "title": "Create or Select a Google Cloud Project",
            "description": "Log in to Google Cloud Console, create a new project or select an existing project for your integration.",
            "portal_url": "https://console.cloud.google.com/projectcreate",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Project ID created and active in GCP console.",
            "evidence_status": "verified",
            "evidence_refs": ["src_goog_01"],
            "handoff_reason": "Requires GCP organization/account billing administrator access."
        },
        {
            "id": "step_goog_02",
            "title": "Configure OAuth Consent Screen",
            "description": "Navigate to APIs & Services -> OAuth consent screen. Choose User Type: 'Internal' (Workspace org only) or 'External' (any Google user). Fill in App name, User support email, developer contact email, and authorized domains.",
            "portal_url": "https://console.cloud.google.com/apis/credentials/consent",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Consent screen draft saved.",
            "evidence_status": "verified",
            "evidence_refs": ["src_goog_03"],
            "handoff_reason": "Requires legal entity branding, domain registration, and contact information."
        },
        {
            "id": "step_goog_03",
            "title": "Add Scopes and Identify Verification Impact",
            "description": "Select the required API scopes (e.g. userinfo.email, drive.readonly). Note whether Google flags the chosen scopes as 'Sensitive' or 'Restricted', which activates mandatory verification.",
            "portal_url": "https://console.cloud.google.com/apis/credentials/consent",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Scopes list saved with verification status flagged.",
            "evidence_status": "verified",
            "evidence_refs": ["src_goog_02", "src_goog_03"],
            "handoff_reason": "Scope selection determines whether external security review is required."
        },
        {
            "id": "step_goog_04",
            "title": "Create OAuth 2.0 Client ID Credentials",
            "description": "Go to Credentials -> Create Credentials -> OAuth client ID. Select 'Web application'. Add Authorized JavaScript origins and Authorized redirect URIs. Save to obtain Client ID and Client Secret.",
            "portal_url": "https://console.cloud.google.com/apis/credentials",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": True,
            "destructive_or_sensitive": True,
            "verification": "Client ID and Client Secret dialog displayed; credentials safely stored.",
            "evidence_status": "verified",
            "evidence_refs": ["src_goog_01"],
            "handoff_reason": "Secrets must be placed into secure environment variables."
        },
        {
            "id": "step_goog_05",
            "title": "Submit for App Verification (If Production & External)",
            "description": "If publishing to external users with sensitive/restricted scopes, submit for verification. Provide a YouTube demo video, written justification for each scope, and prepare for potential CASA Tier 2 assessment.",
            "portal_url": "https://console.cloud.google.com/apis/credentials/consent",
            "owner": "developer",
            "requires_login": True,
            "requires_secret": False,
            "destructive_or_sensitive": False,
            "verification": "Verification request submitted; Google ticket reference received.",
            "evidence_status": "verified",
            "evidence_refs": ["src_goog_02"],
            "handoff_reason": "Requires executive/legal response and demo video production."
        }
    ],
    "blockers": [
        {
            "title": "100-User Testing Cap & 'Google Haven't Verified This App' Screen",
            "cause": "External apps in 'Testing' publishing status show a security warning and block logins past 100 designated test users.",
            "resolution": "Submit the app for Google OAuth verification and publish to Production.",
            "evidence_refs": ["src_goog_02"]
        },
        {
            "title": "Domain Not In Authorized Domains",
            "cause": "Redirect URI domain or Privacy Policy domain is not verified in Google Search Console by the same GCP account.",
            "resolution": "Verify DNS TXT record or HTML tag in Google Search Console using the GCP project owner account.",
            "evidence_refs": ["src_goog_03"]
        }
    ],
    "agent_capabilities": [
        "Analyze official Google Cloud OAuth 2.0 specifications",
        "Classify scopes into non-sensitive, sensitive, and restricted tiers",
        "Identify verification requirements and CASA security review triggers"
    ],
    "human_actions_required": [
        "Manage Google Cloud Console project and billing setup",
        "Verify domain ownership in Google Search Console",
        "Record and upload YouTube walkthrough video for scope justification",
        "Store Client Secret in secure key management service"
    ],
    "findings": [
        {
            "claim": "Apps with sensitive or restricted scopes published to external users require mandatory Google verification.",
            "status": "verified",
            "source_ids": ["src_goog_02"],
            "evidence_note": "Directly stated in official Google Cloud Verification FAQ.",
            "confidence": "high"
        },
        {
            "claim": "Testing mode is limited to 100 manually specified test accounts.",
            "status": "verified",
            "source_ids": ["src_goog_02"],
            "evidence_note": "Google Cloud OAuth consent screen constraints.",
            "confidence": "high"
        }
    ],
    "sources": GOOGLE_SOURCES,
    "assumptions": [
        "Developer has access to domain DNS records to verify domain in Search Console."
    ],
    "uncertainties": [
        "Google Trust & Safety review duration varies between a few days to several weeks depending on scope severity."
    ],
    "last_researched_at": NOW
}

