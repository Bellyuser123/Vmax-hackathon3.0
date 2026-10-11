"""NyayaLens Core Package.

AI-Powered Indian Court Document Intelligence.
"""

from nyayalens.services.pdf_service import extract_pdf, PDFExtractionError
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
)

__all__ = [
    "extract_pdf",
    "PDFExtractionError",
    "validate_pdf",
    "validate_filename",
    "PDFValidationError",
    "PDFEmptyFileError",
    "PDFInvalidExtensionError",
    "PDFSizeLimitExceededError",
    "PDFCorruptedError",
    "PDFEncryptedError",
    "PDFNoPagesError",
]
