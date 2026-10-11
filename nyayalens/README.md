# NyayaLens — PDF Upload, Validation, and Text Extraction Module

Production-grade, modular PDF processing service for **NyayaLens** (AI-Powered Indian Court Document Intelligence).

Built specifically for the PDF processing responsibility within the 5-person hackathon team.

---

## 1. Overview

This module provides an isolated, reliable, and testable foundation for ingesting Indian court documents:
- **Comprehensive Validation**: File existence, `.pdf` extension check, `%PDF-` magic bytes header verification, configurable size enforcement (default: 20 MB), PyMuPDF structure parsing, zero-page rejection, and graceful password/encryption detection.
- **Page-by-Page Extraction**: Extracts text page-by-page using PyMuPDF (`fitz`), preserving strictly 1-indexed page numbering and original document order.
- **Structural Integrity**: Preserves paragraph spacing (`\n\n`) and natural line breaks so legal sections, citations, and holdings remain traceable.
- **Scanned PDF & OCR Detection**: Inspects per-page text density to detect pure scanned PDFs or mixed scanned/digital documents, setting `requires_ocr=True` with descriptive warnings for downstream OCR pipelines.
- **Privacy & Security**: Zero permanent disk persistence required; streams processed in memory; zero logging of confidential judicial text; safe against memory exhaustion from oversized payloads.

---

## 2. Installation

Install the required dependencies from `nyayalens/requirements.txt`:

```bash
pip install -r nyayalens/requirements.txt
```

Core dependencies:
- `pymupdf>=1.24.0` (PyMuPDF / fitz engine)
- `pytest>=8.0.0` (Automated testing suite)

---

## 3. Function Interface

### Signature

```python
from nyayalens.services.pdf_service import extract_pdf

def extract_pdf(
    file_source: Any,
    filename: Optional[str] = None,
    max_size_mb: float = 20.0,
    min_meaningful_chars: int = 10
) -> Dict[str, Any]:
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `file_source` | `bytes`, `bytearray`, `str`, `Path`, `BinaryIO`, `BytesIO`, or Stream | *Required* | Raw binary bytes, local file path, or stream-like file object (e.g. Streamlit `UploadedFile`). |
| `filename` | `str` (or `None`) | `None` | Name of the document (must end with `.pdf`). Inferred automatically if `file_source` is a file path or has a `.name` attribute. |
| `max_size_mb` | `float` | `20.0` | Maximum allowed file size in Megabytes. Uploads exceeding this raise `PDFSizeLimitExceededError`. |
| `min_meaningful_chars` | `int` | `10` | Minimum non-whitespace characters required on a page to treat it as containing extractable text rather than a scan artifact. |

---

## 4. Standard Output Contract

`extract_pdf` returns a standardized Python dictionary conforming strictly to the team's integration contract:

```python
{
    "filename": "judgment.pdf",
    "page_count": 2,
    "pages": [
        {
            "page_number": 1,
            "text": "IN THE SUPREME COURT OF INDIA\nCIVIL APPELLATE JURISDICTION\n..."
        },
        {
            "page_number": 2,
            "text": "Held: The appeal is allowed with costs.\n..."
        }
    ],
    "extraction_status": "success",  # "success" | "partial" | "no_text"
    "requires_ocr": False,           # bool
    "warnings": []                   # list of str
}
```

### Extraction Status Definitions

| Status | Condition | `requires_ocr` | Description |
|---|---|---|---|
| `"success"` | All pages have meaningful text | `False` | Clean digital PDF. Full text extracted across all pages. |
| `"partial"` | Some pages have text, others lack text | `True` | Mixed document (e.g., printed order followed by scanned annexures). OCR needed for specific pages. |
| `"no_text"` | Zero pages contain meaningful text | `True` | Scanned or photocopied document. Optical Character Recognition (OCR) is mandatory. |

---

## 5. Scanned PDF Detection & OCR Integration

Many Indian High Court and District Court orders are uploaded as scanned image PDFs or photocopies.

- **Detection**: The module inspects text density on every page. Pages containing fewer than `min_meaningful_chars` (default: 10 chars) are flagged as lacking extractable text.
- **Reporting**:
  - If **all pages** lack text: `extraction_status` is `"no_text"`, `requires_ocr` is `True`, and a warning informs the user that OCR is needed.
  - If **some pages** lack text: `extraction_status` is `"partial"`, `requires_ocr` is `True`, and a warning explicitly lists the affected page numbers (e.g., `Page(s) 2, 4 contain little or no extractable text...`).
- **Future OCR Pipeline**: Optical Character Recognition (Tesseract / EasyOCR / Cloud Vision) is deliberately deferred to a dedicated OCR module or future enhancement so that text-native extraction remains fast and deterministic.

---

## 6. Exception Hierarchy

All validation and extraction errors inherit from `PDFValidationError` (a subclass of `ValueError`):

```text
PDFValidationError
├── PDFEmptyFileError          (File missing, 0 bytes, or empty stream)
├── PDFInvalidExtensionError  (Filename missing or not ending with .pdf)
├── PDFSizeLimitExceededError  (Payload exceeds configured max_size_mb)
├── PDFCorruptedError          (Missing %PDF- header, truncated or unparsable binary)
├── PDFEncryptedError          (Password-protected or encrypted document)
├── PDFNoPagesError            (Document contains 0 pages)
└── PDFExtractionError         (Unrecoverable PyMuPDF extraction failure)
```

Error messages are sanitized and user-friendly so the frontend developer can surface them directly without leaking internal paths or tracebacks.

---

## 7. Integration Guide for Team Members

### For the Integration Lead & AI Classification Developer

```python
from nyayalens.services.pdf_service import extract_pdf
from nyayalens.utils.validators import PDFValidationError

def process_court_document(uploaded_file, filename):
    try:
        extraction_result = extract_pdf(
            file_source=uploaded_file,
            filename=filename,
            max_size_mb=20.0
        )
        
        # Check if OCR fallback is needed
        if extraction_result["requires_ocr"]:
            print(f"Warnings: {extraction_result['warnings']}")
            if extraction_result["extraction_status"] == "no_text":
                # Route to OCR module when available
                return {"error": "Scanned document requires OCR."}

        # Aggregate text or process page-by-page for legal analysis
        full_text = "\n\n".join(
            f"--- Page {p['page_number']} ---\n{p['text']}"
            for p in extraction_result["pages"]
        )
        
        return {
            "status": extraction_result["extraction_status"],
            "total_pages": extraction_result["page_count"],
            "document_text": full_text
        }
        
    except PDFValidationError as val_err:
        # User-friendly error message ready for display
        return {"error": str(val_err)}
```

### For the Streamlit Frontend Developer

```python
import streamlit as st
from nyayalens.services.pdf_service import extract_pdf
from nyayalens.utils.validators import PDFValidationError

uploaded_file = st.file_uploader("Upload Court Order (PDF)", type=["pdf"])

if uploaded_file is not None:
    try:
        # Streamlit's UploadedFile is passed directly (no disk save needed)
        result = extract_pdf(uploaded_file, uploaded_file.name)
        
        st.success(f"Successfully processed {result['filename']} ({result['page_count']} pages)")
        
        if result["requires_ocr"]:
            for warn in result["warnings"]:
                st.warning(warn)
                
        for page in result["pages"]:
            with st.expander(f"Page {page['page_number']}"):
                st.text(page["text"] if page["text"] else "[No extractable text on this page]")
                
    except PDFValidationError as e:
        st.error(str(e))
```

---

## 8. Running Automated Tests

Run the full pytest suite from the project root:

```bash
pytest nyayalens/tests/test_pdf.py -v
```

The test suite runs in under 0.5s, generates synthetic in-memory PDFs, and requires no external APIs or internet connection.
