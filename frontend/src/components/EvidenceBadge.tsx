import React from 'react';
import { CheckCircle2, Eye, Clock, HelpCircle } from 'lucide-react';
import { EvidenceStatus } from '../api/types';

interface Props {
  status: EvidenceStatus;
  showIcon?: boolean;
  className?: string;
  size?: 'sm' | 'md';
}

export const EvidenceBadge: React.FC<Props> = ({ status, showIcon = true, className = '', size = 'sm' }) => {
  const config = {
    verified: {
      label: 'Verified Source',
      tooltip: 'Directly supported by official provider documentation or reproducible test.',
      classes: 'bg-accent-dim text-accent border-accent-border',
      icon: CheckCircle2,
    },
    attempted: {
      label: 'Attempted',
      tooltip: 'The system inspected or tested this public resource; does not imply provider approval.',
      classes: 'bg-sky-500/15 text-sky-300 border-sky-500/40',
      icon: Eye,
    },
    estimated: {
      label: 'Estimated',
      tooltip: 'Heuristic estimate with explicit rationale and confidence level.',
      classes: 'bg-amber-500/15 text-amber-300 border-amber-500/40',
      icon: Clock,
    },
    unknown: {
      label: 'Unknown',
      tooltip: 'Not confirmed by available official documentation; verify with provider.',
      classes: 'bg-slate-800/80 text-slate-300 border-slate-700',
      icon: HelpCircle,
    },
  }[status] || {
    label: status,
    tooltip: '',
    classes: 'bg-slate-800/80 text-slate-300 border-slate-700',
    icon: HelpCircle,
  };

  const Icon = config.icon;
  const sizeClasses = size === 'md' ? 'text-xs px-3 py-1' : 'text-xs px-2.5 py-0.5';

  return (
    <span
      title={config.tooltip}
      className={`inline-flex items-center space-x-1.5 rounded-full font-semibold border cursor-help shadow-xs ${config.classes} ${sizeClasses} ${className}`}
    >
      {showIcon && <Icon className="w-3.5 h-3.5 shrink-0" />}
      <span>{config.label}</span>
    </span>
  );
};
