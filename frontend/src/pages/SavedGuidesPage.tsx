import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  BookmarkCheck,
  Search,
  ArrowRight,
  Sparkles,
} from 'lucide-react';
import { fetchApps } from '../api/client';
import { AppSummary } from '../api/types';
import { ComplexityBadge } from '../components/ComplexityBadge';

export const SavedGuidesPage: React.FC = () => {
  const [apps, setApps] = useState<AppSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetchApps()
      .then((data) => setApps(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const guides = apps.filter((a) => a.guide_id);
  const filtered = guides.filter(
    (g) =>
      g.name.toLowerCase().includes(filter.toLowerCase()) ||
      g.provider_domain.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3.5 border-b border-border-subtle gap-3">
        <div>
          <div className="flex items-center space-x-2.5">
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
              Saved OAuth Guides
            </h1>
            <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-accent-dim text-accent border border-accent-border font-bold">
              {guides.length} available
            </span>
          </div>
          <p className="text-sm text-slate-300 mt-1 font-normal">
            Persisted guides with stable, shareable URLs, setup steps, and source verification.
          </p>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Search saved guides..."
            className="w-full pl-9 pr-3 py-2 text-xs rounded-xl bg-dark-surface border border-border-subtle text-white placeholder:text-slate-400 focus:outline-hidden focus:border-accent font-mono transition-all"
          />
        </div>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-dark-surface border border-border-subtle rounded-xl animate-pulse" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="bg-dark-surface border border-border-subtle rounded-xl p-10 text-center max-w-md mx-auto space-y-3 shadow-xs">
          <BookmarkCheck className="w-10 h-10 text-slate-400 mx-auto" />
          <h3 className="text-base font-bold text-white">No Saved Guides Found</h3>
          <p className="text-sm text-slate-300 font-normal">
            Use the Live Researcher to generate a new integration guide.
          </p>
          <Link
            to="/generate"
            className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-accent text-dark-bg hover:bg-accent-hover transition-colors shadow-xs"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Generate New Guide</span>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((g) => (
            <Link
              key={g.id}
              to={`/guides/${g.guide_id}`}
              className="bg-dark-surface border border-border-subtle hover:border-accent/60 rounded-xl p-5 block transition-all group hover:bg-dark-elevated shadow-xs"
            >
              <div className="flex items-start justify-between mb-3.5">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-dark-elevated border border-border-subtle flex items-center justify-center font-bold text-sm text-white group-hover:border-accent/60 transition-colors">
                    {g.name.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <h3 className="text-sm sm:text-base font-bold text-white group-hover:text-accent transition-colors">
                      {g.name}
                    </h3>
                    <span className="text-xs font-mono text-slate-400">{g.provider_domain}</span>
                  </div>
                </div>
                <ComplexityBadge level={g.complexity} />
              </div>

              <div className="text-xs text-slate-300 space-y-1.5 pt-1 font-mono">
                <div className="flex justify-between">
                  <span className="text-slate-400">Guide ID:</span>
                  <span className="text-slate-200 font-bold">{g.guide_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Managed Flow:</span>
                  <span className="text-accent font-bold capitalize">
                    {g.managed_oauth_status.replace('_', ' ')}
                  </span>
                </div>
              </div>

              <div className="mt-4 pt-3.5 border-t border-border-subtle flex items-center justify-between text-xs text-white group-hover:text-accent font-bold">
                <span>Open Full Guide</span>
                <ArrowRight className="w-3.5 h-3.5 text-accent" />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};
