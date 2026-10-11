"""Automated Test Suite for NyayaLens PDF Upload, Validation, and Extraction Module.

Tests:
1. Valid PDF with one page.
2. Valid PDF with multiple pages.
3. Correct page numbering (1-indexed) and page order.
4. Empty files (bytes, None, empty streams, empty files).
5. Incorrect file types and extensions (.txt, .docx, .png, etc.).
6. Corrupted PDF content (bad header, truncated PDF payload).
7. Oversized files exceeding configurable max_size_mb.
8. PDF with pages containing no extractable text (image-only or blank).
9. Mixed PDF with text page and image-only/blank page.
10. Consistent output keys and data types matching standard output contract.
11. Encrypted / password-protected PDF handling.
12. Proper error handling, resource cleanup, and stream rewind safety.
13. Line and paragraph break preservation.
14. Filepath and file-like object input sources.
15. Zero-page document rejection.
"""

import io
import sys
from pathlib import Path
import pytest

# Ensure both workspace root and nyayalens are in sys.path
test_dir = Path(__file__).resolve().parent
nyayalens_dir = test_dir.parent
workspace_root = nyayalens_dir.parent

for p in (str(workspace_root), str(nyayalens_dir)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    import pymupdf as fitz
except ImportError:
    import fitz

from nyayalens.services.pdf_service import extract_pdf, PDFExtractionError
from nyayalens.utils.validators import (
    validate_pdf,
    validate_filename,
    read_file_source_safely,
    format_file_size,
    PDFValidationError,
    PDFEmptyFileError,
    PDFInvalidExtensionError,
    PDFSizeLimitExceededError,
    PDFCorruptedError,
    PDFEncryptedError,
    PDFNoPagesError,
)


# =============================================================================
# Synthetic PDF Generation Fixtures and Helpers
# =============================================================================

def build_pdf_bytes(pages_text: list[str]) -> bytes:
    """Generate in-memory PDF bytes with the given text on each page."""
    doc = fitz.open()
    for text in pages_text:
        page = doc.new_page(width=595, height=842)
        if text:
            page.insert_textbox(
                fitz.Rect(50, 70, 545, 780),
                text,
                fontsize=11,
                fontname="helv",
            )
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def build_image_only_pdf_bytes(num_pages: int = 1) -> bytes:
    """Generate in-memory PDF bytes containing only raster images without text."""
    doc = fitz.open()
    # Create a small blank RGB image
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 120, 120), False)
    pix.clear_with(240)  # light gray
    img_bytes = pix.tobytes("png")

    for _ in range(num_pages):
        page = doc.new_page(width=595, height=842)
        page.insert_image(fitz.Rect(50, 50, 300, 300), stream=img_bytes)

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def build_mixed_pdf_bytes() -> bytes:
    """Generate PDF with Page 1 containing legal text and Page 2 containing only an image."""
    doc = fitz.open()
    # Page 1: Text
    p1 = doc.new_page(width=595, height=842)
    p1.insert_textbox(
        fitz.Rect(50, 70, 545, 780),
        "IN THE HIGH COURT OF JUDICATURE AT BOMBAY\nCRIMINAL APPEAL NO. 412 OF 2022\n\n"
        "Held: The appellant is acquitted of all charges under Section 302 IPC.",
        fontsize=11,
        fontname="helv",
    )
    # Page 2: Raster scan image only (no text layer)
    p2 = doc.new_page(width=595, height=842)
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 100, 100), False)
    pix.clear_with(220)
    img_bytes = pix.tobytes("png")
    p2.insert_image(fitz.Rect(50, 50, 400, 400), stream=img_bytes)

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def build_encrypted_pdf_bytes(user_password: str = "courtpass") -> bytes:
    """Generate in-memory encrypted PDF protected with a password."""
    doc = fitz.open()
    p = doc.new_page(width=595, height=842)
    p.insert_text(fitz.Point(60, 60), "Confidential in-camera proceedings.")
    pdf_bytes = doc.tobytes(
        encryption=fitz.PDF_ENCRYPT_AES_256,
        user_pw=user_password,
        owner_pw="owner123",
    )
    doc.close()
    return pdf_bytes


# =============================================================================
# Automated Test Cases
# =============================================================================

def test_01_valid_single_page_pdf():
    """Test 1: Valid PDF with one page extracts cleanly."""
    page_text = "IN THE SUPREME COURT OF INDIA\nCIVIL APPELLATE JURISDICTION\nJudgment delivered on 12th Jan 2024."
    pdf_bytes = build_pdf_bytes([page_text])

    result = extract_pdf(pdf_bytes, filename="judgment_single.pdf")

    assert result["filename"] == "judgment_single.pdf"
    assert result["page_count"] == 1
    assert len(result["pages"]) == 1
    assert result["pages"][0]["page_number"] == 1
    assert "SUPREME COURT OF INDIA" in result["pages"][0]["text"]
    assert result["extraction_status"] == "success"
    assert result["requires_ocr"] is False
    assert result["warnings"] == []


def test_02_valid_multipage_pdf():
    """Test 2: Valid PDF with multiple pages extracts all pages."""
    texts = [
        "Page 1: IN THE HIGH COURT OF DELHI AT NEW DELHI. Criminal Misc. Case 100/2023.",
        "Page 2: The submissions of the learned Senior Counsel for the Petitioner were heard at length.",
        "Page 3: Consequently, the petition is allowed and the interim bail is made absolute."
    ]
    pdf_bytes = build_pdf_bytes(texts)

    result = extract_pdf(pdf_bytes, filename="delhi_hc_order.pdf")

    assert result["page_count"] == 3
    assert len(result["pages"]) == 3
    assert result["extraction_status"] == "success"
    assert result["requires_ocr"] is False
    assert result["warnings"] == []


def test_03_page_numbering_and_order():
    """Test 3: Page numbering is strictly 1-indexed and maintains original order."""
    texts = [
        "FIRST_PAGE_CONTENT: Preliminary facts and prosecution narrative.",
        "SECOND_PAGE_CONTENT: Consideration of evidentiary exhibits and testimonies.",
        "THIRD_PAGE_CONTENT: Final judicial decree and directions to the Registry."
    ]
    pdf_bytes = build_pdf_bytes(texts)

    result = extract_pdf(pdf_bytes, filename="appeal_record.pdf")

    assert [p["page_number"] for p in result["pages"]] == [1, 2, 3]
    assert "FIRST_PAGE_CONTENT" in result["pages"][0]["text"]
    assert "SECOND_PAGE_CONTENT" in result["pages"][1]["text"]
    assert "THIRD_PAGE_CONTENT" in result["pages"][2]["text"]


def test_04_empty_files():
    """Test 4: Empty byte buffers, None, and empty streams are rejected with clear error."""
    # None file_source
    with pytest.raises(PDFEmptyFileError) as exc_info:
        extract_pdf(None, filename="empty.pdf")
    assert "No file supplied" in str(exc_info.value)

    # 0-byte bytes
    with pytest.raises(PDFEmptyFileError) as exc_info:
        extract_pdf(b"", filename="empty.pdf")
    assert "empty" in str(exc_info.value).lower()

    # 0-byte BytesIO stream
    with pytest.raises(PDFEmptyFileError) as exc_info:
        extract_pdf(io.BytesIO(b""), filename="empty.pdf")
    assert "empty" in str(exc_info.value).lower()


def test_05_incorrect_file_types():
    """Test 5: Filenames without .pdf extension are rejected with actionable error."""
    pdf_bytes = build_pdf_bytes(["Sample court order text."])

    # Text extension
    with pytest.raises(PDFInvalidExtensionError) as exc_info:
        extract_pdf(pdf_bytes, filename="order.txt")
    assert "Invalid file extension" in str(exc_info.value)

    # Word document extension
    with pytest.raises(PDFInvalidExtensionError) as exc_info:
        extract_pdf(pdf_bytes, filename="judgment.docx")
    assert "Only PDF documents (.pdf) are supported" in str(exc_info.value)

    # Empty filename
    with pytest.raises(PDFInvalidExtensionError):
        extract_pdf(pdf_bytes, filename="")

    # Case-insensitivity: .PDF should be accepted
    result = extract_pdf(pdf_bytes, filename="JUDGMENT_UPPERCASE.PDF")
    assert result["extraction_status"] == "success"


def test_06_corrupted_pdf_content():
    """Test 6: Non-PDF or corrupted binary content is rejected."""
    # Plain text disguised with .pdf extension (fails magic bytes)
    fake_pdf = b"This is plain text with a pdf extension, not real PDF bytes."
    with pytest.raises(PDFCorruptedError) as exc_info:
        extract_pdf(fake_pdf, filename="fake.pdf")
    assert "lacks a genuine PDF header" in str(exc_info.value)

    # Header with %PDF- but followed by truncated garbage (fails parser)
    corrupted_bytes = b"%PDF-1.4\nTRUNCATED_AND_CORRUPTED_STREAM\x00\xff\xfe\n%%EOF"
    with pytest.raises(PDFCorruptedError) as exc_info:
        extract_pdf(corrupted_bytes, filename="corrupted.pdf")
    assert "Failed to parse" in str(exc_info.value) or "corrupted" in str(exc_info.value)


def test_07_oversized_files():
    """Test 7: Documents exceeding configured size limit are rejected before exhaustion."""
    dummy_text = "Legal text payload for size testing. " * 1000
    pdf_bytes = build_pdf_bytes([dummy_text])
    actual_size_mb = len(pdf_bytes) / (1024 * 1024)

    # Setting max_size_mb well below actual size
    tiny_max_mb = actual_size_mb / 2.0
    with pytest.raises(PDFSizeLimitExceededError) as exc_info:
        extract_pdf(pdf_bytes, filename="large_order.pdf", max_size_mb=tiny_max_mb)

    assert "exceeds maximum allowed limit" in str(exc_info.value)


def test_08_pdf_with_no_extractable_text():
    """Test 8: Document with no extractable text is marked as no_text requiring OCR."""
    # 2 pages with raster images only
    scanned_bytes = build_image_only_pdf_bytes(num_pages=2)

    result = extract_pdf(scanned_bytes, filename="scanned_judgment.pdf")

    assert result["page_count"] == 2
    assert result["extraction_status"] == "no_text"
    assert result["requires_ocr"] is True
    assert len(result["warnings"]) == 1
    assert "scanned image" in result["warnings"][0].lower()
    assert result["pages"][0]["text"] == ""
    assert result["pages"][1]["text"] == ""


def test_09_mixed_pdf_with_text_and_image_only_page():
    """Test 9: Mixed PDF with 1 text page and 1 image page produces partial status."""
    mixed_bytes = build_mixed_pdf_bytes()

    result = extract_pdf(mixed_bytes, filename="mixed_order.pdf")

    assert result["page_count"] == 2
    assert result["extraction_status"] == "partial"
    assert result["requires_ocr"] is True
    assert len(result["warnings"]) == 1
    assert "Page(s) 2" in result["warnings"][0]
    assert "CRIMINAL APPEAL NO. 412" in result["pages"][0]["text"]
    assert result["pages"][1]["text"] == ""


def test_10_consistent_output_keys_and_data_types():
    """Test 10: Standard output contract conforms strictly to schema and types."""
    pdf_bytes = build_pdf_bytes(["Bench decision: Special Leave Petition dismissed."])

    result = extract_pdf(pdf_bytes, filename="slp_order.pdf")

    # Contract top-level keys
    expected_keys = {
        "filename",
        "page_count",
        "pages",
        "extraction_status",
        "requires_ocr",
        "warnings"
    }
    assert set(result.keys()) == expected_keys

    # Data types
    assert isinstance(result["filename"], str)
    assert isinstance(result["page_count"], int)
    assert isinstance(result["pages"], list)
    assert isinstance(result["extraction_status"], str)
    assert isinstance(result["requires_ocr"], bool)
    assert isinstance(result["warnings"], list)
    assert result["extraction_status"] in ("success", "partial", "no_text")

    # Pages structure
    page_item = result["pages"][0]
    assert set(page_item.keys()) == {"page_number", "text"}
    assert isinstance(page_item["page_number"], int)
    assert isinstance(page_item["text"], str)


def test_11_encrypted_pdf_handling():
    """Test 11: Encrypted or password-protected PDFs raise PDFEncryptedError."""
    encrypted_bytes = build_encrypted_pdf_bytes(user_password="secret_pass_123")

    with pytest.raises(PDFEncryptedError) as exc_info:
        extract_pdf(encrypted_bytes, filename="locked_order.pdf")

    assert "password-protected or encrypted" in str(exc_info.value).lower()


def test_12_resource_cleanup_and_stream_rewind():
    """Test 12: Stream-like objects remain valid and rewound after processing."""
    pdf_bytes = build_pdf_bytes(["Test stream safety text."])
    stream = io.BytesIO(pdf_bytes)

    # First extraction
    res1 = extract_pdf(stream, filename="stream_test.pdf")
    assert res1["extraction_status"] == "success"

    # Stream should be rewound to position 0 and reusable
    assert stream.tell() == 0
    res2 = extract_pdf(stream, filename="stream_test.pdf")
    assert res2["extraction_status"] == "success"


def test_13_file_path_input(tmp_path):
    """Test 13: Local file path (str and Path) is supported without disk modification."""
    pdf_bytes = build_pdf_bytes(["Local filesystem court judgment test."])
    temp_pdf_path = tmp_path / "bench_order.pdf"
    temp_pdf_path.write_bytes(pdf_bytes)

    # Pass as Path object
    res_path = extract_pdf(temp_pdf_path, filename="bench_order.pdf")
    assert res_path["page_count"] == 1
    assert "filesystem court judgment" in res_path["pages"][0]["text"]

    # Pass as str
    res_str = extract_pdf(str(temp_pdf_path), filename="bench_order.pdf")
    assert res_str["page_count"] == 1

    # Verify original file was not altered
    assert temp_pdf_path.read_bytes() == pdf_bytes


def test_14_paragraph_and_line_break_preservation():
    """Test 14: Natural paragraph spacing (\n\n) is preserved for downstream AI processing."""
    multiline_text = (
        "Paragraph 1: The prosecution case is founded upon circumstantial evidence.\n\n"
        "Paragraph 2: The chain of circumstances must be unbroken and cogently established.\n\n"
        "Paragraph 3: Applying Sharad Birdhichand Sarda v. State of Maharashtra, the appeal is allowed."
    )
    pdf_bytes = build_pdf_bytes([multiline_text])

    result = extract_pdf(pdf_bytes, filename="precedents.pdf")
    extracted = result["pages"][0]["text"]

    assert "Paragraph 1" in extracted
    assert "Paragraph 2" in extracted
    assert "Paragraph 3" in extracted
    # Ensure line breaks or paragraphs exist in the extracted string
    assert "\n" in extracted


def test_15_zero_page_pdf_rejection():
    """Test 15: Document with 0 pages is rejected with PDFNoPagesError."""
    # Synthesize valid PDF bytes defining a document with an empty page tree (0 pages)
    zero_page_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
        b"xref\n0 3\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n"
        b"trailer\n<< /Size 3 /Root 1 0 R >>\nstartxref\n115\n%%EOF"
    )

    with pytest.raises(PDFNoPagesError) as exc_info:
        extract_pdf(zero_page_bytes, filename="empty_pages.pdf")

    assert "contains 0 pages" in str(exc_info.value)


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
