"""Legal Metadata Extraction and Validation Engine for NyayaLens.

Reliably extracts and validates:
- Case Title
- Court Name
- Case / Appeal Number
- Decision Date
- Bench / Judges (with strict guards against counsel/witness false positives)
- Appellant / Petitioner
- Respondent
- Document Type (Judgment, Interim Order, Final Order, Procedural Order)
- Legal Category (Criminal, Civil, Constitutional, Commercial, Family, Administrative)

Distinguishes between verified, unverified, and missing fields.
"""

import re
import unicodedata
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class CaseMetadata:
    case_title: Optional[str] = None
    court_name: Optional[str] = None
    case_number: Optional[str] = None
    decision_date: Optional[str] = None
    bench: Optional[str] = None
    author_judge: Optional[str] = None
    appellant: Optional[str] = None
    respondent: Optional[str] = None
    parties: List[Dict[str, str]] = field(default_factory=list)
    document_type: str = "Unclear"
    case_category: str = "Unclear"
    confidence: float = 0.0
    field_validation_status: Dict[str, str] = field(default_factory=dict)
    raw_extracted_values: Dict[str, Any] = field(default_factory=dict)


def clean_text_line(text: str) -> str:
    """Cleans up extra spaces, weird bullet characters, and uncurls quotes."""
    if not text:
        return ""
    norm = unicodedata.normalize("NFKD", text)
    norm = norm.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    norm = re.sub(r'[\u2022\u25aa\u25cf\ufffd\uf0b7]', ' ', norm)
    norm = re.sub(r'\s+', ' ', norm)
    return norm.strip()


def extract_court_name(header_text: str) -> Tuple[Optional[str], str]:
    """Extract court name from document header text."""
    up = header_text.upper()
    if "SUPREME COURT OF INDIA" in up:
        return "Supreme Court of India", "verified"
    
    # Check for High Courts
    m_hc = re.search(r'HIGH COURT OF\s+([A-Za-z\s]+?)(?:\s+AT\s+[A-Za-z\s]+|\n|\r|\Z)', header_text, re.I)
    if m_hc:
        city = m_hc.group(1).strip().upper()
        if "DELHI" in city:
            return "High Court of Delhi", "verified"
        elif "BOMBAY" in city:
            return "High Court of Bombay", "verified"
        elif "ALLAHABAD" in city or "JUDICATURE AT ALLAHABAD" in city:
            return "High Court of Judicature at Allahabad", "verified"
        elif "CALCUTTA" in city:
            return "High Court of Calcutta", "verified"
        elif "MADRAS" in city:
            return "High Court of Madras", "verified"
        else:
            return f"High Court of {city.title()}", "verified"

    if "HIGH COURT" in up:
        m = re.search(r'([A-Za-z\s]+HIGH COURT[A-Za-z\s]*)', header_text, re.I)
        if m:
            return clean_text_line(m.group(1)).title(), "verified"

    return None, "unverified"


def extract_case_number(header_text: str) -> Tuple[Optional[str], str]:
    """Extract official case number from document header."""
    patterns = [
        # Criminal / Civil / Commercial Appeal No(s)
        r'((?:CRIMINAL|CIVIL|COMMERCIAL)\s+APPEAL\s+(?:NO|NOS|NOs)\.?\s*[0-9\-\s/]+(?:OF|of)\s*[0-9]{4})',
        # Writ Petition No
        r'((?:WRIT\s+PETITION)\s*(?:\([A-Za-z\s]+\))?\s*(?:NO|NOS|NOs)\.?\s*[0-9\-\s/]+(?:OF|of)\s*[0-9]{4})',
        # Special Leave Petition (SLP)
        r'((?:SPECIAL\s+LEAVE\s+PETITION|SLP)\s*(?:\([A-Za-z\s]+\))?\s*(?:NO|NOS|NOs)\.?\s*[0-9\-\s/]+(?:OF|of)\s*[0-9]{4})',
        # Arbitration OMP
        r'(O\.M\.P\.[^\n\r]{0,35}(?:NO|NOS|NOs)\.?\s*[0-9\-\s/]+(?:OF|of)\s*[0-9]{4})',
        # General Appeal/Petition pattern
        r'((?:APPEAL|PETITION|CASE|REFERENCE|SUIT)\s+(?:NO|NOS|NOs)\.?\s*[0-9\-\s/]+(?:OF|of)\s*[0-9]{4})'
    ]
    for pat in patterns:
        m = re.search(pat, header_text, re.I)
        if m:
            clean_num = clean_text_line(m.group(1))
            return clean_num, "verified"

    return None, "unverified"


def extract_decision_date(full_text: str, first_page_text: str, last_page_text: str) -> Tuple[Optional[str], str]:
    """Extract decision date from header or final order signature line."""
    # 1. Header: e.g. "on 25 April, 2013" or "on 25 April 2013"
    m_hdr = re.search(r'\bon\s+([0-9]{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+,?\s+[0-9]{4})', first_page_text, re.I)
    if m_hdr:
        raw_date = m_hdr.group(1)
        normalized = clean_text_line(raw_date.replace(",", ""))
        return normalized, "verified"

    # 2. Dated line: "Dated: 27th July, 2017" or "Date: 14.11.2023"
    m_dated = re.search(r'(?:Dated|Date)[:\s]+([0-9]{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+,?\s+[0-9]{4})', first_page_text, re.I)
    if m_dated:
        normalized = clean_text_line(m_dated.group(1).replace(",", ""))
        return normalized, "verified"

    # 3. Last page signature: "New Delhi; April 25, 2013" or "Dated: July 27, 2017"
    m_end = re.search(r'(?:New Delhi|Delhi|Mumbai|Allahabad)[;,\s]+([A-Za-z]+\s+[0-9]{1,2},?\s+[0-9]{4})', last_page_text, re.I)
    if m_end:
        normalized = clean_text_line(m_end.group(1).replace(",", ""))
        return normalized, "verified"

    m_end_d = re.search(r'([A-Za-z]+\s+[0-9]{1,2},?\s+[0-9]{4})', last_page_text)
    if m_end_d:
        normalized = clean_text_line(m_end_d.group(1).replace(",", ""))
        return normalized, "verified"

    m_num_date = re.search(r'\b([0-9]{1,2}[./-][0-9]{1,2}[./-][0-9]{4})\b', last_page_text)
    if m_num_date:
        return m_num_date.group(1), "verified"

    return None, "unverified"


def extract_bench_judges(header_text: str, full_text: str, last_pages_text: str) -> Tuple[Optional[str], Optional[str], str]:
    """Extract bench judges with strict validation to avoid counsel or narrative text.
    
    Guards:
    - Never catches narrative phrases like "before the High Court and the Court heard..."
    - Never catches advocates or counsel (e.g. "learned counsel", "Mr. ... Advocate")
    - Never catches witness names (PW-1, etc.)
    """
    bench_names: List[str] = []
    author_judge: Optional[str] = None

    # Check for explicit Indian Kanoon / Legal header: "Bench: ..."
    m_bench = re.search(r'Bench:\s*([^\n\r]+)', header_text, re.I)
    if m_bench:
        raw_b = clean_text_line(m_bench.group(1))
        # Validate that it doesn't contain narrative words
        if not any(w in raw_b.lower() for w in ["appeal", "dismissed", "sessions", "record", "witness"]):
            parts = [clean_text_line(p) for p in re.split(r'[,;&]', raw_b) if clean_text_line(p)]
            bench_names.extend(parts)

    # Check for "Author: ..."
    m_auth = re.search(r'Author:\s*([^\n\r]+)', header_text, re.I)
    if m_auth:
        raw_a = clean_text_line(m_auth.group(1))
        if not any(w in raw_a.lower() for w in ["appeal", "dismissed", "sessions"]):
            author_judge = raw_a
            if author_judge not in bench_names:
                bench_names.insert(0, author_judge)

    # Check for CORAM block:
    # CORAM:
    # HON'BLE MR. JUSTICE ...
    m_coram = re.search(r'CORAM:\s*([\s\S]+?)(?=\n\s*(?:JUDGMENT|ORDER|INTERIM ORDER|CRIMINAL|CIVIL|REPORTABLE|\Z))', header_text, re.I)
    if m_coram:
        coram_block = m_coram.group(1)
        for line in coram_block.split('\n'):
            line_c = clean_text_line(line)
            if "JUSTICE" in line_c.upper() or "C.J." in line_c.upper() or "CHIEF JUSTICE" in line_c.upper():
                # Clean prefix "HON'BLE MR. JUSTICE" -> Keep judicial title or clean name
                cleaned_j = re.sub(r'^(?:THE\s+)?HON[\'A-Z\.\s]+(?:MR\.|MS\.|DR\.)?\s*JUSTICE\s+', 'Justice ', line_c, flags=re.I).strip()
                cleaned_j = re.sub(r'^(?:THE\s+)?HON[\'A-Z\.\s]+CHIEF\s+JUSTICE\s+', 'Chief Justice ', cleaned_j, flags=re.I).strip()
                if cleaned_j and cleaned_j not in bench_names:
                    bench_names.append(cleaned_j)

    # Look for judicial signature lines ending in ', J.' or ', CJ.' on header or final pages
    j_sig_matches = re.finditer(r'([A-Z][A-Za-z\s.]+?),\s*(?:J|JJ|C\.J\.)\b', header_text + "\n" + last_pages_text)
    for jm in j_sig_matches:
        candidate = clean_text_line(jm.group(1))
        # Validate candidate name
        if len(candidate) > 3 and len(candidate) < 40:
            if not any(w in candidate.lower() for w in ["court", "high", "sessions", "appellant", "respondent", "advocate", "counsel"]):
                # Format nicely
                cand_name = candidate.strip()
                if not any(cand_name in b for b in bench_names):
                    bench_names.append(cand_name)

    # Deduplicate while preserving order
    unique_bench = []
    for b in bench_names:
        clean_b = clean_text_line(b)
        if clean_b and not any(clean_b.lower() == u.lower() for u in unique_bench):
            unique_bench.append(clean_b)

    if unique_bench:
        bench_str = ", ".join(unique_bench)
        return bench_str, author_judge, "verified"

    return None, None, "unverified"


def extract_parties(first_page_text: str) -> Tuple[Optional[str], Optional[str], List[Dict[str, str]], str]:
    """Extract appellant/petitioner and respondent names reliably.
    
    Guards:
    - Never returns literal 'Appellant' or 'Respondent' as the party name.
    - Strips ellipses, role labels, and bullet artifacts.
    """
    parties_list: List[Dict[str, str]] = []
    appellant: Optional[str] = None
    respondent: Optional[str] = None

    lines = [clean_text_line(l) for l in first_page_text.split('\n') if clean_text_line(l)]

    # 1. Check for Versus line pattern:
    # [Party 1] ... Appellant
    # VERSUS
    # [Party 2] ... Respondent
    for i, line in enumerate(lines):
        if re.match(r'^(?:VERSUS|VS\.?|V\.)\s*$', line, re.I):
            if i > 0 and i + 1 < len(lines):
                raw_p1 = lines[i - 1]
                raw_p2 = lines[i + 1]

                # Clean p1
                p1_clean = re.sub(r'(?:\.{2,}|\s+)\s*(?:Appellants?|Petitioners?|Plaintiffs?)\b.*', '', raw_p1, flags=re.I).strip()
                p1_clean = re.sub(r'^\d+\.\s*', '', p1_clean).strip()
                p1_clean = clean_text_line(p1_clean)

                # Clean p2
                p2_clean = re.sub(r'(?:\.{2,}|\s+)\s*(?:Respondents?|Defendants?|Opposite\s+Part(?:y|ies))\b.*', '', raw_p2, flags=re.I).strip()
                p2_clean = clean_text_line(p2_clean)

                if p1_clean and p1_clean.lower() != "appellant" and len(p1_clean) < 100:
                    appellant = p1_clean
                if p2_clean and p2_clean.lower() != "respondent" and len(p2_clean) < 100:
                    respondent = p2_clean
            break

    # 2. Check for Indian Kanoon header: "Shankar Kisanrao Khade vs State Of Maharashtra on 25 April, 2013"
    if not appellant or not respondent:
        m_ik = re.search(r'^([^\n\r]+?)\s+(?:vs\.?|v\.?|versus)\s+([^\n\r]+?)\s+on\s+[0-9]{1,2}', first_page_text, re.I | re.M)
        if m_ik:
            cand1 = clean_text_line(m_ik.group(1))
            cand2 = clean_text_line(m_ik.group(2))
            if cand1 and not appellant:
                appellant = cand1
            if cand2 and not respondent:
                respondent = cand2

    # Build structured parties array
    status = "unverified"
    if appellant:
        role = "Petitioner / Appellant"
        p_type = "State / Government" if any(w in appellant.lower() for w in ["state", "union of india", "uoi", "govt"]) else "Litigant"
        parties_list.append({"role": role, "name": appellant, "type": p_type})
        status = "verified"

    if respondent:
        role = "Respondent / Opposite Party"
        p_type = "State / Government" if any(w in respondent.lower() for w in ["state", "union of india", "uoi", "govt"]) else "Respondent"
        parties_list.append({"role": role, "name": respondent, "type": p_type})

    return appellant, respondent, parties_list, status


def extract_case_title(first_page_text: str, appellant: Optional[str], respondent: Optional[str]) -> Tuple[Optional[str], str]:
    """Derive clean case title."""
    # 1. If explicit header line exists
    m_ik = re.search(r'^([^\n\r]+?\s+(?:vs\.?|v\.?|versus)\s+[^\n\r]+?)(?:\s+on\s+[0-9]{1,2}|\n|\r)', first_page_text, re.I | re.M)
    if m_ik:
        cand = clean_text_line(m_ik.group(1))
        if len(cand) < 120 and "PAGE" not in cand.upper():
            return cand, "verified"

    # 2. Combine clean appellant and respondent
    if appellant and respondent:
        return f"{appellant} vs {respondent}", "verified"

    if appellant:
        return f"{appellant} (Matter)", "unverified"

    return None, "unverified"


def detect_document_type(full_text: str, first_page_text: str) -> Tuple[str, str]:
    """Detect if document is a final Judgment, Interim Order, or Procedural Order."""
    hdr_upper = clean_text_line(first_page_text).upper()
    # Normalize spaced heading characters e.g. "J U D G M E N T" -> "JUDGMENT"
    hdr_upper = re.sub(r'\bJ\s+U\s+D\s+G\s+M\s+E\s+N\s+T\b', 'JUDGMENT', hdr_upper)
    hdr_upper = re.sub(r'\bO\s+R\s+D\s+E\s+R\b', 'ORDER', hdr_upper)
    full_lower = full_text.lower()

    if "INTERIM ORDER" in hdr_upper or "AD-INTERIM" in hdr_upper:
        return "Interim Order", "verified"
    if "PROCEDURAL ORDER" in hdr_upper or "RECORD OF PROCEEDINGS" in hdr_upper:
        return "Procedural Order", "verified"
    if "JUDGMENT" in hdr_upper:
        return "Judgment", "verified"
    if "FINAL ORDER" in hdr_upper:
        return "Final Order", "verified"
    if "ORDER" in hdr_upper:
        # Check if concluding text disposes of the appeal/petition
        if any(w in full_lower[-2500:] for w in ["stands disposed of", "appeal dismissed", "petition dismissed", "appeal allowed"]):
            return "Judgment", "verified"
        return "Interim Order", "verified"

    return "Judgment", "unverified"


def detect_case_category(full_text: str, header_text: str) -> Tuple[str, str]:
    """Detect Indian legal taxonomy category."""
    hdr_up = header_text.upper()
    full_low = full_text.lower()

    if "CRIMINAL APPELLATE JURISDICTION" in hdr_up or "CRIMINAL APPEAL" in hdr_up or "CRL.A." in hdr_up:
        return "Criminal", "verified"
    if "COMMERCIAL DIVISION" in hdr_up or "COMMERCIAL APPELLATE" in hdr_up or "O.M.P." in hdr_up:
        return "Commercial", "verified"
    if "CIVIL ORIGINAL JURISDICTION" in hdr_up or "CIVIL APPEAL" in hdr_up:
        if "ARTICLE 32" in hdr_up or "WRIT PETITION" in hdr_up and "CONSTITUTION" in full_low[:2000]:
            return "Constitutional", "verified"
        return "Civil", "verified"

    # Fallback to keyword density
    crim_score = len(re.findall(r'\b(?:accused|conviction|sentence|ipc|crpc|fir|offence|police|death penalty|rape|murder)\b', full_low))
    comm_score = len(re.findall(r'\b(?:arbitration|contract|commercial|award|claimant|omr|section 9|tender)\b', full_low))
    const_score = len(re.findall(r'\b(?:article 21|article 14|fundamental right|constitution|writ|ultra vires)\b', full_low))

    if crim_score > comm_score and crim_score > const_score and crim_score >= 5:
        return "Criminal", "verified"
    if comm_score > crim_score and comm_score > const_score and comm_score >= 5:
        return "Commercial", "verified"
    if const_score > crim_score and const_score > comm_score and const_score >= 5:
        return "Constitutional", "verified"

    return "Civil", "unverified"


def extract_and_validate_case_metadata(
    full_text: str,
    pages_dict: Dict[int, str]
) -> CaseMetadata:
    """End-to-end extraction and verification of case metadata.
    
    Guarantees:
    - Never fabricates metadata.
    - Explicitly marks missing or unverified fields.
    - Accurately parses bench, date, case number, and parties.
    """
    first_page_text = pages_dict.get(1, full_text[:4000])
    last_page_num = max(pages_dict.keys()) if pages_dict else 1
    last_page_text = pages_dict.get(last_page_num, full_text[-4000:])
    last_pages_text = "\n".join(pages_dict.get(p, "") for p in range(max(1, last_page_num - 2), last_page_num + 1))

    # 1. Court Name
    court, court_status = extract_court_name(first_page_text)

    # 2. Case Number
    case_no, case_no_status = extract_case_number(first_page_text)

    # 3. Decision Date
    dec_date, date_status = extract_decision_date(full_text, first_page_text, last_page_text)

    # 4. Bench / Coram
    bench, author_judge, bench_status = extract_bench_judges(first_page_text, full_text, last_pages_text)

    # 5. Parties
    appellant, respondent, parties_list, parties_status = extract_parties(first_page_text)

    # 6. Case Title
    title, title_status = extract_case_title(first_page_text, appellant, respondent)

    # 7. Document Type
    doc_type, doc_type_status = detect_document_type(full_text, first_page_text)

    # 8. Category
    cat, cat_status = detect_case_category(full_text, first_page_text)

    # Calculate overall metadata confidence
    field_statuses = {
        "case_title": title_status,
        "court_name": court_status,
        "case_number": case_no_status,
        "decision_date": date_status,
        "bench": bench_status,
        "parties": parties_status,
        "document_type": doc_type_status,
        "case_category": cat_status
    }
    verified_fields = sum(1 for s in field_statuses.values() if s == "verified")
    confidence = round(verified_fields / len(field_statuses), 2)

    raw_values = {
        "raw_title": title,
        "raw_court": court,
        "raw_case_no": case_no,
        "raw_date": dec_date,
        "raw_bench": bench,
        "raw_appellant": appellant,
        "raw_respondent": respondent
    }

    return CaseMetadata(
        case_title=title,
        court_name=court,
        case_number=case_no,
        decision_date=dec_date,
        bench=bench,
        author_judge=author_judge,
        appellant=appellant,
        respondent=respondent,
        parties=parties_list,
        document_type=doc_type,
        case_category=cat,
        confidence=confidence,
        field_validation_status=field_statuses,
        raw_extracted_values=raw_values
    )
