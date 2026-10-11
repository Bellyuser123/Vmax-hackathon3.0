import React, { useState, useEffect } from 'react';
import { 
  ChevronLeft, 
  ChevronRight, 
  ZoomIn, 
  ZoomOut, 
  RotateCcw, 
  Search, 
  ShieldCheck, 
  CheckCircle2, 
  Copy, 
  FileText, 
  Scale, 
  Sparkles, 
  ArrowLeft,
  BookmarkCheck,
  GitCompare,
  Info
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { EvidenceReference, CaseRecord } from '../types';

export const DocumentViewer: React.FC = () => {
  const { 
    activeCase, 
    activeEvidenceId, 
    setActiveEvidenceId, 
    activeViewerPage, 
    setActiveViewerPage,
    activeProvisionRef,
    setActiveProvisionRef,
    setCurrentRoute,
    showToast 
  } = useApp();

  const caseData: CaseRecord | null = activeCase;
  
  // Viewer state
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [docSearch, setDocSearch] = useState<string>('');
  const [activeRightTab, setActiveRightTab] = useState<'claims' | 'provisions' | 'summary' | 'similar'>('claims');
  const [mobileTab, setMobileTab] = useState<'doc' | 'intelligence'>('doc');

  const totalPages = caseData?.pages?.length || 4;
  const currentPageData = caseData?.pages?.find(p => p.pageNumber === activeViewerPage) || caseData?.pages?.[0];

  // Sync if activeEvidenceId changes
  useEffect(() => {
    if (activeEvidenceId && caseData) {
      const targetEvidence = caseData.evidenceReferences.find(e => e.id === activeEvidenceId);
      if (targetEvidence && targetEvidence.pageNumber !== activeViewerPage) {
        setActiveViewerPage(targetEvidence.pageNumber);
      }
    }
  }, [activeEvidenceId, caseData]);

  if (!caseData) {
    return (
      <div className="p-8 text-center space-y-4">
        <p className="text-[#A5A7AD] text-sm">No judgment loaded in Document Viewer.</p>
        <button
          onClick={() => setCurrentRoute('library')}
          className="px-4 py-2 rounded-xl text-xs font-semibold bg-[#8B7CFF] text-[#08090B]"
        >
          Browse Case Library
        </button>
      </div>
    );
  }

  const handleSelectEvidence = (ref: EvidenceReference) => {
    setActiveEvidenceId(ref.id);
    setActiveViewerPage(ref.pageNumber);
    setActiveProvisionRef(null);
    showToast(`Navigated to Page ${ref.pageNumber} (${ref.id})`);
  };

  const handleSelectProvision = (provRef: string, pageNum: number) => {
    setActiveProvisionRef(provRef);
    setActiveViewerPage(pageNum);
    setActiveEvidenceId(null);
    showToast(`Anchored to ${provRef} on Page ${pageNum}`);
  };

  const copyQuote = (quote: string) => {
    navigator.clipboard.writeText(quote);
    showToast('Quotation copied with judicial citation');
  };

  const getParagraphHighlightStyle = (para: any) => {
    // Priority: user search match
    if (docSearch && para.text.toLowerCase().includes(docSearch.toLowerCase())) {
      return 'bg-blue-500/20 border-l-4 border-blue-400 ring-1 ring-blue-400/40';
    }

    // Active evidence anchor
    if (activeEvidenceId && para.evidenceId === activeEvidenceId) {
      return 'bg-[#8B7CFF]/20 border-l-4 border-[#8B7CFF] ring-1 ring-[#8B7CFF]/50 shadow-violet-glow';
    }

    // Active provision reference
    if (activeProvisionRef && (para.provisionRef === activeProvisionRef || para.text.includes(activeProvisionRef))) {
      return 'bg-[#8B7CFF]/20 border-l-4 border-[#8B7CFF] ring-1 ring-[#8B7CFF]/40 shadow-violet-glow';
    }

    // Multi-color highlight types requested:
    switch (para.type) {
      case 'provision':
        return 'bg-[#8B7CFF]/10 border-l-2 border-[#8B7CFF]';
      case 'finding':
        return 'bg-[#F5B942]/10 border-l-2 border-[#F5B942]';
      case 'outcome':
        return 'bg-[#36C98F]/15 border-l-2 border-[#36C98F]';
      case 'argument':
        return 'bg-blue-500/10 border-l-2 border-blue-400';
      default:
        return 'hover:bg-[#191B20]/40';
    }
  };

  return (
    <div className="space-y-4 animate-in fade-in duration-200">
      {/* Top Bar with Case Navigation & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3.5 rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => setCurrentRoute('analyze')}
            className="p-1.5 rounded-lg text-[#A5A7AD] hover:text-[#F5F5F5] hover:bg-[#191B20] transition-colors"
            title="Back to Analysis"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>

          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-mono text-[#8B7CFF] bg-[#8B7CFF]/10 px-1.5 py-0.5 rounded border border-[#8B7CFF]/30">
                {caseData.court}
              </span>
              <span className="text-xs font-semibold text-[#F5F5F5] line-clamp-1">
                {caseData.title}
              </span>
            </div>
            <p className="text-[10px] font-mono text-[#A5A7AD]">
              {caseData.caseNumber} • SHA: {caseData.sha256Hash.substring(0, 16)}...
            </p>
          </div>
        </div>

        {/* Mobile View Switcher */}
        <div className="flex lg:hidden bg-[#08090B] p-1 rounded-xl border border-[#2B2D33] text-xs">
          <button
            type="button"
            onClick={() => setMobileTab('doc')}
            className={`flex-1 py-1 px-3 rounded-lg font-medium transition-colors ${
              mobileTab === 'doc' ? 'bg-[#8B7CFF] text-[#08090B] font-bold' : 'text-[#A5A7AD]'
            }`}
          >
            Original PDF
          </button>
          <button
            type="button"
            onClick={() => setMobileTab('intelligence')}
            className={`flex-1 py-1 px-3 rounded-lg font-medium transition-colors ${
              mobileTab === 'intelligence' ? 'bg-[#8B7CFF] text-[#08090B] font-bold' : 'text-[#A5A7AD]'
            }`}
          >
            AI Findings
          </button>
        </div>

        {/* Global Toolbar */}
        <div className="hidden sm:flex items-center gap-2">
          {/* Zoom Controls */}
          <div className="flex items-center bg-[#08090B] border border-[#2B2D33] rounded-lg p-0.5 text-xs">
            <button
              type="button"
              onClick={() => setZoomLevel(prev => Math.max(80, prev - 15))}
              className="p-1.5 text-[#A5A7AD] hover:text-[#F5F5F5]"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="px-2 font-mono text-[11px] text-[#A5A7AD]">{zoomLevel}%</span>
            <button
              type="button"
              onClick={() => setZoomLevel(prev => Math.min(150, prev + 15))}
              className="p-1.5 text-[#A5A7AD] hover:text-[#F5F5F5]"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              onClick={() => setZoomLevel(100)}
              className="p-1.5 text-[#A5A7AD] hover:text-[#F5F5F5] border-l border-[#2B2D33]"
              title="Reset Zoom"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Page Navigator */}
          <div className="flex items-center bg-[#08090B] border border-[#2B2D33] rounded-lg p-0.5 text-xs">
            <button
              type="button"
              disabled={activeViewerPage <= 1}
              onClick={() => setActiveViewerPage(Math.max(1, activeViewerPage - 1))}
              className="p-1.5 text-[#A5A7AD] hover:text-[#F5F5F5] disabled:opacity-30"
              title="Previous Page"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <span className="px-2 font-mono text-[11px] text-[#A5A7AD]">
              Page {activeViewerPage} of {totalPages}
            </span>
            <button
              type="button"
              disabled={activeViewerPage >= totalPages}
              onClick={() => setActiveViewerPage(Math.min(totalPages, activeViewerPage + 1))}
              className="p-1.5 text-[#A5A7AD] hover:text-[#F5F5F5] disabled:opacity-30"
              title="Next Page"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Split-Screen Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[680px]">
        {/* LEFT PANEL: Original PDF Document (Interactive High-Fidelity Rendering) */}
        <div className={`lg:col-span-7 flex flex-col rounded-2xl bg-[#08090B] border border-[#2B2D33] shadow-card overflow-hidden ${
          mobileTab === 'intelligence' ? 'hidden lg:flex' : 'flex'
        }`}>
          {/* Document Header Toolbar */}
          <div className="p-3 bg-[#111318] border-b border-[#2B2D33] flex flex-wrap items-center justify-between gap-2 text-xs">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-[#8B7CFF]" />
              <span className="font-semibold text-[#F5F5F5]">Original Court Document</span>
              <span className="text-[10px] text-[#36C98F] bg-[#36C98F]/10 px-1.5 py-0.5 rounded border border-[#36C98F]/20 font-mono">
                Preserved
              </span>
            </div>

            {/* In-Document Search */}
            <div className="relative w-44 sm:w-52">
              <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3 h-3 text-[#A5A7AD]" />
              <input
                type="text"
                placeholder="Find in page text..."
                value={docSearch}
                onChange={(e) => setDocSearch(e.target.value)}
                className="w-full pl-7 pr-2 py-1 bg-[#191B20] border border-[#2B2D33] rounded-md text-[11px] text-[#F5F5F5] placeholder-[#A5A7AD]/60 focus:outline-none focus:border-[#8B7CFF]"
              />
            </div>
          </div>

          {/* Interactive Highlight Legend Toolbar */}
          <div className="px-4 py-2 bg-[#111318]/70 border-b border-[#2B2D33] flex flex-wrap items-center justify-between gap-2 text-[10px] font-mono">
            <span className="text-[#A5A7AD]">Highlight Legend:</span>
            <div className="flex flex-wrap items-center gap-3">
              <span className="text-[#8B7CFF] flex items-center gap-1">
                <span className="w-2 h-2 rounded-sm bg-[#8B7CFF]" /> Provision
              </span>
              <span className="text-blue-400 flex items-center gap-1">
                <span className="w-2 h-2 rounded-sm bg-blue-500" /> Arguments
              </span>
              <span className="text-[#F5B942] flex items-center gap-1">
                <span className="w-2 h-2 rounded-sm bg-[#F5B942]" /> Court Findings
              </span>
              <span className="text-[#36C98F] flex items-center gap-1">
                <span className="w-2 h-2 rounded-sm bg-[#36C98F]" /> Final Outcome
              </span>
            </div>
          </div>

          {/* Document Render Canvas */}
          <div className="flex-1 p-6 lg:p-8 overflow-y-auto bg-[#08090B] relative">
            <div 
              style={{ transform: `scale(${zoomLevel / 100})`, transformOrigin: 'top center' }}
              className="transition-transform duration-200 mx-auto max-w-2xl bg-[#111318] border border-[#2B2D33] rounded-xl p-8 sm:p-12 shadow-2xl relative min-h-[600px] legal-watermark text-[#F5F5F5] font-serif leading-relaxed"
            >
              {/* Official Emblems / Seal Simulation */}
              <div className="text-center space-y-1 pb-6 mb-6 border-b border-[#2B2D33]">
                <div className="flex justify-center mb-2">
                  <div className="w-9 h-9 rounded-full border border-[#8B7CFF]/40 bg-[#08090B] flex items-center justify-center text-[#8B7CFF]">
                    <Scale className="w-4 h-4" />
                  </div>
                </div>
                <h3 className="text-xs uppercase tracking-widest font-bold text-[#F5F5F5] font-sans whitespace-pre-line leading-tight">
                  {currentPageData?.courtHeader || caseData.court}
                </h3>
                <p className="text-[10px] font-mono tracking-wider text-[#A5A7AD] pt-1">
                  {currentPageData?.judgmentDate || caseData.judgmentDate}
                </p>
              </div>

              {/* Page Paragraphs & Evidence Anchors */}
              <div className="space-y-6 text-xs text-[#F5F5F5] font-serif">
                {currentPageData?.paragraphs.map((para, pIdx) => {
                  const highlightClass = getParagraphHighlightStyle(para);
                  const isTarget = para.isEvidenceTarget && (!activeEvidenceId || para.evidenceId === activeEvidenceId);

                  return (
                    <div 
                      key={pIdx}
                      className={`relative p-3 rounded-lg transition-all ${highlightClass}`}
                    >
                      {/* Active Evidence Anchor Badge */}
                      {isTarget && (
                        <div className="absolute -top-3 right-3 px-2 py-0.5 rounded-full bg-[#8B7CFF] text-[#08090B] text-[9px] font-bold font-sans flex items-center gap-1 shadow-sm">
                          <Sparkles className="w-2.5 h-2.5" />
                          <span>EVIDENCE ANCHOR {para.evidenceId}</span>
                        </div>
                      )}

                      <div className="flex items-start gap-2.5">
                        {para.paraNumber && (
                          <span className="font-mono text-[#8B7CFF] font-bold text-[11px] flex-shrink-0 select-none">
                            {para.paraNumber}
                          </span>
                        )}
                        <p className="text-xs leading-relaxed text-[#F5F5F5]">
                          {para.text}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Bottom Document Stamp */}
              <div className="mt-12 pt-4 border-t border-[#2B2D33] flex items-center justify-between text-[10px] font-mono text-[#A5A7AD]">
                <span>Page {activeViewerPage} of {totalPages}</span>
                <span className="text-[#8B7CFF]/80">Certified e-Court Transcript</span>
                <span>SHA-256 Verified</span>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT PANEL: Extracted Legal Intelligence Workspace */}
        <div className={`lg:col-span-5 flex flex-col rounded-2xl bg-[#111318] border border-[#2B2D33] shadow-card overflow-hidden ${
          mobileTab === 'doc' ? 'hidden lg:flex' : 'flex'
        }`}>
          {/* Intelligence Tabs */}
          <div className="p-3 bg-[#191B20] border-b border-[#2B2D33] flex items-center justify-between">
            <div className="flex gap-1">
              {[
                { id: 'claims', label: 'Claims', count: caseData.evidenceReferences.length },
                { id: 'provisions', label: 'Provisions', count: caseData.legalProvisions.length },
                { id: 'summary', label: 'Summary' },
                { id: 'similar', label: 'Similar', count: caseData.relatedCases.length }
              ].map((tab) => (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setActiveRightTab(tab.id as any)}
                  className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                    activeRightTab === tab.id 
                      ? 'bg-[#8B7CFF] text-[#08090B] font-bold shadow-sm' 
                      : 'text-[#A5A7AD] hover:text-[#F5F5F5] hover:bg-[#111318]'
                  }`}
                >
                  {tab.label} {tab.count !== undefined && `(${tab.count})`}
                </button>
              ))}
            </div>

            <span className="text-[10px] font-mono text-[#36C98F] flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" />
              Verified
            </span>
          </div>

          {/* Intelligence Content */}
          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {/* TAB: Evidence Claims */}
            {activeRightTab === 'claims' && (
              <div className="space-y-3">
                <p className="text-[11px] text-[#A5A7AD]">
                  Select any claim to navigate the PDF canvas and illuminate the exact judicial paragraph.
                </p>

                {caseData.evidenceReferences.map((ref) => {
                  const isSelected = activeEvidenceId === ref.id;
                  const isCurrentPage = activeViewerPage === ref.pageNumber;

                  return (
                    <div
                      key={ref.id}
                      onClick={() => handleSelectEvidence(ref)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer space-y-2
                        ${isSelected 
                          ? 'bg-[#191B20] border-[#8B7CFF] shadow-violet-glow' 
                          : isCurrentPage 
                            ? 'bg-[#191B20]/80 border-[#3D404A]' 
                            : 'bg-[#08090B]/60 border-[#2B2D33] hover:bg-[#191B20]/60'
                        }
                      `}
                    >
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="font-mono text-[#8B7CFF] font-bold">{ref.id}</span>
                        <div className="flex items-center gap-1.5">
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-[#111318] text-[#A5A7AD] border border-[#2B2D33]">
                            Page {ref.pageNumber} {ref.paragraph ? `(${ref.paragraph})` : ''}
                          </span>
                          <span className="text-[10px] text-[#36C98F] font-semibold flex items-center gap-0.5">
                            <CheckCircle2 className="w-3 h-3" />
                            {ref.verificationStatus}
                          </span>
                        </div>
                      </div>

                      <p className="text-xs font-semibold text-[#F5F5F5] leading-snug">
                        {ref.claim}
                      </p>

                      <blockquote className="p-2.5 rounded-lg bg-[#08090B] border-l-2 border-[#8B7CFF] text-[11px] font-serif italic text-[#F5F5F5] leading-relaxed">
                        {ref.exactQuotation}
                      </blockquote>

                      <div className="flex items-center justify-between pt-1 text-[10px] text-[#A5A7AD]">
                        <span>Confidence: {(ref.confidence * 100).toFixed(0)}%</span>
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            copyQuote(ref.exactQuotation);
                          }}
                          className="hover:text-[#8B7CFF] flex items-center gap-1"
                        >
                          <Copy className="w-3 h-3" /> Copy Quote
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* TAB: Legal Provisions */}
            {activeRightTab === 'provisions' && (
              <div className="space-y-3">
                {caseData.legalProvisions.map((prov, i) => (
                  <div 
                    key={i}
                    onClick={() => handleSelectProvision(prov.sectionOrArticle, prov.pageNumber)}
                    className="p-3.5 rounded-xl bg-[#08090B] border border-[#2B2D33] hover:border-[#8B7CFF]/50 cursor-pointer transition-colors space-y-1.5"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-[#8B7CFF] font-mono">
                        {prov.sectionOrArticle}
                      </span>
                      <span className="text-[10px] text-[#A5A7AD] font-mono">
                        Page {prov.pageNumber} →
                      </span>
                    </div>
                    <p className="text-xs font-semibold text-[#F5F5F5]">{prov.act}</p>
                    <p className="text-[11px] text-[#A5A7AD] leading-relaxed">{prov.description}</p>
                  </div>
                ))}
              </div>
            )}

            {/* TAB: Summary */}
            {activeRightTab === 'summary' && (
              <div className="space-y-4 text-xs">
                <div className="p-3.5 rounded-xl bg-[#08090B] border border-[#2B2D33] space-y-2">
                  <h4 className="font-sans font-bold text-[#8B7CFF]">Standard Case Summary</h4>
                  <p className="text-[#F5F5F5] leading-relaxed whitespace-pre-line">{caseData.summaries.standard}</p>
                </div>

                <div className="p-3.5 rounded-xl bg-[#08090B] border border-[#2B2D33] space-y-1.5">
                  <h4 className="font-sans font-bold text-[#36C98F]">Final Disposition: {caseData.finalOutcome.disposition}</h4>
                  <p className="text-[#A5A7AD] leading-relaxed">{caseData.finalOutcome.summary}</p>
                </div>
              </div>
            )}

            {/* TAB: Similar Precedents */}
            {activeRightTab === 'similar' && (
              <div className="space-y-3">
                {caseData.relatedCases.map((rel) => (
                  <div 
                    key={rel.id}
                    className="p-3 rounded-xl bg-[#08090B] border border-[#2B2D33] space-y-1.5 text-xs"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-[#F5F5F5]">{rel.title}</span>
                      <span className="text-[10px] font-mono text-[#8B7CFF]">{rel.relevanceScore}% match</span>
                    </div>
                    <p className="text-[11px] text-[#A5A7AD]">{rel.similarityReason}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
