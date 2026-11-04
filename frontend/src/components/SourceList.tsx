import React from 'react';
import { BookOpen, ExternalLink, ShieldCheck, Globe } from 'lucide-react';
import { Source } from '../api/types';

interface Props {
  sources: Source[];
}

export const SourceList: React.FC<Props> = ({ sources }) => {
  const officialSources = sources.filter((s) => s.is_official);
  const secondarySources = sources.filter((s) => !s.is_official);

  const renderSourceGroup = (group: Source[], title: string, isOfficial: boolean) => {
    if (!group.length) return null;

    return (
      <div className="mb-6 last:mb-0">
        <div className="flex items-center text-xs font-mono uppercase tracking-wider text-slate-300 font-bold mb-3">
          {isOfficial ? (
            <ShieldCheck className="w-4 h-4 mr-1.5 text-accent" />
          ) : (
            <Globe className="w-4 h-4 mr-1.5 text-slate-400" />
          )}
          <span>
            {title} ({group.length})
          </span>
        </div>
        <div className="space-y-3">
          {group.map((source) => (
            <div
              key={source.id}
              className="bg-dark-elevated border border-border-subtle hover:border-accent/50 rounded-xl p-4 transition-all group shadow-xs"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs sm:text-sm font-bold text-white hover:text-accent flex items-center group-hover:text-accent transition-colors truncate"
                  >
                    <span className="truncate">{source.title}</span>
                    <ExternalLink className="w-3.5 h-3.5 ml-1.5 text-slate-400 group-hover:text-accent shrink-0" />
                  </a>
                  <p className="text-xs font-mono text-slate-400 mt-1 truncate">{source.url}</p>
                  {source.relevance_note && (
                    <p className="text-xs sm:text-sm text-slate-300 mt-2 italic border-l-2 border-accent/60 pl-2.5 leading-relaxed font-normal">
                      "{source.relevance_note}"
                    </p>
                  )}
                </div>
                <div className="text-right shrink-0">
                  <span className="inline-block px-2 py-0.5 rounded text-xs font-mono bg-dark-bg border border-border-subtle text-accent font-bold">
                    HTTP {source.http_status || 200}
                  </span>
                  <div className="text-xs text-slate-400 mt-1.5 font-mono font-medium">{source.domain}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <section id="sources-and-evidence" className="bg-dark-surface border border-border-subtle rounded-xl p-5 sm:p-6 mb-6 shadow-xs">
      <div className="border-b border-border-subtle pb-3.5 mb-5">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-accent-dim border border-accent-border flex items-center justify-center text-accent">
            <BookOpen className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white tracking-tight">
              Verified Sources & Citations
            </h2>
            <p className="text-xs text-slate-300 mt-0.5 font-medium">
              Empirical grounding extracted strictly from official developer documentation.
            </p>
          </div>
        </div>
      </div>

      {renderSourceGroup(officialSources, 'Primary Official Provider Documentation', true)}
      {renderSourceGroup(secondarySources, 'Secondary Architecture References', false)}
    </section>
  );
};
