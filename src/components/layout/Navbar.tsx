import React, { useState, useRef, useEffect } from 'react';
import { 
  Search, 
  Bell, 
  Menu, 
  ChevronRight, 
  FilePlus, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldCheck, 
  LogOut, 
  User, 
  Sliders,
  Command,
  Sparkles
} from 'lucide-react';
import { useApp } from '../../context/AppContext';

interface NavbarProps {
  setMobileOpen: (v: boolean) => void;
  collapsed: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ setMobileOpen, collapsed }) => {
  const { 
    currentRoute, 
    setCurrentRoute, 
    notifications, 
    markNotificationRead, 
    searchFilter, 
    setSearchFilter,
    showToast 
  } = useApp();

  const [showNotifDropdown, setShowNotifDropdown] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [searchFocused, setSearchFocused] = useState(false);
  const notifRef = useRef<HTMLDivElement>(null);
  const userRef = useRef<HTMLDivElement>(null);

  const unreadCount = notifications.filter(n => !n.read).length;

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) {
        setShowNotifDropdown(false);
      }
      if (userRef.current && !userRef.current.contains(e.target as Node)) {
        setShowUserDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const getBreadcrumbTitle = () => {
    switch (currentRoute) {
      case 'dashboard': return 'Dashboard';
      case 'analyze': return 'Analyze Document';
      case 'library': return 'Case Library';
      case 'similar': return 'Similar Cases';
      case 'provisions': return 'Legal Provisions';
      case 'search': return 'Search Cases';
      case 'vault': return 'Evidence Vault';
      case 'viewer': return 'Document Viewer';
      case 'history': return 'Activity History';
      case 'settings': return 'Settings';
      default: return 'Overview';
    }
  };

  const getRouteIcon = () => {
    switch (currentRoute) {
      case 'vault': return '🛡️';
      case 'analyze': return '🔍';
      case 'library': return '📚';
      case 'search': return '🔎';
      default: return null;
    }
  };

  const handleGlobalSearchKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      setCurrentRoute('search');
    }
  };

  return (
    <header className="sticky top-0 z-30 h-[60px] glass border-b border-[#2B2D33]/50 px-4 lg:px-8 flex items-center justify-between gap-4">
      {/* Left: Mobile hamburger & breadcrumbs */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={() => setMobileOpen(true)}
          className="lg:hidden p-2 rounded-lg text-[#6E7079] hover:text-[#F5F5F5] hover:bg-[#191B20] transition-colors"
          aria-label="Open Navigation"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2 text-xs text-[#525562]">
          <span 
            className="cursor-pointer hover:text-[#8B7CFF] transition-colors font-medium hidden sm:inline"
            onClick={() => setCurrentRoute('dashboard')}
          >
            NyayaLens
          </span>
          <ChevronRight className="w-3 h-3 hidden sm:inline text-[#2B2D33]" />
          <h1 className="text-sm font-semibold text-[#F5F5F5] font-sans tracking-tight flex items-center gap-1.5">
            {getRouteIcon() && <span className="text-sm">{getRouteIcon()}</span>}
            {getBreadcrumbTitle()}
          </h1>
        </div>
      </div>

      {/* Center: Global Search — Premium */}
      <div className="flex-1 max-w-lg hidden md:block">
        <div className={`relative transition-all duration-300 ${searchFocused ? 'scale-[1.02]' : ''}`}>
          <Search className={`absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 transition-colors duration-200 ${searchFocused ? 'text-[#8B7CFF]' : 'text-[#525562]'}`} />
          <input
            type="text"
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            onKeyDown={handleGlobalSearchKeyDown}
            onFocus={() => setSearchFocused(true)}
            onBlur={() => setSearchFocused(false)}
            placeholder="Search judgments, Acts, sections, or citations..."
            className={`w-full pl-10 pr-20 py-2 bg-[#111318]/80 border rounded-xl text-[13px] text-[#F5F5F5] placeholder-[#525562] focus:outline-none transition-all duration-300
              ${searchFocused 
                ? 'border-[#8B7CFF]/50 ring-1 ring-[#8B7CFF]/20 bg-[#111318] shadow-[0_0_20px_-5px_rgba(139,124,255,0.1)]' 
                : 'border-[#2B2D33]/60 hover:border-[#3D404A]'
              }
            `}
          />
          <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1.5">
            <kbd className="px-1.5 py-0.5 text-[9px] font-mono bg-[#191B20] text-[#525562] rounded border border-[#2B2D33]/60 flex items-center gap-0.5">
              <Command className="w-2.5 h-2.5" /> K
            </kbd>
          </div>
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        {/* Quick Analyze Button — Premium gradient */}
        <button
          type="button"
          onClick={() => setCurrentRoute('analyze')}
          className="hidden sm:inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold btn-primary"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Analyze</span>
        </button>

        {/* Notifications */}
        <div className="relative" ref={notifRef}>
          <button
            type="button"
            onClick={() => setShowNotifDropdown(!showNotifDropdown)}
            className={`relative p-2 rounded-xl transition-all duration-200
              ${showNotifDropdown 
                ? 'text-[#F5F5F5] bg-[#191B20] border border-[#2B2D33]' 
                : 'text-[#6E7079] hover:text-[#F5F5F5] hover:bg-[#191B20]/50 border border-transparent'
              }
            `}
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#8B7CFF] opacity-60"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#8B7CFF] text-[6px] text-white font-bold items-center justify-center">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              </span>
            )}
          </button>

          {/* Notifications Dropdown — Glass */}
          {showNotifDropdown && (
            <div className="absolute right-0 mt-2 w-[340px] glass rounded-2xl shadow-modal z-50 p-4 space-y-3 animate-scale-in">
              <div className="flex items-center justify-between pb-3 border-b border-[#2B2D33]/60">
                <div className="flex items-center gap-2">
                  <Bell className="w-4 h-4 text-[#8B7CFF]" />
                  <span className="text-sm font-semibold text-[#F5F5F5]">Notifications</span>
                </div>
                {unreadCount > 0 && (
                  <span className="badge-violet">{unreadCount} New</span>
                )}
              </div>

              <div className="space-y-2 max-h-72 overflow-y-auto">
                {notifications.map((n) => (
                  <div
                    key={n.id}
                    onClick={() => markNotificationRead(n.id)}
                    className={`p-3 rounded-xl cursor-pointer transition-all duration-200 text-left flex gap-3 group ${
                      n.read 
                        ? 'bg-transparent hover:bg-[#191B20]/30 text-[#6E7079]' 
                        : 'bg-[#191B20]/60 border border-[#8B7CFF]/20 text-[#F5F5F5] hover:border-[#8B7CFF]/40'
                    }`}
                  >
                    <div className={`flex-shrink-0 mt-0.5 w-8 h-8 rounded-lg flex items-center justify-center ${
                      n.type === 'verification' ? 'bg-[#36C98F]/10 text-[#36C98F]' :
                      n.type === 'analysis' ? 'bg-[#8B7CFF]/10 text-[#8B7CFF]' :
                      'bg-[#F5B942]/10 text-[#F5B942]'
                    }`}>
                      {n.type === 'verification' && <ShieldCheck className="w-4 h-4" />}
                      {n.type === 'analysis' && <CheckCircle2 className="w-4 h-4" />}
                      {n.type === 'system' && <AlertTriangle className="w-4 h-4" />}
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-xs font-medium leading-tight">{n.title}</p>
                      <p className="text-[11px] text-[#6E7079] mt-1 leading-relaxed">{n.message}</p>
                      <span className="text-[9px] text-[#525562] mt-1.5 block font-mono">{n.timestamp}</span>
                    </div>
                    {!n.read && (
                      <div className="w-1.5 h-1.5 rounded-full bg-[#8B7CFF] flex-shrink-0 mt-2" />
                    )}
                  </div>
                ))}
              </div>

              <div className="pt-3 border-t border-[#2B2D33]/60 flex items-center justify-between">
                <button
                  type="button"
                  onClick={() => {
                    notifications.forEach(n => markNotificationRead(n.id));
                    setShowNotifDropdown(false);
                    showToast('All notifications marked as read', 'info');
                  }}
                  className="text-[11px] text-[#8B7CFF] hover:text-[#9E91FF] font-medium transition-colors"
                >
                  Mark all as read
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setCurrentRoute('history');
                    setShowNotifDropdown(false);
                  }}
                  className="text-[11px] text-[#525562] hover:text-[#A5A7AD] font-medium transition-colors"
                >
                  View History →
                </button>
              </div>
            </div>
          )}
        </div>

        {/* User Avatar Menu */}
        <div className="relative" ref={userRef}>
          <button
            type="button"
            onClick={() => setShowUserDropdown(!showUserDropdown)}
            className={`flex items-center gap-2 p-1 rounded-xl transition-all duration-200
              ${showUserDropdown ? 'bg-[#191B20] ring-1 ring-[#2B2D33]' : 'hover:bg-[#191B20]/50'}
            `}
          >
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#8B7CFF]/20 to-[#5F4EE0]/10 border border-[#8B7CFF]/30 flex items-center justify-center text-[11px] font-bold text-[#8B7CFF]">
              RS
            </div>
          </button>

          {showUserDropdown && (
            <div className="absolute right-0 mt-2 w-60 glass rounded-2xl shadow-modal z-50 p-2 space-y-1 animate-scale-in">
              <div className="px-3 py-3 border-b border-[#2B2D33]/60">
                <p className="text-sm font-semibold text-[#F5F5F5]">Adv. Rajesh Sharma</p>
                <p className="text-[11px] text-[#6E7079] mt-0.5">rajesh.sharma@delhibar.in</p>
                <span className="inline-block mt-2 badge-emerald">
                  Senior Advocate • Delhi HC
                </span>
              </div>

              <button
                type="button"
                onClick={() => {
                  setCurrentRoute('settings');
                  setShowUserDropdown(false);
                }}
                className="w-full flex items-center gap-3 px-3 py-2 text-xs text-[#A5A7AD] hover:text-[#F5F5F5] hover:bg-[#191B20]/60 rounded-xl text-left transition-colors"
              >
                <User className="w-4 h-4" />
                Profile & Bar Credentials
              </button>

              <button
                type="button"
                onClick={() => {
                  setCurrentRoute('vault');
                  setShowUserDropdown(false);
                }}
                className="w-full flex items-center gap-3 px-3 py-2 text-xs text-[#A5A7AD] hover:text-[#F5F5F5] hover:bg-[#191B20]/60 rounded-xl text-left transition-colors"
              >
                <ShieldCheck className="w-4 h-4" />
                Evidence Vault
              </button>

              <div className="border-t border-[#2B2D33]/40 mt-1 pt-1">
                <button
                  type="button"
                  onClick={() => {
                    showToast('Signed out of session. Session preserved locally.', 'info');
                    setShowUserDropdown(false);
                  }}
                  className="w-full flex items-center gap-3 px-3 py-2 text-xs text-[#F87171] hover:bg-[#F87171]/10 rounded-xl text-left transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  Sign Out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
