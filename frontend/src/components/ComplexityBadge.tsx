import React from 'react';
import { ComplexityLevel } from '../api/types';

interface Props {
  level?: ComplexityLevel | string | null;
  size?: 'sm' | 'md';
}

export const ComplexityBadge: React.FC<Props> = ({ level = 'unknown', size = 'sm' }) => {
  const normLevel = (level || 'unknown').toLowerCase() as ComplexityLevel;

  const config = {
    low: {
      label: 'Low Complexity',
      classes: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40',
      dot: 'bg-emerald-400',
    },
    medium: {
      label: 'Medium Complexity',
      classes: 'bg-amber-500/15 text-amber-300 border-amber-500/40',
      dot: 'bg-amber-400',
    },
    high: {
      label: 'High Complexity',
      classes: 'bg-rose-500/15 text-rose-300 border-rose-500/40',
      dot: 'bg-rose-400',
    },
    unknown: {
      label: 'Unknown Complexity',
      classes: 'bg-slate-800/80 text-slate-300 border-slate-700',
      dot: 'bg-slate-400',
    },
  }[normLevel] || {
    label: level,
    classes: 'bg-slate-800/80 text-slate-300 border-slate-700',
    dot: 'bg-slate-400',
  };

  const sizeClasses = size === 'md' ? 'text-xs px-3 py-1' : 'text-xs px-2.5 py-0.5';

  return (
    <span
      className={`inline-flex items-center space-x-1.5 rounded-full font-semibold border ${config.classes} ${sizeClasses} shadow-xs`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`} />
      <span>{config.label}</span>
    </span>
  );
};
