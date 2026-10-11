import React, { useState, useMemo } from 'react';
import { 
  FileText, 
  Library, 
  BookmarkCheck, 
  AlertCircle, 
  ArrowUpRight, 
  Plus, 
  Search, 
  CheckCircle2, 
  ExternalLink, 
  Scale, 
  ShieldCheck,
  GitCompare,
  Sparkles,
  TrendingUp,
  Eye,
  Zap,
  ArrowRight,
  Clock
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell,
  AreaChart,
  Area
} from 'recharts';
import { useApp } from '../context/AppContext';

export const Dashboard: React.FC = () => {
  const { 
    cases, 
    setCurrentRoute, 
    openCaseDetails, 
    openCaseInViewer, 
    showToast 
  } = useApp();

  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedCourt, setSelectedCourt] = useState<string>('All');
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [tableSearch, setTableSearch] = useState<string>('');

  const monthlyData = [
    { month: 'May', analyzed: 18, verified: 18 },
    { month: 'Jun', analyzed: 24, verified: 24 },
    { month: 'Jul', analyzed: 35, verified: 34 },
    { month: 'Aug', analyzed: 42, verified: 41 },
    { month: 'Sep', analyzed: 56, verified: 54 },
    { month: 'Oct', analyzed: 68, verified: 67 },
  ];

  const categoryData = useMemo(() => {
    const counts: Record<string, number> = {
      Constitutional: 0,
      Criminal: 0,
      Civil: 0,
      'Corporate & Commercial': 0,
      Arbitration: 0,
    };
    cases.forEach(c => {
      if (counts[c.category] !== undefined) {
        counts[c.category]++;
      } else {
        counts['Civil']++;
      }
    });
    return [
      { name: 'Constitutional', value: counts['Constitutional'] || 2, color: '#8B7CFF' },
      { name: 'Criminal', value: counts['Criminal'] || 1, color: '#36C98F' },
      { name: 'Corporate & Comm.', value: counts['Corporate & Commercial'] || 1, color: '#F5B942' },
      { name: 'Arbitration', value: counts['Arbitration'] || 1, color: '#9E91FF' },
      { name: 'Civil', value: counts['Civil'] || 1, color: '#6E7079' },
    ];
  }, [cases]);

  const filteredCases = useMemo(() => {
    return cases.filter(c => {
      const matchCat = selectedCategory === 'All' || c.category === selectedCategory;
      const matchCourt = selectedCourt === 'All' || c.court.includes(selectedCourt);
      const matchStatus = selectedStatus === 'All' || c.status === selectedStatus;
      const matchSearch = tableSearch === '' || 
        c.title.toLowerCase().includes(tableSearch.toLowerCase()) ||
        c.caseNumber.toLowerCase().includes(tableSearch.toLowerCase()) ||
        c.court.toLowerCase().includes(tableSearch.toLowerCase());
      return matchCat && matchCourt && matchStatus && matchSearch;
    });
  }, [cases, selectedCategory, selectedCourt, selectedStatus, tableSearch]);

  const totalProvisions = cases.reduce((acc, c) => acc + c.legalProvisions.length, 0);
  const totalReview = cases.reduce((acc, c) => acc + c.requiresReviewCount, 0);

  const statCards = [
    {
      label: 'Documents Analyzed',
      value: '184',
      change: '+14.2%',
      changePositive: true,
      detail: 'Supreme & High Courts • Demo metrics',
      icon: FileText,
      iconColor: 'text-[#8B7CFF]',
      iconBg: 'stat-card-icon',
    },
    {
      label: 'Cases in Library',
      value: `${cases.length}`,
      change: 'Persisted',
      changePositive: true,
      detail: 'Indian jurisprudence records in local vault',
      icon: Library,
      iconColor: 'text-[#36C98F]',
      iconBg: 'stat-card-icon-emerald',
    },
    {
      label: 'Legal Provisions Found',
      value: `${totalProvisions}`,
      change: '100% quoted',
      changePositive: true,
      detail: 'Constitution, IT Act, CrPC & Companies Act',
      icon: BookmarkCheck,
      iconColor: 'text-[#8B7CFF]',
      iconBg: 'stat-card-icon',
    },
    {
      label: 'Claims Requiring Review',
      value: `${totalReview}`,
      change: 'Audit Needed',
      changePositive: false,
      detail: 'Flagged for clerk or advocate verification',
      icon: AlertCircle,
      iconColor: 'text-[#F5B942]',
      iconBg: 'stat-card-icon-amber',
    },
  ];

  return (
    <div className="space-y-8">
      {/* ═══════════════════════════════════════════
          1. HERO SECTION — Premium
          ═══════════════════════════════════════════ */}
      <div className="relative overflow-hidden rounded-2xl card-premium p-6 lg:p-8 noise-overlay animate-fade-in-up">
        {/* Ambient orbs */}
        <div className="ambient-orb ambient-orb-violet w-72 h-72 -top-20 -right-20" />
        <div className="ambient-orb ambient-orb-emerald w-48 h-48 -bottom-10 left-20" style={{animationDelay: '3s'}} />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            {/* Status pill */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass text-[11px] font-medium text-[#A5A7AD]">
              <span className="relative w-2 h-2 rounded-full bg-[#36C98F]">
                <span className="absolute inset-0 rounded-full bg-[#36C98F] animate-ping opacity-40" />
              </span>
              <span>NyayaLens Intelligence Workspace</span>
              <span className="w-px h-3 bg-[#2B2D33]" />
              <span className="text-[#8B7CFF]">Indian Court Precedents</span>
            </div>
            
            <h1 className="text-2xl lg:text-[32px] font-sans font-bold text-[#F5F5F5] tracking-tight leading-[1.2]">
              Understand the judgment. Find the law.{' '}
              <span className="bg-gradient-to-r from-[#8B7CFF] to-[#9E91FF] bg-clip-text text-transparent">
                Verify the evidence.
              </span>
            </h1>
            <p className="text-sm text-[#6E7079] leading-relaxed max-w-lg">
              Transform complex Indian court documents into structured, searchable legal intelligence with AI-powered analysis and SHA-256 verified evidence chains.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <button
              type="button"
              onClick={() => setCurrentRoute('analyze')}
              className="btn-primary inline-flex items-center justify-center gap-2 px-6 py-3 text-sm"
            >
              <Sparkles className="w-4 h-4" />
              <span>Analyze New Document</span>
            </button>

            <button
              type="button"
              onClick={() => {
                const landmark = cases.find(c => c.id === 'case-puttaswamy-2017') || cases[0];
                openCaseDetails(landmark);
                showToast('Loaded landmark Supreme Court Privacy Judgment demonstration.');
              }}
              className="btn-ghost inline-flex items-center justify-center gap-2 px-4 py-3 text-xs"
            >
              <Scale className="w-3.5 h-3.5 text-[#8B7CFF]" />
              <span>Puttaswamy 9-Judge Benchmark</span>
            </button>
          </div>
        </div>

        {/* Demo environment badge */}
        <div className="relative z-10 mt-6 pt-4 border-t border-[#2B2D33]/40 flex flex-wrap items-center justify-between text-[11px] text-[#525562] gap-2">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-[#36C98F]" />
            <span>Demonstration Environment: Indexed against Supreme Court of India precedents</span>
          </div>
          <span className="font-mono text-[#525562] flex items-center gap-1.5">
            <ShieldCheck className="w-3 h-3 text-[#36C98F]" />
            SHA-256 (NIST FIPS 180-4)
          </span>
        </div>
      </div>

      {/* ═══════════════════════════════════════════
          2. STATISTICS CARDS — Animated
          ═══════════════════════════════════════════ */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 stagger-children">
        {statCards.map((card, i) => {
          const Icon = card.icon;
          return (
            <div 
              key={i} 
              className="card-premium p-5 animate-fade-in-up group"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-[#6E7079] uppercase tracking-wider">{card.label}</span>
                <div className={`w-9 h-9 rounded-xl ${card.iconBg} flex items-center justify-center ${card.iconColor} transition-transform duration-300 group-hover:scale-110`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-[28px] font-bold font-sans stat-value leading-none">{card.value}</span>
                <span className={`text-[11px] font-semibold flex items-center gap-0.5 ${card.changePositive ? 'text-[#36C98F]' : 'text-[#F5B942]'}`}>
                  {card.changePositive && <ArrowUpRight className="w-3 h-3" />}
                  {card.change}
                </span>
              </div>
              <p className="mt-2 text-[10px] text-[#525562] leading-relaxed">{card.detail}</p>
            </div>
          );
        })}
      </div>

      {/* ═══════════════════════════════════════════
          3. ANALYTICS CHARTS — Premium
          ═══════════════════════════════════════════ */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Document activity chart */}
        <div className="lg:col-span-2 card-premium p-6 flex flex-col justify-between animate-fade-in-up" style={{animationDelay: '100ms'}}>
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-sm font-semibold text-[#F5F5F5] flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-[#8B7CFF]" />
                Document Activity
              </h3>
              <p className="text-xs text-[#525562] mt-0.5">Court judgments analyzed and verified over time</p>
            </div>
            <div className="flex items-center gap-4 text-[11px]">
              <div className="flex items-center gap-1.5 text-[#8B7CFF]">
                <span className="w-2.5 h-2.5 rounded-sm bg-[#8B7CFF]" /> Analyzed
              </div>
              <div className="flex items-center gap-1.5 text-[#36C98F]">
                <span className="w-2.5 h-2.5 rounded-sm bg-[#36C98F]" /> Verified
              </div>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1C1E24" vertical={false} />
                <XAxis dataKey="month" stroke="#525562" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="#525562" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#191B20', 
                    borderColor: '#2B2D33', 
                    borderRadius: '12px', 
                    color: '#F5F5F5',
                    fontSize: '12px',
                    boxShadow: '0 8px 30px -5px rgba(0,0,0,0.5)'
                  }} 
                  cursor={{ fill: 'rgba(139, 124, 255, 0.04)' }}
                />
                <Bar dataKey="analyzed" fill="#8B7CFF" radius={[6, 6, 0, 0]} barSize={20} />
                <Bar dataKey="verified" fill="#36C98F" radius={[6, 6, 0, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-4 pt-4 border-t border-[#2B2D33]/40 flex items-center justify-between text-[11px] text-[#525562]">
            <div className="flex items-center gap-1.5">
              <Zap className="w-3 h-3 text-[#8B7CFF]" />
              <span>Average OCR throughput: 1.4s per 20 pages</span>
            </div>
            <span className="font-mono text-[#36C98F]">Precision rate: 99.4%</span>
          </div>
        </div>

        {/* Case category distribution */}
        <div className="card-premium p-6 flex flex-col justify-between animate-fade-in-up" style={{animationDelay: '200ms'}}>
          <div>
            <h3 className="text-sm font-semibold text-[#F5F5F5]">Case Categories</h3>
            <p className="text-xs text-[#525562] mt-0.5">Classification across Indian jurisprudence</p>
          </div>

          <div className="h-48 w-full my-auto flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={48}
                  outerRadius={72}
                  paddingAngle={4}
                  dataKey="value"
                  strokeWidth={0}
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#191B20', 
                    borderColor: '#2B2D33', 
                    borderRadius: '12px', 
                    color: '#F5F5F5',
                    fontSize: '11px',
                    boxShadow: '0 8px 30px -5px rgba(0,0,0,0.5)'
                  }} 
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-2 pt-3 border-t border-[#2B2D33]/40 text-xs">
            {categoryData.slice(0, 4).map((cat) => (
              <div key={cat.name} className="flex items-center justify-between group cursor-default">
                <div className="flex items-center gap-2.5">
                  <span className="w-2 h-2 rounded-full transition-transform group-hover:scale-150" style={{ backgroundColor: cat.color }} />
                  <span className="text-[#6E7079] text-[11px] group-hover:text-[#A5A7AD] transition-colors">{cat.name}</span>
                </div>
                <span className="text-[#F5F5F5] font-mono text-[11px]">{cat.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ═══════════════════════════════════════════
          4. RECENT DOCUMENTS TABLE — Premium
          ═══════════════════════════════════════════ */}
      <div className="card-premium overflow-hidden animate-fade-in-up" style={{animationDelay: '300ms'}}>
        {/* Table header & filters */}
        <div className="p-6 border-b border-[#2B2D33]/40 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-base font-semibold text-[#F5F5F5] flex items-center gap-2">
                <Clock className="w-4 h-4 text-[#8B7CFF]" />
                Recently Analyzed Cases
              </h2>
              <p className="text-xs text-[#525562] mt-0.5">
                Structured case records with verifiable quotations and SHA-256 hashes
              </p>
            </div>

            <span className="badge-violet text-[11px]">
              {filteredCases.length} judgments
            </span>
          </div>

          {/* Filters Bar */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#525562]" />
              <input
                type="text"
                placeholder="Filter by title or case no..."
                value={tableSearch}
                onChange={(e) => setTableSearch(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-[#08090B] border border-[#2B2D33]/60 rounded-xl text-xs text-[#F5F5F5] placeholder-[#525562] focus:outline-none focus:border-[#8B7CFF]/50 focus:ring-1 focus:ring-[#8B7CFF]/20 transition-all"
              />
            </div>

            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33]/60 rounded-xl text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]/50 cursor-pointer appearance-none"
            >
              <option value="All">All Categories</option>
              <option value="Constitutional">Constitutional</option>
              <option value="Criminal">Criminal</option>
              <option value="Corporate & Commercial">Corporate & Commercial</option>
              <option value="Arbitration">Arbitration</option>
            </select>

            <select
              value={selectedCourt}
              onChange={(e) => setSelectedCourt(e.target.value)}
              className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33]/60 rounded-xl text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]/50 cursor-pointer appearance-none"
            >
              <option value="All">All Courts</option>
              <option value="Supreme Court">Supreme Court of India</option>
              <option value="High Court">High Courts</option>
            </select>

            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full px-3 py-2 bg-[#08090B] border border-[#2B2D33]/60 rounded-xl text-xs text-[#F5F5F5] focus:outline-none focus:border-[#8B7CFF]/50 cursor-pointer appearance-none"
            >
              <option value="All">All Statuses</option>
              <option value="Verified">Verified</option>
              <option value="Requires Review">Requires Review</option>
            </select>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#08090B]/60 text-[#525562] uppercase tracking-wider text-[10px] border-b border-[#2B2D33]/40">
              <tr>
                <th className="py-3 px-5 font-semibold">Case Title</th>
                <th className="py-3 px-5 font-semibold">Court</th>
                <th className="py-3 px-5 font-semibold">Case Type</th>
                <th className="py-3 px-5 font-semibold">Decision Date</th>
                <th className="py-3 px-5 font-semibold">Analysis Status</th>
                <th className="py-3 px-5 font-semibold text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredCases.map((c, idx) => (
                <tr 
                  key={c.id} 
                  className="table-row group cursor-pointer animate-fade-in-up"
                  style={{animationDelay: `${idx * 50}ms`}}
                  onClick={() => openCaseDetails(c)}
                >
                  <td className="py-4 px-5">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-gradient-to-br from-[#191B20] to-[#111318] border border-[#2B2D33]/60 text-[#8B7CFF] group-hover:border-[#8B7CFF]/30 transition-colors">
                        <Scale className="w-3.5 h-3.5" />
                      </div>
                      <div>
                        <div className="font-semibold text-[#F5F5F5] group-hover:text-[#8B7CFF] transition-colors line-clamp-1 max-w-xs">
                          {c.title}
                        </div>
                        <div className="text-[10px] text-[#525562] font-mono mt-0.5">
                          {c.caseNumber}
                        </div>
                      </div>
                    </div>
                  </td>

                  <td className="py-4 px-5 text-[#6E7079] whitespace-nowrap">
                    {c.court}
                  </td>

                  <td className="py-4 px-5">
                    <span className="px-2.5 py-1 rounded-lg text-[10px] font-medium bg-[#191B20]/80 border border-[#2B2D33]/40 text-[#A5A7AD] whitespace-nowrap">
                      {c.category}
                    </span>
                  </td>

                  <td className="py-4 px-5 text-[#6E7079] font-mono text-[11px] whitespace-nowrap">
                    {c.judgmentDate}
                  </td>

                  <td className="py-4 px-5 whitespace-nowrap">
                    {c.status === 'Verified' ? (
                      <span className="badge-emerald inline-flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" />
                        <span>Verified ({c.verifiedClaimsCount}/{c.extractedClaimsCount})</span>
                      </span>
                    ) : (
                      <span className="badge-amber inline-flex items-center gap-1">
                        <AlertCircle className="w-3 h-3" />
                        <span>Review ({c.requiresReviewCount})</span>
                      </span>
                    )}
                  </td>

                  <td className="py-4 px-5 text-right whitespace-nowrap">
                    <div className="flex items-center justify-end gap-2" onClick={(e) => e.stopPropagation()}>
                      <button
                        type="button"
                        onClick={() => openCaseDetails(c)}
                        className="px-3 py-1.5 rounded-xl text-[11px] font-medium bg-[#191B20] hover:bg-[#8B7CFF] hover:text-[#08090B] text-[#8B7CFF] border border-[#8B7CFF]/20 transition-all inline-flex items-center gap-1.5 group/btn"
                      >
                        <Eye className="w-3 h-3" />
                        <span>View</span>
                      </button>
                      <button
                        type="button"
                        onClick={() => openCaseInViewer(c)}
                        className="p-1.5 rounded-xl text-[#525562] hover:text-[#F5F5F5] hover:bg-[#191B20] border border-transparent hover:border-[#2B2D33] transition-all"
                        title="Open Document Viewer"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Table footer */}
        <div className="p-4 border-t border-[#2B2D33]/40 flex items-center justify-between text-[11px] text-[#525562]">
          <span>Showing {filteredCases.length} of {cases.length} case records</span>
          <button
            type="button"
            onClick={() => setCurrentRoute('library')}
            className="flex items-center gap-1 text-[#8B7CFF] hover:text-[#9E91FF] transition-colors font-medium"
          >
            View Full Library
            <ArrowRight className="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  );
};
