# ⚖️ NyayaLens — AI-Powered Indian Court Document Intelligence

> **Demystifying complex Indian court judgments into verified, plain-English intelligence.**

![NyayaLens Badge](https://img.shields.io/badge/Jurisprudence-Indian%20Law-gold?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit%201.65-red?style=for-the-badge)
![PyMuPDF](https://img.shields.io/badge/PDF%20Engine-PyMuPDF%20fitz-blue?style=for-the-badge)
![AI Engine](https://img.shields.io/badge/AI-Google%20Gemini%202.5-emerald?style=for-the-badge)
![Verification](https://img.shields.io/badge/Evidence-Page--Level%20Corroborated-brightgreen?style=for-the-badge)

---

## 📌 Problem Statement

Indian courts generate thousands of pages of judgments, interim orders, and procedural directions daily. These legal texts are notoriously dense, laden with archaic Latin maxims, complex statutory cross-references, and procedural jargon. 

Lawyers, law students, journalists, and citizens spend countless hours parsing these documents. Existing general-purpose AI summarizers frequently **hallucinate**, conflate party arguments with judicial findings, confuse interim orders with final decrees, and cite unverifiable page numbers.

**NyayaLens** solves this by providing:
1. Multipage PDF text extraction with strict page-level tracking via **PyMuPDF (`fitz`)**.
2. Automated legal classification according to Indian legal taxonomy (Civil, Criminal, Constitutional, Commercial, Family, Administrative).
3. Plain-language synthesis structured into 7 distinct legal sections.
4. **Evidence Verification Engine**: Cross-checks extracted quotations and statutory sections against raw PDF page text with exact match confidence scores and page-number validation.
5. Interactive Document Explorer, Q&A assistant, and one-click JSON/Markdown export.

---

## 🌟 Key Differentiators & Priority Features

| Feature | Generic AI Summarizer | **NyayaLens** |
| :--- | :--- | :--- |
| **Evidence Traceability** | None or hallucinated citations | **Verbatim page-text corroboration** with confidence scores |
| **Order Nuance** | Often declares interim orders as "decided" | **Distinguishes interim vs final judgments** |
| **Statute Application** | Groups all citations together | **Distinguishes applied vs merely cited laws** |
| **Scanned PDF Handling** | Silent failure or corrupted outputs | **OCR detection guard & text-density analysis** |
| **Demo Resilience** | Requires API keys to evaluate | **Pre-loaded benchmark cases & offline intelligence mode** |

---

## 🏛️ System Architecture

```
                                  [ Indian Court PDF ]
                                           │
                                           ▼
                            ┌──────────────────────────────┐
                            │ PyMuPDF (fitz) Text Engine   │
                            │  • Magic bytes validation    │
                            │  • 1-Indexed page tracking   │
                            │  • Text density & OCR guard  │
                            └──────────────┬───────────────┘
                                           │
                                           ▼
                 ┌──────────────────────────────────────────────────┐
                 │       AI Legal Analysis & Classification         │
                 │   (Google Gemini 2.5 Flash / Hybrid Fallback)    │
                 │   • Case category (Criminal, Civil, etc.)        │
                 │   • Parties & counsel isolation                  │
                 │   • Statutory provisions matrix                  │
                 │   • Plain-language 7-section breakdown           │
                 └─────────────────────────┬────────────────────────┘
                                           │
                                           ▼
                 ┌──────────────────────────────────────────────────┐
                 │          Evidence Verification Engine            │
                 │   • Normalizes unicode & whitespace              │
                 │   • Scans claimed page for exact match           │
                 │   • Fallback adjacent-page relocation            │
                 │   • Generates verification integrity score       │
                 └─────────────────────────┬────────────────────────┘
                                           │
                                           ▼
                 ┌──────────────────────────────────────────────────┐
                 │         Streamlit Legal-Tech Dashboard           │
                 │   • Executive Brief & Outcome Cards              │
                 │   • 7-Section Plain English Breakdown            │
                 │   • Statutory Provisions Matrix                  │
                 │   • Corroborated Evidence Inspector              │
                 │   • Page-by-Page Raw Document Explorer           │
                 │   • Interactive Document Q&A Assistant           │
                 │   • 1-Click JSON & Markdown Export               │
                 └──────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
e:\Hackathon3.0\
├── app.py                     # Main Streamlit web application & legal dashboard
├── config.py                  # Taxonomy definitions, constants, and system prompts
├── requirements.txt           # Dependency specifications
├── README.md                  # Hackathon documentation
├── core/
│   ├── __init__.py
│   ├── pdf_processor.py       # PyMuPDF extraction, validation, and OCR detection
│   ├── ai_engine.py           # Gemini AI integration, structured parser, and fallback
│   ├── legal_classifier.py    # Taxonomy schemas and rule-based legal heuristics
│   └── verification_engine.py # Quotation verification & page-matching engine
├── sample_data/
│   ├── __init__.py
│   ├── sample_cases.py        # 3 realistic Indian Court judgments (Criminal, Commercial, Constitutional)
│   ├── generate_sample_pdfs.py# Generates real multipage PDFs using PyMuPDF
│   └── pdf/                   # Generated sample court PDF files
├── styles/
│   └── custom.css             # High-end legal-tech design styling (glassmorphism, dark obsidian, gold)
├── scripts/
│   └── pip_ipv4.py            # Utility runner forcing IPv4 for reliable dependency installations
└── tests/
    └── test_nyayalens.py      # Unit test suite covering the entire pipeline
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Internet connection (or test offline using preloaded cases)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Generate Benchmark PDFs (Optional, auto-generated on startup)
```bash
python sample_data/generate_sample_pdfs.py
```

### 4. Run the Application
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 🧪 Running the Test Suite

NyayaLens includes a comprehensive test suite testing PDF parsing, edge-case validation, evidence matching, and end-to-end classification:

```bash
python tests/test_nyayalens.py
```

All 8 tests run and validate the complete pipeline.

---

## ⚖️ Pre-Loaded Benchmark Cases for Hackathon Judges

1. **Criminal Law Benchmark:** *Rajesh Sharma v. State of UP*
   - Quashing of FIR under Section 482 CrPC and Section 498-A IPC.
   - Guidelines on Section 41-A CrPC notices against mechanical arrests.
2. **Commercial Law Benchmark:** *Nexora Infra v. Apex Global Energy*
   - Section 9 interim measures under Arbitration & Conciliation Act, 1996.
   - Restraint of unconditional performance bank guarantees and escrow orders.
3. **Constitutional Law Benchmark:** *Justice K.S. Puttaswamy v. Union of India*
   - Historic 9-judge bench unanimous declaration of Right to Privacy under Article 21.
   - Triple test of legality, legitimate aim, and proportionality.

---

## 🛡️ License & Acknowledgments

Built for student hackathon demonstration. Designed following Supreme Court of India and High Court reporting standards.
