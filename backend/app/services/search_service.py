import logging
from typing import List, Dict, Any, Optional
import httpx
from app.config import settings
from app.services.source_ranker import rank_source, extract_domain
from app.services.ssrf_validator import is_safe_url

logger = logging.getLogger("oauth_compass.search")

class SearchService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.TAVILY_API_KEY

    async def search_provider_docs(self, app_name: str, provider_domain: str, intent: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Executes targeted OAuth queries using Tavily (or heuristic fallback if unconfigured).
        Ranks and filters official sources.
        """
        queries = [
            f"{app_name} OAuth developer documentation create app",
            f"{app_name} OAuth redirect callback URL scopes permissions",
            f"{app_name} app review verification approval requirements",
        ]
        if intent:
            queries.append(f"{app_name} API OAuth scopes for {intent}")

        candidates: Dict[str, Dict[str, Any]] = {}

        if self.api_key:
            async with httpx.AsyncClient(timeout=15.0) as client:
                for query in queries:
                    try:
                        logger.info(f"Tavily searching: '{query}'")
                        resp = await client.post(
                            "https://api.tavily.com/search",
                            json={
                                "api_key": self.api_key,
                                "query": query,
                                "search_depth": "advanced",
                                "include_domains": [provider_domain] if provider_domain else [],
                                "max_results": 5,
                            },
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            for item in data.get("results", []):
                                url = item.get("url", "").strip()
                                title = item.get("title", "")
                                snippet = item.get("content", "")
                                is_safe, reason = is_safe_url(url)
                                if is_safe and url not in candidates:
                                    ranked = rank_source(url, title, provider_domain)
                                    ranked["snippet"] = snippet
                                    candidates[url] = ranked
                        else:
                            logger.warning(f"Tavily search returned status {resp.status_code}: {resp.text}")
                    except Exception as e:
                        logger.error(f"Tavily search error for query '{query}': {e}")
        else:
            logger.info("TAVILY_API_KEY not configured; using heuristic doc URL discovery.")
            # Heuristic bootstrap URLs when search key is unconfigured
            candidates_urls = [
                f"https://docs.{provider_domain}",
                f"https://developers.{provider_domain}",
                f"https://developer.{provider_domain}",
                f"https://api.{provider_domain}",
                f"https://{provider_domain}/docs",
                f"https://{provider_domain}/developers",
            ]
            for url in candidates_urls:
                is_safe, _ = is_safe_url(url)
                if is_safe and url not in candidates:
                    ranked = rank_source(url, f"{app_name} Developer Documentation", provider_domain)
                    ranked["snippet"] = f"Official developer landing portal for {app_name}."
                    candidates[url] = ranked

        # Sort candidate URLs by priority (official docs highest)
        sorted_results = sorted(candidates.values(), key=lambda x: x["priority"], reverse=True)
        return sorted_results[:settings.MAX_RESEARCH_PAGES]

search_service = SearchService()

