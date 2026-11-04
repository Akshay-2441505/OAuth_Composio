import React, { useState } from 'react';
import { Share2, Check } from 'lucide-react';

interface Props {
  guideId: string;
}

export const CopyShareButton: React.FC<Props> = ({ guideId }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const url = `${window.location.origin}/guides/${guideId}`;
    navigator.clipboard.writeText(url).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <button
      type="button"
      onClick={handleCopy}
      className={`inline-flex items-center space-x-1.5 px-3.5 py-2 text-xs font-semibold rounded-xl border transition-all cursor-pointer shadow-xs ${
        copied
          ? 'border-emerald-500/50 bg-emerald-500/15 text-emerald-300'
          : 'border-border-subtle bg-dark-elevated hover:bg-dark-hover hover:border-border-DEFAULT text-white'
      }`}
      title="Copy shareable link to this guide"
    >
      {copied ? (
        <>
          <Check className="w-3.5 h-3.5 text-emerald-400 stroke-[3]" />
          <span className="font-bold">Link Copied!</span>
        </>
      ) : (
        <>
          <Share2 className="w-3.5 h-3.5 text-slate-400" />
          <span>Share Guide</span>
        </>
      )}
    </button>
  );
};
