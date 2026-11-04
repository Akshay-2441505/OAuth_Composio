import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Guide(Base):
    __tablename__ = "guides"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    app_id = Column(String, ForeignKey("apps.id"), nullable=True, index=True)
    slug = Column(String, index=True, nullable=True)
    origin = Column(String, nullable=False, default="generated") # seeded / generated
    status = Column(String, nullable=False, default="researched") # researched / validated / partial / needs_review
    content_json = Column(JSON, nullable=False, default=dict)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_researched_at = Column(DateTime, nullable=True)
    is_public = Column(Boolean, nullable=False, default=True)

    app = relationship("App", back_populates="guides")
    sources = relationship("Source", back_populates="guide", cascade="all, delete-orphan")
    research_runs = relationship("ResearchRun", back_populates="guide")

