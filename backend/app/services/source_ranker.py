from urllib.parse import urlparse
from typing import Dict, Any

OFFICIAL_DOC_PREFIXES = ["docs.", "developer.", "developers.", "api.", "help.", "support."]

def extract_domain(url: str) -> str:
    try:
        parsed = urlparse(url)
        return parsed.hostname.lower() if parsed.hostname else ""
    except Exception:
        return ""

def is_domain_match(candidate_domain: str, provider_domain: str) -> bool:
    if not candidate_domain or not provider_domain:
        return False
    cand = candidate_domain.lower()
    prov = provider_domain.lower()
    return cand == prov or cand.endswith("." + prov)

def rank_source(url: str, title: str, provider_domain: str) -> Dict[str, Any]:
    domain = extract_domain(url)
    is_official = is_domain_match(domain, provider_domain)

    priority = 0
    source_type = "secondary"

    if is_official:
        source_type = "official_documentation"
        priority = 80
        # If subdomain is specifically docs/developers/api
        if any(domain.startswith(prefix) for prefix in OFFICIAL_DOC_PREFIXES):
            priority = 100
        elif "help." in domain or "support." in domain:
            source_type = "support"
            priority = 85
    else:
        # Reputable secondary sources
        if any(ref in domain for ref in ["composio.dev", "nango.dev", "oauth.net", "auth0.com"]):
            source_type = "secondary"
            priority = 50
        else:
            source_type = "secondary"
            priority = 20

    # Boost score if URL or title mentions oauth, scopes, credentials, or api
    url_lower = url.lower()
    title_lower = title.lower()
    for term in ["oauth", "create-app", "register", "scopes", "callback", "redirect"]:
        if term in url_lower or term in title_lower:
            priority += 5

    return {
        "url": url,
        "title": title,
        "domain": domain,
        "is_official": is_official,
        "source_type": source_type,
        "priority": priority,
    }

