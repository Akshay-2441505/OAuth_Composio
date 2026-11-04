import React from 'react';
import { AlertTriangle, AlertCircle, HelpCircle, CheckCircle2 } from 'lucide-react';
import { SetupBlocker } from '../api/types';

interface Props {
  blockers: SetupBlocker[];
  approvalTriggers: string[];
  assumptions: string[];
  uncertainties: string[];
}

export const BlockersList: React.FC<Props> = ({
  blockers,
  approvalTriggers,
  assumptions,
  uncertainties,
}) => {
  return (
    <section id="blockers-and-risks" className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
      {/* Known Blockers & Remedies */}
      <div className="bg-dark-surface border border-border-subtle rounded-xl p-5 sm:p-6 flex flex-col justify-between shadow-xs">
        <div>
          <div className="flex items-center space-x-3 pb-3.5 border-b border-border-subtle mb-4">
            <div className="w-8 h-8 rounded-lg bg-amber-500/15 border border-amber-500/40 flex items-center justify-center text-amber-400">
              <AlertTriangle className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">
                Setup Blockers & Pitfalls
              </h2>
              <p className="text-xs text-slate-300 font-medium">
                Common obstacles that lead to OAuth registration rejection or runtime auth errors.
              </p>
            </div>
          </div>

          {blockers.length === 0 ? (
            <div className="p-4 rounded-xl bg-dark-elevated border border-border-subtle text-xs text-slate-400 italic">
              No critical blockers identified in official documentation.
            </div>
          ) : (
            <div className="space-y-3.5">
              {blockers.map((b, idx) => (
                <div key={idx} className="bg-dark-elevated border border-amber-500/35 rounded-xl p-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-amber-300">{b.title}</h3>
                    <span className="text-xs font-mono text-slate-400 font-medium">Blocker #{idx + 1}</span>
                  </div>
                  <div className="text-xs sm:text-sm text-slate-300 space-y-1.5 font-normal">
                    <p>
                      <strong className="text-white font-semibold">Cause: </strong>
                      {b.cause}
                    </p>
                    <p className="text-accent flex items-start space-x-2 pt-1 font-medium">
                      <CheckCircle2 className="w-4 h-4 text-accent shrink-0 mt-0.5" />
                      <span>
                        <strong className="text-accent font-bold">Remedy: </strong>
                        {b.resolution}
                      </span>
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {approvalTriggers.length > 0 && (
          <div className="mt-5 pt-4 border-t border-border-subtle">
            <h4 className="text-xs font-bold text-rose-300 mb-2.5 flex items-center font-mono uppercase tracking-wider">
              <AlertCircle className="w-4 h-4 mr-1.5 text-rose-400" />
              Third-Party App Review Triggers
            </h4>
            <ul className="text-xs sm:text-sm text-slate-300 space-y-2 font-normal">
              {approvalTriggers.map((t, idx) => (
                <li key={idx} className="flex items-start space-x-2.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-rose-400 mt-2 shrink-0" />
                  <span className="leading-relaxed">{t}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Assumptions & Uncertainties */}
      <div className="bg-dark-surface border border-border-subtle rounded-xl p-5 sm:p-6 flex flex-col justify-between shadow-xs">
        <div>
          <div className="flex items-center space-x-3 pb-3.5 border-b border-border-subtle mb-4">
            <div className="w-8 h-8 rounded-lg bg-dark-elevated border border-border-subtle flex items-center justify-center text-slate-300">
              <HelpCircle className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">
                Assumptions & Unknowns
              </h2>
              <p className="text-xs text-slate-300 font-medium">
                Assumptions made during synthesis and items requiring environment-specific validation.
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2 font-bold">
                Operational Assumptions
              </h3>
              <ul className="text-xs sm:text-sm text-slate-300 space-y-2 bg-dark-elevated border border-border-subtle rounded-xl p-4 font-normal">
                {assumptions.map((a, idx) => (
                  <li key={idx} className="flex items-start space-x-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-slate-400 mt-2 shrink-0" />
                    <span className="leading-relaxed">{a}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-xs font-mono uppercase tracking-wider text-amber-300 mb-2 font-bold">
                Unverified Items / Unknowns
              </h3>
              <ul className="text-xs sm:text-sm text-amber-200 space-y-2 bg-dark-elevated border border-amber-500/30 rounded-xl p-4 font-normal">
                {uncertainties.map((u, idx) => (
                  <li key={idx} className="flex items-start space-x-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-2 shrink-0" />
                    <span className="leading-relaxed">{u}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-5 pt-4 border-t border-border-subtle text-xs text-slate-400 font-medium">
          <span>Always confirm unverified scopes against provider rate limits and SLAs.</span>
        </div>
      </div>
    </section>
  );
};
