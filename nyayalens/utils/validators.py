"""PDF Validation Utility Module for NyayaLens.

Provides robust, production-grade validation for court document PDF uploads:
1. Verifies file existence and non-empty payload.
2. Validates .pdf filename extension (case-insensitive).
3. Verifies PDF magic bytes signature (%PDF-).
4. Enforces configurable maximum file size limit (default: 20 MB) with stream-safe chunked reading.
5. Verifies document can be opened and parsed by PyMuPDF.
6. Ensures document has at least one page.
7. Gracefully detects and rejects encrypted or password-protected documents without attempting bypass.

All failures raise specific, actionable subclasses of `PDFValidationError`.
"""

import io
import os
from pathlib import Path
from typing import Any, Optional, Union, BinaryIO

try:
    import pymupdf as fitz
except ImportError:
    import fitz


# =============================================================================
# Custom Exception Hierarchy
# =============================================================================

class PDFValidationError(ValueError):
    """Base exception for all PDF validation failures."""
    pass


class PDFEmptyFileError(PDFValidationError):
    """Raised when the uploaded file source is missing or contains 0 bytes."""
    pass


class PDFInvalidExtensionError(PDFValidationError):
    """Raised when the document filename does not end with .pdf."""
    pass


class PDFSizeLimitExceededError(PDFValidationError):
    """Raised when the document size exceeds the allowed threshold."""
    pass


class PDFCorruptedError(PDFValidationError):
    """Raised when the document is malformed or lacks a valid PDF signature."""
    pass


class PDFEncryptedError(PDFValidationError):
    """Raised when the document is encrypted or requires a password."""
    pass


class PDFNoPagesError(PDFValidationError):
    """Raised when the PDF document contains zero pages."""
    pass


# =============================================================================
# Constants & Defaults
# =============================================================================

DEFAULT_MAX_FILE_SIZE_MB: float = 20.0
PDF_MAGIC_BYTES: bytes = b"%PDF-"
PDF_MAGIC_WINDOW_BYTES: int = 1024
CHUNK_SIZE_BYTES: int = 64 * 1024  # 64 KB read buffer


# =============================================================================
# Helper Utilities
# =============================================================================

def format_file_size(size_bytes: int) -> str:
    """Format bytes into a human-readable size string (B, KB, MB)."""
    if size_bytes < 0:
        return "0 B"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"


def validate_filename(filename: Optional[str]) -> str:
    """Validate that the filename is a non-empty string ending with .pdf.

    Args:
        filename: Name of the file being processed.

    Returns:
        Cleaned, stripped filename.

    Raises:
        PDFInvalidExtensionError: If filename is missing or lacks .pdf extension.
    """
    if not filename or not isinstance(filename, str) or not filename.strip():
        raise PDFInvalidExtensionError(
            "Filename is missing or empty. A valid filename ending with '.pdf' is required."
        )

    cleaned = filename.strip()
    if not cleaned.lower().endswith(".pdf"):
        raise PDFInvalidExtensionError(
            f"Invalid file extension for '{cleaned}'. Only PDF documents (.pdf) are supported."
        )

    return cleaned


def read_file_source_safely(
    file_source: Any,
    max_size_mb: float = DEFAULT_MAX_FILE_SIZE_MB
) -> bytes:
    """Read bytes from various source types while enforcing size limits safely.

    Avoids reading unbounded files into memory by checking file stats where
    available or streaming with an early-exit threshold.

    Supported source types:
    - bytes or bytearray
    - str or Path (filesystem paths)
    - File-like objects with read() method (io.BytesIO, UploadedFile, etc.)

    Args:
        file_source: The binary or file source to read.
        max_size_mb: Configurable maximum size limit in megabytes.

    Returns:
        Raw bytes of the document.

    Raises:
        PDFEmptyFileError: If file is missing or 0 bytes.
        PDFSizeLimitExceededError: If file exceeds max_size_mb.
        PDFValidationError: If source type is unsupported or cannot be read.
    """
    if file_source is None:
        raise PDFEmptyFileError("No file supplied. Please provide a PDF document.")

    max_size_bytes = int(max_size_mb * 1024 * 1024)

    # 1. Raw bytes / bytearray
    if isinstance(file_source, (bytes, bytearray)):
        size = len(file_source)
        if size == 0:
            raise PDFEmptyFileError("The uploaded file is empty (0 bytes). Please upload a valid PDF document.")
        if size > max_size_bytes:
            raise PDFSizeLimitExceededError(
                f"File size ({format_file_size(size)}) exceeds maximum allowed limit of "
                f"{max_size_mb} MB ({format_file_size(max_size_bytes)})."
            )
        return bytes(file_source)

    # 2. File path (str or Path)
    if isinstance(file_source, (str, Path, os.PathLike)):
        path = Path(file_source)
        if not path.exists():
            raise PDFEmptyFileError(f"File not found at path: '{path}'.")
        if not path.is_file():
            raise PDFValidationError(f"Provided path is not a file: '{path}'.")

        file_size = path.stat().st_size
        if file_size == 0:
            raise PDFEmptyFileError(f"The file '{path.name}' is empty (0 bytes).")
        if file_size > max_size_bytes:
            raise PDFSizeLimitExceededError(
                f"File size ({format_file_size(file_size)}) exceeds maximum allowed limit of "
                f"{max_size_mb} MB ({format_file_size(max_size_bytes)})."
            )

        with open(path, "rb") as f:
            return f.read()

    # 3. File-like object (has .read)
    if hasattr(file_source, "read"):
        # Check if seekable to check size prior to full read
        if hasattr(file_source, "seek") and hasattr(file_source, "tell"):
            try:
                current_pos = file_source.tell()
                file_source.seek(0, os.SEEK_END)
                total_size = file_source.tell()
                file_source.seek(current_pos, os.SEEK_SET)

                if total_size == 0:
                    raise PDFEmptyFileError("The uploaded file is empty (0 bytes).")
                if total_size > max_size_bytes:
                    raise PDFSizeLimitExceededError(
                        f"File size ({format_file_size(total_size)}) exceeds maximum allowed limit of "
                        f"{max_size_mb} MB ({format_file_size(max_size_bytes)})."
                    )
            except (OSError, io.UnsupportedOperation):
                # Fallback to chunked streaming if seek fails
                pass

        # Stream with chunked reading and early abort on size overflow
        buffer = bytearray()
        bytes_read = 0

        # If it has getvalue() (e.g. io.BytesIO), we can inspect length directly
        if hasattr(file_source, "getvalue"):
            val = file_source.getvalue()
            val_size = len(val)
            if val_size == 0:
                raise PDFEmptyFileError("The uploaded file is empty (0 bytes).")
            if val_size > max_size_bytes:
                raise PDFSizeLimitExceededError(
                    f"File size ({format_file_size(val_size)}) exceeds maximum allowed limit of "
                    f"{max_size_mb} MB ({format_file_size(max_size_bytes)})."
                )
            # Ensure stream position is preserved/rewound
            if hasattr(file_source, "seek"):
                try:
                    file_source.seek(0)
                except Exception:
                    pass
            return bytes(val)

        # Chunked read
        while True:
            chunk = file_source.read(CHUNK_SIZE_BYTES)
            if not chunk:
                break
            buffer.extend(chunk)
            bytes_read += len(chunk)
            if bytes_read > max_size_bytes:
                raise PDFSizeLimitExceededError(
                    f"File size exceeds maximum allowed limit of {max_size_mb} MB "
                    f"({format_file_size(max_size_bytes)})."
                )

        if bytes_read == 0:
            raise PDFEmptyFileError("The uploaded file is empty (0 bytes). Please upload a valid PDF document.")

        # Rewind if seekable so caller's stream remains intact
        if hasattr(file_source, "seek"):
            try:
                file_source.seek(0)
            except Exception:
                pass

        return bytes(buffer)

    raise PDFValidationError(
        f"Unsupported file source type: '{type(file_source).__name__}'. "
        "Expected bytes, file path, or binary stream."
    )


def validate_pdf_signature(file_bytes: bytes, filename: str) -> None:
    """Verify that file contains the standard PDF magic bytes signature (%PDF-).

    According to the PDF specification, the %PDF- header must appear within
    the first 1024 bytes of the file.

    Args:
        file_bytes: Binary payload of the file.
        filename: Name of the file for error reporting.

    Raises:
        PDFCorruptedError: If the magic bytes are missing.
    """
    header_window = file_bytes[:PDF_MAGIC_WINDOW_BYTES]
    if PDF_MAGIC_BYTES not in header_window:
        raise PDFCorruptedError(
            f"Invalid PDF content in '{filename}'. The file lacks a genuine PDF header signature (%PDF-)."
        )


def validate_pdf_structure(file_bytes: bytes, filename: str) -> None:
    """Verify the document can be opened and parsed by PyMuPDF, is unencrypted, and has >=1 page.

    Args:
        file_bytes: Binary payload of the file.
        filename: Name of the file for error reporting.

    Raises:
        PDFCorruptedError: If PyMuPDF cannot parse the document.
        PDFEncryptedError: If document is encrypted or password-protected.
        PDFNoPagesError: If document contains 0 pages.
    """
    doc = None
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as exc:
        raise PDFCorruptedError(
            f"Failed to parse '{filename}' as a PDF document. The file may be corrupted or truncated."
        ) from None

    try:
        # Check password / encryption
        if getattr(doc, "is_encrypted", False) or getattr(doc, "needs_pass", False):
            raise PDFEncryptedError(
                f"The document '{filename}' is password-protected or encrypted. "
                "NyayaLens does not bypass passwords; please provide an unlocked document."
            )

        # Check page count
        page_count = len(doc)
        if page_count < 1:
            raise PDFNoPagesError(
                f"The PDF document '{filename}' contains 0 pages and cannot be processed."
            )
    finally:
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass


# =============================================================================
# Primary Public Validation Interface
# =============================================================================

def validate_pdf(
    file_source: Any,
    filename: Optional[str] = None,
    max_size_mb: float = DEFAULT_MAX_FILE_SIZE_MB
) -> bytes:
    """Perform complete, end-to-end validation of an uploaded PDF file.

    Validates:
    1. File source exists and is not empty.
    2. Filename has .pdf extension.
    3. File size does not exceed `max_size_mb`.
    4. Content starts with PDF magic bytes (%PDF-).
    5. Document can be parsed cleanly with PyMuPDF.
    6. Document has at least one page.
    7. Document is not encrypted or password-protected.

    Args:
        file_source: Raw bytes, file path, or stream-like object.
        filename: Optional filename. If omitted and file_source is a path,
            path.name is used.
        max_size_mb: Maximum allowed file size in MB (default: 20 MB).

    Returns:
        The validated raw bytes of the PDF document.

    Raises:
        PDFEmptyFileError: File is missing or 0 bytes.
        PDFInvalidExtensionError: Extension is not .pdf.
        PDFSizeLimitExceededError: Size exceeds max_size_mb.
        PDFCorruptedError: Malformed file or invalid header.
        PDFEncryptedError: Password-protected or encrypted PDF.
        PDFNoPagesError: PDF with 0 pages.
        PDFValidationError: Any other validation violation.
    """
    # Infer filename if file_source is a path
    if (not filename) and isinstance(file_source, (str, Path, os.PathLike)):
        filename = Path(file_source).name

    # 1. Filename extension check
    clean_name = validate_filename(filename)

    # 2. File existence and size check with safe streaming
    file_bytes = read_file_source_safely(file_source, max_size_mb=max_size_mb)

    # 3. Content signature check
    validate_pdf_signature(file_bytes, clean_name)

    # 4. PyMuPDF parsing, encryption, and page count checks
    validate_pdf_structure(file_bytes, clean_name)

    return file_bytes
