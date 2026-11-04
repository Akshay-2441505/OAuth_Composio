import React, { useState, useEffect, useMemo } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  Search,
  Sparkles,
  ArrowRight,
  Filter,
  ExternalLink,
  X,
  CheckCircle2,
  AlertCircle,
} from 'lucide-react';
import { fetchApps } from '../api/client';
import { AppSummary } from '../api/types';
import { ComplexityBadge } from '../components/ComplexityBadge';

export const DirectoryPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialSearch = searchParams.get('q') || '';

  const [apps, setApps] = useState<AppSummary[]>([]);
  const [search, setSearch] = useState(initialSearch);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedManagedStatus, setSelectedManagedStatus] = useState<string>('All');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadApps = () => {
    setLoading(true);
    fetchApps()
      .then((data) => {
        setApps(data);
        setError(null);
      })
      .catch((err) => {
        setError(err.message || 'Failed to load application directory');
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadApps();
  }, []);

  // Synchronize URL ?q= if present
  useEffect(() => {
    if (initialSearch && initialSearch !== search) {
      setSearch(initialSearch);
    }
  }, [initialSearch]);

  const categories = useMemo(() => {
    const set = new Set<string>();
    apps.forEach((a) => {
      if (a.category) set.add(a.category);
    });
    return ['All', ...Array.from(set)];
  }, [apps]);

  const filteredApps = useMemo(() => {
    return apps.filter((app) => {
      const q = search.trim().toLowerCase();
      const matchesSearch =
        q === '' ||
        app.name.toLowerCase().includes(q) ||
        app.slug.toLowerCase().includes(q) ||
        app.provider_domain.toLowerCase().includes(q) ||
        (app.category && app.category.toLowerCase().includes(q));

      const matchesCat =
        selectedCategory === 'All' || app.category === selectedCategory;

      const matchesManaged =
        selectedManagedStatus === 'All' ||
        app.managed_oauth_status === selectedManagedStatus;

      return matchesSearch && matchesCat && matchesManaged;
    });
  }, [apps, search, selectedCategory, selectedManagedStatus]);

  // Statistics
  const managedCount = useMemo(
    () => apps.filter((a) => a.managed_oauth_status === 'available').length,
    [apps]
  );
  const guidesCount = useMemo(
    () => apps.filter((a) => a.guide_status === 'validated').length,
    [apps]
  );

  return (
    <div className="space-y-6">
      {/* Workspace Header & Metrics */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-3 border-b border-border-subtle">
        <div>
          <div className="flex items-center space-x-2.5">
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
              OAuth Provider Directory
            </h1>
            <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-accent-dim text-accent border border-accent-border font-bold">
              {apps.length} cataloged
            </span>
          </div>
          <p className="text-sm text-slate-300 mt-1 font-normal">
            Pre-integration intelligence, registration requirements, and managed auth availability for major developer platforms.
          </p>
        </div>

        {/* Compact stats pill cluster */}
        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="bg-dark-surface border border-border-subtle px-3 py-1.5 rounded-xl flex items-center space-x-2 shadow-xs">
            <span className="text-slate-400">Managed Auth:</span>
            <span className="text-accent font-bold">{managedCount}</span>
            <span className="text-slate-400">/ {apps.length}</span>
          </div>
          <div className="bg-dark-surface border border-border-subtle px-3 py-1.5 rounded-xl flex items-center space-x-2 shadow-xs">
            <span className="text-slate-400">Verified Guides:</span>
            <span className="text-white font-bold">{guidesCount}</span>
          </div>
        </div>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="space-y-3.5">
        <div className="flex flex-col sm:flex-row items-stretch gap-3">
          {/* Main search box */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter by app name, domain, or category (e.g. GitHub, Google, Slack, Notion)..."
              className="w-full pl-10 pr-10 py-2.5 text-sm rounded-xl bg-dark-surface border border-border-subtle text-white placeholder:text-slate-400 focus:outline-hidden focus:border-accent focus:ring-1 focus:ring-accent transition-all font-mono"
            />
            {search && (
              <button
                type="button"
                onClick={() => setSearch('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Managed Auth Filter */}
          <select
            value={selectedManagedStatus}
            onChange={(e) => setSelectedManagedStatus(e.target.value)}
            className="px-3.5 py-2.5 text-xs rounded-xl bg-dark-surface border border-border-subtle text-slate-200 focus:outline-hidden focus:border-accent font-medium"
          >
            <option value="All">All Auth Modes</option>
            <option value="available">Managed OAuth Available</option>
            <option value="not_available">Custom App Required</option>
            <option value="unknown">Unknown / Unchecked</option>
          </select>
        </div>

        {/* Category Filter Pills */}
        <div className="flex items-center space-x-2 overflow-x-auto pb-1 text-xs">
          <Filter className="w-3.5 h-3.5 text-slate-400 mr-1 shrink-0" />
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all shadow-xs cursor-pointer ${
                selectedCategory === cat
                  ? 'bg-[#A3E635] text-[#0A0E17] font-bold shadow-sm'
                  : 'bg-dark-surface hover:bg-dark-elevated text-slate-300 hover:text-white border border-border-subtle'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Directory Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div
              key={i}
              className="bg-dark-surface border border-border-subtle rounded-xl p-5 h-52 animate-pulse space-y-3"
            >
              <div className="w-1/3 h-5 bg-dark-elevated rounded" />
              <div className="w-2/3 h-4 bg-dark-elevated rounded" />
              <div className="w-1/2 h-4 bg-dark-elevated rounded" />
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="bg-dark-surface border border-rose-500/30 rounded-xl p-6 text-center max-w-md mx-auto space-y-3">
          <AlertCircle className="w-8 h-8 text-rose-400 mx-auto" />
          <p className="text-xs text-rose-300 font-medium">{error}</p>
          <button
            type="button"
            onClick={loadApps}
            className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-dark-elevated border border-border-subtle hover:border-accent text-white text-xs font-bold transition-all"
          >
            <span>Retry Connection</span>
          </button>
        </div>
      ) : filteredApps.length === 0 ? (
        /* Empty State with Autonomous Research Trigger */
        <div className="bg-dark-surface border border-border-subtle rounded-xl p-8 text-center space-y-4 max-w-xl mx-auto">
          <div className="w-12 h-12 rounded-xl bg-accent-dim border border-accent-border flex items-center justify-center text-accent mx-auto">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">
              No matching provider in seed catalog
            </h3>
            <p className="text-sm text-slate-300 mt-1 max-w-md mx-auto leading-relaxed">
              OAuth Compass hasn't indexed pre-verified docs for{' '}
              <strong className="text-white">"{search || 'this query'}"</strong> yet.
              You can trigger the AI research agent to discover its official documentation and synthesize an OAuth guide now.
            </p>
          </div>
          <Link
            to={`/generate?q=${encodeURIComponent(search)}`}
            className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-bold bg-accent text-dark-bg hover:bg-accent-hover transition-all shadow-xs"
          >
            <Sparkles className="w-4 h-4" />
            <span>Generate Guide for "{search || 'New App'}"</span>
          </Link>
        </div>
      ) : (
        /* Active Cards Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredApps.map((app) => {
            const isManaged = app.managed_oauth_status === 'available';

            return (
              <div
                key={app.id}
                className="bg-dark-surface border border-border-subtle hover:border-accent/60 rounded-xl p-5 flex flex-col justify-between transition-all group hover:bg-dark-elevated shadow-xs"
              >
                <div>
                  {/* Top Bar: Icon initial & Badges */}
                  <div className="flex items-start justify-between gap-3 mb-3.5">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-xl bg-dark-elevated border border-border-subtle flex items-center justify-center font-bold text-sm text-white group-hover:border-accent/60 transition-colors">
                        {app.name.slice(0, 2).toUpperCase()}
                      </div>
                      <div>
                        <h3 className="text-sm font-bold text-white group-hover:text-accent transition-colors">
                          {app.name}
                        </h3>
                        <a
                          href={app.website_url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-xs font-mono text-slate-400 hover:text-slate-200 flex items-center"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <span>{app.provider_domain}</span>
                          <ExternalLink className="w-3 h-3 ml-1" />
                        </a>
                      </div>
                    </div>

                    <ComplexityBadge level={app.complexity} />
                  </div>

                  {/* Badges / Meta row */}
                  <div className="space-y-2 text-xs pt-1">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 font-medium">Managed Auth</span>
                      <span
                        className={`inline-flex items-center space-x-1 font-bold ${
                          isManaged ? 'text-accent' : 'text-slate-300'
                        }`}
                      >
                        {isManaged && <CheckCircle2 className="w-3.5 h-3.5 text-accent" />}
                        <span className="capitalize">
                          {app.managed_oauth_status.replace('_', ' ')}
                        </span>
                      </span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 font-medium">Auth Standard</span>
                      <span className="font-mono text-slate-200 font-semibold">
                        {(app.auth_types || ['OAuth2']).join(', ')}
                      </span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 font-medium">Category</span>
                      <span className="px-2 py-0.5 rounded bg-dark-elevated border border-border-subtle text-xs text-slate-300 font-medium">
                        {app.category || 'Developer Tools'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Bottom CTA Button */}
                <div className="pt-4 mt-4 border-t border-border-subtle flex items-center justify-between">
                  <span className="text-xs font-mono text-slate-400 font-medium">
                    {app.last_researched_at
                      ? `Updated ${new Date(app.last_researched_at).toLocaleDateString()}`
                      : 'Seed guide'}
                  </span>

                  <Link
                    to={app.guide_id ? `/guides/${app.guide_id}` : `/apps/${app.slug}`}
                    className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-dark-elevated hover:bg-[#A3E635] hover:text-[#0A0E17] border border-border-subtle text-xs font-bold text-white transition-all shadow-xs group/btn cursor-pointer"
                  >
                    <span>View Guide</span>
                    <ArrowRight className="w-3.5 h-3.5 text-accent group-hover/btn:text-[#0A0E17] transition-colors" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
