import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ArrowRight,
  ShieldCheck,
  KeyRound,
  Layers,
  Cpu,
  Database,
  Search,
} from 'lucide-react';
import { fetchApps } from '../api/client';
import { AppSummary } from '../api/types';
import { ComplexityBadge } from '../components/ComplexityBadge';

export const OverviewPage: React.FC = () => {
  const navigate = useNavigate();
  const [apps, setApps] = useState<AppSummary[]>([]);
  const [, setLoading] = useState(true);
  const [quickInput, setQuickInput] = useState('');

  useEffect(() => {
    fetchApps()
      .then((data) => setApps(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleQuickSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (quickInput.trim()) {
      navigate(`/generate?q=${encodeURIComponent(quickInput.trim())}`);
    }
  };

  const managedCount = apps.filter((a) => a.managed_oauth_status === 'available').length;
  const guidesCount = apps.filter((a) => a.guide_status === 'validated').length;

  return (
    <div className="space-y-6">
      {/* Hero Developer Console Card */}
      <div className="bg-dark-surface border border-border-subtle rounded-2xl p-6 sm:p-8 relative overflow-hidden shadow-xs">
        <div className="max-w-2xl relative z-10 space-y-3.5">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-accent-dim text-accent text-xs font-bold border border-accent-border">
            <ShieldCheck className="w-4 h-4" />
            <span>Developer Pre-Integration Intelligence</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Know before you build your OAuth connection.
          </h1>

          <p className="text-sm text-slate-300 leading-relaxed font-normal">
            Verify whether an integration requires custom developer console setup or supports Composio managed OAuth. Obtain evidence-backed setup checklists, approval waiting SLAs, and sensitive permission scopes.
          </p>

          {/* Inline Research Box */}
          <form onSubmit={handleQuickSubmit} className="pt-3 max-w-xl">
            <div className="relative flex items-center">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5" />
              <input
                type="text"
                value={quickInput}
                onChange={(e) => setQuickInput(e.target.value)}
                placeholder="Enter any provider (e.g. Asana, Linear, Box, Salesforce)..."
                className="w-full pl-10 pr-28 py-3 text-xs sm:text-sm rounded-xl bg-dark-bg border border-border-subtle text-white placeholder:text-slate-400 focus:outline-hidden focus:border-accent focus:ring-1 focus:ring-accent font-mono transition-all shadow-inner"
              />
              <button
                type="submit"
                className="absolute right-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-[#A3E635] text-[#0A0E17] hover:bg-[#BEF264] transition-all shadow-sm cursor-pointer"
              >
                Inspect
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* KPI Metrics Cluster */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-dark-surface border border-border-subtle rounded-xl p-4 sm:p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-1">
            <span>Seeded Providers</span>
            <Database className="w-4 h-4 text-accent" />
          </div>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-white">3 / 3</div>
          <p className="text-xs text-slate-400 mt-1 font-medium">GitHub, Google Workspace, Slack</p>
        </div>

        <div className="bg-dark-surface border border-border-subtle rounded-xl p-4 sm:p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-1">
            <span>Total Cataloged</span>
            <Layers className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-white">{apps.length}</div>
          <p className="text-xs text-slate-400 mt-1 font-medium">{guidesCount} validated guides</p>
        </div>

        <div className="bg-dark-surface border border-border-subtle rounded-xl p-4 sm:p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-1">
            <span>Managed OAuth</span>
            <KeyRound className="w-4 h-4 text-accent" />
          </div>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-accent">
            {apps.length ? Math.round((managedCount / apps.length) * 100) : 0}%
          </div>
          <p className="text-xs text-slate-400 mt-1 font-medium">{managedCount} providers ready</p>
        </div>

        <div className="bg-dark-surface border border-border-subtle rounded-xl p-4 sm:p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-1">
            <span>Synthesis Engine</span>
            <Cpu className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-base font-bold font-mono text-white">Dual-Router LLM</div>
          <p className="text-xs text-slate-400 mt-1 font-medium">OpenRouter + Groq fallback</p>
        </div>
      </div>

      {/* Featured Seed Integrations */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold tracking-tight text-white uppercase font-mono">
            Featured Seeded Integrations
          </h2>
          <Link
            to="/"
            className="text-xs text-accent hover:underline flex items-center font-bold"
          >
            <span>View All Providers</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {apps.slice(0, 3).map((app) => (
            <Link
              key={app.id}
              to={app.guide_id ? `/guides/${app.guide_id}` : `/apps/${app.slug}`}
              className="bg-dark-surface border border-border-subtle hover:border-accent/60 rounded-xl p-5 block transition-all group hover:bg-dark-elevated"
            >
              <div className="flex items-start justify-between mb-3.5">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-dark-elevated border border-border-subtle flex items-center justify-center font-bold text-sm text-white group-hover:border-accent/60 transition-colors">
                    {app.name.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white group-hover:text-accent transition-colors">
                      {app.name}
                    </h3>
                    <span className="text-xs font-mono text-slate-400">{app.provider_domain}</span>
                  </div>
                </div>
                <ComplexityBadge level={app.complexity} />
              </div>

              <div className="text-xs text-slate-300 space-y-1.5 pt-1">
                <div className="flex justify-between">
                  <span className="text-slate-400">Managed Flow:</span>
                  <span className="capitalize font-bold text-accent">
                    {app.managed_oauth_status.replace('_', ' ')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Category:</span>
                  <span className="font-medium text-slate-200">{app.category}</span>
                </div>
              </div>

              <div className="mt-4 pt-3.5 border-t border-border-subtle flex items-center justify-between text-xs text-white group-hover:text-accent font-bold">
                <span>Open Readiness Guide</span>
                <ArrowRight className="w-3.5 h-3.5 text-accent" />
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};
