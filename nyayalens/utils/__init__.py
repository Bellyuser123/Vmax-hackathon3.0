"""NyayaLens Utilities Package."""

from .validators import (
    validate_pdf,
    validate_filename,
    read_file_source_safely,
    validate_pdf_signature,
    validate_pdf_structure,
    format_file_size,
    DEFAULT_MAX_FILE_SIZE_MB,
    PDF_MAGIC_BYTES,
    PDFValidationError,
    PDFEmptyFileError,
    PDFInvalidExtensionError,
    PDFSizeLimitExceededError,
    PDFCorruptedError,
    PDFEncryptedError,
    PDFNoPagesError,
)

__all__ = [
    "validate_pdf",
    "validate_filename",
    "read_file_source_safely",
    "validate_pdf_signature",
    "validate_pdf_structure",
    "format_file_size",
    "DEFAULT_MAX_FILE_SIZE_MB",
    "PDF_MAGIC_BYTES",
    "PDFValidationError",
    "PDFEmptyFileError",
    "PDFInvalidExtensionError",
    "PDFSizeLimitExceededError",
    "PDFCorruptedError",
    "PDFEncryptedError",
    "PDFNoPagesError",
]
