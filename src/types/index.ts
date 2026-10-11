export type CaseCategory = 
  | 'Constitutional' 
  | 'Criminal' 
  | 'Civil' 
  | 'Corporate & Commercial' 
  | 'Arbitration' 
  | 'Taxation' 
  | 'Other';

export type AnalysisStatus = 'Verified' | 'Requires Review' | 'Processing' | 'Failed';

export type Disposition = 
  | 'Allowed' 
  | 'Dismissed' 
  | 'Partly Allowed' 
  | 'Remanded' 
  | 'Disposed of' 
  | 'Unable to determine confidently';

export type SummaryLength = 'quick' | 'standard' | 'detailed' | 'comprehensive';

export type ProvisionTreatment = 'Mentioned' | 'Discussed' | 'Interpreted' | 'Applied';

export type EvidenceVerificationStatus = 
  | 'Matched to source text' 
  | 'Needs human review' 
  | 'Source not found' 
  | 'Uncertain';

export interface LegalProvision {
  act: string;
  sectionOrArticle: string;
  description: string;
  treatment: ProvisionTreatment;
  supportingQuotation: string;
  pageNumber: number;
}

export interface IssueAndArgument {
  issue: string;
  petitionerArguments: string[];
  respondentArguments: string[];
  courtFindings: string;
}

export interface EvidenceReference {
  id: string;
  claim: string;
  exactQuotation: string;
  pageNumber: number;
  paragraph?: string;
  verificationStatus: EvidenceVerificationStatus;
  confidence: number;
  context: string;
}

export interface RelatedCase {
  id: string;
  title: string;
  court: string;
  decisionDate: string;
  category: CaseCategory;
  relevantProvisions: string[];
  similarityReason: string;
  sourceLink: string;
  relevanceScore: number;
  sharedFactors: string[];
}

export interface DocumentPage {
  pageNumber: number;
  courtHeader: string;
  judgmentDate: string;
  paragraphs: {
    paraNumber?: string;
    text: string;
    type?: 'provision' | 'argument' | 'finding' | 'outcome' | 'standard';
    isEvidenceTarget?: boolean;
    evidenceId?: string;
    provisionRef?: string;
  }[];
}

export interface CaseRecord {
  id: string;
  title: string;
  caseNumber: string;
  court: string;
  bench: string[];
  judgmentDate: string;
  category: CaseCategory;
  documentType: 'Judgment' | 'Order' | 'Interim Order' | 'Decree';
  status: AnalysisStatus;
  uploadDate: string;
  fileSize: string;
  pageCount: number;
  fileName: string;
  sha256Hash: string;
  integrityStatus: 'Untampered' | 'Unverified' | 'Mismatch';
  extractedClaimsCount: number;
  verifiedClaimsCount: number;
  requiresReviewCount: number;
  
  // Configurable summary lengths
  selectedSummaryLength: SummaryLength;
  outputLanguage: string;
  summaries: {
    quick: string;         // 100-150 words
    standard: string;      // 250-350 words
    detailed: string;      // 500-700 words
    comprehensive: string; // 1,000-1,500 words
  };
  executiveSummary: string; // default active view
  disputeBackground: string;
  
  parties: {
    petitioner: string[];
    respondent: string[];
    petitionerCounsel: string[];
    respondentCounsel: string[];
  };
  
  legalProvisions: LegalProvision[];
  issuesAndArguments: IssueAndArgument[];
  
  finalOutcome: {
    disposition: Disposition;
    confidence: number;
    summary: string;
    orderDirection: string;
  };
  
  evidenceReferences: EvidenceReference[];
  relatedCases: RelatedCase[];
  pages: DocumentPage[];
}

export interface ActivityItem {
  id: string;
  timestamp: string;
  action: 'Document Upload' | 'Analysis Completed' | 'Integrity Check' | 'Report Exported' | 'Review Flagged';
  caseTitle: string;
  caseId: string;
  status: 'success' | 'warning' | 'info' | 'error';
  details: string;
  user: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  type: 'verification' | 'system' | 'analysis';
}
