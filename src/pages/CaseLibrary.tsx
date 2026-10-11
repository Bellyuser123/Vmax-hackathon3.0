import React, { useState, useMemo } from 'react';
import { 
  LayoutGrid, 
  List, 
  Search, 
  Trash2, 
  Eye, 
  ExternalLink, 
  Scale, 
  CheckCircle2, 
  AlertCircle, 
  Plus, 
  ShieldCheck
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { CaseRecord } from '../types';

export const CaseLibrary: React.FC = () => {
  const { cases, deleteCase, openCaseDetails, openCaseInViewer, setCurrentRoute } = useApp();

  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [courtFilter, setCourtFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');
  const [sortBy, setSortBy] = useState<'uploadDate' | 'judgmentDate' | 'title'>('uploadDate');
  
  // Delete dialog state
  const [caseToDelete, setCaseToDelete] = useState<CaseRecord | null>(null);

  const filteredCases = useMemo(() => {
    return cases.filter(c => {
      const q = searchQuery.toLowerCase();
      const matchSearch = 
        c.title.toLowerCase().includes(q) ||
        c.caseNumber.toLowerCase().includes(q) ||
        c.court.toLowerCase().includes(q) ||
        c.legalProvisions.some(p => p.act.toLowerCase().includes(q) || p.sectionOrArticle.toLowerCase().includes(q)) ||
        c.parties.petitioner.some(p => p.toLowerCase().includes(q)) ||
        c.parties.respondent.some(p => p.toLowerCase().includes(q));

      const matchCat = categoryFilter === 'All' || c.category === categoryFilter;
      const matchCourt = courtFilter === 'All' || c.court.includes(courtFilter);
      const matchStatus = statusFilter === 'All' || c.status === statusFilter;

      return matchSearch && matchCat && matchCourt && matchStatus;
    }).sort((a, b) => {
      if (sortBy === 'title') return a.title.localeCompare(b.title);
      if (sortBy === 'judgmentDate') return b.judgmentDate.localeCompare(a.judgmentDate);
      return b.uploadDate.localeCompare(a.uploadDate);
    });
  }, [cases, searchQuery, categoryFilter, courtFilter, statusFilter, sortBy]);

  const confirmDelete = () => {
    if (caseToDelete) {
      deleteCase(caseToDelete.id);
      setCaseToDelete(null);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#2B2D33]">
        <div>
          <h2 className="text-xl lg:text-2xl font-sans font-bold text-[#F5F5F5] tracking-tight flex items-center gap-2">
            <span>Court Case Library</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-[#8B7CFF]/10 text-[#8B7CFF] border border-[#8B7CFF]/30 font-mono">
              {filteredCases.length} Judgments
            </span>
          </h2>
          <p className="text-xs text-[#A5A7AD] mt-1">
            Searchable repository of analyzed Indian court records with persistent local vault storage.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          {/* View toggle */}
          <div className="flex bg-[#111318] p-1 rounded-xl border border-[#2B2D33]">
            <button
              type="button"
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg text-xs transition-colors ${
                viewMode === 'grid' ? 'bg-[#191B20] text-[#8B7CFF] shadow-sm' : 'text-[#A5A7AD] hover:text-[#F5F5F5]'
              }`}
              title="Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded-lg text-xs transition-colors ${
                viewMode === 'table' ? 'bg-[#191B20] text-[#8B7CFF] shadow-sm' : 'text-[#A5A7AD] hover:text-[#F5F5F5]'
              }`}
              title="Table View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>

          <button
            type="button"
            onClick={() => setCurrentRoute('analyze')}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-[#8B7CFF] hover:bg-[#7564F5] text-[#08090B] flex items-center gap-1.5 transition-all shadow-sm"
          >
            <Plus className="w-4 h-4" />
            <span>Upload Judgment</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <div className="relative lg:col-span-2">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#A5A7AD]" />
          <input
            type="text"
            placeholder="Search title, case number, Act, party, or section..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-2 bg-[#08090B] border border-[#2B2D33] rounded-xl text-xs text-[#F5F5F5] placeholder-[#A5A7AD]/60 focus:outline-none focus:border-[#8B7CFF]"
          />
        </div>

        <div>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33] rounded-xl text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF] cursor-pointer"
          >
            <option value="All">All Categories</option>
            <option value="Constitutional">Constitutional</option>
            <option value="Criminal">Criminal</option>
            <option value="Corporate & Commercial">Corporate & Commercial</option>
            <option value="Arbitration">Arbitration</option>
          </select>
        </div>

        <div>
          <select
            value={courtFilter}
            onChange={(e) => setCourtFilter(e.target.value)}
            className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33] rounded-xl text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF] cursor-pointer"
          >
            <option value="All">All Courts</option>
            <option value="Supreme Court">Supreme Court of India</option>
            <option value="High Court">High Courts</option>
          </select>
        </div>

        <div>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33] rounded-xl text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF] cursor-pointer"
          >
            <option value="uploadDate">Sort by Upload Date</option>
            <option value="judgmentDate">Sort by Judgment Date</option>
            <option value="title">Sort by Case Title</option>
          </select>
        </div>
      </div>

      {/* Grid View */}
      {viewMode === 'grid' && filteredCases.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCases.map((c) => (
            <div
              key={c.id}
              className="p-5 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card hover:border-[#8B7CFF]/50 transition-all flex flex-col justify-between group space-y-4"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#08090B] text-[#8B7CFF] border border-[#2B2D33]">
                    {c.category}
                  </span>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium flex items-center gap-1 ${
                    c.status === 'Verified' 
                      ? 'bg-[#36C98F]/10 text-[#36C98F] border border-[#36C98F]/30' 
                      : 'bg-[#F5B942]/10 text-[#F5B942] border border-[#F5B942]/30'
                  }`}>
                    {c.status === 'Verified' ? <CheckCircle2 className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                    {c.status}
                  </span>
                </div>

                <div>
                  <h3 
                    onClick={() => openCaseDetails(c)}
                    className="text-sm font-sans font-bold text-[#F5F5F5] group-hover:text-[#8B7CFF] transition-colors line-clamp-2 cursor-pointer"
                  >
                    {c.title}
                  </h3>
                  <p className="text-[11px] font-mono text-[#A5A7AD] mt-1 truncate">
                    {c.caseNumber}
                  </p>
                </div>

                <p className="text-xs text-[#A5A7AD] line-clamp-3 leading-relaxed">
                  {c.summaries?.standard || c.executiveSummary}
                </p>

                {/* Key Legal Provisions Badges */}
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {c.legalProvisions.slice(0, 2).map((p, pIdx) => (
                    <span key={pIdx} className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#08090B] text-[#F5F5F5] border border-[#2B2D33]">
                      {p.sectionOrArticle}
                    </span>
                  ))}
                  {c.legalProvisions.length > 2 && (
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-[#08090B] text-[#A5A7AD]">
                      +{c.legalProvisions.length - 2} more
                    </span>
                  )}
                </div>
              </div>

              {/* Card Footer Actions */}
              <div className="pt-3 border-t border-[#2B2D33] flex items-center justify-between text-xs">
                <span className="text-[10px] font-mono text-[#A5A7AD]">
                  {c.court}
                </span>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => openCaseInViewer(c)}
                    className="p-1.5 rounded-lg text-[#A5A7AD] hover:text-[#8B7CFF] hover:bg-[#191B20] transition-colors"
                    title="Open Document Viewer"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </button>

                  <button
                    type="button"
                    onClick={() => openCaseDetails(c)}
                    className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-[#191B20] hover:bg-[#8B7CFF] hover:text-[#08090B] text-[#8B7CFF] border border-[#8B7CFF]/30 transition-all"
                  >
                    View Record
                  </button>

                  <button
                    type="button"
                    onClick={() => setCaseToDelete(c)}
                    className="p-1.5 rounded-lg text-[#A5A7AD] hover:text-[#F87171] hover:bg-[#191B20] transition-colors"
                    title="Delete Case Record"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Table View */}
      {viewMode === 'table' && filteredCases.length > 0 && (
        <div className="rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card overflow-hidden">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#08090B] text-[#A5A7AD] uppercase tracking-wider text-[10px] border-b border-[#2B2D33]">
              <tr>
                <th className="py-3 px-4 font-semibold">Title & Case No</th>
                <th className="py-3 px-4 font-semibold">Category</th>
                <th className="py-3 px-4 font-semibold">Court</th>
                <th className="py-3 px-4 font-semibold">Date</th>
                <th className="py-3 px-4 font-semibold">Claims Verified</th>
                <th className="py-3 px-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2B2D33]/60">
              {filteredCases.map((c) => (
                <tr key={c.id} className="hover:bg-[#191B20]/60 transition-colors">
                  <td className="py-3.5 px-4">
                    <div 
                      className="font-semibold text-[#F5F5F5] hover:text-[#8B7CFF] cursor-pointer line-clamp-1 max-w-sm"
                      onClick={() => openCaseDetails(c)}
                    >
                      {c.title}
                    </div>
                    <div className="text-[10px] text-[#A5A7AD] font-mono">
                      {c.caseNumber}
                    </div>
                  </td>
                  <td className="py-3.5 px-4">
                    <span className="px-2 py-0.5 rounded bg-[#08090B] border border-[#2B2D33] text-[10px]">
                      {c.category}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-[#A5A7AD] whitespace-nowrap">
                    {c.court}
                  </td>
                  <td className="py-3.5 px-4 text-[#A5A7AD] font-mono text-[11px] whitespace-nowrap">
                    {c.judgmentDate}
                  </td>
                  <td className="py-3.5 px-4 whitespace-nowrap">
                    <span className="inline-flex items-center gap-1 text-[10px] text-[#36C98F] bg-[#36C98F]/10 px-2 py-0.5 rounded-full border border-[#36C98F]/20">
                      <ShieldCheck className="w-3 h-3" />
                      {c.verifiedClaimsCount} / {c.extractedClaimsCount}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right whitespace-nowrap">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        type="button"
                        onClick={() => openCaseDetails(c)}
                        className="px-2.5 py-1 rounded-lg text-xs bg-[#191B20] hover:bg-[#8B7CFF] hover:text-[#08090B] text-[#8B7CFF] border border-[#8B7CFF]/30 transition-all"
                      >
                        Record
                      </button>
                      <button
                        type="button"
                        onClick={() => openCaseInViewer(c)}
                        className="p-1 rounded-lg text-[#A5A7AD] hover:text-[#F5F5F5] hover:bg-[#191B20]"
                        title="Document Viewer"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setCaseToDelete(c)}
                        className="p-1 rounded-lg text-[#A5A7AD] hover:text-[#F87171] hover:bg-[#191B20]"
                        title="Delete"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Delete Confirmation Dialog */}
      {caseToDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
          <div className="bg-[#111318] border border-[#2B2D33] rounded-2xl max-w-md w-full p-6 space-y-4 shadow-modal">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-red-500/10 text-[#F87171] border border-red-500/30">
                <Trash2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-[#F5F5F5]">Confirm Record Deletion</h3>
                <p className="text-xs text-[#A5A7AD] mt-0.5">This action removes the record from your local demonstration vault.</p>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-[#08090B] border border-[#2B2D33] text-xs">
              <p className="font-semibold text-[#F5F5F5]">{caseToDelete.title}</p>
              <p className="text-[11px] font-mono text-[#A5A7AD] mt-1">{caseToDelete.caseNumber}</p>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setCaseToDelete(null)}
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-[#191B20] text-[#A5A7AD] hover:text-[#F5F5F5] transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={confirmDelete}
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-[#F87171] hover:bg-red-600 text-white transition-colors"
              >
                Delete Record
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
