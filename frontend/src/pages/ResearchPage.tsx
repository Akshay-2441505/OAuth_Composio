import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import {
  Sparkles,
  ArrowLeft,
  AlertCircle,
  RotateCcw,
  Clock,
  ArrowRight,
  CheckCircle2,
} from 'lucide-react';
import { startResearchRun, fetchResearchRun, retryResearchRun } from '../api/client';
import { ResearchRun } from '../api/types';
import { ResearchProgress } from '../components/ResearchProgress';
import { CopyShareButton } from '../components/CopyShareButton';

const QUICK_SUGGESTIONS = [
  { name: 'Linear', domain: 'linear.app' },
  { name: 'Stripe', domain: 'stripe.com' },
  { name: 'Airtable', domain: 'airtable.com' },
  { name: 'Figma', domain: 'figma.com' },
  { name: 'Zoom', domain: 'zoom.us' },
];

export const ResearchPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const runIdParam = searchParams.get('run_id');

  const [appName, setAppName] = useState('');
  const [websiteUrl, setWebsiteUrl] = useState('');
  const [intent, setIntent] = useState('');
  const [loading, setLoading] = useState(false);
  const [retrying, setRetrying] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pollTimeoutWarning, setPollTimeoutWarning] = useState(false);

  // Active run state
  const [currentRun, setCurrentRun] = useState<ResearchRun | null>(null);

  // Prefill from ?q= parameter if user arrived from empty search
  useEffect(() => {
    const q = searchParams.get('q');
    if (q && !runIdParam) {
      if (q.startsWith('http://') || q.startsWith('https://')) {
        setWebsiteUrl(q);
      } else {
        setAppName(q);
      }
    }
  }, [searchParams, runIdParam]);

  // Polling effect when run_id is active
  useEffect(() => {
    if (!runIdParam) {
      setCurrentRun(null);
      return;
    }

    let isMounted = true;
    let pollCount = 0;
    const MAX_POLLS = 60; // 60 * 1.5s = 90s timeout protection
    let pollInterval: ReturnType<typeof setInterval>;

    const poll = async () => {
      pollCount++;
      try {
        const runData = await fetchResearchRun(runIdParam);
        if (isMounted) {
          setCurrentRun(runData);

          // Stop polling if completed or failed
          if (runData.status === 'completed' || runData.status === 'failed') {
            clearInterval(pollInterval);
          } else if (pollCount >= MAX_POLLS) {
            setPollTimeoutWarning(true);
            clearInterval(pollInterval);
          }
        }
      } catch (err: unknown) {
        if (isMounted) {
          const msg = err instanceof Error ? err.message : 'Error checking run status';
          setError(msg);
          clearInterval(pollInterval);
        }
      }
    };

    poll();
    pollInterval = setInterval(poll, 1500);

    return () => {
      isMounted = false;
      clearInterval(pollInterval);
    };
  }, [runIdParam]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    let formattedUrl = websiteUrl.trim();
    if (formattedUrl && !formattedUrl.startsWith('http://') && !formattedUrl.startsWith('https://')) {
      formattedUrl = `https://${formattedUrl}`;
    }

    if (!appName.trim() && !formattedUrl) {
      setError('Please provide either an application name or a developer website URL.');
      return;
    }

    // Client-side guard against submitting secrets
    const combinedInput = `${appName} ${formattedUrl} ${intent}`.toLowerCase();
    for (const secretWord of ['client_secret', 'refresh_token', 'access_token', 'bearer ']) {
      if (combinedInput.includes(secretWord)) {
        setError(`Prohibited input: do not enter secrets or tokens (${secretWord}). OAuth Compass never requires or stores credentials.`);
        return;
      }
    }

    setLoading(true);
    setError(null);
    setPollTimeoutWarning(false);

    try {
      const res = await startResearchRun(appName.trim(), formattedUrl, intent.trim());
      setSearchParams({ run_id: res.run_id });
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : 'Research run could not be initiated.';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = async () => {
    const idToRetry = currentRun?.run_id || runIdParam;
    if (!idToRetry) return;
    setRetrying(true);
    setError(null);
    try {
      const res = await retryResearchRun(idToRetry);
      setCurrentRun(res);
      setPollTimeoutWarning(false);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to trigger research retry';
      setError(msg);
    } finally {
      setRetrying(false);
    }
  };

  const handleReset = () => {
    setSearchParams({});
    setCurrentRun(null);
    setError(null);
    setPollTimeoutWarning(false);
  };

  const applySuggestion = (s: { name: string; domain: string }) => {
    setAppName(s.name);
    setWebsiteUrl(`https://${s.domain}`);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Top Header & Breadcrumbs */}
      <div className="flex items-center justify-between">
        <Link
          to="/"
          className="inline-flex items-center text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5 mr-1 text-slate-400" />
          <span>Back to App Directory</span>
        </Link>
        {currentRun?.guide_id && <CopyShareButton guideId={currentRun.guide_id} />}
      </div>

      {/* If a run is in progress or completed, show live tracker */}
      {runIdParam && currentRun ? (
        <div className="space-y-6">
          <ResearchProgress
            stages={currentRun.stages}
            currentStatus={currentRun.status}
            providerUsed={currentRun.provider_used}
            modelUsed={currentRun.model_used}
          />

          {pollTimeoutWarning && currentRun.status !== 'completed' && (
            <div className="bg-dark-surface border border-amber-500/40 rounded-xl p-4 text-xs text-amber-200 flex items-start space-x-3">
              <Clock className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <strong className="text-white">Research is taking longer than usual.</strong>
                <p className="mt-0.5 text-slate-300">
                  The documentation server might be slow. The research continues in the background. You can check back later or retry.
                </p>
              </div>
            </div>
          )}

          {/* Completion Success Card */}
          {currentRun.status === 'completed' && currentRun.guide_id && (
            <div className="bg-dark-surface border border-accent rounded-xl p-6 sm:p-8 text-center space-y-4 shadow-xs">
              <div className="w-12 h-12 rounded-xl bg-accent-dim border border-accent-border text-accent flex items-center justify-center mx-auto shadow-xs">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base sm:text-lg font-bold text-white">
                  OAuth Setup Guide Published!
                </h3>
                <p className="text-sm text-slate-300 max-w-md mx-auto mt-1 leading-relaxed">
                  Documentation scraped, schemas verified, and setup instructions saved. Permanent URL generated at{' '}
                  <code className="text-accent font-mono text-xs font-bold">/guides/{currentRun.guide_id}</code>.
                </p>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => navigate(`/guides/${currentRun.guide_id}`)}
                  className="inline-flex items-center space-x-1.5 px-5 py-2.5 rounded-xl bg-accent hover:bg-accent-hover text-dark-bg text-xs font-bold shadow-xs transition-all"
                >
                  <span>Open Generated Guide</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  onClick={handleReset}
                  className="inline-flex items-center space-x-1.5 px-4 py-2.5 rounded-xl border border-border-subtle bg-dark-elevated text-slate-300 hover:text-white hover:border-border-DEFAULT text-xs font-semibold transition-all"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Research Another App</span>
                </button>
              </div>
            </div>
          )}

          {/* Failure Alert Card */}
          {currentRun.status === 'failed' && (
            <div className="bg-dark-surface border border-rose-500/40 rounded-xl p-6 sm:p-8 text-center space-y-4">
              <div className="w-12 h-12 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-300 flex items-center justify-center mx-auto">
                <AlertCircle className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base sm:text-lg font-bold text-white">
                  Research Pipeline Terminated
                </h3>
                <p className="text-xs text-rose-300 max-w-md mx-auto mt-1 leading-relaxed font-mono">
                  {currentRun.error || 'Documentation was inaccessible or safety validation blocked external resources.'}
                </p>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleRetry}
                  disabled={retrying}
                  className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-accent text-dark-bg hover:bg-accent-hover text-xs font-bold transition-all shadow-xs disabled:opacity-50"
                >
                  <RotateCcw className={`w-3.5 h-3.5 ${retrying ? 'animate-spin' : ''}`} />
                  <span>{retrying ? 'Restarting...' : 'Retry Research'}</span>
                </button>
                <button
                  type="button"
                  onClick={handleReset}
                  className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-dark-elevated border border-border-subtle hover:border-border-DEFAULT text-white text-xs font-semibold transition-all"
                >
                  <span>Research Another App</span>
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        /* Research Request Form */
        <div className="bg-dark-surface border border-border-subtle rounded-xl p-6 sm:p-8 space-y-6 shadow-xs">
          <div className="space-y-1.5">
            <div className="flex items-center space-x-2 text-accent">
              <Sparkles className="w-4 h-4" />
              <span className="text-xs font-mono uppercase tracking-wider font-bold">
                Autonomous Research Agent
              </span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
              Discover an Uncataloged OAuth Provider
            </h1>
            <p className="text-sm text-slate-300 leading-relaxed font-normal pt-1">
              Provide an application name or developer portal URL. The agent performs web discovery, fetches official docs with SSRF containment, synthesizes scopes and approval requirements, and constructs a schema-compliant setup guide.
            </p>
          </div>

          {error && (
            <div className="p-3.5 bg-rose-950/40 border border-rose-500/40 rounded-xl flex items-center text-xs text-rose-300 space-x-2 font-medium">
              <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Quick Suggestions Chips */}
          <div className="space-y-2">
            <span className="text-xs font-mono text-slate-400 font-semibold">Quick Presets:</span>
            <div className="flex flex-wrap gap-2">
              {QUICK_SUGGESTIONS.map((s) => (
                <button
                  key={s.name}
                  type="button"
                  onClick={() => applySuggestion(s)}
                  className="px-3 py-1.5 text-xs rounded-xl bg-dark-elevated hover:bg-dark-hover border border-border-subtle text-slate-200 hover:text-white hover:border-[#A3E635]/40 transition-all font-mono font-medium shadow-xs cursor-pointer"
                >
                  {s.name}
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5 pt-2">
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-bold text-white">
                  Application / Provider Name
                </label>
                <span className="text-xs font-mono text-slate-400">{appName.length}/100</span>
              </div>
              <input
                type="text"
                value={appName}
                onChange={(e) => setAppName(e.target.value)}
                maxLength={100}
                placeholder="e.g. Linear, Notion, Hubspot, Box, Asana"
                className="w-full px-4 py-3 text-sm rounded-xl bg-dark-elevated border border-border-subtle text-white placeholder:text-slate-500 focus:outline-hidden focus:border-accent focus:ring-1 focus:ring-accent transition-all font-mono shadow-inner"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-bold text-white">
                  Website or Documentation URL (Optional)
                </label>
                <span className="text-xs font-mono text-slate-400">{websiteUrl.length}/500</span>
              </div>
              <input
                type="text"
                value={websiteUrl}
                onChange={(e) => setWebsiteUrl(e.target.value)}
                maxLength={500}
                placeholder="https://linear.app or https://developers.notion.com"
                className="w-full px-4 py-3 text-sm rounded-xl bg-dark-elevated border border-border-subtle text-white placeholder:text-slate-500 focus:outline-hidden focus:border-accent focus:ring-1 focus:ring-accent transition-all font-mono shadow-inner"
              />
              <span className="text-xs text-slate-400 mt-2 block font-normal">
                Public HTTP/HTTPS URLs only. Loopback, private IP ranges, and cloud metadata addresses are blocked.
              </span>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-bold text-white">
                  Integration Intent / Use Case (Optional)
                </label>
                <span className="text-xs font-mono text-slate-400">{intent.length}/300</span>
              </div>
              <textarea
                value={intent}
                onChange={(e) => setIntent(e.target.value)}
                maxLength={300}
                rows={2}
                placeholder="e.g. Sync issues and comments, read user profile, trigger webhooks on new pull requests"
                className="w-full px-4 py-3 text-sm rounded-xl bg-dark-elevated border border-border-subtle text-white placeholder:text-slate-500 focus:outline-hidden focus:border-accent focus:ring-1 focus:ring-accent transition-all resize-none shadow-inner"
              />
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 px-5 rounded-xl text-xs sm:text-sm font-bold bg-[#A3E635] text-[#0A0E17] hover:bg-[#BEF264] transition-all shadow-md shadow-lime-500/10 flex items-center justify-center space-x-2 disabled:opacity-50 cursor-pointer active:scale-[0.99]"
              >
                {loading ? (
                  <>
                    <span className="w-4 h-4 border-2 border-[#0A0E17] border-t-transparent rounded-full animate-spin" />
                    <span className="font-bold">Initiating Pipeline...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-[#0A0E17]" />
                    <span className="font-bold">Start Autonomous Research</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
