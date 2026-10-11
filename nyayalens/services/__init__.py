"""NyayaLens Services Package."""

from .pdf_service import extract_pdf, PDFExtractionError

__all__ = ["extract_pdf", "PDFExtractionError"]
