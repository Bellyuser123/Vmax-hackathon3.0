"""Legal Classification taxonomy, heuristic analysis, and schema definitions for NyayaLens."""

import re
from typing import Dict, List, Optional, Tuple
from config import CASE_CATEGORIES, DOCUMENT_TYPES


def heuristic_detect_case_type(text: str) -> Tuple[str, float]:
    """Analyzes text for key Indian legal keywords to provide heuristic classification.

    Returns:
        (category, confidence_score)
    """
    if not text or len(text.strip()) < 50:
        return "Unclear", 0.0

    lower = text.lower()

    # Scores
    scores: Dict[str, int] = {cat: 0 for cat in CASE_CATEGORIES}

    # Criminal markers
    criminal_keywords = [
        "criminal appeal", "crl.a.", "crl.m.c.", "bail application", "anticipatory bail",
        "first information report", "fir no", "police station", "ipc", "indian penal code",
        "crpc", "code of criminal procedure", "bns", "bharatiya nyaya", "accused", "conviction",
        "acquittal", "charge sheet", "cognizance", "sections 302", "sections 420", "section 376",
        "narcotic drugs", "ndps act", "prevention of corruption"
    ]
    for kw in criminal_keywords:
        if kw in lower:
            scores["Criminal"] += 2

    # Constitutional markers
    constitutional_keywords = [
        "writ petition", "w.p.", "article 32", "article 226", "article 136", "article 21",
        "article 14", "article 19", "constitution of india", "fundamental right",
        "ultra vires", "mandamus", "certiorari", "habeas corpus", "public interest litigation", "pil"
    ]
    for kw in constitutional_keywords:
        if kw in lower:
            scores["Constitutional"] += 2

    # Commercial markers
    commercial_keywords = [
        "arbitration and conciliation act", "section 11", "section 34", "section 9",
        "arbitral tribunal", "insolvency and bankruptcy code", "ibc", "nclt", "nclat",
        "commercial suit", "commercial court", "negotiable instruments act", "section 138",
        "cheque bounce", "companies act", "breach of contract", "trademark", "patent infringement"
    ]
    for kw in commercial_keywords:
        if kw in lower:
            scores["Commercial"] += 2

    # Family markers
    family_keywords = [
        "hindu marriage act", "divorce petition", "family court", "restitution of conjugal",
        "section 13(1)", "section 125 crpc", "maintenance", "child custody", "guardianship",
        "domestic violence act", "protection of women from domestic", "special marriage act"
    ]
    for kw in family_keywords:
        if kw in lower:
            scores["Family"] += 2

    # Administrative markers
    admin_keywords = [
        "central administrative tribunal", "cat", "service matter", "disciplinary proceedings",
        "suspension order", "pensionary benefits", "promotion dispute", "public service commission",
        "departmental inquiry", "government employee", "civil services"
    ]
    for kw in admin_keywords:
        if kw in lower:
            scores["Administrative"] += 2

    # Civil markers
    civil_keywords = [
        "regular first appeal", "rfa", "second appeal", "code of civil procedure", "cpc",
        "order vii rule 11", "order 39", "injunction", "specific performance", "partition suit",
        "title suit", "transfer of property act", "declaration and possession", "mesne profits"
    ]
    for kw in civil_keywords:
        if kw in lower:
            scores["Civil"] += 2

    # Evaluate best category
    best_cat = max(scores, key=lambda k: scores[k])
    best_score = scores[best_cat]

    if best_score < 3:
        return "Unclear", 0.2

    # Normalize confidence
    confidence = min(0.95, 0.4 + (best_score * 0.05))
    return best_cat, confidence


def heuristic_detect_doc_type(text: str) -> Tuple[str, float]:
    """Detects whether document is Judgment, Final Order, Interim Order, or Procedural Order."""
    if not text:
        return "Unclear", 0.0

    lower = text.lower()

    if "interim order" in lower or "ad-interim" in lower or "stay granted until" in lower or "pending final disposal" in lower:
        return "Interim Order", 0.85

    if "procedural order" in lower or "notice issued" in lower or "re-notify on" in lower or "list the matter on" in lower:
        return "Procedural Order", 0.80

    if "judgment" in lower or "delivered the following judgment" in lower or "per curiam" in lower:
        return "Judgment", 0.90

    if "final order" in lower or "disposed of accordingly" in lower:
        return "Final Order", 0.85

    return "Unclear", 0.3
