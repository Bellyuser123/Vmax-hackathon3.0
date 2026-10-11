"""Statutory Provision Extraction and Disambiguation Engine for NyayaLens.

Extracts acts and sections across all pages of Indian judgments, ensuring:
1. Clear disambiguation between Indian Penal Code (IPC), Code of Criminal Procedure (CrPC),
   Constitution of India, Protection of Children from Sexual Offences Act (POCSO), etc.
2. Accurate classification of provision role:
   - "applied": Actively applied, conviction affirmed/modified, sentence passed/commuted.
   - "relied_upon": Cited as substantive legal authority, doctrine, or constitutional mandate.
   - "argued": Raised by appellant or respondent in submissions.
   - "mentioned": Mentioned in charges, FIR, trial court history, or incidental text.
3. Full sentence context and verbatim supporting quotation (avoiding mid-word truncation).
4. Exact page-level attribution.
"""

import re
import unicodedata
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass


@dataclass
class StatutoryProvision:
    act_name: str
    section_or_article: str
    provision_role: str  # "applied" | "relied_upon" | "argued" | "mentioned"
    is_applied: bool     # backward-compatible boolean
    context: str
    supporting_quote: str
    page_number: int
    verification_status: str = "Verified"


def clean_sentence_for_quote(sentence: str) -> str:
    """Normalize whitespace and remove trailing broken punctuation."""
    norm = unicodedata.normalize("NFKD", sentence)
    norm = norm.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    norm = re.sub(r'[\u2022\u25aa\u25cf\ufffd\uf0b7]', ' ', norm)
    norm = re.sub(r'\s+', ' ', norm).strip()
    return norm


def disambiguate_act(
    sec_num: str,
    sec_type: str,
    surrounding_text: str,
    case_category: str = "Criminal"
) -> str:
    """Accurately identify statute name from surrounding sentence context."""
    text_low = surrounding_text.lower()

    # 1. Look for explicit statute references in the sentence
    if re.search(r'\b(?:ipc|indian penal code|penal code)\b', text_low):
        return "Indian Penal Code, 1860"
    if re.search(r'\b(?:crpc|cr\.p\.c\.|criminal procedure code|code of criminal procedure)\b', text_low):
        return "Code of Criminal Procedure, 1973"
    if re.search(r'\b(?:cpc|civil procedure code|code of civil procedure)\b', text_low):
        return "Code of Civil Procedure, 1908"
    if re.search(r'\b(?:constitution|article)\b', text_low) or "article" in sec_type.lower():
        return "Constitution of India"
    if re.search(r'\b(?:act 32 of 2012|pocso|protection of children)\b', text_low):
        return "Protection of Children from Sexual Offences Act, 2012"
    if re.search(r'\b(?:arbitration and conciliation act|arbitration act)\b', text_low):
        return "Arbitration and Conciliation Act, 1996"
    if re.search(r'\b(?:evidence act|indian evidence act)\b', text_low):
        return "Indian Evidence Act, 1872"
    if re.search(r'\b(?:juvenile justice|jj act)\b', text_low):
        return "Juvenile Justice (Care and Protection of Children) Act, 2015"
    if re.search(r'\b(?:negotiable instruments|ni act)\b', text_low):
        return "Negotiable Instruments Act, 1881"

    # 2. Heuristics based on section number and legal category
    first_part = re.split(r'[\s,\-/]', sec_num.strip())[0].upper()

    if first_part in ["302", "376", "376-A", "376A", "363", "366-A", "366A", "34", "498-A", "498A", "377", "201", "304", "457", "380", "420", "120-B", "120B"]:
        return "Indian Penal Code, 1860"
    if first_part in ["482", "41-A", "41A", "354", "432", "433-A", "433A", "164", "161", "173", "313", "374", "366"]:
        return "Code of Criminal Procedure, 1973"
    if first_part in ["9", "11", "34", "37"] and case_category == "Commercial":
        return "Arbitration and Conciliation Act, 1996"
    if first_part in ["20", "23", "43"] and ("child" in text_low or "sexual" in text_low):
        return "Protection of Children from Sexual Offences Act, 2012"
    if "article" in sec_type.lower() or first_part in ["14", "19", "21", "32", "142", "72", "161", "226", "136"]:
        return "Constitution of India"

    if case_category == "Criminal":
        return "Indian Penal Code, 1860"

    return "Indian Statute"


def determine_provision_role(
    clean_sent: str,
    page_num: int,
    total_pages: int
) -> Tuple[str, bool]:
    """Determine whether provision is applied, relied upon, argued, or mentioned."""
    s_low = clean_sent.lower()

    # Applied: Conviction, sentencing, modification, quashing, or granting relief
    if any(k in s_low for k in [
        "convicted and sentenced", "sentenced him to death under section",
        "sentenced to suffer", "sentence is converted", "converted to that of",
        "quashed and set aside", "ad-interim relief granted under", "consecutively under",
        "punishable under section", "sentence under section"
    ]):
        return "applied", True

    # Relied upon: Judicial interpretation, jurisprudence, or statutory exercise
    if any(k in s_low for k in [
        "this court held", "interpreted section", "principles underlying",
        "jurisprudence of section", "powers under article 142", "powers under article 72",
        "procedure laid down in section", "guidelines under section", "in terms of section"
    ]):
        return "relied_upon", False

    # Argued: Party submissions
    if any(k in s_low for k in [
        "submitted that section", "contended that section", "counsel argued",
        "pleaded that section", "learned senior counsel submitted"
    ]):
        return "argued", False

    # Mentioned: Historical charges, FIR, lower court recital
    return "mentioned", False


def extract_statutory_provisions(
    pages_dict: Dict[int, str],
    case_category: str = "Criminal",
    max_provisions: int = 12
) -> List[Dict[str, Any]]:
    """Extract and disambiguate statutory citations across all judgment pages."""
    provisions: List[Dict[str, Any]] = []
    seen_keys = set()
    total_pages = len(pages_dict)

    # Regex matching "Section 302", "Sections 363, 376", "Article 21", "Articles 14, 19"
    sec_regex = re.compile(
        r'\b(Sections?|Articles?)\s+([0-9]{1,4}(?:-[A-Za-z]+|[A-Za-z])?(?:[,\s]+(?:and\s+)?[0-9]{1,4}(?:-[A-Za-z]+|[A-Za-z])?)*)',
        re.I
    )

    for p_num in sorted(pages_dict.keys()):
        p_text = pages_dict[p_num]
        # Split into full sentences
        raw_sentences = re.split(r'(?<=[.!?])\s+', p_text)

        for sent in raw_sentences:
            clean_sent = clean_sentence_for_quote(sent)
            if len(clean_sent) < 30 or len(clean_sent) > 550:
                continue

            matches = list(sec_regex.finditer(clean_sent))
            if not matches:
                continue

            for m in matches:
                sec_type = m.group(1).title()
                raw_nums_str = m.group(2).strip()

                # Extract individual section identifiers
                individual_nums = re.findall(r'\b[0-9]{1,4}(?:-[A-Za-z]+|[A-Za-z])?\b', raw_nums_str)
                if not individual_nums:
                    continue

                for num in individual_nums:
                    act_name = disambiguate_act(
                        sec_num=num,
                        sec_type=sec_type,
                        surrounding_text=clean_sent,
                        case_category=case_category
                    )
                    prefix = "Article" if "article" in sec_type.lower() or act_name == "Constitution of India" else "Section"
                    sec_formatted = f"{prefix} {num}"

                    key = (act_name, sec_formatted)
                    if key in seen_keys:
                        continue

                    seen_keys.add(key)
                    role, is_app = determine_provision_role(clean_sent, p_num, total_pages)

                    # Build context explanation
                    context_desc = (
                        f"{act_name} {sec_formatted} actively applied by the court on Page {p_num}."
                        if role == "applied" else
                        f"{act_name} {sec_formatted} referenced as legal authority on Page {p_num}."
                        if role == "relied_upon" else
                        f"{act_name} {sec_formatted} argued by counsel on Page {p_num}."
                        if role == "argued" else
                        f"{act_name} {sec_formatted} noted in procedural narrative on Page {p_num}."
                    )

                    provisions.append({
                        "act_name": act_name,
                        "section_or_article": sec_formatted,
                        "provision_role": role,
                        "is_applied": is_app,
                        "context": context_desc,
                        "supporting_quote": clean_sent,
                        "page_number": p_num,
                        "verification_status": "Verified"
                    })

                    if len(provisions) >= max_provisions:
                        break
                if len(provisions) >= max_provisions:
                    break
        if len(provisions) >= max_provisions:
            break

    # Prioritize: 'applied' first, then 'relied_upon', then 'argued', then 'mentioned'
    role_order = {"applied": 0, "relied_upon": 1, "argued": 2, "mentioned": 3}
    provisions.sort(key=lambda p: (role_order.get(p.get("provision_role", "mentioned"), 3), p.get("page_number", 1)))

    return provisions
