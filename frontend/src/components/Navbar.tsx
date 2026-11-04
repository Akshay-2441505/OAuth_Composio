import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Compass, Sparkles, Server } from 'lucide-react';
import { fetchHealth } from '../api/client';

export const Navbar: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<'checking' | 'ok' | 'error'>('checking');

  useEffect(() => {
    fetchHealth()
      .then((data) => {
        if (data.status === 'ok') setHealthStatus('ok');
        else setHealthStatus('error');
      })
      .catch(() => setHealthStatus('error'));
  }, []);

  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-30 shadow-xs">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="w-10 h-10 rounded-lg bg-emerald-600 text-white flex items-center justify-center shadow-xs group-hover:bg-emerald-700 transition-colors">
            <Compass className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-slate-900 tracking-tight">OAuth Compass</span>
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200">
                MVP
              </span>
            </div>
            <p className="text-[11px] text-slate-500 leading-none">Integration Readiness & Research</p>
          </div>
        </Link>

        <div className="flex items-center space-x-4">
          <div className="hidden sm:flex items-center text-xs text-slate-500 bg-slate-50 px-2.5 py-1 rounded-md border border-slate-200">
            <Server className="w-3.5 h-3.5 mr-1.5 text-slate-400" />
            <span>API:</span>
            <span
              className={`inline-block w-2 h-2 rounded-full mx-1.5 ${
                healthStatus === 'ok'
                  ? 'bg-emerald-500'
                  : healthStatus === 'error'
                  ? 'bg-rose-500'
                  : 'bg-amber-400 animate-pulse'
              }`}
            />
            <span className="font-medium text-slate-700">
              {healthStatus === 'ok' ? 'Online' : healthStatus === 'error' ? 'Unavailable' : 'Connecting...'}
            </span>
          </div>

          <Link
            to="/generate"
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 shadow-xs transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Research an App</span>
          </Link>
        </div>
      </div>
    </header>
  );
};

