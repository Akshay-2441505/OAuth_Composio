from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True) # e.g. "src_github_01" or generated ID
    guide_id = Column(String, ForeignKey("guides.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    source_type = Column(String, nullable=False, default="official_documentation")
    is_official = Column(Boolean, nullable=False, default=True)
    retrieved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    http_status = Column(Integer, nullable=True)
    fetch_status = Column(String, nullable=False, default="success")
    relevance_note = Column(String, nullable=False, default="")

    guide = relationship("Guide", back_populates="sources")

