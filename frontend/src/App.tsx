import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from './components/layout/AppLayout';
import { DirectoryPage } from './pages/DirectoryPage';
import { GuideDetailPage } from './pages/GuideDetailPage';
import { ResearchPage } from './pages/ResearchPage';
import { OverviewPage } from './pages/OverviewPage';
import { ResearchRunsPage } from './pages/ResearchRunsPage';
import { SavedGuidesPage } from './pages/SavedGuidesPage';

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout>
        <Routes>
          <Route path="/" element={<DirectoryPage />} />
          <Route path="/overview" element={<OverviewPage />} />
          <Route path="/apps/:slug" element={<GuideDetailPage />} />
          <Route path="/guides/:id" element={<GuideDetailPage />} />
          <Route path="/generate" element={<ResearchPage />} />
          <Route path="/runs" element={<ResearchRunsPage />} />
          <Route path="/saved" element={<SavedGuidesPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppLayout>
    </BrowserRouter>
  );
}
