import React, { createContext, useContext, useState, useEffect } from 'react';
import { CaseRecord, ActivityItem, NotificationItem, SummaryLength } from '../types';
import { SAMPLE_CASES, SAMPLE_ACTIVITIES, INITIAL_NOTIFICATIONS } from '../data/sampleCases';

export type AppRoute = 
  | 'dashboard'
  | 'analyze'
  | 'library'
  | 'similar'
  | 'provisions'
  | 'search'
  | 'vault'
  | 'viewer'
  | 'history'
  | 'settings';

interface AppContextType {
  currentRoute: AppRoute;
  setCurrentRoute: (route: AppRoute) => void;
  cases: CaseRecord[];
  activeCase: CaseRecord | null;
  setActiveCase: (c: CaseRecord | null) => void;
  activeEvidenceId: string | null;
  setActiveEvidenceId: (id: string | null) => void;
  activeViewerPage: number;
  setActiveViewerPage: (page: number) => void;
  activeProvisionRef: string | null;
  setActiveProvisionRef: (ref: string | null) => void;
  summaryLength: SummaryLength;
  setSummaryLength: (len: SummaryLength) => void;
  activities: ActivityItem[];
  notifications: NotificationItem[];
  markNotificationRead: (id: string) => void;
  addCase: (newCase: CaseRecord) => void;
  deleteCase: (caseId: string) => void;
  searchFilter: string;
  setSearchFilter: (query: string) => void;
  toast: { message: string; type: 'success' | 'info' | 'warning' } | null;
  showToast: (message: string, type?: 'success' | 'info' | 'warning') => void;
  openCaseInViewer: (caseRecord: CaseRecord, evidenceId?: string, pageNum?: number, provisionRef?: string) => void;
  openCaseDetails: (caseRecord: CaseRecord) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentRoute, setCurrentRoute] = useState<AppRoute>('dashboard');
  
  // Persistent store with graceful fallback
  const [cases, setCases] = useState<CaseRecord[]>(() => {
    try {
      const saved = localStorage.getItem('nyayalens_cases');
      return saved ? JSON.parse(saved) : SAMPLE_CASES;
    } catch {
      return SAMPLE_CASES;
    }
  });

  const [activeCase, setActiveCase] = useState<CaseRecord | null>(SAMPLE_CASES[0]);
  const [activeEvidenceId, setActiveEvidenceId] = useState<string | null>(null);
  const [activeViewerPage, setActiveViewerPage] = useState<number>(1);
  const [activeProvisionRef, setActiveProvisionRef] = useState<string | null>(null);
  const [summaryLength, setSummaryLength] = useState<SummaryLength>('standard');
  const [activities, setActivities] = useState<ActivityItem[]>(SAMPLE_ACTIVITIES);
  const [notifications, setNotifications] = useState<NotificationItem[]>(INITIAL_NOTIFICATIONS);
  const [searchFilter, setSearchFilter] = useState<string>('');
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'info' | 'warning' } | null>(null);

  useEffect(() => {
    try {
      localStorage.setItem('nyayalens_cases', JSON.stringify(cases));
    } catch (e) {
      console.error('Failed to save to localStorage', e);
    }
  }, [cases]);

  const showToast = (message: string, type: 'success' | 'info' | 'warning' = 'success') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(prev => (prev?.message === message ? null : prev));
    }, 4000);
  };

  const markNotificationRead = (id: string) => {
    setNotifications(prev =>
      prev.map(n => (n.id === id ? { ...n, read: true } : n))
    );
  };

  const addCase = (newCase: CaseRecord) => {
    setCases(prev => [newCase, ...prev]);
    setActiveCase(newCase);
    
    // Add activity record
    const newActivity: ActivityItem = {
      id: 'act-' + Date.now(),
      timestamp: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) + ' IST',
      action: 'Analysis Completed',
      caseTitle: newCase.title,
      caseId: newCase.id,
      status: 'success',
      details: `${newCase.extractedClaimsCount} claims verified with SHA-256 fingerprint ${newCase.sha256Hash.substring(0, 10)}...`,
      user: 'Adv. R. Sharma (Senior Registrar)'
    };
    setActivities(prev => [newActivity, ...prev]);
    showToast(`Judgment "${newCase.title.slice(0, 32)}..." analyzed and added to library.`);
  };

  const deleteCase = (caseId: string) => {
    const targetCase = cases.find(c => c.id === caseId);
    setCases(prev => prev.filter(c => c.id !== caseId));
    if (activeCase?.id === caseId) {
      setActiveCase(cases.find(c => c.id !== caseId) || null);
    }
    showToast(`Case record "${targetCase?.title.slice(0, 24) || 'item'}" removed.`, 'info');
  };

  const openCaseInViewer = (
    caseRecord: CaseRecord, 
    evidenceId?: string, 
    pageNum?: number, 
    provisionRef?: string
  ) => {
    setActiveCase(caseRecord);
    if (evidenceId) setActiveEvidenceId(evidenceId);
    if (pageNum) setActiveViewerPage(pageNum);
    if (provisionRef) setActiveProvisionRef(provisionRef);
    setCurrentRoute('viewer');
  };

  const openCaseDetails = (caseRecord: CaseRecord) => {
    setActiveCase(caseRecord);
    setCurrentRoute('analyze');
  };

  return (
    <AppContext.Provider
      value={{
        currentRoute,
        setCurrentRoute,
        cases,
        activeCase,
        setActiveCase,
        activeEvidenceId,
        setActiveEvidenceId,
        activeViewerPage,
        setActiveViewerPage,
        activeProvisionRef,
        setActiveProvisionRef,
        summaryLength,
        setSummaryLength,
        activities,
        notifications,
        markNotificationRead,
        addCase,
        deleteCase,
        searchFilter,
        setSearchFilter,
        toast,
        showToast,
        openCaseInViewer,
        openCaseDetails
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
