import React, { useState } from 'react';
import { AppProvider, useApp } from './context/AppContext';
import { Sidebar } from './components/layout/Sidebar';
import { Navbar } from './components/layout/Navbar';
import { Toast } from './components/common/Toast';
import { Dashboard } from './pages/Dashboard';
import { AnalyzeDocument } from './pages/AnalyzeDocument';
import { CaseLibrary } from './pages/CaseLibrary';
import { SimilarCases } from './pages/SimilarCases';
import { LegalProvisionsPage } from './pages/LegalProvisionsPage';
import { SearchCases } from './pages/SearchCases';
import { EvidenceVault } from './pages/EvidenceVault';
import { DocumentViewer } from './pages/DocumentViewer';
import { ActivityHistory } from './pages/ActivityHistory';
import { SettingsPage } from './pages/SettingsPage';
import { Scale, ShieldCheck, Lock } from 'lucide-react';

const AppContent: React.FC = () => {
  const { currentRoute } = useApp();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const renderActiveRoute = () => {
    switch (currentRoute) {
      case 'dashboard':
        return <Dashboard />;
      case 'analyze':
        return <AnalyzeDocument />;
      case 'library':
        return <CaseLibrary />;
      case 'similar':
        return <SimilarCases />;
      case 'provisions':
        return <LegalProvisionsPage />;
      case 'search':
        return <SearchCases />;
      case 'vault':
        return <EvidenceVault />;
      case 'viewer':
        return <DocumentViewer />;
      case 'history':
        return <ActivityHistory />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-[#08090B] text-[#F5F5F5] flex flex-col selection:bg-[#8B7CFF]/30 selection:text-white">
      {/* Persistent Left Sidebar */}
      <Sidebar
        collapsed={collapsed}
        setCollapsed={setCollapsed}
        mobileOpen={mobileOpen}
        setMobileOpen={setMobileOpen}
      />

      {/* Main Container */}
      <div 
        className={`flex-1 flex flex-col transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] min-w-0
          ${collapsed ? 'lg:pl-[72px]' : 'lg:pl-[260px]'}
        `}
      >
        {/* Top Navbar */}
        <Navbar 
          setMobileOpen={setMobileOpen} 
          collapsed={collapsed} 
        />

        {/* Page Content */}
        <main className="flex-1 p-4 lg:p-8 max-w-[1400px] w-full mx-auto">
          {renderActiveRoute()}
        </main>

        {/* Premium Legal Footer */}
        <footer className="mt-auto border-t border-[#2B2D33]/40 py-5 px-4 lg:px-8 bg-gradient-to-r from-[#08090B] via-[#0A0C10] to-[#08090B] text-xs text-[#525562]">
          <div className="max-w-[1400px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <Scale className="w-3.5 h-3.5 text-[#8B7CFF]" />
                <span className="font-sans font-bold text-[#F5F5F5] text-sm tracking-tight">
                  Nyaya<span className="text-[#8B7CFF]">Lens</span>
                </span>
              </div>
              <div className="hidden md:block w-px h-4 bg-[#2B2D33]" />
              <span className="hidden md:inline text-[11px] text-[#525562]">
                AI-Powered Indian Court Document Intelligence
              </span>
            </div>

            <div className="flex items-center gap-4 text-[10px] font-mono text-[#525562]">
              <div className="flex items-center gap-1.5">
                <ShieldCheck className="w-3 h-3 text-[#36C98F]" />
                <span>SHA-256 Validated</span>
              </div>
              <span className="text-[#2B2D33]">•</span>
              <div className="flex items-center gap-1.5">
                <Lock className="w-3 h-3 text-[#8B7CFF]" />
                <span>End-to-End Secure</span>
              </div>
              <span className="text-[#2B2D33]">•</span>
              <span>Indian Legal Tech Workspace</span>
            </div>
          </div>
        </footer>
      </div>

      {/* Interactive Toast Notifications */}
      <Toast />
    </div>
  );
};

export function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
