import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  History,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  Loader2,
} from 'lucide-react';
import { fetchResearchRuns } from '../api/client';
import { ResearchRun } from '../api/types';

export const ResearchRunsPage: React.FC = () => {
  const navigate = useNavigate();
  const [runs, setRuns] = useState<ResearchRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchResearchRuns()
      .then((data) => {
        setRuns(data);
        setError(null);
      })
      .catch((err) => {
        setError(err.message || 'Failed to retrieve research run history');
      })
      .finally(() => setLoading(false));
  }, []);

  const renderStatusBadge = (status: string) => {
    if (status === 'completed') {
      return (
        <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-accent-dim text-accent border border-accent-border">
          <CheckCircle2 className="w-3.5 h-3.5 text-accent" />
          <span>Completed</span>
        </span>
      );
    }
    if (status === 'failed') {
      return (
        <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-rose-500/15 text-rose-300 border border-rose-500/40">
          <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
          <span>Failed</span>
        </span>
      );
    }
    return (
      <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-dark-elevated text-slate-300 border border-border-subtle animate-pulse">
        <Loader2 className="w-3.5 h-3.5 animate-spin text-accent" />
        <span className="capitalize">{status}</span>
      </span>
    );
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3.5 border-b border-border-subtle gap-3">
        <div>
          <div className="flex items-center space-x-2.5">
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
              Research Runs & Synthesis Traces
            </h1>
            <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-accent-dim text-accent border border-accent-border font-bold">
              {runs.length} runs recorded
            </span>
          </div>
          <p className="text-sm text-slate-300 mt-1 font-normal">
            Historical trace logs of autonomous documentation discovery, extraction, and Pydantic validation.
          </p>
        </div>

        <Link
          to="/generate"
          className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-bold bg-accent text-dark-bg hover:bg-accent-hover transition-all shadow-xs"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Launch New Run</span>
        </Link>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-dark-surface border border-border-subtle rounded-xl animate-pulse" />
          ))}
        </div>
      ) : error ? (
        <div className="bg-dark-surface border border-rose-500/40 rounded-xl p-6 text-center text-xs text-rose-300">
          <AlertCircle className="w-6 h-6 text-rose-400 mx-auto mb-2" />
          <p>{error}</p>
        </div>
      ) : runs.length === 0 ? (
        <div className="bg-dark-surface border border-border-subtle rounded-xl p-10 text-center max-w-md mx-auto space-y-3 shadow-xs">
          <History className="w-10 h-10 text-slate-400 mx-auto" />
          <h3 className="text-base font-bold text-white">No Research Runs Yet</h3>
          <p className="text-sm text-slate-300 leading-relaxed font-normal">
            Use the Live Researcher to generate a new integration guide.
          </p>
          <Link
            to="/generate"
            className="inline-flex items-center space-x-1 px-4 py-2 rounded-xl text-xs font-bold bg-accent text-dark-bg hover:bg-accent-hover transition-colors shadow-xs"
          >
            <span>Start First Run</span>
          </Link>
        </div>
      ) : (
        <div className="bg-dark-surface border border-border-subtle rounded-xl overflow-hidden divide-y divide-border-subtle shadow-xs">
          {runs.map((r) => (
            <div
              key={r.run_id}
              onClick={() => {
                if (r.guide_id) {
                  navigate(`/guides/${r.guide_id}`);
                } else {
                  navigate(`/generate?run_id=${r.run_id}`);
                }
              }}
              className="p-4 sm:p-5 hover:bg-dark-elevated transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer group"
            >
              <div className="space-y-1.5">
                <div className="flex items-center space-x-3">
                  <span className="text-sm sm:text-base font-bold text-white group-hover:text-accent transition-colors">
                    {r.input_name || r.normalized_domain || 'Unknown Provider'}
                  </span>
                  {renderStatusBadge(r.status)}
                </div>

                <div className="flex flex-wrap items-center gap-3.5 text-xs text-slate-400 font-mono font-medium">
                  <span>ID: <code className="text-slate-200 font-bold">{r.run_id}</code></span>
                  {r.normalized_domain && (
                    <span>Domain: <code className="text-accent font-semibold">{r.normalized_domain}</code></span>
                  )}
                  {r.started_at && (
                    <span>Started: {new Date(r.started_at).toLocaleTimeString()}</span>
                  )}
                  {r.provider_used && (
                    <span className="text-slate-300">Model: {r.provider_used}</span>
                  )}
                </div>

                {r.error && (
                  <p className="text-xs text-rose-300 font-mono pt-1">
                    Error: {r.error}
                  </p>
                )}
              </div>

              <div className="flex items-center space-x-3 shrink-0">
                {r.guide_id ? (
                  <span className="inline-flex items-center space-x-1 text-xs font-bold text-accent group-hover:translate-x-0.5 transition-all">
                    <span>View Guide</span>
                    <ArrowRight className="w-3.5 h-3.5 text-accent" />
                  </span>
                ) : (
                  <span className="inline-flex items-center space-x-1 text-xs font-medium text-slate-300 group-hover:text-white group-hover:translate-x-0.5 transition-all">
                    <span>Inspect Pipeline</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
