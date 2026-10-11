"""PDF Processing module for NyayaLens using PyMuPDF (fitz).

Handles:
- File validation (size, magic bytes, structure)
- Per-page text extraction with 1-indexed page preserving
- Detection of scanned / OCR-requiring documents
- Text density metrics and character statistics
"""

import os
import io
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

from config import (
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    MIN_TEXT_PER_PAGE_THRESHOLD
)


@dataclass
class PageData:
    page_num: int  # 1-indexed
    text: str
    char_count: int
    word_count: int
    image_count: int
    is_empty: bool


@dataclass
class PDFValidationResult:
    is_valid: bool
    error_message: Optional[str] = None
    file_name: str = ""
    file_size_bytes: int = 0
    file_size_formatted: str = ""


@dataclass
class PDFDocumentData:
    file_name: str
    file_size_bytes: int
    file_size_formatted: str
    total_pages: int
    pages: List[PageData] = field(default_factory=list)
    total_characters: int = 0
    total_words: int = 0
    is_scanned_pdf: bool = False
    warning_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def full_text(self) -> str:
        """Concatenated text of all pages with page markers."""
        chunks = []
        for p in self.pages:
            chunks.append(f"--- [PAGE {p.page_num}] ---\n{p.text}\n")
        return "\n".join(chunks)

    def get_page_text(self, page_num: int) -> str:
        """Get text of a specific 1-indexed page."""
        for p in self.pages:
            if p.page_num == page_num:
                return p.text
        return ""

    def search_query(self, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Search query across all pages and return matches with page numbers."""
        results = []
        if not query or not query.strip():
            return results

        q = query.strip() if case_sensitive else query.strip().lower()
        for p in self.pages:
            text_to_search = p.text if case_sensitive else p.text.lower()
            if q in text_to_search:
                # Find context snippets
                idx = 0
                while True:
                    idx = text_to_search.find(q, idx)
                    if idx == -1:
                        break
                    start = max(0, idx - 80)
                    end = min(len(p.text), idx + len(query) + 80)
                    snippet = p.text[start:end].replace("\n", " ").strip()
                    results.append({
                        "page_num": p.page_num,
                        "snippet": f"...{snippet}..."
                    })
                    idx += len(q)
        return results


def format_file_size(size_bytes: int) -> str:
    """Format bytes to human-readable string (KB/MB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def validate_pdf_file(
    file_bytes: bytes,
    file_name: str
) -> PDFValidationResult:
    """Validates the uploaded file is a genuine PDF within size constraints."""
    size_bytes = len(file_bytes)
    formatted_size = format_file_size(size_bytes)

    # 1. Size validation
    if size_bytes == 0:
        return PDFValidationResult(
            is_valid=False,
            error_message="The uploaded file is empty (0 bytes). Please upload a valid PDF document.",
            file_name=file_name,
            file_size_bytes=size_bytes,
            file_size_formatted=formatted_size
        )

    if size_bytes > MAX_FILE_SIZE_BYTES:
        return PDFValidationResult(
            is_valid=False,
            error_message=(
                f"File size ({formatted_size}) exceeds the maximum allowed limit of "
                f"{MAX_FILE_SIZE_MB} MB. Please upload a smaller file or compress the PDF."
            ),
            file_name=file_name,
            file_size_bytes=size_bytes,
            file_size_formatted=formatted_size
        )

    # 2. Extension check
    if not file_name.lower().endswith(".pdf"):
        return PDFValidationResult(
            is_valid=False,
            error_message=f"Invalid file format: '{file_name}'. Only PDF (.pdf) documents are supported.",
            file_name=file_name,
            file_size_bytes=size_bytes,
            file_size_formatted=formatted_size
        )

    # 3. Magic bytes validation (PDF starts with %PDF)
    if not file_bytes.startswith(b"%PDF"):
        return PDFValidationResult(
            is_valid=False,
            error_message="Corrupted or invalid PDF header. The file does not have a standard PDF signature.",
            file_name=file_name,
            file_size_bytes=size_bytes,
            file_size_formatted=formatted_size
        )

    return PDFValidationResult(
        is_valid=True,
        file_name=file_name,
        file_size_bytes=size_bytes,
        file_size_formatted=formatted_size
    )


def extract_pdf_data(
    file_bytes: bytes,
    file_name: str
) -> Tuple[Optional[PDFDocumentData], Optional[str]]:
    """Extracts text and metadata from every page using PyMuPDF (fitz).

    Returns:
        (PDFDocumentData, error_message)
    """
    if fitz is None:
        return None, "PyMuPDF (fitz) is not installed in the environment."

    val_res = validate_pdf_file(file_bytes, file_name)
    if not val_res.is_valid:
        return None, val_res.error_message

    try:
        # Open PDF stream with PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        return None, f"Failed to parse PDF document with PyMuPDF: {str(e)}"

    total_pages = len(doc)
    if total_pages == 0:
        doc.close()
        return None, "The uploaded PDF document contains 0 pages."

    pages_data: List[PageData] = []
    total_chars = 0
    total_words = 0
    scanned_pages_count = 0

    try:
        for idx in range(total_pages):
            page = doc[idx]
            page_num = idx + 1  # 1-indexed for legal traceability

            # Extract text preserving blocks and reading order
            page_text = page.get_text("text") or ""
            # Clean up excessive null bytes or control characters if any
            clean_text = page_text.replace("\x00", "")

            char_count = len(clean_text.strip())
            word_count = len(clean_text.split())
            image_list = page.get_images(full=True)
            image_count = len(image_list)

            is_empty = char_count == 0
            if char_count < MIN_TEXT_PER_PAGE_THRESHOLD and image_count > 0:
                scanned_pages_count += 1

            pages_data.append(PageData(
                page_num=page_num,
                text=clean_text,
                char_count=char_count,
                word_count=word_count,
                image_count=image_count,
                is_empty=is_empty
            ))

            total_chars += char_count
            total_words += word_count

        raw_metadata = doc.metadata or {}
    except Exception as e:
        doc.close()
        return None, f"Error while extracting text from PDF pages: {str(e)}"
    finally:
        doc.close()

    # Determine if document is scanned or has non-extractable text
    is_scanned = False
    warning_msg = None

    if total_chars == 0:
        is_scanned = True
        warning_msg = (
            "⚠️ No extractable text detected in this PDF. This document appears to be a "
            "scanned image. Indian court orders in pure scanned format require Optical Character "
            "Recognition (OCR) before automated text intelligence can be extracted."
        )
    elif (total_chars / max(1, total_pages)) < MIN_TEXT_PER_PAGE_THRESHOLD:
        is_scanned = True
        warning_msg = (
            f"⚠️ Low text density detected (avg {int(total_chars / max(1, total_pages))} chars/page). "
            "Multiple pages may be scanned images or photocopies lacking embedded text layers. "
            "Portions of the judgment may require OCR for complete analysis."
        )

    doc_data = PDFDocumentData(
        file_name=file_name,
        file_size_bytes=len(file_bytes),
        file_size_formatted=format_file_size(len(file_bytes)),
        total_pages=total_pages,
        pages=pages_data,
        total_characters=total_chars,
        total_words=total_words,
        is_scanned_pdf=is_scanned,
        warning_message=warning_msg,
        metadata={
            "title": raw_metadata.get("title", ""),
            "author": raw_metadata.get("author", ""),
            "creator": raw_metadata.get("creator", ""),
            "producer": raw_metadata.get("producer", ""),
            "creation_date": raw_metadata.get("creationDate", ""),
        }
    )

    return doc_data, None
