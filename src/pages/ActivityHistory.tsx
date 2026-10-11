import React, { useState } from 'react';
import { 
  History, 
  UploadCloud, 
  ShieldCheck, 
  Download, 
  AlertTriangle, 
  Clock, 
  CheckCircle2, 
  ExternalLink,
  Search
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { ActivityItem } from '../types';

export const ActivityHistory: React.FC = () => {
  const { activities, cases, openCaseDetails } = useApp();

  const [filterAction, setFilterAction] = useState<string>('All');
  const [filterSearch, setFilterSearch] = useState<string>('');

  const filteredActivities = activities.filter((act) => {
    const matchAction = filterAction === 'All' || act.action === filterAction;
    const matchSearch = filterSearch === '' || 
      act.caseTitle.toLowerCase().includes(filterSearch.toLowerCase()) ||
      act.details.toLowerCase().includes(filterSearch.toLowerCase()) ||
      act.action.toLowerCase().includes(filterSearch.toLowerCase());
    return matchAction && matchSearch;
  });

  const getActionIcon = (action: ActivityItem['action']) => {
    switch (action) {
      case 'Document Upload':
        return <UploadCloud className="w-4 h-4 text-[#8B7CFF]" />;
      case 'Analysis Completed':
        return <CheckCircle2 className="w-4 h-4 text-[#36C98F]" />;
      case 'Integrity Check':
        return <ShieldCheck className="w-4 h-4 text-[#8B7CFF]" />;
      case 'Report Exported':
        return <Download className="w-4 h-4 text-[#A5A7AD]" />;
      case 'Review Flagged':
        return <AlertTriangle className="w-4 h-4 text-[#F5B942]" />;
      default:
        return <Clock className="w-4 h-4 text-[#A5A7AD]" />;
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#2B2D33]">
        <div>
          <h2 className="text-xl lg:text-2xl font-sans font-bold text-[#F5F5F5] tracking-tight flex items-center gap-2">
            <span>Activity History & Audit Log</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-[#8B7CFF]/10 text-[#8B7CFF] border border-[#8B7CFF]/30 font-mono">
              {filteredActivities.length} Events Logged
            </span>
          </h2>
          <p className="text-xs text-[#A5A7AD] mt-1">
            Chronological audit trail of document ingestions, cryptographic hash checks, and verified exports.
          </p>
        </div>

        <div className="text-[11px] font-mono text-[#A5A7AD] bg-[#111318] px-3 py-1.5 rounded-lg border border-[#2B2D33]">
          Audit Standard • FIPS 180-4 Verified
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="p-4 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#A5A7AD]" />
          <input
            type="text"
            placeholder="Filter audit events..."
            value={filterSearch}
            onChange={(e) => setFilterSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-[#08090B] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] placeholder-[#A5A7AD]/60 focus:outline-none focus:border-[#8B7CFF]"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <select
            value={filterAction}
            onChange={(e) => setFilterAction(e.target.value)}
            className="w-full sm:w-auto px-3 py-1.5 bg-[#08090B] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF] cursor-pointer"
          >
            <option value="All">All Audit Actions</option>
            <option value="Document Upload">Document Uploads</option>
            <option value="Analysis Completed">Analysis Completions</option>
            <option value="Integrity Check">Integrity Checks</option>
            <option value="Report Exported">Report Exports</option>
            <option value="Review Flagged">Review Flags</option>
          </select>
        </div>
      </div>

      {/* Audit Log Timeline */}
      <div className="rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card p-6 space-y-6">
        {filteredActivities.length === 0 ? (
          <div className="py-12 text-center text-[#A5A7AD] text-xs">
            No activity events recorded matching the current filter.
          </div>
        ) : (
          <div className="space-y-6 relative before:absolute before:inset-0 before:left-3.5 before:w-0.5 before:bg-[#2B2D33]">
            {filteredActivities.map((act) => {
              const matchedCase = cases.find(c => c.id === act.caseId);

              return (
                <div key={act.id} className="relative flex items-start gap-4 pl-1 group">
                  <div className="relative z-10 w-7 h-7 rounded-full bg-[#08090B] border border-[#2B2D33] group-hover:border-[#8B7CFF]/60 flex items-center justify-center flex-shrink-0 transition-colors shadow-sm">
                    {getActionIcon(act.action)}
                  </div>

                  <div className="flex-1 p-4 rounded-xl bg-[#08090B] border border-[#2B2D33] group-hover:border-[#3D404A] transition-colors space-y-2">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-[#F5F5F5] font-sans">
                          {act.action}
                        </span>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#111318] text-[#8B7CFF] border border-[#2B2D33]">
                          {act.caseTitle}
                        </span>
                      </div>

                      <span className="text-[10px] font-mono text-[#A5A7AD] flex items-center gap-1">
                        <Clock className="w-3 h-3 text-[#A5A7AD]" />
                        {act.timestamp}
                      </span>
                    </div>

                    <p className="text-xs text-[#A5A7AD] leading-relaxed">
                      {act.details}
                    </p>

                    <div className="flex items-center justify-between pt-1 border-t border-[#2B2D33] text-[10px] text-[#A5A7AD] font-mono">
                      <span>Operator: {act.user}</span>
                      
                      {matchedCase && (
                        <button
                          type="button"
                          onClick={() => openCaseDetails(matchedCase)}
                          className="hover:text-[#8B7CFF] flex items-center gap-1 transition-colors"
                        >
                          <span>Open Case Record</span>
                          <ExternalLink className="w-3 h-3" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
