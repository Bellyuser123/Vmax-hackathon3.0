import React from 'react';
import { 
  LayoutDashboard, 
  FileSearch, 
  BookOpen, 
  Scale, 
  GitCompare, 
  ShieldCheck, 
  History, 
  Settings, 
  HelpCircle, 
  ChevronLeft, 
  ChevronRight,
  FileText,
  BookmarkCheck,
  Search,
  Zap,
  ExternalLink
} from 'lucide-react';
import { useApp, AppRoute } from '../../context/AppContext';

interface SidebarProps {
  collapsed: boolean;
  setCollapsed: (v: boolean) => void;
  mobileOpen: boolean;
  setMobileOpen: (v: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  collapsed,
  setCollapsed,
  mobileOpen,
  setMobileOpen,
}) => {
  const { currentRoute, setCurrentRoute, cases, activeCase } = useApp();

  const mainNav: { 
    route: AppRoute; 
    label: string; 
    icon: React.ElementType; 
    badge?: string | number; 
    isAccent?: boolean;
    section?: string;
  }[] = [
    { route: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, section: 'OVERVIEW' },
    { route: 'analyze', label: 'Analyze Document', icon: FileSearch, badge: 'AI', section: 'INTELLIGENCE' },
    { route: 'library', label: 'Case Library', icon: BookOpen, badge: cases.length },
    { route: 'similar', label: 'Similar Cases', icon: GitCompare, badge: activeCase ? activeCase.relatedCases.length : undefined },
    { route: 'provisions', label: 'Legal Provisions', icon: BookmarkCheck, badge: activeCase ? activeCase.legalProvisions.length : undefined },
    { route: 'search', label: 'Search Cases', icon: Search, section: 'DISCOVERY' },
    { route: 'vault', label: 'Evidence Vault', icon: ShieldCheck, badge: 'SHA-256', isAccent: true, section: 'VERIFICATION' },
    { route: 'history', label: 'Activity History', icon: History, section: 'AUDIT' },
    { route: 'settings', label: 'Settings', icon: Settings },
  ];

  const handleNavClick = (route: AppRoute) => {
    setCurrentRoute(route);
    setMobileOpen(false);
  };

  // Group items by sections
  let currentSection = '';

  return (
    <>
      {/* Mobile backdrop */}
      {mobileOpen && (
        <div 
          className="fixed inset-0 bg-black/70 z-40 lg:hidden backdrop-blur-md transition-opacity duration-300"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar container */}
      <aside 
        className={`fixed top-0 bottom-0 left-0 z-50 flex flex-col glass-sidebar border-r border-[#2B2D33]/60 transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)]
          ${collapsed ? 'w-[72px]' : 'w-[260px]'}
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        {/* Brand header */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-[#2B2D33]/60">
          <div 
            className="flex items-center gap-3 cursor-pointer overflow-hidden select-none group"
            onClick={() => handleNavClick('dashboard')}
          >
            {/* Logo icon with animated glow */}
            <div className="relative flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-[#191B20] to-[#111318] border border-[#2B2D33] text-[#8B7CFF] flex-shrink-0 group-hover:border-[#8B7CFF]/40 transition-all duration-300">
              <svg 
                className="w-5 h-5 transition-transform duration-300 group-hover:scale-110" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
                <circle cx="17" cy="18" r="3" stroke="#8B7CFF" fill="#111318" />
                <line x1="19" y1="20" x2="22" y2="23" stroke="#8B7CFF" />
              </svg>
              {/* Online indicator */}
              <div className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-[#36C98F] ring-2 ring-[#111318]">
                <div className="absolute inset-0 rounded-full bg-[#36C98F] animate-ping opacity-40" />
              </div>
            </div>

            {!collapsed && (
              <div className="flex flex-col min-w-0 animate-fade-in">
                <div className="flex items-center gap-1.5">
                  <span className="font-sans font-bold text-[15px] tracking-tight text-[#F5F5F5] leading-tight">
                    Nyaya<span className="text-[#8B7CFF]">Lens</span>
                  </span>
                  <span className="badge-violet text-[8px] py-0 px-1.5 tracking-wider">PRO</span>
                </div>
                <span className="text-[9px] text-[#6E7079] tracking-[0.12em] uppercase font-medium truncate mt-0.5">
                  Court Intelligence
                </span>
              </div>
            )}
          </div>

          {/* Desktop collapse toggle */}
          <button 
            type="button"
            onClick={() => setCollapsed(!collapsed)}
            className="hidden lg:flex items-center justify-center w-7 h-7 rounded-lg text-[#6E7079] hover:text-[#F5F5F5] hover:bg-[#191B20] border border-transparent hover:border-[#2B2D33] transition-all duration-200"
            title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            {collapsed ? <ChevronRight className="w-3.5 h-3.5" /> : <ChevronLeft className="w-3.5 h-3.5" />}
          </button>
        </div>

        {/* Navigation list */}
        <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
          {mainNav.map((item, idx) => {
            const Icon = item.icon;
            const isActive = currentRoute === item.route;
            const showSection = !collapsed && item.section && item.section !== currentSection;
            if (item.section) currentSection = item.section;

            return (
              <React.Fragment key={item.route}>
                {/* Section dividers */}
                {showSection && (
                  <div className={`${idx > 0 ? 'pt-4 mt-2 border-t border-[#2B2D33]/40' : ''} pb-1.5 px-3`}>
                    <span className="text-[9px] tracking-[0.15em] uppercase text-[#525562] font-semibold">
                      {item.section}
                    </span>
                  </div>
                )}

                <button
                  type="button"
                  onClick={() => handleNavClick(item.route)}
                  title={collapsed ? item.label : undefined}
                  className={`nav-item w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-[13px] transition-all duration-200 group relative
                    ${isActive 
                      ? 'nav-item-active text-[#F5F5F5]' 
                      : 'text-[#6E7079] hover:text-[#A5A7AD] hover:bg-[#191B20]/50'
                    }
                    ${collapsed ? 'justify-center px-2' : 'justify-start'}
                  `}
                >
                  <div className={`relative flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 flex-shrink-0
                    ${isActive 
                      ? 'bg-[#8B7CFF]/10 text-[#8B7CFF]' 
                      : 'text-[#6E7079] group-hover:text-[#A5A7AD]'
                    }
                  `}>
                    <Icon className="w-[18px] h-[18px]" />
                    {isActive && (
                      <div className="absolute inset-0 rounded-lg bg-[#8B7CFF]/5 animate-pulse-glow" style={{animationDuration: '4s'}} />
                    )}
                  </div>
                  
                  {!collapsed && (
                    <span className="truncate text-left flex-1">
                      {item.label}
                    </span>
                  )}

                  {!collapsed && item.badge !== undefined && (
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full flex-shrink-0 transition-all
                      ${item.isAccent 
                        ? 'badge-violet' 
                        : isActive 
                          ? 'bg-[#8B7CFF]/10 text-[#9E91FF] border border-[#8B7CFF]/20' 
                          : 'bg-[#191B20] text-[#6E7079] border border-[#2B2D33]/60'
                      }
                    `}>
                      {item.badge}
                    </span>
                  )}
                </button>
              </React.Fragment>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-3 border-t border-[#2B2D33]/40 space-y-2">
          {/* Quick Action */}
          {!collapsed && (
            <button
              type="button"
              onClick={() => handleNavClick('analyze')}
              className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold btn-primary"
            >
              <Zap className="w-3.5 h-3.5" />
              Quick Analyze
            </button>
          )}

          {/* Help */}
          <button
            type="button"
            onClick={() => handleNavClick('settings')}
            className={`w-full flex items-center gap-2.5 px-3 py-1.5 text-xs text-[#525562] hover:text-[#A5A7AD] rounded-lg hover:bg-[#191B20]/50 transition-colors ${collapsed ? 'justify-center' : ''}`}
          >
            <HelpCircle className="w-3.5 h-3.5" />
            {!collapsed && <span>Help & Legal Docs</span>}
          </button>

          {/* User Profile */}
          <div className={`flex items-center gap-2.5 p-2.5 rounded-xl bg-gradient-to-r from-[#191B20] to-[#111318] border border-[#2B2D33]/60 hover:border-[#3D404A] transition-all duration-200 cursor-pointer group ${collapsed ? 'justify-center p-2' : ''}`}>
            <div className="relative flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#8B7CFF]/20 to-[#5F4EE0]/10 border border-[#8B7CFF]/30 flex items-center justify-center text-[11px] font-bold text-[#8B7CFF] group-hover:border-[#8B7CFF]/50 transition-colors">
                RS
              </div>
              <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-[#36C98F] ring-2 ring-[#191B20]" />
            </div>

            {!collapsed && (
              <div className="flex flex-col min-w-0 flex-1">
                <span className="text-[12px] font-semibold text-[#F5F5F5] truncate">
                  Adv. Rajesh Sharma
                </span>
                <span className="text-[10px] text-[#525562] truncate">
                  Delhi High Court Bar
                </span>
              </div>
            )}
          </div>
        </div>
      </aside>
    </>
  );
};
