import logging
from typing import Dict, Any
from urllib.parse import urljoin
import httpx
import trafilatura
from bs4 import BeautifulSoup
from app.services.ssrf_validator import is_safe_url
from app.config import settings

logger = logging.getLogger("oauth_compass.fetch")

USER_AGENT = "OAuthCompass/1.0 (Developer Documentation Research Assistant; +https://github.com/composio)"
MAX_REDIRECTS = 5

class FetchService:
    async def fetch_and_extract(self, url: str) -> Dict[str, Any]:
        """
        Safely fetches a documentation page and extracts readable text.
        Guards against SSRF and validates each redirect hop manually before following.
        """
        current_url = url
        try:
            async with httpx.AsyncClient(
                timeout=settings.API_TIMEOUT_SECONDS,
                headers={"User-Agent": USER_AGENT},
                follow_redirects=False,
            ) as client:
                resp = None
                for redirect_idx in range(MAX_REDIRECTS + 1):
                    # Validate URL safety before initiating HTTP connection
                    is_safe, reason = is_safe_url(current_url)
                    if not is_safe:
                        logger.warning(f"SSRF safety check failed for {current_url}: {reason}")
                        return {
                            "url": current_url,
                            "http_status": None,
                            "fetch_status": "blocked",
                            "content": "",
                            "error": f"Security check blocked: {reason}",
                        }

                    resp = await client.get(current_url)

                    # Handle HTTP redirects explicitly to protect against SSRF bypass
                    if resp.is_redirect:
                        location = resp.headers.get("Location")
                        if not location:
                            break
                        next_url = urljoin(current_url, location)
                        logger.info(f"Safe redirect #{redirect_idx + 1} from {current_url} to {next_url}")
                        current_url = next_url
                        continue
                    else:
                        break

                if resp is None:
                    return {
                        "url": url,
                        "http_status": None,
                        "fetch_status": "failed",
                        "content": "",
                        "error": "No response received",
                    }

                if resp.status_code != 200:
                    return {
                        "url": current_url,
                        "http_status": resp.status_code,
                        "fetch_status": "failed",
                        "content": "",
                        "error": f"HTTP status {resp.status_code}",
                    }

                # Check Content-Length header early to prevent memory exhaustion
                content_len_hdr = resp.headers.get("content-length")
                if content_len_hdr:
                    try:
                        if int(content_len_hdr) > settings.MAX_PAGE_BYTES * 2:
                            return {
                                "url": current_url,
                                "http_status": resp.status_code,
                                "fetch_status": "failed",
                                "content": "",
                                "error": f"Payload size {content_len_hdr} bytes exceeds safety limit",
                            }
                    except ValueError:
                        pass

                # Check payload size
                content_bytes = resp.content
                if len(content_bytes) > settings.MAX_PAGE_BYTES:
                    content_bytes = content_bytes[:settings.MAX_PAGE_BYTES]

                html_text = resp.text

                # Trafilatura main content extraction
                extracted_text = trafilatura.extract(
                    html_text,
                    include_links=True,
                    include_tables=True,
                    output_format="txt",
                )

                # Fallback to BeautifulSoup if Trafilatura returned empty
                if not extracted_text or len(extracted_text.strip()) < 100:
                    soup = BeautifulSoup(html_text, "html.parser")
                    # Remove scripts and styling
                    for tag in soup(["script", "style", "nav", "footer", "aside"]):
                        tag.decompose()
                    extracted_text = soup.get_text(separator="\n", strip=True)

                # Bounded text truncation (max 30k chars per page)
                truncated_text = (extracted_text or "")[:30000]

                return {
                    "url": current_url,
                    "http_status": resp.status_code,
                    "fetch_status": "success",
                    "content": truncated_text,
                    "error": None,
                }
        except httpx.TimeoutException:
            logger.warning(f"Timeout fetching {current_url}")
            return {
                "url": current_url,
                "http_status": None,
                "fetch_status": "failed",
                "content": "",
                "error": "Request timed out",
            }
        except Exception as e:
            logger.error(f"Error fetching {current_url}: {e}")
            return {
                "url": current_url,
                "http_status": None,
                "fetch_status": "failed",
                "content": "",
                "error": str(e),
            }

fetch_service = FetchService()
