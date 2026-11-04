from typing import Optional
from pydantic import BaseModel, ConfigDict

class SourceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    url: str
    domain: str
    source_type: str = "official_documentation" # official_documentation / official_portal / support / secondary
    is_official: bool = True
    retrieved_at: str
    http_status: Optional[int] = 200
    fetch_status: str = "success" # success / blocked / failed / partial
    relevance_note: str = ""

