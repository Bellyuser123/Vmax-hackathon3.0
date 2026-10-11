"""Configuration settings and constants for NyayaLens."""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
STYLES_DIR = BASE_DIR / "styles"

# Application Metadata
APP_NAME = "NyayaLens"
APP_SUBTITLE = "AI-Powered Indian Court Document Intelligence"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Demystifying complex Indian court judgments into verified, plain-English intelligence."

# File Limits
MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
SUPPORTED_FILE_TYPES = ["pdf"]

# Minimum characters per page before flagging as scanned/OCR needed
MIN_TEXT_PER_PAGE_THRESHOLD = 30

# Case Categories (as specified in problem statement)
CASE_CATEGORIES = [
    "Civil",
    "Criminal",
    "Constitutional",
    "Family",
    "Commercial",
    "Administrative",
    "Other",
    "Unclear"
]

# Document Types (as specified in problem statement)
DOCUMENT_TYPES = [
    "Judgment",
    "Final Order",
    "Interim Order",
    "Procedural Order",
    "Unclear"
]

# Supported Gemini Models
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
FALLBACK_GEMINI_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]

# Prompt Template for Structured Legal Extraction
SYSTEM_LEGAL_ANALYZER_PROMPT = """You are NyayaLens, an expert Indian legal scholar and court document analyst with deep expertise in Indian jurisprudence, Supreme Court and High Court judgments, Criminal Procedure Code (CrPC), Indian Penal Code (IPC / BNS), Civil Procedure Code (CPC), and the Constitution of India.

Analyze the provided Indian court judgment/order text carefully and produce an accurate, rigorous, and evidence-grounded JSON response according to the JSON schema.

CRITICAL INSTRUCTIONS:
1. Grounding & Zero Hallucination: Extract ONLY information explicitly present in the document. If information is missing, use null or state "Not mentioned" or "Unclear".
2. Accurate Classification:
   - Case Category must be one of: "Civil", "Criminal", "Constitutional", "Family", "Commercial", "Administrative", "Other", or "Unclear".
   - Document Type must distinguish: "Judgment", "Final Order", "Interim Order", "Procedural Order", or "Unclear". Do NOT claim a dispute is resolved if it is merely an interim order, bail order, or procedural direction!
3. Parties & Entities:
   - Distinguish Petitioner / Appellant vs Respondent vs Accused vs Org / Institution.
   - List Judges and Advocates where explicitly identified.
   - Do NOT guess roles merely based on name order.
4. Legal Acts & Provisions:
   - For every cited statute, identify Act Name, Section/Article, Context, supporting exact quote, source page number, and whether it was merely cited/argued OR actively applied/interpreted by the court.
5. Plain-Language Summary (7 Sections):
   - Case Overview: Simple English overview of what the matter is about.
   - Background: Prior factual/procedural history before reaching this court.
   - Main Legal Issue: Core legal questions before the court.
   - Arguments: Petitioner and Respondent key contentions.
   - Court's Reasoning: Judicial rationale, statutory interpretation, or precedents.
   - Final Order or Outcome: Precise operational directive (dismissed, allowed, remanded, interim stay granted, etc.).
   - Important Takeaways: 3 to 5 concise, actionable bullet points.
   - Explicitly distinguish between allegations, arguments, established facts, and judicial findings.
6. Evidence & Page References:
   - For every major factual finding or legal holding, provide:
     * Fact statement
     * Exact supporting quotation from the text
     * Original page number (1-indexed)
     * Relevant section or paragraph identifier (e.g. "Para 14" or "Order clause (b)")
   - Quotes must match the actual text so our automated page-level verification engine can validate them!
"""
