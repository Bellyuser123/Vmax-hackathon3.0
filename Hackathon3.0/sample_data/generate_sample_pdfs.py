"""Generates genuine multipage PDF files for the sample cases using PyMuPDF (fitz).

These PDFs are saved into sample_data/pdf/ so users can either:
1. Directly load them with 1-click in the UI, or
2. Download them and test the upload & extraction workflow.
"""

import sys
from pathlib import Path

# Ensure root dir is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

try:
    import pymupdf as fitz
except ImportError:
    import fitz

from sample_data.sample_cases import SAMPLE_CASES

PDF_OUTPUT_DIR = Path(__file__).resolve().parent / "pdf"


def generate_all_sample_pdfs() -> None:
    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for case_id, case_data in SAMPLE_CASES.items():
        doc = fitz.open()  # create new blank PDF
        pages_dict = case_data.get("pages_text", {})

        for p_num in sorted(pages_dict.keys()):
            text = pages_dict[p_num]
            # Standard A4: 595.28 x 841.89 points
            page = doc.new_page(width=595, height=842)

            # Insert Header Banner
            header_rect = fitz.Rect(50, 30, 545, 55)
            page.draw_rect(header_rect, color=(0.85, 0.88, 0.92), fill=(0.95, 0.96, 0.98))
            page.insert_text(
                fitz.Point(60, 48),
                f"NYAYALENS BENCH DOCUMENT ARCHIVE  |  PAGE {p_num} OF {len(pages_dict)}",
                fontsize=8,
                color=(0.2, 0.3, 0.4)
            )

            # Insert Main Document Text Box
            content_rect = fitz.Rect(50, 70, 545, 800)
            page.insert_textbox(
                content_rect,
                text,
                fontsize=10.5,
                fontname="helv",
                color=(0.05, 0.05, 0.05)
            )

        pdf_path = PDF_OUTPUT_DIR / f"{case_id}.pdf"
        doc.save(str(pdf_path))
        doc.close()
        print(f"Generated sample PDF: {pdf_path} ({len(pages_dict)} pages)")


if __name__ == "__main__":
    generate_all_sample_pdfs()
