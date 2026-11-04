import React from 'react';
import {
  CheckCircle2,
  Clock,
  Loader2,
  AlertCircle,
  Search,
  BookOpen,
  Cpu,
  ShieldCheck,
  Globe,
} from 'lucide-react';
import { StageEvent } from '../api/types';

interface Props {
  stages: StageEvent[];
  currentStatus: string;
  providerUsed?: string | null;
  modelUsed?: string | null;
}

const STAGE_CONFIG: Record<string, { label: string; icon: React.FC<{ className?: string }> }> = {
  identify: { label: 'Identify Provider & Canonical Domain', icon: Globe },
  search: { label: 'Search Official Developer Documentation', icon: Search },
  fetch: { label: 'Fetch & Extract Documentation Content', icon: BookOpen },
  analyze: { label: 'Synthesize OAuth Scopes & Requirements', icon: Cpu },
  validate: { label: 'Validate Schema & Publish Shareable Guide', icon: ShieldCheck },
};

const ALL_STAGES = ['identify', 'search', 'fetch', 'analyze', 'validate'];

export const ResearchProgress: React.FC<Props> = ({
  stages,
  currentStatus,
  providerUsed,
  modelUsed,
}) => {
  const stageMap = new Map<string, StageEvent>();
  stages.forEach((s) => stageMap.set(s.name, s));

  return (
    <div className="bg-dark-surface border border-border-subtle rounded-2xl p-6 sm:p-7 space-y-6 shadow-sm">
      <div className="border-b border-border-subtle pb-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center space-x-3">
            {currentStatus === 'completed' ? (
              <div className="w-9 h-9 rounded-xl bg-accent-dim border border-accent-border flex items-center justify-center text-accent">
                <CheckCircle2 className="w-5 h-5" />
              </div>
            ) : currentStatus === 'failed' ? (
              <div className="w-9 h-9 rounded-xl bg-rose-500/15 border border-rose-500/40 flex items-center justify-center text-rose-400">
                <AlertCircle className="w-5 h-5" />
              </div>
            ) : (
              <div className="w-9 h-9 rounded-xl bg-accent-dim border border-accent-border flex items-center justify-center text-accent">
                <Loader2 className="w-5 h-5 animate-spin" />
              </div>
            )}
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">
                {currentStatus === 'completed'
                  ? 'Research Completed & Guide Published'
                  : currentStatus === 'failed'
                  ? 'Research Pipeline Terminated'
                  : 'Autonomous OAuth Research In Flight'}
              </h2>
              <p className="text-xs text-slate-300 mt-0.5 font-medium">
                Deterministic 5-stage synthesis strictly adhering to official provider sources.
              </p>
            </div>
          </div>

          {providerUsed && (
            <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-dark-elevated border border-border-subtle text-xs font-mono text-slate-300">
              <span className="text-slate-400">Model:</span>
              <span className="text-accent font-bold">{providerUsed}</span>
              {modelUsed && <span className="text-slate-400">({modelUsed})</span>}
            </div>
          )}
        </div>
      </div>

      <div className="relative pl-7 space-y-6 before:absolute before:left-3 before:top-2 before:bottom-2 before:w-[2px] before:bg-border-subtle">
        {ALL_STAGES.map((stageKey) => {
          const cfg = STAGE_CONFIG[stageKey] || { label: stageKey, icon: Globe };
          const stageEvent = stageMap.get(stageKey);

          let status: 'queued' | 'running' | 'completed' | 'failed' = 'queued';
          if (stageEvent) {
            status = stageEvent.status as any;
          } else if (currentStatus === 'completed') {
            status = 'completed';
          }

          const Icon = cfg.icon;

          return (
            <div key={stageKey} className="relative flex items-start space-x-3.5">
              {/* Timeline Icon Node */}
              <div
                className={`absolute -left-7 mt-0.5 w-6 h-6 rounded-full flex items-center justify-center border text-[11px] transition-all ${
                  status === 'completed'
                    ? 'bg-accent border-accent text-dark-bg font-bold shadow-xs'
                    : status === 'running'
                    ? 'bg-dark-bg border-accent text-accent ring-4 ring-accent/15'
                    : status === 'failed'
                    ? 'bg-rose-950 border-rose-500 text-rose-400'
                    : 'bg-dark-bg border-border-subtle text-slate-500'
                }`}
              >
                {status === 'completed' ? (
                  <CheckCircle2 className="w-3.5 h-3.5 stroke-[3]" />
                ) : status === 'running' ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-accent" />
                ) : status === 'failed' ? (
                  <AlertCircle className="w-3.5 h-3.5" />
                ) : (
                  <Clock className="w-3 h-3 text-slate-500" />
                )}
              </div>

              {/* Stage Content */}
              <div className="flex-1 bg-dark-elevated/70 border border-border-subtle rounded-xl p-4 shadow-xs">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center space-x-2">
                    <Icon className="w-4 h-4 text-slate-400 shrink-0" />
                    <span
                      className={`text-xs sm:text-sm font-bold tracking-tight ${
                        status === 'running'
                          ? 'text-accent'
                          : status === 'completed'
                          ? 'text-white'
                          : status === 'failed'
                          ? 'text-rose-400'
                          : 'text-slate-400'
                      }`}
                    >
                      {cfg.label}
                    </span>
                  </div>

                  <span
                    className={`text-[11px] uppercase font-mono font-bold px-2.5 py-0.5 rounded-full border ${
                      status === 'completed'
                        ? 'bg-accent-dim text-accent border-accent-border'
                        : status === 'running'
                        ? 'bg-accent-dim text-accent border-accent-border animate-pulse'
                        : status === 'failed'
                        ? 'bg-rose-500/15 text-rose-300 border-rose-500/40'
                        : 'bg-dark-surface text-slate-400 border-border-subtle'
                    }`}
                  >
                    {status}
                  </span>
                </div>

                {stageEvent?.message && (
                  <p className="text-xs sm:text-sm text-slate-300 mt-2 leading-relaxed font-mono">
                    {stageEvent.message}
                  </p>
                )}

                {stageEvent?.timestamp && (
                  <span className="text-[11px] text-slate-400 mt-2 block font-mono">
                    {new Date(stageEvent.timestamp).toLocaleTimeString()}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
