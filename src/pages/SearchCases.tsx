import React, { useState, useMemo } from 'react';
import { 
  Search, 
  ExternalLink, 
  Info
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { CaseRecord } from '../types';

export const SearchCases: React.FC = () => {
  const { cases, openCaseDetails, openCaseInViewer, searchFilter, setSearchFilter } = useApp();

  const [query, setQuery] = useState(searchFilter || 'privacy');
  const [selectedAct, setSelectedAct] = useState('All');
  const [selectedCourt, setSelectedCourt] = useState('All');

  const suggestedSearches = [
    'Right to Privacy Article 21',
    'Section 66A IT Act vagueness',
    'Section 154 CrPC mandatory FIR',
    'Three-fold proportionality test',
    'Bodily autonomy and informational privacy'
  ];

  const searchResults = useMemo(() => {
    if (!query.trim()) return [];

    const q = query.toLowerCase().trim();
    const results: {
      caseRecord: CaseRecord;
      matchType: 'Provision' | 'Claim' | 'Title/Party' | 'Summary';
      excerpt: string;
      pageNumber: number;
      relevanceScore: number;
    }[] = [];

    cases.forEach((c) => {
      if (selectedCourt !== 'All' && !c.court.includes(selectedCourt)) return;

      // Title & parties
      if (
        c.title.toLowerCase().includes(q) ||
        c.caseNumber.toLowerCase().includes(q) ||
        c.parties.petitioner.some(p => p.toLowerCase().includes(q)) ||
        c.parties.respondent.some(p => p.toLowerCase().includes(q))
      ) {
        results.push({
          caseRecord: c,
          matchType: 'Title/Party',
          excerpt: `Cause title or party recital: ${c.title} (${c.caseNumber})`,
          pageNumber: 1,
          relevanceScore: 95
        });
      }

      // Legal provisions
      c.legalProvisions.forEach((prov) => {
        if (selectedAct !== 'All' && !prov.act.includes(selectedAct)) return;

        if (
          prov.act.toLowerCase().includes(q) ||
          prov.sectionOrArticle.toLowerCase().includes(q) ||
          prov.description.toLowerCase().includes(q)
        ) {
          results.push({
            caseRecord: c,
            matchType: 'Provision',
            excerpt: `${prov.act} — ${prov.sectionOrArticle}: "${prov.description}"`,
            pageNumber: prov.pageNumber,
            relevanceScore: 92
          });
        }
      });

      // Evidence references
      c.evidenceReferences.forEach((ref) => {
        if (
          ref.claim.toLowerCase().includes(q) ||
          ref.exactQuotation.toLowerCase().includes(q) ||
          ref.context.toLowerCase().includes(q)
        ) {
          results.push({
            caseRecord: c,
            matchType: 'Claim',
            excerpt: `${ref.exactQuotation} — Context: ${ref.context}`,
            pageNumber: ref.pageNumber,
            relevanceScore: 89
          });
        }
      });
    });

    return results.sort((a, b) => b.relevanceScore - a.relevanceScore);
  }, [cases, query, selectedAct, selectedCourt]);

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="pb-4 border-b border-[#2B2D33]">
        <h2 className="text-xl lg:text-2xl font-sans font-bold text-[#F5F5F5] tracking-tight flex items-center gap-2">
          <span>Search Indian Legal Documents & Provisions</span>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-[#8B7CFF]/10 text-[#8B7CFF] border border-[#8B7CFF]/30 font-mono">
            Provision & Ratio Indexing
          </span>
        </h2>
        <p className="text-xs text-[#A5A7AD] mt-1 max-w-2xl leading-relaxed">
          Search across indexed Indian Supreme Court judgments by constitutional articles, statutes, sections, and verbatim judicial quotations.
        </p>
      </div>

      {/* Main Search Input Form */}
      <div className="p-6 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card space-y-4">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#8B7CFF]" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by legal concepts (e.g., 'Article 21 privacy', 'Section 154 mandatory FIR', 'Section 66A IT Act')..."
            className="w-full pl-12 pr-4 py-3 bg-[#08090B] border border-[#2B2D33] rounded-xl text-xs text-[#F5F5F5] placeholder-[#A5A7AD]/60 focus:outline-none focus:border-[#8B7CFF] focus:ring-1 focus:ring-[#8B7CFF]/50"
          />
        </div>

        {/* Suggested Queries */}
        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
          <span className="text-[#A5A7AD] text-[11px]">Popular Searches:</span>
          {suggestedSearches.map((tag, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => setQuery(tag)}
              className="px-2.5 py-1 rounded-lg bg-[#08090B] border border-[#2B2D33] text-[#8B7CFF] hover:border-[#8B7CFF]/50 hover:bg-[#191B20] transition-colors text-[11px]"
            >
              {tag}
            </button>
          ))}
        </div>

        {/* Filter controls */}
        <div className="pt-3 border-t border-[#2B2D33] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-3">
            <select
              value={selectedAct}
              onChange={(e) => setSelectedAct(e.target.value)}
              className="px-3 py-1.5 bg-[#08090B] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]"
            >
              <option value="All">All Statutes / Acts</option>
              <option value="Constitution">Constitution of India</option>
              <option value="Information Technology">Information Technology Act, 2000</option>
              <option value="Criminal Procedure">Code of Criminal Procedure (CrPC)</option>
            </select>

            <select
              value={selectedCourt}
              onChange={(e) => setSelectedCourt(e.target.value)}
              className="px-3 py-1.5 bg-[#08090B] border border-[#2B2D33] rounded-lg text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]"
            >
              <option value="All">All Courts</option>
              <option value="Supreme Court">Supreme Court of India</option>
              <option value="High Court">High Courts</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 text-[#A5A7AD] text-[11px]">
            <Info className="w-3.5 h-3.5 text-[#8B7CFF] flex-shrink-0" />
            <span>Search mode: <strong className="text-[#F5F5F5]">Keyword & Provision Indexing</strong></span>
          </div>
        </div>
      </div>

      {/* Results Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between text-xs text-[#A5A7AD]">
          <span>Found <strong className="text-[#8B7CFF]">{searchResults.length}</strong> matching passages</span>
          <span className="font-mono">Index Size: {cases.length} judgments</span>
        </div>

        {searchResults.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#111318] border border-[#2B2D33] text-center space-y-3">
            <Search className="w-8 h-8 text-[#A5A7AD] mx-auto" />
            <h3 className="text-sm font-semibold text-[#F5F5F5]">No matching judicial passages found</h3>
            <p className="text-xs text-[#A5A7AD] max-w-sm mx-auto">
              Try searching with terms like "Privacy", "Article 21", "Section 66A", or "Section 154".
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {searchResults.map((res, idx) => (
              <div
                key={idx}
                className="p-5 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card hover:border-[#8B7CFF]/50 transition-all space-y-3"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#08090B] text-[#8B7CFF] border border-[#2B2D33]">
                      {res.caseRecord.court}
                    </span>
                    <span className="text-xs font-bold text-[#F5F5F5]">
                      {res.caseRecord.title}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[#36C98F]/10 text-[#36C98F] border border-[#36C98F]/20">
                      Page {res.pageNumber}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-[#08090B] text-[#A5A7AD] border border-[#2B2D33] font-mono">
                      Match: {res.matchType}
                    </span>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-[#08090B] border-l-4 border-[#8B7CFF] text-xs font-serif italic text-[#F5F5F5] leading-relaxed">
                  "{res.excerpt}"
                </div>

                <div className="flex items-center justify-between pt-1 text-xs">
                  <span className="text-[11px] font-mono text-[#A5A7AD]">
                    Case No: {res.caseRecord.caseNumber}
                  </span>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => openCaseInViewer(res.caseRecord, undefined, res.pageNumber)}
                      className="px-3 py-1.5 rounded-lg text-xs font-medium bg-[#191B20] hover:bg-[#8B7CFF] hover:text-[#08090B] text-[#8B7CFF] border border-[#8B7CFF]/30 transition-all flex items-center gap-1.5"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      <span>Inspect on Page {res.pageNumber}</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => openCaseDetails(res.caseRecord)}
                      className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#191B20] hover:bg-[#22252C] text-[#F5F5F5] border border-[#2B2D33] transition-colors"
                    >
                      View Analysis
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
