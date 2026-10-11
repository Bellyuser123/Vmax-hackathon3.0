"""Evidence and Citation Verification Engine for NyayaLens.

Validates that AI-extracted legal quotations, facts, and statutory provisions
actually exist verbatim or with high fidelity in the page-level PDF text.
Labels citations as 'Verified', 'Page Corrected', 'Partial Match', or 'Unverified / Uncertain'.
"""

import re
import unicodedata
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class VerificationStatus(str, Enum):
    VERIFIED_EXACT = "Verified (Exact Match)"
    VERIFIED_PARTIAL = "Verified (High Confidence)"
    PAGE_CORRECTED = "Verified on Adjacent Page"
    UNVERIFIED = "Unverified / Uncertain"


@dataclass
class VerificationResult:
    fact: str
    quote: str
    claimed_page: int
    actual_page: Optional[int]
    status: VerificationStatus
    confidence: float
    matched_snippet: str
    section_or_para: Optional[str] = None
    notes: Optional[str] = None

    @property
    def is_verified(self) -> bool:
        return self.status in [
            VerificationStatus.VERIFIED_EXACT,
            VerificationStatus.VERIFIED_PARTIAL,
            VerificationStatus.PAGE_CORRECTED
        ]

    @property
    def badge_color(self) -> str:
        if self.status == VerificationStatus.VERIFIED_EXACT:
            return "#10b981"  # Emerald green
        elif self.status == VerificationStatus.VERIFIED_PARTIAL:
            return "#06b6d4"  # Cyan
        elif self.status == VerificationStatus.PAGE_CORRECTED:
            return "#f59e0b"  # Amber
        else:
            return "#ef4444"  # Crimson / Red


def normalize_text_for_search(text: str) -> str:
    """Normalizes text by removing diacritics, uncurling quotes, collapsing whitespace."""
    if not text:
        return ""
    # Unicode normalize
    norm = unicodedata.normalize("NFKD", text)
    # Replace curly quotes and apostrophes
    norm = norm.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    norm = norm.replace("—", "-").replace("–", "-")
    # De-hyphenate broken words across line breaks (e.g. "dis-\npute" -> "dispute")
    norm = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', norm)
    # Collapse multiple whitespaces and newlines
    norm = re.sub(r'\s+', ' ', norm)
    return norm.strip().lower()


def find_quote_in_page(
    quote: str,
    page_text: str
) -> Tuple[bool, float, str]:
    """Checks if quote is present in page text, returning (found, confidence, snippet)."""
    if not quote or not page_text:
        return False, 0.0, ""

    norm_quote = normalize_text_for_search(quote)
    norm_page = normalize_text_for_search(page_text)

    if not norm_quote:
        return False, 0.0, ""

    # 1. Exact normalized substring match
    if norm_quote in norm_page:
        idx = norm_page.find(norm_quote)
        start = max(0, idx - 60)
        end = min(len(norm_page), idx + len(norm_quote) + 60)
        snippet = norm_page[start:end]
        return True, 1.0, f"...{snippet}..."

    # 2. Key phrases match (if quote is long, check if 80%+ contiguous phrases match)
    words = norm_quote.split()
    if len(words) >= 6:
        # Check first 5 words and last 5 words
        first_phrase = " ".join(words[:5])
        last_phrase = " ".join(words[-5:])
        if first_phrase in norm_page and last_phrase in norm_page:
            p1 = norm_page.find(first_phrase)
            p2 = norm_page.find(last_phrase)
            if p2 > p1 and (p2 - p1) < (len(norm_quote) * 2):
                start = max(0, p1 - 40)
                end = min(len(norm_page), p2 + len(last_phrase) + 40)
                return True, 0.92, f"...{norm_page[start:end]}..."

        # Check middle 70% window
        mid_len = max(4, int(len(words) * 0.7))
        mid_phrase = " ".join(words[:mid_len])
        if mid_phrase in norm_page:
            p = norm_page.find(mid_phrase)
            start = max(0, p - 40)
            end = min(len(norm_page), p + len(mid_phrase) + 60)
            return True, 0.85, f"...{norm_page[start:end]}..."

    # 3. Sliding window token overlap for slight OCR/transcription variations
    if len(words) >= 4:
        # Check if 85% of unique significant words exist in close proximity
        sig_words = [w for w in words if len(w) > 3]
        if sig_words:
            found_count = sum(1 for w in sig_words if w in norm_page)
            ratio = found_count / len(sig_words)
            if ratio >= 0.85 and sig_words[0] in norm_page:
                p = norm_page.find(sig_words[0])
                start = max(0, p - 40)
                end = min(len(norm_page), p + 180)
                return True, 0.80, f"...{norm_page[start:end]}..."

    return False, 0.0, ""


def verify_evidence_item(
    fact: str,
    quote: str,
    claimed_page: int,
    pdf_pages_dict: Dict[int, str],
    section_or_para: Optional[str] = None
) -> VerificationResult:
    """Verifies a single evidence quotation against PDF page contents."""
    if not quote or not quote.strip():
        return VerificationResult(
            fact=fact,
            quote=quote or "No quote provided",
            claimed_page=claimed_page,
            actual_page=None,
            status=VerificationStatus.UNVERIFIED,
            confidence=0.0,
            matched_snippet="",
            section_or_para=section_or_para,
            notes="No supporting quotation was provided by the AI."
        )

    # 1. First, check claimed page
    claimed_page_text = pdf_pages_dict.get(claimed_page, "")
    found, conf, snippet = find_quote_in_page(quote, claimed_page_text)

    if found:
        status = VerificationStatus.VERIFIED_EXACT if conf >= 0.98 else VerificationStatus.VERIFIED_PARTIAL
        return VerificationResult(
            fact=fact,
            quote=quote,
            claimed_page=claimed_page,
            actual_page=claimed_page,
            status=status,
            confidence=conf,
            matched_snippet=snippet,
            section_or_para=section_or_para,
            notes=f"Corroborated on cited Page {claimed_page} with {int(conf * 100)}% match."
        )

    # 2. Check adjacent pages (claimed_page - 1, claimed_page + 1)
    for offset in [-1, 1, -2, 2]:
        adj_page = claimed_page + offset
        if adj_page in pdf_pages_dict:
            adj_text = pdf_pages_dict[adj_page]
            found_adj, conf_adj, snippet_adj = find_quote_in_page(quote, adj_text)
            if found_adj:
                return VerificationResult(
                    fact=fact,
                    quote=quote,
                    claimed_page=claimed_page,
                    actual_page=adj_page,
                    status=VerificationStatus.PAGE_CORRECTED,
                    confidence=conf_adj * 0.95,
                    matched_snippet=snippet_adj,
                    section_or_para=section_or_para,
                    notes=f"Original citation specified Page {claimed_page}, but text verified on Page {adj_page}."
                )

    # 3. Check all other pages
    for p_num, p_text in pdf_pages_dict.items():
        if p_num in [claimed_page, claimed_page - 1, claimed_page + 1]:
            continue
        found_other, conf_other, snippet_other = find_quote_in_page(quote, p_text)
        if found_other:
            return VerificationResult(
                fact=fact,
                quote=quote,
                claimed_page=claimed_page,
                actual_page=p_num,
                status=VerificationStatus.PAGE_CORRECTED,
                confidence=conf_other * 0.90,
                matched_snippet=snippet_other,
                section_or_para=section_or_para,
                notes=f"Citation relocated: Located on Page {p_num} (cited as Page {claimed_page})."
            )

    # 4. Not found anywhere
    return VerificationResult(
        fact=fact,
        quote=quote,
        claimed_page=claimed_page,
        actual_page=None,
        status=VerificationStatus.UNVERIFIED,
        confidence=0.0,
        matched_snippet="",
        section_or_para=section_or_para,
        notes="Uncorroborated: The exact text could not be verified in the extracted document pages. Flagged as uncertain."
    )


def verify_all_evidence(
    evidence_items: List[Dict[str, Any]],
    pdf_pages_dict: Dict[int, str]
) -> List[VerificationResult]:
    """Verifies a list of evidence dicts from AI output against PDF page text dictionary."""
    results = []
    for item in evidence_items:
        fact = item.get("fact", "")
        quote = item.get("quote", "")
        page = item.get("page", 1)
        if isinstance(page, str):
            try:
                page = int(re.sub(r'[^\d]', '', page))
            except Exception:
                page = 1

        sec = item.get("section_or_para", "") or item.get("paragraph", "")
        res = verify_evidence_item(
            fact=fact,
            quote=quote,
            claimed_page=page,
            pdf_pages_dict=pdf_pages_dict,
            section_or_para=sec
        )
        results.append(res)
    return results


def verify_legal_provisions(
    provisions: List[Dict[str, Any]],
    pdf_pages_dict: Dict[int, str]
) -> List[Dict[str, Any]]:
    """Verifies supporting quotes of legal provisions against the document."""
    verified_provisions = []
    for prov in provisions:
        quote = prov.get("supporting_quote", "")
        page = prov.get("page_number", 1)
        if isinstance(page, str):
            try:
                page = int(re.sub(r'[^\d]', '', page))
            except Exception:
                page = 1

        if quote:
            ver = verify_evidence_item(
                fact=f"{prov.get('act_name', '')} {prov.get('section_or_article', '')}",
                quote=quote,
                claimed_page=page,
                pdf_pages_dict=pdf_pages_dict
            )
            prov_copy = dict(prov)
            prov_copy["verification_status"] = ver.status.value
            prov_copy["is_verified"] = ver.is_verified
            prov_copy["verification_badge_color"] = ver.badge_color
            prov_copy["verified_page"] = ver.actual_page or page
            prov_copy["verification_notes"] = ver.notes
            verified_provisions.append(prov_copy)
        else:
            prov_copy = dict(prov)
            prov_copy["verification_status"] = VerificationStatus.UNVERIFIED.value
            prov_copy["is_verified"] = False
            prov_copy["verification_badge_color"] = "#ef4444"
            prov_copy["verified_page"] = page
            prov_copy["verification_notes"] = "No quote cited in document."
            verified_provisions.append(prov_copy)

    return verified_provisions
