import React, { useState } from 'react';
import { 
  User, 
  Sliders, 
  Database, 
  HelpCircle, 
  Save, 
  Trash2, 
  CheckCircle2, 
  Scale, 
  Lock 
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { SAMPLE_CASES } from '../data/sampleCases';

export const SettingsPage: React.FC = () => {
  const { showToast } = useApp();

  const [profileName, setProfileName] = useState('Adv. Rajesh Sharma');
  const [barNumber, setBarNumber] = useState('D/1482/2018 (Bar Council of Delhi)');
  const [userRole, setUserRole] = useState('Senior Legal Researcher / High Court Advocate');
  const [primaryCourt, setPrimaryCourt] = useState('High Court of Delhi / Supreme Court of India');

  const [ocrPrecision, setOcrPrecision] = useState<'deep' | 'balanced'>('deep');
  const [citationFormat, setCitationFormat] = useState('SCC (Supreme Court Cases)');
  const [strictGrounding, setStrictGrounding] = useState(true);

  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    showToast('User profile settings saved successfully.');
  };

  const resetDemoData = () => {
    try {
      localStorage.setItem('nyayalens_cases', JSON.stringify(SAMPLE_CASES));
      showToast('Restored original sample court judgments in demonstration vault.', 'info');
      setTimeout(() => window.location.reload(), 1000);
    } catch {
      showToast('Reset failed', 'warning');
    }
  };

  return (
    <div className="space-y-8 max-w-4xl animate-in fade-in duration-200">
      {/* Header */}
      <div className="pb-4 border-b border-[#2B2D33]">
        <h2 className="text-xl lg:text-2xl font-sans font-bold text-[#F5F5F5] tracking-tight flex items-center gap-2">
          <span>Settings & Platform Preferences</span>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-[#8B7CFF]/10 text-[#8B7CFF] border border-[#8B7CFF]/30 font-mono">
            Configuration
          </span>
        </h2>
        <p className="text-xs text-[#A5A7AD] mt-1">
          Customize your legal workstation, citation formats, and local demonstration vault.
        </p>
      </div>

      {/* 1. User Profile Section */}
      <div className="p-6 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card space-y-4">
        <div className="flex items-center gap-3 pb-3 border-b border-[#2B2D33]">
          <div className="p-2 rounded-xl bg-[#191B20] text-[#8B7CFF] border border-[#2B2D33]">
            <User className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-[#F5F5F5]">Professional Profile & Bar Credentials</h3>
            <p className="text-xs text-[#A5A7AD]">Information attached to exported legal intelligence briefs</p>
          </div>
        </div>

        <form onSubmit={handleSaveProfile} className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block text-[#A5A7AD] mb-1 font-medium">Full Name & Title</label>
            <input
              type="text"
              value={profileName}
              onChange={(e) => setProfileName(e.target.value)}
              className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33] rounded-xl text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]"
            />
          </div>

          <div>
            <label className="block text-[#A5A7AD] mb-1 font-medium">Bar Enrolment Number</label>
            <input
              type="text"
              value={barNumber}
              onChange={(e) => setBarNumber(e.target.value)}
              className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33] rounded-xl text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]"
            />
          </div>

          <div>
            <label className="block text-[#A5A7AD] mb-1 font-medium">Professional Role</label>
            <input
              type="text"
              value={userRole}
              onChange={(e) => setUserRole(e.target.value)}
              className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33] rounded-xl text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]"
            />
          </div>

          <div>
            <label className="block text-[#A5A7AD] mb-1 font-medium">Primary Court of Practice</label>
            <input
              type="text"
              value={primaryCourt}
              onChange={(e) => setPrimaryCourt(e.target.value)}
              className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33] rounded-xl text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]"
            />
          </div>

          <div className="col-span-full flex justify-end pt-2">
            <button
              type="submit"
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-[#8B7CFF] hover:bg-[#7564F5] text-[#08090B] transition-colors flex items-center gap-1.5"
            >
              <Save className="w-3.5 h-3.5" />
              <span>Save Profile Changes</span>
            </button>
          </div>
        </form>
      </div>

      {/* 2. Processing Preferences */}
      <div className="p-6 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card space-y-4">
        <div className="flex items-center gap-3 pb-3 border-b border-[#2B2D33]">
          <div className="p-2 rounded-xl bg-[#191B20] text-[#36C98F] border border-[#2B2D33]">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-[#F5F5F5]">Document Processing & Citation Engine</h3>
            <p className="text-xs text-[#A5A7AD]">Extraction settings for Indian jurisprudence analysis</p>
          </div>
        </div>

        <div className="space-y-3 text-xs">
          <div className="flex items-center justify-between p-3.5 rounded-xl bg-[#08090B] border border-[#2B2D33]">
            <div>
              <p className="font-semibold text-[#F5F5F5]">Strict Evidence Grounding</p>
              <p className="text-[#A5A7AD] text-[11px]">Enforce that every extracted legal proposition must map to an exact source quote.</p>
            </div>
            <input
              type="checkbox"
              checked={strictGrounding}
              onChange={(e) => {
                setStrictGrounding(e.target.checked);
                showToast(`Strict grounding mode: ${e.target.checked ? 'Enabled' : 'Disabled'}`);
              }}
              className="w-4 h-4 accent-[#8B7CFF] cursor-pointer rounded"
            />
          </div>

          <div className="flex items-center justify-between p-3.5 rounded-xl bg-[#08090B] border border-[#2B2D33]">
            <div>
              <p className="font-semibold text-[#F5F5F5]">Preferred Citation Format</p>
              <p className="text-[#A5A7AD] text-[11px]">Primary reporter format used when generating judicial headnotes.</p>
            </div>
            <select
              value={citationFormat}
              onChange={(e) => {
                setCitationFormat(e.target.value);
                showToast(`Citation format changed to ${e.target.value}`);
              }}
              className="px-3 py-1.5 bg-[#191B20] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]"
            >
              <option value="SCC (Supreme Court Cases)">SCC (Supreme Court Cases)</option>
              <option value="AIR (All India Reporter)">AIR (All India Reporter)</option>
              <option value="SCR (Supreme Court Reports)">SCR (Supreme Court Reports)</option>
            </select>
          </div>
        </div>
      </div>

      {/* 3. Storage & Demonstration State */}
      <div className="p-6 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card space-y-4">
        <div className="flex items-center gap-3 pb-3 border-b border-[#2B2D33]">
          <div className="p-2 rounded-xl bg-[#191B20] text-[#F5B942] border border-[#2B2D33]">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-[#F5F5F5]">Demonstration Vault Reset</h3>
            <p className="text-xs text-[#A5A7AD]">Manage local cache and sample Indian judgments</p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-[#08090B] border border-[#2B2D33] text-xs">
          <div>
            <p className="font-semibold text-[#F5F5F5]">Restore Sample Benchmark Database</p>
            <p className="text-[#A5A7AD] text-[11px] mt-0.5">
              Reset uploaded test files and reload landmark Supreme Court datasets (Puttaswamy, Shreya Singhal, Lalita Kumari).
            </p>
          </div>

          <button
            type="button"
            onClick={resetDemoData}
            className="px-3.5 py-2 rounded-xl text-xs font-medium bg-[#191B20] hover:bg-[#22252C] text-[#8B7CFF] border border-[#2B2D33] transition-colors whitespace-nowrap"
          >
            Reset Sample Data
          </button>
        </div>
      </div>
    </div>
  );
};
