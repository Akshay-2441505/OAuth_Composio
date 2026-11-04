export type EvidenceStatus = 'verified' | 'attempted' | 'estimated' | 'unknown';
export type ComplexityLevel = 'low' | 'medium' | 'high' | 'unknown';
export type ManagedOAuthStatus = 'available' | 'not_available' | 'unknown' | 'not_checked';

export interface AppSummary {
  id: string;
  slug: string;
  name: string;
  website_url: string;
  provider_domain: string;
  category: string;
  auth_types: string[];
  managed_oauth_status: ManagedOAuthStatus;
  managed_oauth_source_url?: string | null;
  guide_status?: string | null;
  guide_id?: string | null;
  complexity?: ComplexityLevel | null;
  last_researched_at?: string | null;
}

export interface Source {
  id: string;
  title: string;
  url: string;
  domain: string;
  source_type: string;
  is_official: boolean;
  retrieved_at: string;
  http_status?: number | null;
  fetch_status: string;
  relevance_note: string;
}

export interface SetupStep {
  id: string;
  title: string;
  description: string;
  portal_url?: string | null;
  owner: 'developer' | 'agent' | 'shared';
  requires_login: boolean;
  requires_secret: boolean;
  destructive_or_sensitive: boolean;
  verification: string;
  evidence_status: EvidenceStatus;
  evidence_refs: string[];
  handoff_reason?: string | null;
}

export interface SetupBlocker {
  title: string;
  cause: string;
  resolution: string;
  evidence_refs: string[];
}

export interface Finding {
  claim: string;
  status: EvidenceStatus;
  source_ids: string[];
  evidence_note: string;
  confidence: 'high' | 'medium' | 'low';
}

export interface GuideContent {
  app: {
    name: string;
    website_url: string;
    provider_domain: string;
    category: string;
  };
  readiness: {
    recommended_auth_product: string;
    custom_oauth_app_required: 'yes' | 'no' | 'conditional' | 'unknown';
    managed_oauth: {
      status: ManagedOAuthStatus;
      source_url?: string | null;
      checked_at?: string | null;
    };
    complexity: ComplexityLevel;
    complexity_rationale: string;
  };
  time_estimates: {
    active_setup: {
      minimum_minutes?: number | null;
      maximum_minutes?: number | null;
      confidence: 'low' | 'medium' | 'high';
      basis: string;
      evidence_refs: string[];
    };
    external_wait: {
      status: 'none' | 'conditional' | 'published_sla' | 'unknown';
      minimum_hours?: number | null;
      maximum_hours?: number | null;
      basis: string;
      evidence_refs: string[];
    };
  };
  approval: {
    required: 'yes' | 'no' | 'conditional' | 'unknown';
    triggers: string[];
    requirements: string[];
    unknowns: string[];
  };
  prerequisites: string[];
  steps: SetupStep[];
  blockers: SetupBlocker[];
  agent_capabilities: string[];
  human_actions_required: string[];
  findings: Finding[];
  sources: Source[];
  assumptions: string[];
  uncertainties: string[];
  last_researched_at: string;
}

export interface GuideResponse {
  id: string;
  app_id?: string | null;
  slug?: string | null;
  origin: 'seeded' | 'generated';
  status: 'researched' | 'validated' | 'partial' | 'needs_review';
  content: GuideContent;
  version: number;
  is_public: boolean;
  last_researched_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface StageEvent {
  name: string;
  status: 'queued' | 'running' | 'completed' | 'partial' | 'failed';
  message: string;
  timestamp?: string | null;
}

export interface ResearchRun {
  run_id: string;
  status: string;
  input_name?: string | null;
  input_url?: string | null;
  normalized_domain?: string | null;
  stages: StageEvent[];
  provider_used?: string | null;
  model_used?: string | null;
  fallback_reason?: string | null;
  guide_id?: string | null;
  error?: string | null;
  started_at?: string | null;
  completed_at?: string | null;
}

