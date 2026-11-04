from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.source import SourceSchema

class AppInfo(BaseModel):
    name: str
    website_url: str
    provider_domain: str
    category: str = "Developer tools"

class ManagedOAuthInfo(BaseModel):
    status: str = "unknown" # available / not_available / unknown / not_checked
    source_url: Optional[str] = None
    checked_at: Optional[str] = None

class ReadinessSchema(BaseModel):
    recommended_auth_product: str
    custom_oauth_app_required: str # yes / no / conditional / unknown
    managed_oauth: ManagedOAuthInfo = ManagedOAuthInfo()
    complexity: str # low / medium / high / unknown
    complexity_rationale: str

class ActiveSetupTime(BaseModel):
    minimum_minutes: Optional[int] = None
    maximum_minutes: Optional[int] = None
    confidence: str = "low" # low / medium / high
    basis: str
    evidence_refs: List[str] = []

class ExternalWaitTime(BaseModel):
    status: str = "unknown" # none / conditional / published_sla / unknown
    minimum_hours: Optional[int] = None
    maximum_hours: Optional[int] = None
    basis: str
    evidence_refs: List[str] = []

class TimeEstimatesSchema(BaseModel):
    active_setup: ActiveSetupTime
    external_wait: ExternalWaitTime

class ApprovalSchema(BaseModel):
    required: str = "unknown" # yes / no / conditional / unknown
    triggers: List[str] = []
    requirements: List[str] = []
    unknowns: List[str] = []

class StepSchema(BaseModel):
    id: str
    title: str
    description: str
    portal_url: Optional[str] = None
    owner: str = "developer" # developer / agent / shared
    requires_login: bool = False
    requires_secret: bool = False
    destructive_or_sensitive: bool = False
    verification: str
    evidence_status: str = "verified" # verified / attempted / estimated / unknown
    evidence_refs: List[str] = []
    handoff_reason: Optional[str] = None

class BlockerSchema(BaseModel):
    title: str
    cause: str
    resolution: str
    evidence_refs: List[str] = []

class FindingSchema(BaseModel):
    claim: str
    status: str = "verified" # verified / attempted / estimated / unknown
    source_ids: List[str] = []
    evidence_note: str = ""
    confidence: str = "high" # high / medium / low

class GuideSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    app: AppInfo
    readiness: ReadinessSchema
    time_estimates: TimeEstimatesSchema
    approval: ApprovalSchema
    prerequisites: List[str] = []
    steps: List[StepSchema] = []
    blockers: List[BlockerSchema] = []
    agent_capabilities: List[str] = []
    human_actions_required: List[str] = []
    findings: List[FindingSchema] = []
    sources: List[SourceSchema] = []
    assumptions: List[str] = []
    uncertainties: List[str] = []
    last_researched_at: str

class GuideResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    app_id: Optional[str] = None
    slug: Optional[str] = None
    origin: str
    status: str
    content: GuideSchema
    version: int
    is_public: bool
    last_researched_at: Optional[str] = None
    created_at: str
    updated_at: str

