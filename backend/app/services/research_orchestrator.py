import uuid
import re
import logging
from datetime import datetime, timezone
from urllib.parse import urlparse
from typing import Optional, Dict, Any, List
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.app import App
from app.models.guide import Guide
from app.models.source import Source
from app.models.research_run import ResearchRun
from app.schemas.guide import GuideSchema
from app.services.search_service import search_service
from app.services.fetch_service import fetch_service
from app.services.llm.router import llm_router

logger = logging.getLogger("oauth_compass.orchestrator")

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def enforce_evidence_grounding(guide: GuideSchema, fetched_evidence: List[Dict[str, Any]]) -> GuideSchema:
    """
    Enforces strict claim-to-source grounding per Invariants 7, 9 & 10:
    - Never mark steps, claims, or SLAs 'verified' without valid, fetched documentation.
    - Downgrades unsupported claims to 'estimated' or 'unknown'.
    """
    valid_fetched_ids = {src["id"] for src in fetched_evidence if src.get("fetch_status") == "success" and src.get("http_status") == 200}
    official_fetched_ids = {src["id"] for src in fetched_evidence if src.get("is_official") and src["id"] in valid_fetched_ids}

    # Validate setup steps
    for step in guide.steps:
        valid_refs = [ref for ref in (step.evidence_refs or []) if ref in valid_fetched_ids]
        step.evidence_refs = valid_refs
        
        if step.evidence_status == "verified":
            has_official = any(ref in official_fetched_ids for ref in valid_refs)
            if not has_official:
                step.evidence_status = "estimated" if valid_refs else "unknown"

    # Validate atomic findings
    for finding in guide.findings:
        valid_refs = [ref for ref in (finding.source_ids or []) if ref in valid_fetched_ids]
        finding.source_ids = valid_refs
        if finding.status == "verified":
            has_official = any(ref in official_fetched_ids for ref in valid_refs)
            if not has_official:
                finding.status = "estimated" if valid_refs else "unknown"

    # Validate external wait SLA
    if guide.time_estimates.external_wait.status == "published_sla":
        valid_refs = [ref for ref in (guide.time_estimates.external_wait.evidence_refs or []) if ref in official_fetched_ids]
        if not valid_refs:
            guide.time_estimates.external_wait.status = "unknown"
            guide.time_estimates.external_wait.basis = f"Unverified wait SLA (no cited official documentation): {guide.time_estimates.external_wait.basis}"

    # Validate active setup confidence
    if guide.time_estimates.active_setup.confidence == "high":
        valid_refs = [ref for ref in (guide.time_estimates.active_setup.evidence_refs or []) if ref in valid_fetched_ids]
        if not valid_refs:
            guide.time_estimates.active_setup.confidence = "medium"

    # Invariant 5: Managed OAuth availability verification
    if guide.readiness.managed_oauth.status == "available" and not guide.readiness.managed_oauth.source_url:
        guide.readiness.managed_oauth.status = "unknown"

    return guide

class ResearchOrchestrator:
    def update_stage(self, db: Session, run: ResearchRun, stage_name: str, status: str, message: str):
        event = {
            "name": stage_name,
            "status": status,
            "message": message,
            "timestamp": now_iso(),
        }
        logs = list(run.stage_log_json or [])
        existing_idx = next((i for i, e in enumerate(logs) if e.get("name") == stage_name), None)
        if existing_idx is not None:
            logs[existing_idx] = event
        else:
            logs.append(event)
        
        run.stage_log_json = logs
        run.status = status if status in ("completed", "partial", "failed") else stage_name
        db.commit()
        db.refresh(run)

    async def execute_research(self, run_id: str, app_name: Optional[str], website_url: Optional[str], intent: Optional[str] = None):
        """
        Executes the full research pipeline:
        identify -> search -> fetch -> analyze -> validate -> persist
        """
        db = SessionLocal()
        try:
            run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
            if not run:
                logger.error(f"Research run '{run_id}' not found")
                return

            # Stage 1: Identify application & provider domain
            self.update_stage(db, run, "identify", "running", "Resolving provider identity and domain...")
            
            resolved_name = app_name or ""
            resolved_domain = ""

            if website_url:
                try:
                    parsed = urlparse(website_url.strip())
                    resolved_domain = parsed.hostname or ""
                    if not resolved_name and resolved_domain:
                        parts = resolved_domain.split(".")
                        resolved_name = parts[-2].capitalize() if len(parts) >= 2 else resolved_domain
                except Exception:
                    pass

            if not resolved_domain and resolved_name:
                resolved_domain = f"{resolved_name.lower().replace(' ', '')}.com"

            run.normalized_domain = resolved_domain
            run.input_name = resolved_name
            db.commit()

            self.update_stage(
                db, run, "identify", "completed",
                f"Resolved application '{resolved_name}' with domain '{resolved_domain}'."
            )

            # Stage 2: Search official documentation
            self.update_stage(db, run, "search", "running", "Searching for official OAuth developer documentation...")
            
            candidate_sources = await search_service.search_provider_docs(
                app_name=resolved_name,
                provider_domain=resolved_domain,
                intent=intent,
            )

            if not candidate_sources:
                self.update_stage(db, run, "search", "failed", "No documentation sources discovered.")
                run.status = "failed"
                run.error_message = f"Could not locate developer documentation for {resolved_name}."
                db.commit()
                return

            self.update_stage(
                db, run, "search", "completed",
                f"Discovered {len(candidate_sources)} candidate documentation pages."
            )

            # Stage 3: Fetch and extract readable documentation
            self.update_stage(db, run, "fetch", "running", "Fetching and extracting readable documentation text...")
            
            fetched_evidence: List[Dict[str, Any]] = []
            for src in candidate_sources:
                url = src["url"]
                res = await fetch_service.fetch_and_extract(url)
                if res["fetch_status"] == "success" and res["content"]:
                    fetched_evidence.append({
                        "id": f"src_{len(fetched_evidence)+1:02d}",
                        "title": src["title"],
                        "url": url,
                        "domain": src["domain"],
                        "source_type": src["source_type"],
                        "is_official": src["is_official"],
                        "http_status": res["http_status"],
                        "fetch_status": res["fetch_status"],
                        "content": res["content"],
                        "relevance_note": src.get("snippet", ""),
                    })

            if not fetched_evidence:
                self.update_stage(db, run, "fetch", "failed", "Documentation pages were unreachable or blocked.")
                run.status = "failed"
                run.error_message = "Failed to fetch readable documentation from discovered sources."
                db.commit()
                return

            self.update_stage(
                db, run, "fetch", "completed",
                f"Successfully extracted readable text from {len(fetched_evidence)} documentation sources."
            )

            # Stage 4: Analyze with LLM & Structured Fallback Router
            self.update_stage(db, run, "analyze", "running", "Synthesizing OAuth requirements, scopes, and setup steps...")

            evidence_package = {
                "app_name": resolved_name,
                "provider_domain": resolved_domain,
                "intent": intent,
                "sources": fetched_evidence,
            }

            guide_schema, provider_used, model_used, fallback_reason = await llm_router.generate_structured_guide(evidence_package)

            if not guide_schema:
                logger.warning(f"All LLM providers failed: {fallback_reason}. Not fabricating heuristic guide.")
                self.update_stage(
                    db, run, "analyze", "failed",
                    f"AI synthesis failed: Both primary and fallback LLM providers failed ({fallback_reason}). Incomplete research state."
                )
                run.status = "failed"
                run.error_message = f"AI synthesis incomplete: {fallback_reason}. Both OpenRouter and Groq adapters failed or were unconfigured."
                run.fallback_reason = fallback_reason
                db.commit()
                return

            run.provider_used = provider_used
            run.model_used = model_used
            run.fallback_reason = fallback_reason
            db.commit()

            self.update_stage(
                db, run, "analyze", "completed",
                f"Synthesized guide using provider '{provider_used}' ({model_used})."
            )

            # Stage 5: Validate & Persist to Database
            self.update_stage(db, run, "validate", "running", "Validating schema integrity, grounding evidence, and persisting guide...")

            # Validate against GuideSchema
            validated_guide = GuideSchema.model_validate(guide_schema.model_dump())

            # Enforce evidence grounding and downgrade unverified claims
            validated_guide = enforce_evidence_grounding(validated_guide, fetched_evidence)

            # 1. Ensure or update App record in SQLite with clean slug
            clean_name = re.sub(r'[^a-zA-Z0-9\s-]', '', resolved_name).strip()
            app_slug = re.sub(r'[-\s]+', '-', clean_name.lower()) or f"app-{uuid.uuid4().hex[:6]}"

            existing_app = db.query(App).filter(App.slug == app_slug).first()
            if not existing_app:
                new_app = App(
                    id=str(uuid.uuid4()),
                    slug=app_slug,
                    name=resolved_name,
                    website_url=f"https://{resolved_domain}",
                    provider_domain=resolved_domain,
                    category=validated_guide.app.category or "Developer tools",
                    auth_types=["OAuth2"],
                    managed_oauth_status=validated_guide.readiness.managed_oauth.status or "unknown",
                )
                db.add(new_app)
                db.flush()
                app_record = new_app
            else:
                app_record = existing_app

            # 2. Persist Guide record with versioning
            max_ver = db.query(func.max(Guide.version)).filter(Guide.app_id == app_record.id).scalar() or 0
            next_version = max_ver + 1
            guide_id = f"guide_{app_slug}_{uuid.uuid4().hex[:6]}"
            new_guide = Guide(
                id=guide_id,
                app_id=app_record.id,
                slug=app_slug,
                origin="generated",
                status="validated",
                content_json=validated_guide.model_dump(),
                version=next_version,
                last_researched_at=datetime.now(timezone.utc),
                is_public=True,
            )
            db.add(new_guide)
            db.flush()

            # 3. Persist Source records
            for s in validated_guide.sources:
                source_record = Source(
                    id=f"{guide_id}_{s.id}",
                    guide_id=new_guide.id,
                    title=s.title,
                    url=s.url,
                    domain=s.domain,
                    source_type=s.source_type,
                    is_official=s.is_official,
                    retrieved_at=datetime.now(timezone.utc),
                    http_status=s.http_status or 200,
                    fetch_status=s.fetch_status,
                    relevance_note=s.relevance_note,
                )
                db.add(source_record)

            # 4. Finalize ResearchRun
            run.guide_id = new_guide.id
            run.status = "completed"
            run.completed_at = datetime.now(timezone.utc)
            db.commit()

            self.update_stage(
                db, run, "validate", "completed",
                f"Guide validated and published at /guides/{new_guide.id}."
            )
            logger.info(f"Research run '{run_id}' successfully generated guide '{new_guide.id}'.")

        except Exception as e:
            logger.error(f"Unhandled exception in research run {run_id}: {e}", exc_info=True)
            try:
                db.rollback()
                run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
                if run:
                    run.status = "failed"
                    run.error_message = f"Internal error during research: {str(e)}"
                    self.update_stage(db, run, "error", "failed", f"Research failed: {str(e)}")
                    db.commit()
            except Exception as rollback_err:
                logger.error(f"Failed to record failure state for run {run_id}: {rollback_err}")
        finally:
            db.close()

orchestrator = ResearchOrchestrator()
