import React from 'react';
import { Clock, Hourglass, KeyRound, Layers, ExternalLink, CheckCircle2 } from 'lucide-react';
import { GuideContent } from '../api/types';

interface Props {
  content: GuideContent;
}

export const ReadinessBanner: React.FC<Props> = ({ content }) => {
  const { readiness, time_estimates } = content;

  const formatActiveTime = () => {
    const min = time_estimates.active_setup.minimum_minutes;
    const max = time_estimates.active_setup.maximum_minutes;
    if (min && max) {
      return `${min}–${max} mins`;
    }
    if (min) return `~${min} mins`;
    return 'Unknown';
  };

  const formatWaitTime = () => {
    if (time_estimates.external_wait.status === 'none') {
      return 'Instant / No approval queue';
    }
    const min = time_estimates.external_wait.minimum_hours;
    const max = time_estimates.external_wait.maximum_hours;
    if (min && max) {
      if (max >= 24) {
        return `${Math.round(min / 24)}–${Math.round(max / 24)} days`;
      }
      return `${min}–${max} hours`;
    }
    if (time_estimates.external_wait.status === 'conditional') {
      return 'Conditional (scope-dependent)';
    }
    return 'Unknown / Not published';
  };

  const isManagedAvailable = readiness.managed_oauth.status === 'available';
  const waitText = formatWaitTime();
  const isLongWait = waitText.length > 14;

  return (
    <section id="readiness-summary" className="bg-dark-surface border border-border-subtle rounded-2xl p-5 sm:p-6 mb-6 space-y-5 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-border-subtle gap-3">
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-accent-dim border border-accent-border flex items-center justify-center text-accent shadow-xs">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base sm:text-lg font-bold text-white tracking-tight">
              OAuth Readiness Profile
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 font-normal leading-relaxed mt-0.5">
              {readiness.complexity_rationale}
            </p>
          </div>
        </div>

        {readiness.managed_oauth.status && (
          <div className="flex items-center space-x-2 shrink-0">
            <span className="text-xs font-mono text-slate-400 font-semibold">Managed Flow:</span>
            <span
              className={`inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold border ${
                isManagedAvailable
                  ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40 shadow-xs'
                  : 'bg-dark-elevated text-slate-300 border-border-subtle'
              }`}
            >
              {isManagedAvailable && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
              <span className="capitalize">{readiness.managed_oauth.status.replace('_', ' ')}</span>
            </span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Active Setup Effort */}
        <div className="bg-dark-elevated/80 border border-border-subtle rounded-xl p-4 sm:p-5 flex flex-col justify-between hover:border-border-DEFAULT transition-colors shadow-xs">
          <div>
            <div className="flex items-center text-xs font-semibold text-slate-300 mb-2">
              <Clock className="w-4 h-4 mr-1.5 text-accent" />
              <span>Active Setup Time</span>
            </div>
            <div className="text-xl sm:text-2xl font-bold font-mono text-white tracking-tight">{formatActiveTime()}</div>
          </div>
          <p className="text-xs text-slate-300 mt-3 leading-relaxed font-normal">
            {time_estimates.active_setup.basis}
          </p>
        </div>

        {/* External Provider Wait Time */}
        <div className="bg-dark-elevated/80 border border-border-subtle rounded-xl p-4 sm:p-5 flex flex-col justify-between hover:border-border-DEFAULT transition-colors shadow-xs">
          <div>
            <div className="flex items-center text-xs font-semibold text-slate-300 mb-2">
              <Hourglass className="w-4 h-4 mr-1.5 text-amber-400" />
              <span>External Review Wait</span>
            </div>
            <div
              className={`font-bold tracking-tight ${
                isLongWait
                  ? 'text-base sm:text-lg text-amber-300 leading-snug font-sans'
                  : 'text-xl sm:text-2xl text-white font-mono'
              }`}
            >
              {waitText}
            </div>
          </div>
          <p className="text-xs text-slate-300 mt-3 leading-relaxed font-normal">
            {time_estimates.external_wait.basis}
          </p>
        </div>

        {/* Custom OAuth Requirement */}
        <div className="bg-dark-elevated/80 border border-border-subtle rounded-xl p-4 sm:p-5 flex flex-col justify-between hover:border-border-DEFAULT transition-colors shadow-xs">
          <div>
            <div className="flex items-center text-xs font-semibold text-slate-300 mb-2">
              <KeyRound className="w-4 h-4 mr-1.5 text-sky-400" />
              <span>App Registration</span>
            </div>
            <div className="text-xl sm:text-2xl font-bold text-white capitalize tracking-tight">
              {readiness.custom_oauth_app_required === 'yes' ? 'Custom Console' : readiness.custom_oauth_app_required}
            </div>
          </div>
          <p className="text-xs text-slate-300 mt-3 leading-relaxed font-normal">
            Target Product: <span className="text-slate-100 font-semibold">{readiness.recommended_auth_product}</span>
          </p>
        </div>

        {/* Managed Auth Option */}
        <div className="bg-dark-elevated/80 border border-border-subtle rounded-xl p-4 sm:p-5 flex flex-col justify-between hover:border-border-DEFAULT transition-colors shadow-xs">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-2">
              <span>Managed Auth</span>
              {readiness.managed_oauth.source_url && (
                <a
                  href={readiness.managed_oauth.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-accent hover:text-accent-hover font-bold"
                  title="Source documentation"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
            <div
              className={`text-xl sm:text-2xl font-bold capitalize tracking-tight ${
                isManagedAvailable ? 'text-accent' : 'text-slate-200'
              }`}
            >
              {readiness.managed_oauth.status.replace('_', ' ')}
            </div>
          </div>
          <p className="text-xs text-slate-300 mt-3 leading-relaxed font-normal">
            {isManagedAvailable
              ? 'Managed credentials available; skip custom credential provisioning.'
              : 'Dedicated developer console credentials are required.'}
          </p>
        </div>
      </div>
    </section>
  );
};
