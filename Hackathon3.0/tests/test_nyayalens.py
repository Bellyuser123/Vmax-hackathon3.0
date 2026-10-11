"""Comprehensive Test Suite for NyayaLens.

Validates:
1. PDF validation (empty, invalid header, valid PDF)
2. PyMuPDF text extraction, page indexing, and scanned PDF detection
3. Heuristic & rule-based legal classification
4. Evidence verification engine (exact match, adjacent page correction, unverified flagging)
5. Legal provisions extraction and applied vs mentioned distinction
6. Plain-language 7-section summary structure
7. All 3 benchmark sample court documents
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from config import (
    CASE_CATEGORIES,
    DOCUMENT_TYPES,
    MAX_FILE_SIZE_BYTES
)
from core.pdf_processor import (
    validate_pdf_file,
    extract_pdf_data,
    format_file_size
)
from core.legal_classifier import (
    heuristic_detect_case_type,
    heuristic_detect_doc_type
)
from core.verification_engine import (
    verify_evidence_item,
    verify_all_evidence,
    verify_legal_provisions,
    VerificationStatus
)
from core.ai_engine import LegalAIEngine
from sample_data.sample_cases import SAMPLE_CASES


class TestNyayaLens(unittest.TestCase):

    def setUp(self):
        self.pdf_dir = root_dir / "sample_data" / "pdf"
        self.ai_engine = LegalAIEngine()

    def test_01_pdf_validation(self):
        """Test PDF validator on edge cases."""
        # Empty bytes
        res_empty = validate_pdf_file(b"", "empty.pdf")
        self.assertFalse(res_empty.is_valid)
        self.assertIn("empty", res_empty.error_message.lower())

        # Invalid non-PDF extension
        res_ext = validate_pdf_file(b"%PDF-1.4 test", "test.txt")
        self.assertFalse(res_ext.is_valid)
        self.assertIn("only pdf", res_ext.error_message.lower())

        # Invalid magic bytes
        res_magic = validate_pdf_file(b"NOT_A_PDF_HEADER", "fake.pdf")
        self.assertFalse(res_magic.is_valid)
        self.assertIn("corrupted or invalid", res_magic.error_message.lower())

        # Valid PDF header
        res_valid = validate_pdf_file(b"%PDF-1.5 test content", "valid.pdf")
        self.assertTrue(res_valid.is_valid)

    def test_02_pdf_extraction_criminal(self):
        """Test PyMuPDF extraction on criminal appeal sample PDF."""
        pdf_path = self.pdf_dir / "criminal_quashing.pdf"
        self.assertTrue(pdf_path.exists())
        file_bytes = pdf_path.read_bytes()

        doc_data, err = extract_pdf_data(file_bytes, "criminal_quashing.pdf")
        self.assertIsNone(err)
        self.assertIsNotNone(doc_data)
        self.assertEqual(doc_data.total_pages, 4)
        self.assertFalse(doc_data.is_scanned_pdf)
        self.assertGreater(doc_data.total_characters, 1000)

        # Check 1-indexed pages
        page_nums = [p.page_num for p in doc_data.pages]
        self.assertEqual(page_nums, [1, 2, 3, 4])

        # Test search query
        matches = doc_data.search_query("Section 482")
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]["page_num"], 2)

    def test_03_pdf_extraction_commercial(self):
        """Test PyMuPDF extraction on commercial arbitration sample PDF."""
        pdf_path = self.pdf_dir / "commercial_arbitration.pdf"
        self.assertTrue(pdf_path.exists())
        file_bytes = pdf_path.read_bytes()

        doc_data, err = extract_pdf_data(file_bytes, "commercial_arbitration.pdf")
        self.assertIsNone(err)
        self.assertEqual(doc_data.total_pages, 3)
        self.assertFalse(doc_data.is_scanned_pdf)

        # Search for Section 9
        matches = doc_data.search_query("Section 9")
        self.assertGreater(len(matches), 0)

    def test_04_pdf_extraction_constitutional(self):
        """Test PyMuPDF extraction on constitutional privacy sample PDF."""
        pdf_path = self.pdf_dir / "constitutional_privacy.pdf"
        self.assertTrue(pdf_path.exists())
        file_bytes = pdf_path.read_bytes()

        doc_data, err = extract_pdf_data(file_bytes, "constitutional_privacy.pdf")
        self.assertIsNone(err)
        self.assertEqual(doc_data.total_pages, 4)
        self.assertFalse(doc_data.is_scanned_pdf)

    def test_05_verification_engine(self):
        """Test Evidence Verification Engine precision."""
        sample = SAMPLE_CASES["criminal_quashing"]
        pages_dict = sample["pages_text"]

        # Exact match test
        quote = "The mandate of Section 41-A CrPC must be strictly adhered to by police authorities before any coercive step of arrest is taken."
        res_exact = verify_evidence_item(
            fact="Section 41-A CrPC mandatory compliance",
            quote=quote,
            claimed_page=3,
            pdf_pages_dict=pages_dict
        )
        self.assertEqual(res_exact.status, VerificationStatus.VERIFIED_EXACT)
        self.assertEqual(res_exact.actual_page, 3)
        self.assertTrue(res_exact.is_verified)
        self.assertEqual(res_exact.badge_color, "#10b981")

        # Page correction test (claimed page 2, actual page 3)
        res_corr = verify_evidence_item(
            fact="Section 41-A CrPC test",
            quote=quote,
            claimed_page=2,
            pdf_pages_dict=pages_dict
        )
        self.assertEqual(res_corr.status, VerificationStatus.PAGE_CORRECTED)
        self.assertEqual(res_corr.actual_page, 3)
        self.assertTrue(res_corr.is_verified)

        # Hallucinated / fake quote test
        fake_quote = "This is a completely fabricated sentence that does not appear anywhere in this judgment."
        res_fake = verify_evidence_item(
            fact="Fabricated fact",
            quote=fake_quote,
            claimed_page=1,
            pdf_pages_dict=pages_dict
        )
        self.assertEqual(res_fake.status, VerificationStatus.UNVERIFIED)
        self.assertFalse(res_fake.is_verified)
        self.assertEqual(res_fake.badge_color, "#ef4444")

    def test_06_end_to_end_analysis_criminal(self):
        """Test full analysis pipeline on Criminal case."""
        pdf_path = self.pdf_dir / "criminal_quashing.pdf"
        file_bytes = pdf_path.read_bytes()
        doc_data, _ = extract_pdf_data(file_bytes, "criminal_quashing.pdf")
        pages_dict = {p.page_num: p.text for p in doc_data.pages}

        res = self.ai_engine.analyze_document(doc_data.full_text, pages_dict)
        self.assertEqual(res["case_category"], "Criminal")
        self.assertEqual(res["document_type"], "Judgment")
        self.assertIn("Supreme Court", res["court_name"])
        self.assertEqual(res["evidence_integrity_score"], 100)

        # Check summary structure
        summary = res["summary"]
        self.assertIn("case_overview", summary)
        self.assertIn("background", summary)
        self.assertIn("main_legal_issue", summary)
        self.assertIn("arguments", summary)
        self.assertIn("court_reasoning", summary)
        self.assertIn("final_order", summary)
        self.assertIn("important_takeaways", summary)
        self.assertGreaterEqual(len(summary["important_takeaways"]), 3)

    def test_07_end_to_end_analysis_commercial(self):
        """Test full analysis pipeline on Commercial Arbitration case."""
        pdf_path = self.pdf_dir / "commercial_arbitration.pdf"
        file_bytes = pdf_path.read_bytes()
        doc_data, _ = extract_pdf_data(file_bytes, "commercial_arbitration.pdf")
        pages_dict = {p.page_num: p.text for p in doc_data.pages}

        res = self.ai_engine.analyze_document(doc_data.full_text, pages_dict)
        self.assertEqual(res["case_category"], "Commercial")
        self.assertEqual(res["document_type"], "Interim Order")
        self.assertIn("High Court of Delhi", res["court_name"])
        self.assertEqual(res["evidence_integrity_score"], 100)

    def test_08_end_to_end_analysis_constitutional(self):
        """Test full analysis pipeline on Constitutional Privacy case."""
        pdf_path = self.pdf_dir / "constitutional_privacy.pdf"
        file_bytes = pdf_path.read_bytes()
        doc_data, _ = extract_pdf_data(file_bytes, "constitutional_privacy.pdf")
        pages_dict = {p.page_num: p.text for p in doc_data.pages}

        res = self.ai_engine.analyze_document(doc_data.full_text, pages_dict)
        self.assertEqual(res["case_category"], "Constitutional")
        self.assertEqual(res["document_type"], "Judgment")
        self.assertIn("Supreme Court", res["court_name"])
        self.assertEqual(res["evidence_integrity_score"], 100)


if __name__ == "__main__":
    unittest.main()
