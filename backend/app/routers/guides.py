import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.guide import Guide
from app.models.source import Source
from app.schemas.guide import GuideResponse
from app.schemas.source import SourceSchema

router = APIRouter(prefix="/api/guides", tags=["guides"])

GUIDE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_\-]{3,80}$")

def validate_guide_id(guide_id: str) -> str:
    if not guide_id or not GUIDE_ID_PATTERN.match(guide_id):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid guide ID format: '{guide_id}'. Must be 3-80 alphanumeric, hyphen or underscore characters."
        )
    return guide_id

def guide_to_response(guide: Guide) -> GuideResponse:
    """Helper to convert a Guide ORM instance to a GuideResponse schema."""
    return GuideResponse(
        id=guide.id,
        app_id=guide.app_id,
        slug=guide.slug,
        origin=guide.origin,
        status=guide.status,
        content=guide.content_json,
        version=guide.version,
        is_public=guide.is_public,
        last_researched_at=guide.last_researched_at.isoformat() if guide.last_researched_at else None,
        created_at=guide.created_at.isoformat(),
        updated_at=guide.updated_at.isoformat(),
    )

@router.get("/{guide_id}", response_model=GuideResponse)
def get_guide(guide_id: str, db: Session = Depends(get_db)):
    valid_id = validate_guide_id(guide_id)
    guide = db.query(Guide).filter(Guide.id == valid_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail=f"Guide '{guide_id}' not found")
    return guide_to_response(guide)

@router.get("/{guide_id}/sources", response_model=List[SourceSchema])
def get_guide_sources(guide_id: str, db: Session = Depends(get_db)):
    valid_id = validate_guide_id(guide_id)
    guide = db.query(Guide).filter(Guide.id == valid_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail=f"Guide '{guide_id}' not found")
    
    sources = db.query(Source).filter(Source.guide_id == guide.id).all()
    return [
        SourceSchema(
            id=s.id,
            title=s.title,
            url=s.url,
            domain=s.domain,
            source_type=s.source_type,
            is_official=s.is_official,
            retrieved_at=s.retrieved_at.isoformat(),
            http_status=s.http_status,
            fetch_status=s.fetch_status,
            relevance_note=s.relevance_note,
        )
        for s in sources
    ]
