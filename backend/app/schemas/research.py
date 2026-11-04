import re
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

def clean_input_string(v: Optional[str], max_len: int) -> Optional[str]:
    if v is None:
        return None
    # Strip leading/trailing whitespace
    s = str(v).strip()
    if not s:
        return None
    # Remove control characters and non-printable characters (except normal whitespace)
    s = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', s)
    # Reject attempts to pass credentials or secret tokens
    lower_s = s.lower()
    for secret_keyword in ("client_secret", "refresh_token", "access_token", "bearer ", "private_key"):
        if secret_keyword in lower_s:
            raise ValueError(f"Input contains prohibited credential pattern: '{secret_keyword}'. Secrets must never be submitted to OAuth Compass.")
    return s[:max_len]

class ResearchRunCreate(BaseModel):
    app_name: Optional[str] = Field(None, max_length=100, description="Application or OAuth provider name")
    website_url: Optional[str] = Field(None, max_length=500, description="Official website or developer portal URL")
    integration_intent: Optional[str] = Field(None, max_length=300, description="Intended integration scope or use case")

    @field_validator("app_name")
    @classmethod
    def sanitize_app_name(cls, v: Optional[str]) -> Optional[str]:
        cleaned = clean_input_string(v, 100)
        if cleaned is not None:
            if not re.search(r'[a-zA-Z0-9]', cleaned):
                raise ValueError("app_name must contain at least one alphanumeric character.")
        return cleaned

    @field_validator("website_url")
    @classmethod
    def sanitize_website_url(cls, v: Optional[str]) -> Optional[str]:
        cleaned = clean_input_string(v, 500)
        if cleaned is not None:
            if not (cleaned.startswith("http://") or cleaned.startswith("https://")):
                raise ValueError("website_url must start with http:// or https://")
        return cleaned

    @field_validator("integration_intent")
    @classmethod
    def sanitize_intent(cls, v: Optional[str]) -> Optional[str]:
        return clean_input_string(v, 300)

class StageEvent(BaseModel):
    name: str # identify, search, fetch, analyze, validate
    status: str # queued, running, completed, partial, failed
    message: str
    timestamp: Optional[str] = None

class ResearchRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    run_id: str
    status: str
    input_name: Optional[str] = None
    input_url: Optional[str] = None
    normalized_domain: Optional[str] = None
    stages: List[StageEvent] = []
    provider_used: Optional[str] = None
    model_used: Optional[str] = None
    fallback_reason: Optional[str] = None
    guide_id: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
