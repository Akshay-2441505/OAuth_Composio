import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  Calendar,
  ExternalLink,
  ShieldAlert,
  Sparkles,
  CheckCircle2,
  Info,
  Copy,
  Check,
} from 'lucide-react';
import { fetchAppGuide, fetchGuideById } from '../api/client';
import { GuideResponse } from '../api/types';
import { ComplexityBadge } from '../components/ComplexityBadge';
import { CopyShareButton } from '../components/CopyShareButton';
import { ReadinessBanner } from '../components/ReadinessBanner';
import { StepsList } from '../components/StepsList';
import { HandoffMatrix } from '../components/HandoffMatrix';
import { BlockersList } from '../components/BlockersList';
import { SourceList } from '../components/SourceList';

export const GuideDetailPage: React.FC = () => {
  const { slug, id } = useParams<{ slug?: string; id?: string }>();
  const [guide, setGuide] = useState<GuideResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copiedMd, setCopiedMd] = useState(false);

  const loadGuide = () => {
    setLoading(true);
    const fetchPromise = slug ? fetchAppGuide(slug) : id ? fetchGuideById(id) : null;

    if (!fetchPromise) {
      setError('Invalid guide parameters');
      setLoading(false);
      return;
    }

    fetchPromise
      .then((data) => {
        setGuide(data);
        setError(null);
      })
      .catch((err) => {
        setError(err.message || 'Failed to retrieve guide');
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadGuide();
  }, [slug, id]);

  const copyAsMarkdown = () => {
    if (!guide) return;
    const { content } = guide;
    let md = `# ${content.app.name} — OAuth Readiness Guide\n\n`;
    md += `**Canonical Domain:** ${content.app.provider_domain}\n`;
    md += `**Managed OAuth:** ${content.readiness.managed_oauth.status}\n`;
    md += `**Complexity:** ${content.readiness.complexity}\n`;
    md += `**Setup Time:** ${content.time_estimates.active_setup.minimum_minutes ?? 'Unknown'} mins\n\n`;
    md += `## Architecture Recommendation\n${content.readiness.recommended_auth_product}\n\n`;
    md += `## Setup Steps\n`;
    content.steps.forEach((s, idx) => {
      md += `${idx + 1}. **${s.title}** (${s.owner})\n   ${s.description}\n   *Verification:* ${s.verification}\n\n`;
    });
    md += `*Generated via OAuth Compass (${window.location.origin}/guides/${guide.id})*\n`;

    navigator.clipboard.writeText(md).then(() => {
      setCopiedMd(true);
      setTimeout(() => setCopiedMd(false), 2000);
    });
  };

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse max-w-5xl mx-auto">
        <div className="h-6 bg-dark-elevated rounded w-1/4" />
        <div className="h-20 bg-dark-surface border border-border-subtle rounded-xl" />
        <div className="h-44 bg-dark-surface border border-border-subtle rounded-xl" />
        <div className="h-64 bg-dark-surface border border-border-subtle rounded-xl" />
      </div>
    );
  }

  if (error || !guide) {
    return (
      <div className="bg-dark-surface border border-border-subtle rounded-xl p-10 text-center max-w-lg mx-auto shadow-xs">
        <div className="w-12 h-12 rounded-xl bg-rose-950/40 border border-rose-500/40 flex items-center justify-center text-rose-400 mx-auto mb-3">
          <ShieldAlert className="w-6 h-6" />
        </div>
        <h2 className="text-base font-bold text-white mb-1">Guide Not Found</h2>
        <p className="text-xs text-slate-300 mb-5 font-medium">
          {error || 'The requested OAuth readiness guide could not be retrieved.'}
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <button
            type="button"
            onClick={loadGuide}
            className="inline-flex items-center space-x-1.5 px-4 py-2.5 rounded-xl bg-accent text-dark-bg text-xs font-bold hover:bg-accent-hover transition-colors shadow-xs"
          >
            <span>Retry Loading</span>
          </button>
          <Link
            to="/"
            className="inline-flex items-center space-x-1.5 px-4 py-2.5 rounded-xl bg-dark-elevated border border-border-subtle hover:border-border-DEFAULT text-white text-xs font-semibold transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Return to Provider Directory</span>
          </Link>
        </div>
      </div>
    );
  }

  const { content } = guide;

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Top Header & Breadcrumbs & Share Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <Link
          to="/"
          className="inline-flex items-center text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5 mr-1 text-slate-400" />
          <span>Back to App Directory</span>
        </Link>

        <div className="flex items-center space-x-2.5">
          <button
            onClick={copyAsMarkdown}
            type="button"
            className={`inline-flex items-center space-x-1.5 px-3.5 py-2 text-xs font-semibold rounded-xl border transition-all cursor-pointer shadow-xs ${
              copiedMd
                ? 'border-emerald-500/50 bg-emerald-500/15 text-emerald-300'
                : 'border-border-subtle bg-dark-elevated hover:bg-dark-hover hover:border-border-DEFAULT text-white'
            }`}
            title="Copy as Markdown to clipboard"
          >
            {copiedMd ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400 stroke-[3]" />
                <span className="font-bold">Markdown Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5 text-slate-400" />
                <span>Export Markdown</span>
              </>
            )}
          </button>
          <CopyShareButton guideId={guide.id} />
        </div>
      </div>

      {/* Guide Identity Banner */}
      <div className="bg-dark-surface border border-border-subtle rounded-2xl p-6 sm:p-7 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-3">
              <span
                className={`text-xs font-mono font-bold px-3 py-1 rounded-full border uppercase shadow-xs ${
                  guide.origin === 'seeded'
                    ? 'bg-accent-dim text-accent border-accent-border'
                    : 'bg-sky-500/15 text-sky-300 border-sky-500/40'
                }`}
              >
                {guide.origin === 'seeded' ? 'Official Seed Guide' : 'AI Autonomous Research'}
              </span>
              <ComplexityBadge level={content.readiness.complexity} />
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center">
              <span>{content.app.name}</span>
              <span className="text-slate-400 font-normal text-lg sm:text-xl ml-2.5">OAuth Readiness</span>
            </h1>

            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-300 mt-3 font-mono">
              <a
                href={content.app.website_url}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center text-accent hover:underline font-bold"
              >
                <span>{content.app.provider_domain}</span>
                <ExternalLink className="w-3.5 h-3.5 ml-1" />
              </a>
              <span className="flex items-center text-slate-300">
                <Calendar className="w-3.5 h-3.5 mr-1.5 text-slate-400" />
                {new Date(content.last_researched_at).toLocaleDateString(undefined, {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric',
                })}
              </span>
              <span className="text-slate-400">Guide ID: <code className="text-white font-bold bg-dark-elevated px-2 py-0.5 rounded border border-border-subtle">{guide.id}</code></span>
            </div>
          </div>
        </div>
      </div>

      {/* In-Page Sticky Anchor Navigation (Table of Contents) */}
      <div className="sticky top-16 z-20 -mx-2 px-3 py-2.5 bg-[#0E1321]/95 backdrop-blur-md border-y border-border-subtle flex items-center space-x-2 overflow-x-auto text-xs shadow-xs">
        <span className="text-xs font-mono uppercase text-slate-400 font-bold mr-1 shrink-0">Jump to:</span>
        {[
          { href: '#readiness-summary', label: 'Readiness' },
          { href: '#recommended-architecture', label: 'Architecture' },
          { href: '#prerequisites', label: 'Prerequisites' },
          { href: '#setup-steps', label: 'Setup Steps' },
          { href: '#handoff-matrix', label: 'Responsibilities' },
          { href: '#blockers-and-risks', label: 'Blockers' },
          { href: '#sources-and-evidence', label: 'Sources' },
        ].map((anchor) => (
          <a
            key={anchor.href}
            href={anchor.href}
            className="px-3 py-1.5 rounded-lg bg-dark-elevated text-slate-300 hover:text-white hover:bg-dark-hover border border-border-subtle transition-all whitespace-nowrap font-medium text-xs shadow-xs"
          >
            {anchor.label}
          </a>
        ))}
      </div>

      {/* Legal & Empirical Research Disclaimer */}
      <div className="bg-dark-surface border border-border-subtle rounded-xl p-4 flex items-start space-x-3 text-xs text-slate-300 shadow-xs">
        <Info className="w-4 h-4 text-accent shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <strong className="text-white">Empirical Grounding:</strong> This guide provides pre-integration developer intelligence synthesized from official developer documentation. Never store OAuth client secrets on public repositories or client-side bundles.
        </div>
      </div>

      {/* Section 1: Readiness Overview */}
      <ReadinessBanner content={content} />

      {/* Section 2: Architectural Decision Callout (Invariant 4: GitHub Apps vs. OAuth Apps) */}
      <section
        id="recommended-architecture"
        className="bg-dark-surface border border-accent/40 rounded-2xl p-5 sm:p-6 mb-6 shadow-sm"
      >
        <div className="flex items-center space-x-3 mb-3">
          <div className="w-8 h-8 rounded-lg bg-accent-dim border border-accent-border flex items-center justify-center text-accent">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white tracking-tight">
              Architectural Product Recommendation
            </h2>
            <p className="text-xs text-slate-400 font-normal">
              Recommended integration product and OAuth registration model
            </p>
          </div>
        </div>
        <div className="bg-dark-elevated border border-border-subtle p-4 rounded-xl">
          <p className="text-sm text-slate-200 leading-relaxed font-mono font-medium">
            {content.readiness.recommended_auth_product}
          </p>
        </div>
      </section>

      {/* Section 3: Prerequisites Checklist */}
      {content.prerequisites && content.prerequisites.length > 0 && (
        <section id="prerequisites" className="bg-dark-surface border border-border-subtle rounded-xl p-5 sm:p-6 mb-6 shadow-xs">
          <div className="flex items-center space-x-2.5 mb-3.5">
            <CheckCircle2 className="w-4 h-4 text-accent" />
            <h2 className="text-sm sm:text-base font-bold text-white tracking-tight">
              Prerequisites & Developer Account Requirements
            </h2>
          </div>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs sm:text-sm text-slate-300">
            {content.prerequisites.map((p, idx) => (
              <li
                key={idx}
                className="flex items-start bg-dark-elevated border border-border-subtle rounded-xl p-3.5 font-normal"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 mr-3 shrink-0" />
                <span className="leading-relaxed">{p}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Section 4: Step-by-Step Setup (with persistent local checklist) */}
      <StepsList steps={content.steps} guideId={guide.id} />

      {/* Section 5: Human vs. Agent Responsibility Boundary */}
      <HandoffMatrix
        agentCapabilities={content.agent_capabilities}
        humanActions={content.human_actions_required}
      />

      {/* Section 6: Blockers & Assumptions */}
      <BlockersList
        blockers={content.blockers}
        approvalTriggers={content.approval.triggers}
        assumptions={content.assumptions}
        uncertainties={content.uncertainties}
      />

      {/* Section 7: Evidence & Verified Sources */}
      <SourceList sources={content.sources} />
    </div>
  );
};
