import React, { useState, useMemo } from 'react';
import { 
  GitCompare, 
  Search, 
  Filter, 
  ExternalLink, 
  Scale, 
  Sparkles, 
  AlertTriangle, 
  CheckCircle2, 
  Info,
  Calendar,
  Layers
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { RelatedCase, CaseRecord } from '../types';

export const SimilarCases: React.FC = () => {
  const { cases, activeCase, openCaseDetails, showToast } = useApp();

  const [selectedCaseId, setSelectedCaseId] = useState<string>(activeCase ? activeCase.id : cases[0].id);
  const [categoryFilter, setCategoryFilter] = useState<string>('All');
  const [searchTerm, setSearchTerm] = useState<string>('');

  const currentCase = cases.find(c => c.id === selectedCaseId) || activeCase || cases[0];

  const filteredRelated = useMemo(() => {
    return currentCase.relatedCases.filter((rel) => {
      const matchCat = categoryFilter === 'All' || rel.category === categoryFilter;
      const matchSearch = searchTerm === '' ||
        rel.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        rel.similarityReason.toLowerCase().includes(searchTerm.toLowerCase()) ||
        rel.relevantProvisions.some(p => p.toLowerCase().includes(searchTerm.toLowerCase()));
      return matchCat && matchSearch;
    });
  }, [currentCase, categoryFilter, searchTerm]);

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#2B2D33]">
        <div>
          <h2 className="text-xl lg:text-2xl font-sans font-bold text-[#F5F5F5] tracking-tight flex items-center gap-2">
            <span>Similar Cases & Precedents Discovery</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-[#8B7CFF]/10 text-[#8B7CFF] border border-[#8B7CFF]/30 font-mono">
              Similarity Engine
            </span>
          </h2>
          <p className="text-xs text-[#A5A7AD] mt-1 max-w-2xl leading-relaxed">
            Discover related judgments grounded in shared statutory provisions, procedural context, and judicial ratios.
          </p>
        </div>

        {/* Case Switcher */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-[#A5A7AD]">Active Judgment:</span>
          <select
            value={selectedCaseId}
            onChange={(e) => setSelectedCaseId(e.target.value)}
            className="px-3 py-1.5 bg-[#111318] border border-[#2B2D33] rounded-xl text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]"
          >
            {cases.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title.slice(0, 32)}...
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Legal Precedent Caveat Box */}
      <div className="p-4 rounded-xl bg-[#111318] border border-[#2B2D33] text-xs text-[#A5A7AD] flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-[#F5B942] flex-shrink-0 mt-0.5" />
        <div className="space-y-1">
          <span className="font-semibold text-[#F5F5F5]">Precedent & Binding Authority Notice:</span>
          <p className="text-[11px] leading-relaxed text-[#A5A7AD]">
            A similar case identified through shared legal provisions or factual analogies is not necessarily binding precedent. AI similarity rankings represent structural and topical closeness and do not replace professional judicial determination under Article 141 of the Constitution.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#A5A7AD]" />
          <input
            type="text"
            placeholder="Search by precedent title, Act, or reason..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-[#08090B] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] placeholder-[#A5A7AD]/60 focus:outline-none focus:border-[#8B7CFF]"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="w-full sm:w-auto px-3 py-1.5 bg-[#08090B] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF] cursor-pointer"
          >
            <option value="All">All Categories</option>
            <option value="Constitutional">Constitutional</option>
            <option value="Criminal">Criminal</option>
            <option value="Civil">Civil</option>
            <option value="Corporate & Commercial">Corporate & Commercial</option>
          </select>
        </div>
      </div>

      {/* Similar Cases Grid */}
      <div className="space-y-4">
        {filteredRelated.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#111318] border border-[#2B2D33] text-center text-xs text-[#A5A7AD]">
            No similar precedents found matching your filters for this case.
          </div>
        ) : (
          filteredRelated.map((rel) => (
            <div
              key={rel.id}
              className="p-5 rounded-2xl bg-[#111318] border border-[#2B2D33] hover:border-[#8B7CFF]/50 transition-all space-y-3 shadow-card"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono px-2 py-0.5 rounded bg-[#191B20] text-[#A5A7AD] border border-[#2B2D33]">
                      {rel.court}
                    </span>
                    <span className="text-xs font-mono text-[#A5A7AD]">
                      Decision: {rel.decisionDate}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-[#F5F5F5] mt-1">
                    {rel.title}
                  </h3>
                </div>

                <div className="flex items-center gap-2 self-start sm:self-center">
                  <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-[#8B7CFF]/15 text-[#8B7CFF] border border-[#8B7CFF]/30">
                    Relevance Score: {rel.relevanceScore}%
                  </span>
                  <a
                    href={rel.sourceLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-1.5 rounded-lg bg-[#191B20] text-[#8B7CFF] hover:bg-[#8B7CFF] hover:text-[#08090B] transition-colors"
                    title="Open Official Record"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </div>

              {/* Similarity Rationale */}
              <div className="p-3.5 rounded-xl bg-[#191B20] text-xs text-[#F5F5F5] leading-relaxed">
                <strong className="text-[#8B7CFF] block mb-0.5">Why it is related:</strong>
                <p className="text-[#A5A7AD]">{rel.similarityReason}</p>
              </div>

              {/* Shared Factors and Provisions */}
              <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-[#2B2D33] text-xs">
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="text-[#A5A7AD] text-[11px]">Provisions:</span>
                  {rel.relevantProvisions.map((p, pIdx) => (
                    <span key={pIdx} className="px-2 py-0.5 rounded bg-[#08090B] border border-[#2B2D33] font-mono text-[10px] text-[#F5F5F5]">
                      {p}
                    </span>
                  ))}
                </div>

                <div className="flex flex-wrap items-center gap-1.5 text-[11px] text-[#A5A7AD]">
                  <span>Shared Factors:</span>
                  {rel.sharedFactors.map((f, fIdx) => (
                    <span key={fIdx} className="px-1.5 py-0.5 rounded bg-[#191B20] text-[#36C98F] text-[10px]">
                      ✓ {f}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
