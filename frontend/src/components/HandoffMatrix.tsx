import React from 'react';
import { Bot, UserCheck, ShieldCheck, Key } from 'lucide-react';

interface Props {
  agentCapabilities: string[];
  humanActions: string[];
}

export const HandoffMatrix: React.FC<Props> = ({ agentCapabilities, humanActions }) => {
  return (
    <section id="handoff-matrix" className="bg-dark-surface border border-border-subtle rounded-xl p-5 sm:p-6 mb-6 shadow-xs">
      <div className="border-b border-border-subtle pb-3.5 mb-5">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-sky-500/15 border border-sky-500/40 flex items-center justify-center text-sky-400">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white tracking-tight">
              Human vs. Agent Responsibility Boundary
            </h2>
            <p className="text-xs text-slate-300 mt-0.5 font-medium">
              Clear delineation between automated pre-integration research and manual portal operations.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-5">
        {/* Agent Automated Research */}
        <div className="bg-dark-elevated border border-border-subtle rounded-xl p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle mb-3.5">
              <div className="flex items-center space-x-2">
                <Bot className="w-4 h-4 text-accent" />
                <span className="text-xs font-bold font-mono uppercase tracking-wider text-accent">
                  Agent Automated Research
                </span>
              </div>
              <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-accent-dim text-accent border border-accent-border">
                Automated
              </span>
            </div>

            <ul className="space-y-3 text-xs sm:text-sm text-slate-300 font-normal">
              {agentCapabilities.map((cap, idx) => (
                <li key={idx} className="flex items-start space-x-2.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 shrink-0" />
                  <span className="leading-relaxed">{cap}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-5 pt-3.5 border-t border-border-subtle text-xs text-slate-400 flex items-center font-medium">
            <span>Official documentation scraped & structured into validated schemas</span>
          </div>
        </div>

        {/* Human Actions Required */}
        <div className="bg-dark-elevated border border-border-subtle rounded-xl p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle mb-3.5">
              <div className="flex items-center space-x-2">
                <UserCheck className="w-4 h-4 text-amber-400" />
                <span className="text-xs font-bold font-mono uppercase tracking-wider text-amber-300">
                  Developer Manual Actions
                </span>
              </div>
              <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-amber-500/15 text-amber-300 border border-amber-500/40">
                Manual Console
              </span>
            </div>

            <ul className="space-y-3 text-xs sm:text-sm text-slate-300 font-normal">
              {humanActions.map((act, idx) => (
                <li key={idx} className="flex items-start space-x-2.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-2 shrink-0" />
                  <span className="leading-relaxed">{act}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-5 pt-3.5 border-t border-border-subtle flex items-center text-xs text-amber-200 font-semibold space-x-2">
            <Key className="w-4 h-4 text-amber-400 shrink-0" />
            <span>Zero credential retention: OAuth Compass never prompts for, receives, or stores client secrets.</span>
          </div>
        </div>
      </div>
    </section>
  );
};
