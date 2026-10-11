import React, { useState, useMemo } from 'react';
import { 
  BookmarkCheck, 
  Search, 
  Filter, 
  Eye, 
  ExternalLink, 
  BookOpen, 
  Scale, 
  Info,
  ChevronRight,
  ArrowRight
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { LegalProvision, CaseRecord, ProvisionTreatment } from '../types';

export const LegalProvisionsPage: React.FC = () => {
  const { cases, activeCase, openCaseInViewer, openCaseDetails, setCurrentRoute } = useApp();

  const [selectedCaseId, setSelectedCaseId] = useState<string>(activeCase ? activeCase.id : cases[0].id);
  const [treatmentFilter, setTreatmentFilter] = useState<string>('All');
  const [searchTerm, setSearchTerm] = useState<string>('');

  const currentCase = cases.find(c => c.id === selectedCaseId) || activeCase || cases[0];

  const filteredProvisions = useMemo(() => {
    return currentCase.legalProvisions.filter(prov => {
      const matchTreatment = treatmentFilter === 'All' || prov.treatment === treatmentFilter;
      const matchSearch = searchTerm === '' ||
        prov.act.toLowerCase().includes(searchTerm.toLowerCase()) ||
        prov.sectionOrArticle.toLowerCase().includes(searchTerm.toLowerCase()) ||
        prov.description.toLowerCase().includes(searchTerm.toLowerCase());
      return matchTreatment && matchSearch;
    });
  }, [currentCase, treatmentFilter, searchTerm]);

  const getTreatmentBadge = (treatment: ProvisionTreatment) => {
    switch (treatment) {
      case 'Applied':
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-[#36C98F]/15 text-[#36C98F] border border-[#36C98F]/30">Status: Applied in judgment</span>;
      case 'Interpreted':
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-[#8B7CFF]/15 text-[#8B7CFF] border border-[#8B7CFF]/30">Status: Interpreted by bench</span>;
      case 'Discussed':
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-[#F5B942]/15 text-[#F5B942] border border-[#F5B942]/30">Status: Discussed in judgment</span>;
      case 'Mentioned':
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-[#191B20] text-[#A5A7AD] border border-[#2B2D33]">Status: Mentioned in passing</span>;
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#2B2D33]">
        <div>
          <h2 className="text-xl lg:text-2xl font-sans font-bold text-[#F5F5F5] tracking-tight flex items-center gap-2">
            <span>Legal Acts, Sections & Articles</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-[#8B7CFF]/10 text-[#8B7CFF] border border-[#8B7CFF]/30 font-mono">
              Statutory Ontology
            </span>
          </h2>
          <p className="text-xs text-[#A5A7AD] mt-1 max-w-2xl leading-relaxed">
            Precise identification of constitutional provisions, statutes, and procedural sections with treatment categorization and source-page anchors.
          </p>
        </div>

        {/* Case Switcher */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-[#A5A7AD]">Judgment:</span>
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

      {/* Highlight Legend Banner */}
      <div className="p-4 rounded-xl bg-[#111318] border border-[#2B2D33] flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <BookmarkCheck className="w-4 h-4 text-[#8B7CFF]" />
          <span className="font-semibold text-[#F5F5F5]">Interactive Highlight Legend:</span>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-[11px] font-mono">
          <span className="flex items-center gap-1.5 text-[#8B7CFF]">
            <span className="w-2.5 h-2.5 rounded-sm bg-[#8B7CFF]" /> Legal Provisions
          </span>
          <span className="flex items-center gap-1.5 text-blue-400">
            <span className="w-2.5 h-2.5 rounded-sm bg-blue-500" /> Party Arguments
          </span>
          <span className="flex items-center gap-1.5 text-[#F5B942]">
            <span className="w-2.5 h-2.5 rounded-sm bg-[#F5B942]" /> Court Findings
          </span>
          <span className="flex items-center gap-1.5 text-[#36C98F]">
            <span className="w-2.5 h-2.5 rounded-sm bg-[#36C98F]" /> Final Outcome
          </span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#A5A7AD]" />
          <input
            type="text"
            placeholder="Search Act, section, or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-[#08090B] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] placeholder-[#A5A7AD]/60 focus:outline-none focus:border-[#8B7CFF]"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <select
            value={treatmentFilter}
            onChange={(e) => setTreatmentFilter(e.target.value)}
            className="w-full sm:w-auto px-3 py-1.5 bg-[#08090B] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF] cursor-pointer"
          >
            <option value="All">All Statutory Treatments</option>
            <option value="Applied">Applied in judgment</option>
            <option value="Interpreted">Interpreted by bench</option>
            <option value="Discussed">Discussed in judgment</option>
            <option value="Mentioned">Mentioned in passing</option>
          </select>
        </div>
      </div>

      {/* Provisions Cards List */}
      <div className="space-y-4">
        {filteredProvisions.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#111318] border border-[#2B2D33] text-center text-xs text-[#A5A7AD]">
            No legal provisions match the specified search and treatment filter.
          </div>
        ) : (
          filteredProvisions.map((prov, idx) => (
            <div
              key={idx}
              className="p-5 rounded-2xl bg-[#111318] border border-[#2B2D33] hover:border-[#8B7CFF]/50 transition-all space-y-3 shadow-card"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <h3 className="text-sm font-bold text-[#F5F5F5]">
                    {prov.act}, {prov.sectionOrArticle}
                  </h3>
                  <div className="mt-1">
                    {getTreatmentBadge(prov.treatment)}
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => openCaseInViewer(currentCase, undefined, prov.pageNumber, prov.sectionOrArticle)}
                  className="px-3 py-1.5 rounded-lg text-xs font-medium bg-[#191B20] hover:bg-[#8B7CFF] hover:text-[#08090B] text-[#8B7CFF] border border-[#8B7CFF]/30 transition-all inline-flex items-center gap-1.5 self-start sm:self-center"
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>Inspect on Source Page {prov.pageNumber}</span>
                </button>
              </div>

              {/* Context Explanation */}
              <div className="text-xs text-[#A5A7AD] leading-relaxed">
                <strong className="text-[#F5F5F5]">Context:</strong> {prov.description}
              </div>

              {/* Supporting Verbatim Quotation */}
              <div className="p-3.5 rounded-xl bg-[#08090B] border-l-4 border-[#8B7CFF] border-[#2B2D33] text-xs">
                <span className="text-[10px] font-mono text-[#8B7CFF] block mb-1">
                  Supporting Judicial Text:
                </span>
                <blockquote className="font-serif italic text-[#F5F5F5] leading-relaxed">
                  "{prov.supportingQuotation}"
                </blockquote>
              </div>

              <div className="flex items-center justify-between pt-1 text-[11px] text-[#A5A7AD] font-mono">
                <span>Source: Page {prov.pageNumber}</span>
                <span>Case: {currentCase.caseNumber}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
