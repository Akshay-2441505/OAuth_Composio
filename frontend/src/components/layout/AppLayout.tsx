import React, { useState } from 'react';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';

interface Props {
  children: React.ReactNode;
}

export const AppLayout: React.FC<Props> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-dark-bg text-content-primary flex flex-col font-sans">
      {/* Left Persistent Navigation Sidebar */}
      <Sidebar mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} />

      {/* Main Content Area (Offset by sidebar width on desktop) */}
      <div className="lg:pl-64 flex flex-col flex-1 min-w-0">
        <TopBar onToggleMobile={() => setMobileOpen(!mobileOpen)} />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          {children}
        </main>

        <footer className="border-t border-border-subtle bg-dark-sidebar/40 py-4 px-6 text-center sm:text-left text-xs text-content-muted">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
            <div>
              <span className="font-semibold text-content-secondary">OAuth Compass</span> — Developer readiness & research layer.
            </div>
            <div className="flex items-center space-x-4 text-[11px]">
              <span className="inline-flex items-center space-x-1">
                <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                <span>Backend v1.0.0</span>
              </span>
              <span>Composio APM Assignment</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

