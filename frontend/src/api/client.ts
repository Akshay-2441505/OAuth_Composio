import { AppSummary, GuideResponse, ResearchRun } from './types';

const API_BASE = '/api';

async function handleResponse<T>(res: Response, defaultMessage: string): Promise<T> {
  if (!res.ok) {
    let errorDetail = defaultMessage;
    try {
      const errorJson = await res.json();
      if (errorJson && errorJson.detail) {
        errorDetail = typeof errorJson.detail === 'string' ? errorJson.detail : JSON.stringify(errorJson.detail);
      }
    } catch {
      errorDetail = `${defaultMessage} (HTTP ${res.status}: ${res.statusText})`;
    }
    throw new Error(errorDetail);
  }
  return res.json();
}

export async function fetchApps(query?: string, category?: string, authType?: string): Promise<AppSummary[]> {
  const params = new URLSearchParams();
  if (query) params.append('q', query);
  if (category) params.append('category', category);
  if (authType) params.append('auth_type', authType);

  try {
    const res = await fetch(`${API_BASE}/apps?${params.toString()}`);
    return await handleResponse<AppSummary[]>(res, 'Failed to fetch application directory');
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Cannot connect to OAuth Compass API. Please ensure the backend server is running on port 8000.');
    }
    throw err;
  }
}

export async function fetchAppDetail(slug: string): Promise<AppSummary> {
  try {
    const res = await fetch(`${API_BASE}/apps/${encodeURIComponent(slug)}`);
    return await handleResponse<AppSummary>(res, `Failed to fetch app detail for '${slug}'`);
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Backend server unreachable. Please check connection.');
    }
    throw err;
  }
}

export async function fetchAppGuide(slug: string): Promise<GuideResponse> {
  try {
    const res = await fetch(`${API_BASE}/apps/${encodeURIComponent(slug)}/guide`);
    return await handleResponse<GuideResponse>(res, `Failed to fetch guide for '${slug}'`);
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Backend server unreachable. Please check connection.');
    }
    throw err;
  }
}

export async function fetchGuideById(guideId: string): Promise<GuideResponse> {
  try {
    const res = await fetch(`${API_BASE}/guides/${encodeURIComponent(guideId)}`);
    return await handleResponse<GuideResponse>(res, `Failed to fetch guide '${guideId}'`);
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Backend server unreachable. Please check connection.');
    }
    throw err;
  }
}

export async function startResearchRun(appName?: string, websiteUrl?: string, integrationIntent?: string): Promise<{ run_id: string; status: string }> {
  try {
    const res = await fetch(`${API_BASE}/research-runs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        app_name: appName || null,
        website_url: websiteUrl || null,
        integration_intent: integrationIntent || null,
      }),
    });
    return await handleResponse<{ run_id: string; status: string }>(res, 'Failed to start research run');
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Cannot reach OAuth Compass backend. Please ensure the server is running on port 8000.');
    }
    throw err;
  }
}

export async function fetchResearchRun(runId: string): Promise<ResearchRun> {
  try {
    const res = await fetch(`${API_BASE}/research-runs/${encodeURIComponent(runId)}`);
    return await handleResponse<ResearchRun>(res, `Failed to retrieve research run '${runId}'`);
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Backend server unreachable. Please check connection.');
    }
    throw err;
  }
}

export async function retryResearchRun(runId: string): Promise<ResearchRun> {
  try {
    const res = await fetch(`${API_BASE}/research-runs/${encodeURIComponent(runId)}/retry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    return await handleResponse<ResearchRun>(res, `Failed to retry research run '${runId}'`);
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Backend server unreachable. Please check connection.');
    }
    throw err;
  }
}

export async function fetchResearchRuns(): Promise<ResearchRun[]> {
  try {
    const res = await fetch(`${API_BASE}/research-runs`);
    return await handleResponse<ResearchRun[]>(res, 'Failed to fetch research runs history');
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Backend server unreachable. Please check connection.');
    }
    throw err;
  }
}

export async function fetchHealth(): Promise<{ status: string; providers_configured: Record<string, boolean> }> {
  const res = await fetch(`${API_BASE}/health`);
  return await handleResponse<{ status: string; providers_configured: Record<string, boolean> }>(res, 'Health check failed');
}

