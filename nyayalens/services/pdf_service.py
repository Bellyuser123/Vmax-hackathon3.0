"""PDF Text Extraction Service Module for NyayaLens.

Provides robust, production-ready text extraction for Indian court documents
using PyMuPDF (fitz).

Key Features:
- Validates file source, size, extension, header, and parseability.
- Extracts text strictly page-by-page preserving 1-indexed page numbering.
- Preserves natural line breaks and paragraph spacing.
- Detects scanned / image-only documents and mixed documents.
- Sets requires_ocr=True with informative warnings when OCR is needed.
- Enforces strict privacy: never logs confidential court document text.
- Cleans up all document and stream resources reliably.
"""

import io
import logging
from typing import Any, Dict, List, Optional, Union

try:
    import pymupdf as fitz
except ImportError:
    import fitz

# Robust import allowing both top-level package and direct module imports
try:
    from nyayalens.utils.validators import (
        validate_pdf,
        validate_filename,
        PDFValidationError,
        PDFEmptyFileError,
        PDFInvalidExtensionError,
        PDFSizeLimitExceededError,
        PDFCorruptedError,
        PDFEncryptedError,
        PDFNoPagesError,
        DEFAULT_MAX_FILE_SIZE_MB,
    )
except ImportError:
    from utils.validators import (
        validate_pdf,
        validate_filename,
        PDFValidationError,
        PDFEmptyFileError,
        PDFInvalidExtensionError,
        PDFSizeLimitExceededError,
        PDFCorruptedError,
        PDFEncryptedError,
        PDFNoPagesError,
        DEFAULT_MAX_FILE_SIZE_MB,
    )

logger = logging.getLogger("nyayalens.pdf_service")

# Minimum characters on a page to consider it containing meaningful text.
# Purely scanned pages often produce 0 chars, or 1-9 chars from random speckle/stamps.
MIN_MEANINGFUL_TEXT_CHARS: int = 10


# =============================================================================
# Custom Exception Hierarchy
# =============================================================================

class PDFExtractionError(PDFValidationError):
    """Raised when an unrecoverable error occurs during text extraction."""
    pass


# =============================================================================
# Internal Extraction Helper
# =============================================================================

def _clean_page_text(raw_text: str) -> str:
    """Normalize extracted page text while preserving line and paragraph breaks.

    Removes null bytes and cleans up trailing line whitespace without
    collapsing meaningful paragraph structure.

    Args:
        raw_text: Raw string extracted from PyMuPDF page.

    Returns:
        Sanitized text string.
    """
    if not raw_text:
        return ""

    # Remove null bytes occasionally present in corrupted font tables
    sanitized = raw_text.replace("\x00", "")

    # Clean trailing whitespace on each line while preserving blank lines (paragraphs)
    lines = [line.rstrip() for line in sanitized.splitlines()]
    return "\n".join(lines).strip()


# =============================================================================
# Primary Public Extraction Function
# =============================================================================

def extract_pdf(
    file_source: Any,
    filename: Optional[str] = None,
    max_size_mb: float = DEFAULT_MAX_FILE_SIZE_MB,
    min_meaningful_chars: int = MIN_MEANINGFUL_TEXT_CHARS
) -> Dict[str, Any]:
    """Extract text from every page of a valid PDF document page-by-page.

    Standard Output Contract:
        {
            "filename": "judgment.pdf",
            "page_count": 2,
            "pages": [
                {
                    "page_number": 1,
                    "text": "Extracted text from page one."
                },
                {
                    "page_number": 2,
                    "text": "Extracted text from page two."
                }
            ],
            "extraction_status": "success",  # "success" | "partial" | "no_text"
            "requires_ocr": False,           # bool
            "warnings": []                   # list of str
        }

    Args:
        file_source: Binary source (bytes, file path, io.BytesIO, or stream).
        filename: Optional name of the uploaded document (must end with .pdf).
            If omitted and file_source is a path, the path's name is inferred.
        max_size_mb: Maximum allowed file size limit in MB (default: 20 MB).
        min_meaningful_chars: Minimum character threshold per page to consider
            the page as having meaningful text (default: 10).

    Returns:
        Agreed contract dictionary matching the standard NyayaLens schema.

    Raises:
        PDFEmptyFileError: If file is missing or contains 0 bytes.
        PDFInvalidExtensionError: If filename lacks a .pdf extension.
        PDFSizeLimitExceededError: If file exceeds max_size_mb.
        PDFCorruptedError: If file cannot be parsed as a valid PDF.
        PDFEncryptedError: If document is password-protected or encrypted.
        PDFNoPagesError: If document contains 0 pages.
        PDFExtractionError: If an unrecoverable extraction failure occurs.
    """
    # Infer filename if file_source is a file path and filename was not provided
    if (not filename) and hasattr(file_source, "name") and isinstance(file_source.name, str):
        filename = file_source.name
    elif (not filename) and isinstance(file_source, (str, bytes, bytearray)):
        import os
        from pathlib import Path
        if isinstance(file_source, (str, Path, os.PathLike)):
            try:
                filename = Path(file_source).name
            except Exception:
                pass

    # 1. Comprehensive pre-validation (extension, size, magic bytes, integrity)
    clean_filename = validate_filename(filename)
    validated_bytes = validate_pdf(
        file_source=file_source,
        filename=clean_filename,
        max_size_mb=max_size_mb
    )

    doc = None
    try:
        # Open in-memory PDF stream
        doc = fitz.open(stream=validated_bytes, filetype="pdf")
        page_count = len(doc)

        pages: List[Dict[str, Any]] = []
        pages_without_meaningful_text: List[int] = []
        total_extracted_chars = 0

        for page_idx in range(page_count):
            page_number = page_idx + 1  # 1-indexed for legal traceability
            try:
                page = doc[page_idx]
                # PyMuPDF "text" mode preserves natural reading order and line breaks
                raw_text = page.get_text("text") or ""
                cleaned_text = _clean_page_text(raw_text)
            except Exception as page_err:
                logger.warning(
                    "Error extracting text from page %d of '%s'",
                    page_number,
                    clean_filename
                )
                cleaned_text = ""

            char_count = len(cleaned_text.strip())
            total_extracted_chars += char_count

            # Evaluate text presence for scanned page detection
            if char_count < min_meaningful_chars:
                pages_without_meaningful_text.append(page_number)

            pages.append({
                "page_number": page_number,
                "text": cleaned_text
            })

    except (PDFValidationError, fitz.FileDataError, fitz.EmptyFileError):
        raise
    except Exception as exc:
        raise PDFExtractionError(
            f"An error occurred while extracting text from '{clean_filename}'. "
            "The document content could not be read."
        ) from None
    finally:
        # Always close PyMuPDF resources safely
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass

    # 2. Scanned PDF and OCR requirement analysis
    warnings: List[str] = []
    requires_ocr = False

    if len(pages_without_meaningful_text) == page_count:
        # Case A: Entirely scanned / image-only PDF
        extraction_status = "no_text"
        requires_ocr = True
        warnings.append(
            f"Document contains no extractable text across all {page_count} page(s). "
            "This document appears to be a scanned image or photocopy. "
            "OCR (Optical Character Recognition) is required to extract text."
        )
    elif len(pages_without_meaningful_text) > 0:
        # Case B: Mixed document (some pages have text, others are scanned or blank)
        extraction_status = "partial"
        requires_ocr = True
        pages_str = ", ".join(str(p) for p in sorted(pages_without_meaningful_text))
        warnings.append(
            f"Page(s) {pages_str} contain little or no extractable text and appear to be "
            "scanned images or photocopies. OCR is required to obtain complete text for these pages."
        )
    else:
        # Case C: Fully extractable digital document
        extraction_status = "success"
        requires_ocr = False

    # Privacy compliance: Never log confidential court document text
    logger.info(
        "Extracted PDF '%s': %d pages, %d total chars, status=%s, requires_ocr=%s",
        clean_filename,
        page_count,
        total_extracted_chars,
        extraction_status,
        requires_ocr
    )

    return {
        "filename": clean_filename,
        "page_count": page_count,
        "pages": pages,
        "extraction_status": extraction_status,
        "requires_ocr": requires_ocr,
        "warnings": warnings,
    }
