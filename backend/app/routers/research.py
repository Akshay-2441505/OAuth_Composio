import uuid
import re
import time
from typing import List, Dict
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.research_run import ResearchRun
from app.schemas.research import ResearchRunCreate, ResearchRunResponse, StageEvent
from app.services.ssrf_validator import is_safe_url
from app.services.research_orchestrator import orchestrator

router = APIRouter(prefix="/api/research-runs", tags=["research"])

RUN_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_\-]{3,64}$")

# In-memory sliding window rate limiter: client_ip -> list of epoch timestamps
RATE_LIMIT_BUCKET: Dict[str, List[float]] = {}
MAX_REQUESTS_PER_MINUTE = 20

def check_rate_limit(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()
    cutoff = now - 60.0
    timestamps = [ts for ts in RATE_LIMIT_BUCKET.get(client_ip, []) if ts > cutoff]
    if len(timestamps) >= MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail="Too many research requests. Please wait a minute before starting another research run."
        )
    timestamps.append(now)
    RATE_LIMIT_BUCKET[client_ip] = timestamps

def validate_run_id(run_id: str) -> str:
    if not run_id or not RUN_ID_PATTERN.match(run_id):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid research run ID format: '{run_id}'."
        )
    return run_id

@router.get("", response_model=List[ResearchRunResponse])
def list_research_runs(db: Session = Depends(get_db)):
    runs = db.query(ResearchRun).order_by(ResearchRun.started_at.desc()).limit(50).all()
    return [
        ResearchRunResponse(
            run_id=r.id,
            status=r.status,
            input_name=r.input_name,
            input_url=r.input_url,
            normalized_domain=r.normalized_domain,
            stages=[StageEvent(**s) for s in (r.stage_log_json or [])],
            provider_used=r.provider_used,
            model_used=r.model_used,
            fallback_reason=r.fallback_reason,
            guide_id=r.guide_id,
            error=r.error_message,
            started_at=r.started_at.isoformat() if r.started_at else None,
            completed_at=r.completed_at.isoformat() if r.completed_at else None,
        )
        for r in runs
    ]

@router.post("", response_model=ResearchRunResponse, status_code=201)
def create_research_run(
    payload: ResearchRunCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    check_rate_limit(request)
    app_name = (payload.app_name or "").strip()
    website_url = (payload.website_url or "").strip()
    intent = (payload.integration_intent or "").strip()

    if not app_name and not website_url:
        raise HTTPException(
            status_code=400,
            detail="Either 'app_name' or 'website_url' must be provided."
        )

    if website_url:
        is_safe, reason = is_safe_url(website_url)
        if not is_safe:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid or restricted URL: {reason}"
            )

    # Duplicate in-flight run detection (within last 3 minutes)
    recent_cutoff = datetime.now(timezone.utc) - timedelta(minutes=3)
    in_flight_statuses = ["queued", "identify", "search", "fetch", "analyze", "validate"]
    
    dup_query = db.query(ResearchRun).filter(
        ResearchRun.status.in_(in_flight_statuses),
        ResearchRun.started_at >= recent_cutoff,
    )
    if app_name and website_url:
        existing_run = dup_query.filter(
            (ResearchRun.input_name.ilike(app_name)) | (ResearchRun.input_url == website_url)
        ).first()
    elif app_name:
        existing_run = dup_query.filter(ResearchRun.input_name.ilike(app_name)).first()
    else:
        existing_run = dup_query.filter(ResearchRun.input_url == website_url).first()

    if existing_run:
        return ResearchRunResponse(
            run_id=existing_run.id,
            status=existing_run.status,
            input_name=existing_run.input_name,
            input_url=existing_run.input_url,
            normalized_domain=existing_run.normalized_domain,
            stages=[StageEvent(**s) for s in (existing_run.stage_log_json or [])],
            provider_used=existing_run.provider_used,
            model_used=existing_run.model_used,
            fallback_reason=existing_run.fallback_reason,
            guide_id=existing_run.guide_id,
            error=existing_run.error_message,
            started_at=existing_run.started_at.isoformat() if existing_run.started_at else None,
            completed_at=existing_run.completed_at.isoformat() if existing_run.completed_at else None,
        )

    run_id = f"run_{uuid.uuid4().hex[:12]}"
    initial_stage = StageEvent(
        name="identify",
        status="queued",
        message="Queued research run.",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    new_run = ResearchRun(
        id=run_id,
        input_name=app_name or None,
        input_url=website_url or None,
        status="queued",
        stage_log_json=[initial_stage.model_dump()],
        started_at=datetime.now(timezone.utc),
    )
    db.add(new_run)
    db.commit()
    db.refresh(new_run)

    # Launch background asynchronous research workflow
    background_tasks.add_task(
        orchestrator.execute_research,
        run_id=run_id,
        app_name=app_name,
        website_url=website_url,
        intent=intent,
    )

    return ResearchRunResponse(
        run_id=new_run.id,
        status=new_run.status,
        input_name=new_run.input_name,
        input_url=new_run.input_url,
        normalized_domain=new_run.normalized_domain,
        stages=[StageEvent(**s) for s in (new_run.stage_log_json or [])],
        guide_id=new_run.guide_id,
        error=new_run.error_message,
        started_at=new_run.started_at.isoformat() if new_run.started_at else None,
        completed_at=new_run.completed_at.isoformat() if new_run.completed_at else None,
    )

@router.get("/{run_id}", response_model=ResearchRunResponse)
def get_research_run(run_id: str, db: Session = Depends(get_db)):
    valid_id = validate_run_id(run_id)
    run = db.query(ResearchRun).filter(ResearchRun.id == valid_id).first()
    if not run:
        raise HTTPException(status_code=404, detail=f"Research run '{run_id}' not found")

    return ResearchRunResponse(
        run_id=run.id,
        status=run.status,
        input_name=run.input_name,
        input_url=run.input_url,
        normalized_domain=run.normalized_domain,
        stages=[StageEvent(**s) for s in (run.stage_log_json or [])],
        provider_used=run.provider_used,
        model_used=run.model_used,
        fallback_reason=run.fallback_reason,
        guide_id=run.guide_id,
        error=run.error_message,
        started_at=run.started_at.isoformat() if run.started_at else None,
        completed_at=run.completed_at.isoformat() if run.completed_at else None,
    )

@router.post("/{run_id}/retry", response_model=ResearchRunResponse)
def retry_research_run(
    run_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    check_rate_limit(request)
    valid_id = validate_run_id(run_id)
    run = db.query(ResearchRun).filter(ResearchRun.id == valid_id).first()
    if not run:
        raise HTTPException(status_code=404, detail=f"Research run '{run_id}' not found")

    initial_stage = StageEvent(
        name="identify",
        status="queued",
        message="Queued research run retry.",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    run.status = "queued"
    run.error_message = None
    run.stage_log_json = [initial_stage.model_dump()]
    run.started_at = datetime.now(timezone.utc)
    run.completed_at = None
    db.commit()
    db.refresh(run)

    background_tasks.add_task(
        orchestrator.execute_research,
        run_id=run.id,
        app_name=run.input_name,
        website_url=run.input_url,
        intent=None,
    )

    return ResearchRunResponse(
        run_id=run.id,
        status=run.status,
        input_name=run.input_name,
        input_url=run.input_url,
        normalized_domain=run.normalized_domain,
        stages=[StageEvent(**s) for s in (run.stage_log_json or [])],
        guide_id=run.guide_id,
        error=run.error_message,
        started_at=run.started_at.isoformat() if run.started_at else None,
        completed_at=run.completed_at.isoformat() if run.completed_at else None,
    )

