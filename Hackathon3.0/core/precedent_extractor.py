"""Precedent and Judicial Citation Extraction Engine for NyayaLens.

Identifies previous landmark judgments cited in Indian court judgments:
- Case Name (e.g., 'Bachan Singh v. State of Punjab')
- Reporter Citation (e.g., '(1980) 2 SCC 684', 'AIR 1980 SC 898')
- Proposition / How Used (e.g., 'Rarest of rare doctrine; mitigating vs aggravating circumstances')
- Supporting Quote (full clean sentence)
- Source Page Number
"""

import re
import unicodedata
from typing import Dict, List, Optional, Any, Tuple


def clean_text(text: str) -> str:
    norm = unicodedata.normalize("NFKD", text)
    norm = norm.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    norm = re.sub(r'[\u2022\u25aa\u25cf\ufffd\uf0b7]', ' ', norm)
    norm = re.sub(r'\s+', ' ', norm).strip()
    return norm


def extract_precedents_cited(
    pages_dict: Dict[int, str],
    max_precedents: int = 8
) -> List[Dict[str, Any]]:
    """Extract precedent case citations across all pages of the judgment."""
    precedents: List[Dict[str, Any]] = []
    seen_cases = set()

    # Pattern matching: Party v. Party / State of ... (YEAR) VOL REPORTER PAGE
    # e.g. Bachan Singh v. State of Punjab, (1980) 2 SCC 684
    # e.g. Swamy Shraddananda (2) v. State of Karnataka, (2008) 13 SCC 767
    case_regex = re.compile(
        r'([A-Z][A-Za-z0-9\s.,\(\)]+?\s+(?:v\.|vs\.|versus)\s+[A-Z][A-Za-z0-9\s.,\(\)]+?)(?:,?\s*(\([0-9]{4}\)\s*[0-9]+\s*(?:SCC|SCR|AIR|CrLJ|CriLJ)[A-Za-z0-9\s\(\)]*|\bAIR\s+[0-9]{4}\s+[A-Za-z\s]+[0-9]+))?',
        re.M
    )

    for p_num in sorted(pages_dict.keys()):
        p_text = pages_dict[p_num]
        sentences = re.split(r'(?<=[.!?])\s+', p_text)

        for sent in sentences:
            clean_s = clean_text(sent)
            if len(clean_s) < 30 or "Versus" in clean_s[:15]:
                continue

            matches = list(case_regex.finditer(clean_s))
            for m in matches:
                case_raw = m.group(1).strip()
                cite_raw = m.group(2).strip() if m.group(2) else ""

                # Filter out current case or generic text
                if any(w in case_raw.lower() for w in ["appellant preferred", "the accused", "this court", "high court dismissed", "criminal appeal"]):
                    continue

                # Clean case name
                clean_name = re.sub(r'^\d+\.\s*', '', case_raw).strip()
                clean_name = re.sub(r'\s+', ' ', clean_name)

                # Must look like a real case title
                if len(clean_name) < 8 or len(clean_name) > 75:
                    continue

                case_key = clean_name.lower().split(" v.")[0].split(" vs.")[0].strip()
                if case_key in seen_cases or len(case_key) < 3:
                    continue

                seen_cases.add(case_key)

                # Determine proposition context
                prop_desc = "Cited as judicial precedent."
                s_low = clean_s.lower()
                if "rarest of rare" in s_low:
                    prop_desc = "Rarest of rare doctrine; sentencing guidelines for capital punishment."
                elif "life sentence" in s_low or "imprisonment for life" in s_low:
                    prop_desc = "Interpretation of sentence of imprisonment for life (remainder of natural life)."
                elif "circumstantial evidence" in s_low:
                    prop_desc = "Standards for conviction based on circumstantial evidence."
                elif "aggravating" in s_low or "mitigating" in s_low:
                    prop_desc = "Balancing aggravating circumstances (crime test) and mitigating circumstances (criminal test)."
                elif "quash" in s_low or "section 482" in s_low:
                    prop_desc = "Principles governing inherent powers to quash criminal proceedings."
                elif "privacy" in s_low or "article 21" in s_low:
                    prop_desc = "Fundamental right to privacy under Article 21."
                elif "arbitrat" in s_low or "section 9" in s_low:
                    prop_desc = "Principles governing interim measures under the Arbitration Act."

                full_citation = f"{clean_name}, {cite_raw}".rstrip(", ") if cite_raw else clean_name

                precedents.append({
                    "case_name": clean_name,
                    "citation": cite_raw or "Reported citation identified in judgment text",
                    "full_reference": full_citation,
                    "how_used": prop_desc,
                    "supporting_quote": clean_s,
                    "page_number": p_num
                })

                if len(precedents) >= max_precedents:
                    break
        if len(precedents) >= max_precedents:
            break

    return precedents
