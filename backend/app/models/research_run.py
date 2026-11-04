import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ResearchRun(Base):
    __tablename__ = "research_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    input_name = Column(String, nullable=True)
    input_url = Column(String, nullable=True)
    normalized_domain = Column(String, nullable=True)
    status = Column(String, nullable=False, default="queued")
    stage_log_json = Column(JSON, nullable=False, default=list)
    provider_used = Column(String, nullable=True)
    model_used = Column(String, nullable=True)
    fallback_reason = Column(String, nullable=True)
    guide_id = Column(String, ForeignKey("guides.id"), nullable=True)
    error_message = Column(String, nullable=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    guide = relationship("Guide", back_populates="research_runs")

