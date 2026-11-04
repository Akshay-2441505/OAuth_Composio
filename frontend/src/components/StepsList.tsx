import React, { useState, useEffect } from 'react';
import { ExternalLink, Check, User, Bot, Users, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { SetupStep } from '../api/types';
import { EvidenceBadge } from './EvidenceBadge';

interface Props {
  steps: SetupStep[];
  guideId?: string;
}

export const StepsList: React.FC<Props> = ({ steps, guideId }) => {
  const storageKey = guideId ? `oauth_compass_steps_${guideId}` : null;

  const [completedSteps, setCompletedSteps] = useState<Record<string, boolean>>(() => {
    if (storageKey) {
      try {
        const saved = localStorage.getItem(storageKey);
        if (saved) return JSON.parse(saved);
      } catch {
        // ignore storage error
      }
    }
    return {};
  });

  useEffect(() => {
    if (storageKey) {
      try {
        localStorage.setItem(storageKey, JSON.stringify(completedSteps));
      } catch {
        // ignore storage error
      }
    }
  }, [completedSteps, storageKey]);

  const toggleStep = (id: string) => {
    setCompletedSteps((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const completedCount = Object.values(completedSteps).filter(Boolean).length;
  const progressPercent = steps.length ? Math.round((completedCount / steps.length) * 100) : 0;

  const renderOwnerBadge = (owner: string) => {
    if (owner === 'agent') {
      return (
        <span className="inline-flex items-center text-xs font-mono px-2.5 py-0.5 rounded-md bg-accent-dim text-accent border border-accent-border font-bold">
          <Bot className="w-3.5 h-3.5 mr-1" /> Agent
        </span>
      );
    }
    if (owner === 'shared') {
      return (
        <span className="inline-flex items-center text-xs font-mono px-2.5 py-0.5 rounded-md bg-sky-500/15 text-sky-300 border border-sky-500/40 font-bold">
          <Users className="w-3.5 h-3.5 mr-1" /> Shared
        </span>
      );
    }
    return (
      <span className="inline-flex items-center text-xs font-mono px-2.5 py-0.5 rounded-md bg-dark-elevated text-slate-300 border border-border-subtle font-bold">
        <User className="w-3.5 h-3.5 mr-1" /> Developer
      </span>
    );
  };

  return (
    <section id="setup-steps" className="bg-dark-surface border border-border-subtle rounded-2xl p-6 sm:p-7 mb-6 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-border-subtle gap-3">
        <div>
          <div className="flex items-center space-x-2.5">
            <h2 className="text-base sm:text-lg font-bold text-white tracking-tight">
              App Registration & Setup Steps
            </h2>
            <span className="text-xs font-mono px-2.5 py-0.5 rounded-md bg-dark-elevated text-slate-300 border border-border-subtle font-bold">
              {steps.length} steps
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-300 mt-1 font-normal">
            Sequential registration checklist extracted from provider documentation.
          </p>
        </div>

        {/* Progress indicator */}
        <div className="flex items-center space-x-3 bg-dark-elevated border border-border-subtle px-3.5 py-2 rounded-xl shadow-xs">
          <span className="text-xs font-mono text-slate-300">
            <span className="text-accent font-bold text-sm">{completedCount}</span>/{steps.length} done
          </span>
          <div className="w-24 bg-dark-bg rounded-full h-2 overflow-hidden border border-border-muted">
            <div
              className="bg-accent h-2 rounded-full transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <span className="text-xs font-mono text-slate-300 font-bold">{progressPercent}%</span>
        </div>
      </div>

      <div className="space-y-4 mt-5">
        {steps.map((step, idx) => {
          const isDone = Boolean(completedSteps[step.id]);

          return (
            <div
              key={step.id}
              className={`p-5 rounded-xl border transition-all shadow-xs ${
                isDone
                  ? 'bg-dark-elevated/40 border-border-muted opacity-75'
                  : 'bg-dark-elevated/70 border-border-subtle hover:border-border-DEFAULT'
              }`}
            >
              <div className="flex items-start space-x-4">
                <button
                  type="button"
                  onClick={() => toggleStep(step.id)}
                  className={`mt-0.5 w-5 h-5 rounded-md flex items-center justify-center border transition-all shrink-0 cursor-pointer ${
                    isDone
                      ? 'bg-[#A3E635] border-[#A3E635] text-[#0A0E17] font-bold shadow-xs'
                      : 'border-slate-500 hover:border-accent bg-dark-bg text-transparent'
                  }`}
                  aria-label={`Mark step ${idx + 1} complete`}
                >
                  <Check className={`w-3.5 h-3.5 stroke-[3] ${isDone ? 'block' : 'hidden'}`} />
                </button>

                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-2.5 mb-2">
                    <span className="text-xs font-mono font-bold text-accent px-1.5 py-0.5 rounded bg-dark-bg border border-border-subtle">
                      #{idx + 1}
                    </span>
                    <h3
                      className={`text-sm sm:text-base font-bold text-white ${
                        isDone ? 'line-through text-slate-500' : ''
                      }`}
                    >
                      {step.title}
                    </h3>
                    <div className="flex items-center space-x-2 ml-auto">
                      {renderOwnerBadge(step.owner)}
                      <EvidenceBadge status={step.evidence_status} />
                    </div>
                  </div>

                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-normal">
                    {step.description}
                  </p>

                  {/* Verification Criteria */}
                  <div className="mt-3.5 text-xs bg-dark-bg border border-border-subtle rounded-xl p-3.5 flex items-start space-x-2.5 text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-accent shrink-0 mt-0.5" />
                    <div className="leading-relaxed">
                      <span className="font-bold text-white mr-1.5">Verification:</span>
                      <span className="text-slate-300 font-medium">{step.verification}</span>
                    </div>
                  </div>

                  {/* Handoff / Secret Warning */}
                  {(step.requires_secret || step.requires_login) && (
                    <div className="mt-2.5 text-xs text-amber-200 bg-amber-500/15 border border-amber-500/40 rounded-xl p-3 flex items-center space-x-2.5 font-medium">
                      <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0" />
                      <span>
                        {step.handoff_reason ||
                          (step.requires_secret
                            ? 'Human Action Required: Secrets cannot be generated or held by agents. Generate and store securely in your vault.'
                            : 'Human Action Required: Developer account authentication required in provider portal.')}
                      </span>
                    </div>
                  )}

                  {/* Portal link if provided */}
                  {step.portal_url && (
                    <div className="mt-3">
                      <a
                        href={step.portal_url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-dark-surface hover:bg-dark-hover border border-border-subtle text-xs text-accent hover:text-accent-hover font-bold shadow-xs transition-colors"
                      >
                        <span>Open Console Portal</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};
