import re
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.app import App
from app.models.guide import Guide
from app.schemas.app import AppSummary, AppDetail
from app.schemas.guide import GuideResponse
from app.routers.guides import guide_to_response

router = APIRouter(prefix="/api/apps", tags=["apps"])

SLUG_PATTERN = re.compile(r"^[a-z0-9\-_]{1,80}$")

def validate_app_slug(slug: str) -> str:
    cleaned = (slug or "").strip().lower()
    if not cleaned or not SLUG_PATTERN.match(cleaned):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid app slug format: '{slug}'. Must be 1-80 lowercase alphanumeric characters, hyphens or underscores."
        )
    return cleaned

@router.get("", response_model=List[AppSummary])
def list_apps(
    q: Optional[str] = Query(None, max_length=100, description="Search query by name or domain"),
    category: Optional[str] = Query(None, max_length=50, description="Filter by category"),
    auth_type: Optional[str] = Query(None, max_length=50, description="Filter by auth type"),
    db: Session = Depends(get_db)
):
    query = db.query(App)
    if q:
        clean_q = re.sub(r'[\x00-\x1F\x7F]', '', q).strip().lower()[:100]
        if clean_q:
            search_filter = f"%{clean_q}%"
            query = query.filter(
                or_(
                    App.name.ilike(search_filter),
                    App.slug.ilike(search_filter),
                    App.provider_domain.ilike(search_filter),
                )
            )
    if category:
        query = query.filter(App.category == category)
    
    apps = query.all()
    if not apps:
        return []

    # Batch-load all guides for matching apps to prevent N+1 queries
    app_ids = [app.id for app in apps]
    all_guides = (
        db.query(Guide)
        .filter(Guide.app_id.in_(app_ids))
        .order_by(Guide.app_id, Guide.version.desc())
        .all()
    )
    latest_guides_by_app_id = {}
    for g in all_guides:
        if g.app_id not in latest_guides_by_app_id:
            latest_guides_by_app_id[g.app_id] = g

    results = []
    for app in apps:
        if auth_type and auth_type not in (app.auth_types or []):
            continue
        
        latest_guide = latest_guides_by_app_id.get(app.id)
        complexity = None
        if latest_guide and latest_guide.content_json:
            complexity = latest_guide.content_json.get("readiness", {}).get("complexity")

        results.append(
            AppSummary(
                id=app.id,
                slug=app.slug,
                name=app.name,
                website_url=app.website_url,
                provider_domain=app.provider_domain,
                category=app.category,
                auth_types=app.auth_types or [],
                managed_oauth_status=app.managed_oauth_status,
                managed_oauth_source_url=app.managed_oauth_source_url,
                guide_status=latest_guide.status if latest_guide else None,
                guide_id=latest_guide.id if latest_guide else None,
                complexity=complexity,
                last_researched_at=latest_guide.last_researched_at.isoformat() if latest_guide and latest_guide.last_researched_at else None,
            )
        )
    return results

@router.get("/{slug}", response_model=AppDetail)
def get_app(slug: str, db: Session = Depends(get_db)):
    valid_slug = validate_app_slug(slug)
    app = db.query(App).filter(App.slug == valid_slug).first()
    if not app:
        raise HTTPException(status_code=404, detail=f"App with slug '{slug}' not found")
    
    latest_guide = (
        db.query(Guide)
        .filter(Guide.app_id == app.id)
        .order_by(Guide.version.desc())
        .first()
    )
    complexity = None
    if latest_guide and latest_guide.content_json:
        complexity = latest_guide.content_json.get("readiness", {}).get("complexity")

    return AppDetail(
        id=app.id,
        slug=app.slug,
        name=app.name,
        website_url=app.website_url,
        provider_domain=app.provider_domain,
        category=app.category,
        auth_types=app.auth_types or [],
        managed_oauth_status=app.managed_oauth_status,
        managed_oauth_source_url=app.managed_oauth_source_url,
        guide_status=latest_guide.status if latest_guide else None,
        guide_id=latest_guide.id if latest_guide else None,
        complexity=complexity,
        last_researched_at=latest_guide.last_researched_at.isoformat() if latest_guide and latest_guide.last_researched_at else None,
        created_at=app.created_at.isoformat(),
        updated_at=app.updated_at.isoformat(),
    )

@router.get("/{slug}/guide", response_model=GuideResponse)
def get_app_guide(slug: str, db: Session = Depends(get_db)):
    valid_slug = validate_app_slug(slug)
    app = db.query(App).filter(App.slug == valid_slug).first()
    if not app:
        raise HTTPException(status_code=404, detail=f"App with slug '{slug}' not found")
    
    guide = (
        db.query(Guide)
        .filter(Guide.app_id == app.id)
        .order_by(Guide.version.desc())
        .first()
    )
    if not guide:
        raise HTTPException(status_code=404, detail=f"No guide found for app '{slug}'")
    
    return guide_to_response(guide)
