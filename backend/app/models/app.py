import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class App(Base):
    __tablename__ = "apps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    website_url = Column(String, nullable=False)
    provider_domain = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, default="Developer tools")
    auth_types = Column(JSON, nullable=False, default=list)
    managed_oauth_status = Column(String, nullable=False, default="unknown")
    managed_oauth_source_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    guides = relationship("Guide", back_populates="app", cascade="all, delete-orphan")

