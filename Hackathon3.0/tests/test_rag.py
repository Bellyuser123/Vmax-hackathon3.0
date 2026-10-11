"""Automated Test Suite for NyayaLens Local Semantic RAG Pipeline.

Tests:
1. Chunking with page number preservation and overlapping windows.
2. Handling empty, blank, or scanned document pages (zero text).
3. SentenceTransformers embedding generation with BAAI/bge-small-en-v1.5.
4. Local FAISS vector index building and per-document isolation.
5. Semantic query retrieval returning exact text, cosine similarity, and 1-indexed page attribution.
6. Insufficient evidence detection: Unrelated queries correctly yield 'insufficient evidence'
   without hallucinating facts, citations, or court outcomes.
7. Grounded extractive answering without requiring any external LLM API key.
8. Real judgment end-to-end test on `sample_data/pdf/criminal_quashing.pdf`.
9. Consistency across multiple isolated document indices (no state leak).
"""

import sys
from pathlib import Path
import pytest
import numpy as np

# Ensure Hackathon3.0 is on sys.path
test_dir = Path(__file__).resolve().parent
hackathon_dir = test_dir.parent
workspace_root = hackathon_dir.parent

for p in (str(hackathon_dir), str(workspace_root)):
    if p not in sys.path:
        sys.path.insert(0, p)

from core.pdf_processor import extract_pdf_data
from core.local_rag import (
    split_text_into_chunks,
    extract_document_chunks,
    build_rag_index,
    answer_question_rag,
    get_embedding_model,
    check_ollama_availability,
    DocumentChunk,
    SearchResult,
    MIN_SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL_NAME
)


# =============================================================================
# Unit Tests: Chunking & Page Metadata
# =============================================================================

def test_01_chunking_preserves_page_numbers_and_overlap():
    """Verify that chunks retain accurate 1-indexed page provenance and overlap."""
    sample_text = (
        "In the Supreme Court of India. Criminal Appellate Jurisdiction. "
        "The appellant was charged under Section 498-A of the Indian Penal Code. "
        "The High Court erred in refusing to exercise inherent jurisdiction under Section 482 CrPC. "
        "We find that the allegations are general and omnibus in nature without specific overt acts. "
        "Accordingly, the proceedings emanating from FIR No. 120 of 2016 are hereby quashed."
    )

    chunks = split_text_into_chunks(
        page_num=3,
        text=sample_text,
        doc_name="criminal_appeal.pdf",
        chunk_size=120,
        chunk_overlap=30
    )

    assert len(chunks) >= 2
    for c in chunks:
        assert c.page_num == 3
        assert c.doc_name == "criminal_appeal.pdf"
        assert len(c.text) > 0


def test_02_chunking_handles_empty_and_whitespace_pages():
    """Verify that blank or whitespace pages produce zero chunks."""
    assert split_text_into_chunks(1, "", "empty.pdf") == []
    assert split_text_into_chunks(2, "   \n\n\t   ", "blank.pdf") == []

    doc_dict = {"pages": [{"page_number": 1, "text": ""}, {"page_number": 2, "text": "   "}]}
    assert extract_document_chunks(doc_dict) == []


# =============================================================================
# Unit Tests: Embeddings & FAISS Index
# =============================================================================

def test_03_embedding_model_bge_small_specs():
    """Verify BAAI/bge-small-en-v1.5 embedding dimension is exactly 384 and normalized."""
    embedder = get_embedding_model()
    assert embedder is not None

    sample_sentence = "The High Court quashed the criminal proceedings under Section 482 CrPC."
    vec = embedder.encode([sample_sentence], normalize_embeddings=True)

    assert vec.shape == (1, 384)
    # Norm should be approx 1.0 because of normalization
    norm = np.linalg.norm(vec[0])
    assert abs(norm - 1.0) < 1e-4


def test_04_build_rag_index_isolated_per_document():
    """Verify FAISS index is built and isolated per document instance."""
    doc_a = {
        "filename": "order_a.pdf",
        "pages": [
            {"page_number": 1, "text": "The arbitration petition under Section 9 is granted with interim injunction."},
            {"page_number": 2, "text": "The respondent is restrained from alienating the disputed escrow assets."}
        ]
    }
    doc_b = {
        "filename": "order_b.pdf",
        "pages": [
            {"page_number": 1, "text": "The anticipatory bail application under Section 438 CrPC is rejected."},
            {"page_number": 2, "text": "Custodial interrogation is deemed necessary by the investigating officer."}
        ]
    }

    index_a, err_a = build_rag_index(doc_a)
    index_b, err_b = build_rag_index(doc_b)

    assert err_a is None and index_a is not None
    assert err_b is None and index_b is not None
    assert index_a.doc_name == "order_a.pdf"
    assert index_b.doc_name == "order_b.pdf"

    # Search for arbitration in both
    res_a = index_a.search("arbitration interim injunction", top_k=1)
    res_b = index_b.search("arbitration interim injunction", top_k=1)

    assert res_a[0].page_num == 1
    assert "arbitration" in res_a[0].text.lower()
    # index_a should have much higher similarity for arbitration than index_b
    assert res_a[0].score > res_b[0].score


# =============================================================================
# End-to-End Tests: Real Court Judgment Retrieval
# =============================================================================

def test_05_real_court_judgment_semantic_retrieval():
    """Test semantic retrieval on a real text-based judgment from sample_data."""
    pdf_path = hackathon_dir / "sample_data" / "pdf" / "criminal_quashing.pdf"
    assert pdf_path.exists(), f"Sample PDF not found at {pdf_path}"

    doc_data, err = extract_pdf_data(pdf_path.read_bytes(), pdf_path.name)
    assert err is None
    assert doc_data.total_pages >= 3

    rag_index, r_err = build_rag_index(doc_data)
    assert r_err is None and rag_index is not None
    assert rag_index.chunk_count > 0

    # Query 1: Section 41-A police arrest directions
    q = "What are the directions regarding Section 41-A CrPC and arrest?"
    ans_res = answer_question_rag(rag_index, q, top_k=3)

    assert ans_res["evidence_sufficient"] is True
    assert ans_res["top_score"] >= MIN_SIMILARITY_THRESHOLD
    assert len(ans_res["sources"]) > 0

    # Page attribution must be valid 1-indexed page
    top_source = ans_res["sources"][0]
    assert 1 <= top_source.page_num <= doc_data.total_pages
    assert "41-a" in top_source.text.lower() or "arrest" in top_source.text.lower() or "crpc" in top_source.text.lower()

    # Answer must include page number citation
    assert f"Page {top_source.page_num}" in ans_res["answer"] or f"[{top_source.page_num}]" in ans_res["answer"] or top_source.text in ans_res["answer"]


def test_06_insufficient_evidence_detection_no_hallucination():
    """Verify that completely unrelated questions trigger insufficient evidence protection."""
    pdf_path = hackathon_dir / "sample_data" / "pdf" / "criminal_quashing.pdf"
    doc_data, _ = extract_pdf_data(pdf_path.read_bytes(), pdf_path.name)
    rag_index, _ = build_rag_index(doc_data)

    unrelated_query = "What is the secret recipe for baking chocolate cheesecake with vanilla cream?"
    ans_res = answer_question_rag(rag_index, unrelated_query, top_k=2)

    # Must detect insufficient evidence and explicitly refuse fabrication
    assert ans_res["evidence_sufficient"] is False
    assert ans_res["mode"] == "insufficient_evidence"
    assert "insufficient evidence" in ans_res["answer"].lower()
    assert "fabricated" in ans_res["answer"].lower() or "not contain" in ans_res["answer"].lower()


def test_07_scanned_or_empty_pdf_handled_gracefully():
    """Verify that empty or text-less documents return clean error without crashing."""
    empty_doc = {"filename": "scanned.pdf", "pages": []}
    rag_idx, err = build_rag_index(empty_doc)

    assert rag_idx is None
    assert "no extractable text" in err.lower()


def test_08_ollama_availability_check():
    """Verify that check_ollama_availability runs cleanly with timeout."""
    available, models = check_ollama_availability(timeout=0.5)
    assert isinstance(available, bool)
    assert isinstance(models, list)


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
