from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class AppSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    name: str
    website_url: str
    provider_domain: str
    category: str
    auth_types: List[str]
    managed_oauth_status: str
    managed_oauth_source_url: Optional[str] = None
    guide_status: Optional[str] = None
    guide_id: Optional[str] = None
    complexity: Optional[str] = None
    last_researched_at: Optional[str] = None

class AppDetail(AppSummary):
    created_at: str
    updated_at: str

