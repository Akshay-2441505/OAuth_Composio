import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Compass,
  LayoutGrid,
  Sparkles,
  History,
  BookmarkCheck,
  ShieldCheck,
  ExternalLink,
  Cpu,
  Layers,
} from 'lucide-react';

interface Props {
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<Props> = ({ mobileOpen, onCloseMobile }) => {
  const navItems = [
    {
      to: '/overview',
      label: 'Overview',
      icon: Layers,
      description: 'Readiness metrics & activity',
    },
    {
      to: '/',
      label: 'App Directory',
      icon: LayoutGrid,
      description: 'Provider catalog & filters',
      exact: true,
    },
    {
      to: '/generate',
      label: 'Live Researcher',
      icon: Sparkles,
      description: 'Discover unknown provider',
    },
    {
      to: '/runs',
      label: 'Research Runs',
      icon: History,
      description: 'Execution logs & traces',
    },
    {
      to: '/saved',
      label: 'Saved Guides',
      icon: BookmarkCheck,
      description: 'Persistent OAuth guides',
    },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {mobileOpen && (
        <div
          onClick={onCloseMobile}
          className="fixed inset-0 z-40 bg-black/80 backdrop-blur-xs lg:hidden"
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-dark-sidebar border-r border-border-subtle flex flex-col transition-transform duration-200 ease-in-out lg:translate-x-0 ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand header */}
        <div className="h-16 flex items-center justify-between px-5 border-b border-border-subtle">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-accent-dim border border-accent-border flex items-center justify-center text-accent shadow-xs">
              <Compass className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-sm tracking-tight text-white">
                  OAuth Compass
                </span>
                <span className="text-[11px] font-mono px-1.5 py-0.5 rounded bg-dark-elevated text-accent border border-accent-border/50 font-bold">
                  v1.0
                </span>
              </div>
              <p className="text-xs text-slate-400 font-medium">Composio Integrations</p>
            </div>
          </div>
        </div>

        {/* Navigation list */}
        <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
          <div className="px-3 pb-2 text-xs font-mono uppercase tracking-wider text-slate-400 font-semibold">
            Workspace
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.exact}
                onClick={onCloseMobile}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-sm transition-all group ${
                    isActive
                      ? 'bg-[#A3E635]/10 text-white font-semibold border border-[#A3E635]/30 shadow-xs'
                      : 'border border-transparent text-slate-300 hover:text-white hover:bg-dark-surface/60 font-medium'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon
                      className={`w-4 h-4 shrink-0 transition-colors ${
                        isActive
                          ? 'text-accent'
                          : 'text-slate-400 group-hover:text-white'
                      }`}
                    />
                    <div className="flex-1 truncate">
                      <div className="truncate">{item.label}</div>
                    </div>
                    {isActive && (
                      <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
                    )}
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* System Intelligence Box (Bottom Widget) */}
        <div className="p-3 border-t border-border-subtle">
          <div className="bg-dark-surface border border-border-subtle rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-slate-400 uppercase tracking-wider font-semibold">
                System Status
              </span>
              <span className="inline-flex items-center space-x-1.5 text-xs text-accent font-bold">
                <span className="w-2 h-2 rounded-full bg-accent animate-ping" />
                <span>Ready</span>
              </span>
            </div>

            <div className="space-y-1.5 text-xs">
              <div className="flex items-center justify-between text-slate-300">
                <span className="flex items-center space-x-1.5">
                  <Cpu className="w-3.5 h-3.5 text-slate-400" />
                  <span>Primary LLM</span>
                </span>
                <span className="font-mono text-xs text-white font-semibold">Llama 3.3 70B</span>
              </div>
              <div className="flex items-center justify-between text-slate-300">
                <span className="flex items-center space-x-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
                  <span>SSRF Defense</span>
                </span>
                <span className="font-mono text-xs text-accent font-bold">Active</span>
              </div>
            </div>

            <a
              href="https://github.com/composio/composio"
              target="_blank"
              rel="noreferrer"
              className="flex items-center justify-between pt-2.5 border-t border-border-muted text-xs text-slate-400 hover:text-white transition-colors font-medium"
            >
              <span>Composio SDK Docs</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </aside>
    </>
  );
};
