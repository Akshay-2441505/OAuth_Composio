import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import {
  Search,
  Sparkles,
  Menu,
  X,
  ChevronRight,
} from 'lucide-react';

interface Props {
  onToggleMobile: () => void;
}

export const TopBar: React.FC<Props> = ({ onToggleMobile }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [quickSearch, setQuickSearch] = useState('');

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (quickSearch.trim()) {
      navigate(`/?q=${encodeURIComponent(quickSearch.trim())}`);
    }
  };

  const getBreadcrumbs = () => {
    const path = location.pathname;
    if (path === '/') return 'App Directory';
    if (path === '/overview') return 'Overview';
    if (path === '/generate') return 'Live Researcher';
    if (path === '/runs') return 'Research Runs';
    if (path === '/saved') return 'Saved Guides';
    if (path.startsWith('/apps/')) return 'Guide Details';
    if (path.startsWith('/guides/')) return 'Shareable Guide';
    return 'Workspace';
  };

  return (
    <header className="sticky top-0 z-30 h-16 bg-[#0E1321]/95 backdrop-blur-md border-b border-border-subtle flex items-center justify-between px-4 sm:px-6 shadow-sm">
      {/* Left: Mobile hamburger & breadcrumbs */}
      <div className="flex items-center space-x-3">
        <button
          onClick={onToggleMobile}
          className="lg:hidden p-2 rounded-xl text-slate-300 hover:text-white bg-dark-surface hover:bg-dark-elevated border border-border-subtle transition-colors"
          aria-label="Toggle navigation"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="hidden sm:flex items-center space-x-2 text-xs">
          <Link to="/" className="text-slate-400 hover:text-white transition-colors font-medium">
            OAuth Compass
          </Link>
          <ChevronRight className="w-3.5 h-3.5 text-slate-500" />
          <span className="font-semibold text-white px-2 py-0.5 rounded-md bg-dark-elevated border border-border-subtle/50">
            {getBreadcrumbs()}
          </span>
        </div>
      </div>

      {/* Center: Global Search Bar */}
      <form onSubmit={handleSearchSubmit} className="flex-1 max-w-md mx-4">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={quickSearch}
            onChange={(e) => setQuickSearch(e.target.value)}
            placeholder="Search provider (e.g. GitHub, Notion, Linear) or enter domain..."
            className="w-full pl-10 pr-12 py-2 text-xs rounded-xl bg-dark-surface border border-border-subtle text-white placeholder:text-slate-400 focus:outline-hidden focus:border-accent focus:ring-1 focus:ring-accent transition-all font-mono shadow-inner"
          />
          {quickSearch ? (
            <button
              type="button"
              onClick={() => setQuickSearch('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white p-1"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          ) : (
            <span className="hidden sm:inline-block absolute right-3 top-1/2 -translate-y-1/2 text-[10px] font-mono text-slate-400 border border-border-subtle px-1.5 py-0.5 rounded bg-dark-elevated">
              ↵
            </span>
          )}
        </div>
      </form>

      {/* Right: Quick actions */}
      <div className="flex items-center space-x-3">
        <Link
          to="/generate"
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold bg-[#A3E635] text-[#0A0E17] hover:bg-[#BEF264] shadow-md shadow-lime-500/10 transition-all font-sans cursor-pointer active:scale-95"
        >
          <Sparkles className="w-4 h-4 text-[#0A0E17]" />
          <span className="font-bold">New Research</span>
        </Link>
      </div>
    </header>
  );
};
