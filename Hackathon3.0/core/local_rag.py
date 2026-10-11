"""Local RAG Pipeline for NyayaLens using sentence-transformers and FAISS.

Key Features:
1. Sentence-transformers embeddings using 'BAAI/bge-small-en-v1.5' (384 dimensions).
2. Local FAISS (IndexFlatIP) for fast, memory-safe semantic similarity search.
3. Isolated per-document / per-session indexing (no shared state, zero disk leaks).
4. Page-level attribution: Every chunk preserves 1-indexed page metadata.
5. Strict anti-hallucination guard: If retrieved evidence is below similarity threshold,
   it explicitly reports insufficient evidence.
6. Optional Ollama integration: If an Ollama model is available locally, it generates
   grounded answers restricted strictly to retrieved passages. Otherwise, provides
   faithful extractive answers directly from the verbatim text.
7. Zero external LLM APIs (no Gemini/OpenAI required). 100% offline-capable.
"""

import re
import os
import json
import logging
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

logger = logging.getLogger("nyayalens.local_rag")

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384
DEFAULT_CHUNK_SIZE_CHARS = 650
DEFAULT_CHUNK_OVERLAP_CHARS = 150
MIN_SIMILARITY_THRESHOLD = 0.52  # Cosine similarity threshold for relevance on bge-small

# Global cache for the embedding model to avoid reloading weights per query
_CACHED_EMBEDDER: Optional[Any] = None


@dataclass
class DocumentChunk:
    """Represents a text passage with document and page provenance."""
    chunk_id: int
    page_num: int  # 1-indexed
    text: str
    doc_name: str
    char_count: int


@dataclass
class SearchResult:
    """Represents a retrieved passage with similarity score."""
    chunk_id: int
    page_num: int
    text: str
    score: float
    doc_name: str
    is_sufficient: bool


def get_embedding_model(model_name: str = EMBEDDING_MODEL_NAME) -> Any:
    """Load and cache the sentence-transformers embedding model.

    Attempts local cache first, falling back to download if needed.
    """
    global _CACHED_EMBEDDER
    if _CACHED_EMBEDDER is not None:
        return _CACHED_EMBEDDER

    if SentenceTransformer is None:
        raise ImportError(
            "sentence-transformers is not installed. Run `pip install sentence-transformers`."
        )

    try:
        # Try local cache first
        _CACHED_EMBEDDER = SentenceTransformer(model_name, local_files_only=True)
    except Exception:
        # Fall back to standard load
        _CACHED_EMBEDDER = SentenceTransformer(model_name)

    return _CACHED_EMBEDDER


# =============================================================================
# CHUNKING WITH PAGE METADATA
# =============================================================================

def split_text_into_chunks(
    page_num: int,
    text: str,
    doc_name: str,
    start_chunk_id: int = 0,
    chunk_size: int = DEFAULT_CHUNK_SIZE_CHARS,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS
) -> List[DocumentChunk]:
    """Split page text into overlapping windows while preserving page numbers.

    Attempts to break along paragraph or sentence boundaries where possible.
    """
    cleaned = text.strip()
    if not cleaned:
        return []

    # If text is smaller than chunk size, return single chunk
    if len(cleaned) <= chunk_size:
        return [
            DocumentChunk(
                chunk_id=start_chunk_id,
                page_num=page_num,
                text=cleaned,
                doc_name=doc_name,
                char_count=len(cleaned)
            )
        ]

    chunks: List[DocumentChunk] = []
    current_idx = 0
    total_len = len(cleaned)
    cid = start_chunk_id

    while current_idx < total_len:
        end_idx = min(current_idx + chunk_size, total_len)
        candidate = cleaned[current_idx:end_idx]

        # If not at the end of text, try breaking on sentence or paragraph boundary
        if end_idx < total_len:
            # Look for paragraph break (\n\n) or sentence period (. ) near the end
            last_para = candidate.rfind("\n\n")
            last_period = candidate.rfind(". ")
            last_newline = candidate.rfind("\n")

            break_point = -1
            if last_para > chunk_size // 2:
                break_point = last_para + 2
            elif last_period > chunk_size // 2:
                break_point = last_period + 2
            elif last_newline > chunk_size // 2:
                break_point = last_newline + 1

            if break_point != -1:
                candidate = candidate[:break_point]
                end_idx = current_idx + break_point

        chunk_text = candidate.strip()
        if chunk_text:
            chunks.append(
                DocumentChunk(
                    chunk_id=cid,
                    page_num=page_num,
                    text=chunk_text,
                    doc_name=doc_name,
                    char_count=len(chunk_text)
                )
            )
            cid += 1

        # Advance with overlap
        if end_idx >= total_len:
            break
        current_idx = max(current_idx + 1, end_idx - chunk_overlap)

    return chunks


def extract_document_chunks(
    doc_data: Any,
    chunk_size: int = DEFAULT_CHUNK_SIZE_CHARS,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS
) -> List[DocumentChunk]:
    """Extract overlapping chunks from various document representations.

    Supports:
    - PDFDocumentData object (has doc_data.pages with .page_num and .text)
    - Dict with 'pages' list of {'page_number': int, 'text': str}
    - Dict of {page_num: text}
    """
    if doc_data is None:
        return []

    doc_name = getattr(doc_data, "file_name", "document.pdf")
    all_chunks: List[DocumentChunk] = []
    current_chunk_id = 0

    # Case A: PDFDocumentData object from core.pdf_processor
    if hasattr(doc_data, "pages") and isinstance(doc_data.pages, list):
        for page in doc_data.pages:
            p_num = getattr(page, "page_num", getattr(page, "page_number", 1))
            p_text = getattr(page, "text", "")
            if not p_text:
                continue
            chunks = split_text_into_chunks(
                page_num=p_num,
                text=p_text,
                doc_name=doc_name,
                start_chunk_id=current_chunk_id,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            all_chunks.extend(chunks)
            current_chunk_id += len(chunks)

    # Case B: Standard dictionary with 'pages' list
    elif isinstance(doc_data, dict) and "pages" in doc_data:
        doc_name = doc_data.get("filename", doc_name)
        for page in doc_data["pages"]:
            p_num = page.get("page_number", page.get("page_num", 1))
            p_text = page.get("text", "")
            if not p_text:
                continue
            chunks = split_text_into_chunks(
                page_num=p_num,
                text=p_text,
                doc_name=doc_name,
                start_chunk_id=current_chunk_id,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            all_chunks.extend(chunks)
            current_chunk_id += len(chunks)

    # Case C: Dictionary mapping page_num -> text
    elif isinstance(doc_data, dict):
        for p_num, p_text in sorted(doc_data.items(), key=lambda x: int(x[0]) if str(x[0]).isdigit() else 1):
            if not p_text:
                continue
            chunks = split_text_into_chunks(
                page_num=int(p_num) if str(p_num).isdigit() else 1,
                text=str(p_text),
                doc_name=doc_name,
                start_chunk_id=current_chunk_id,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            all_chunks.extend(chunks)
            current_chunk_id += len(chunks)

    return all_chunks


# =============================================================================
# FAISS ISOLATED VECTOR INDEX
# =============================================================================

class LocalRAGIndex:
    """Isolated, in-memory FAISS semantic index for a single document."""

    def __init__(
        self,
        doc_name: str,
        chunks: List[DocumentChunk],
        index: Any,
        dimension: int = EMBEDDING_DIM
    ):
        self.doc_name = doc_name
        self.chunks = chunks
        self.index = index
        self.dimension = dimension
        self.chunk_count = len(chunks)

    def search(
        self,
        query: str,
        top_k: int = 4,
        min_similarity: float = MIN_SIMILARITY_THRESHOLD
    ) -> List[SearchResult]:
        """Search for top_k relevant passages using cosine similarity.

        Returns exact text and source page number for each retrieved chunk.
        """
        cleaned_query = query.strip()
        if not cleaned_query or self.chunk_count == 0 or self.index is None:
            return []

        embedder = get_embedding_model()

        # BGE models recommend query prefix for retrieval
        prefixed_query = f"Represent this sentence for searching relevant passages: {cleaned_query}"
        query_vec = embedder.encode([prefixed_query], normalize_embeddings=True)
        query_vec = np.ascontiguousarray(query_vec, dtype=np.float32)

        k = min(top_k, self.chunk_count)
        distances, indices = self.index.search(query_vec, k)

        results: List[SearchResult] = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.chunks):
                continue
            score = float(dist)
            chunk = self.chunks[idx]
            results.append(
                SearchResult(
                    chunk_id=chunk.chunk_id,
                    page_num=chunk.page_num,
                    text=chunk.text,
                    score=round(score, 4),
                    doc_name=self.doc_name,
                    is_sufficient=(score >= min_similarity)
                )
            )

        return results


def build_rag_index(
    doc_data: Any,
    chunk_size: int = DEFAULT_CHUNK_SIZE_CHARS,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP_CHARS
) -> Tuple[Optional[LocalRAGIndex], Optional[str]]:
    """Build an isolated FAISS index from an uploaded document.

    Returns:
        (LocalRAGIndex, error_message)
    """
    if faiss is None:
        return None, "FAISS is not installed. Please run `pip install faiss-cpu`."

    if SentenceTransformer is None:
        return None, "sentence-transformers is not installed. Run `pip install sentence-transformers`."

    chunks = extract_document_chunks(doc_data, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if not chunks:
        return None, "Document contains no extractable text chunks to index (empty or scanned PDF)."

    doc_name = getattr(doc_data, "file_name", "document.pdf")
    if isinstance(doc_data, dict):
        doc_name = doc_data.get("filename", doc_name)

    try:
        embedder = get_embedding_model()
        texts = [c.text for c in chunks]

        # Batch encode with normalization for exact cosine similarity via inner product
        embeddings = embedder.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            normalize_embeddings=True
        )
        embeddings = np.ascontiguousarray(embeddings, dtype=np.float32)

        # Build FAISS inner product index
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)

        rag_index = LocalRAGIndex(
            doc_name=doc_name,
            chunks=chunks,
            index=index,
            dimension=dim
        )
        return rag_index, None

    except Exception as exc:
        logger.error("Failed to build FAISS index for '%s': %s", doc_name, exc)
        return None, f"Failed to build semantic index: {str(exc)}"


# =============================================================================
# OPTIONAL OLLAMA INTEGRATION (LOCAL INSTRUCTION MODEL)
# =============================================================================

def check_ollama_availability(timeout: float = 1.0) -> Tuple[bool, List[str]]:
    """Check if Ollama is running locally and return list of installed models."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
                return True, models
    except Exception:
        pass
    return False, []


def query_ollama(
    prompt: str,
    model_name: str,
    timeout: float = 30.0
) -> Optional[str]:
    """Generate a response using local Ollama instance."""
    try:
        payload = json.dumps({
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for factual precision
                "top_p": 0.9
            }
        }).encode("utf-8")

        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response", "").strip()
    except Exception as exc:
        logger.warning("Ollama query failed: %s", exc)
    return None


# =============================================================================
# EXTRACTIVE & GROUNDED ANSWER GENERATION
# =============================================================================

def _synthesize_extractive_answer(
    query: str,
    passages: List[SearchResult]
) -> str:
    """Generate a faithful extractive answer exclusively using retrieved text.

    Finds the most salient sentences in the retrieved passages that share
    key terms with the query, ensuring zero hallucinated claims.
    """
    query_terms = set(re.findall(r"\w+", query.lower())) - {
        "what", "is", "the", "in", "of", "and", "to", "a", "an", "was",
        "were", "did", "court", "judge", "held", "by", "for", "on", "with"
    }

    scored_sentences: List[Tuple[float, int, str]] = []

    for p in passages:
        sentences = re.split(r"(?<=[.!?])\s+", p.text)
        for s in sentences:
            clean_s = s.strip()
            if len(clean_s) < 20:
                continue
            words = set(re.findall(r"\w+", clean_s.lower()))
            overlap = len(words & query_terms)
            score = (overlap * 2.0) + (p.score * 1.5)
            scored_sentences.append((score, p.page_num, clean_s))

    # Sort sentences by relevance
    scored_sentences.sort(key=lambda x: x[0], reverse=True)

    if not scored_sentences or scored_sentences[0][0] < 1.0:
        # Return the top passage verbatim
        top = passages[0]
        return f"**Direct Passage from [Page {top.page_num}]:**\n\n> \"{top.text}\""

    # Take top 2-3 most relevant sentences
    top_picks = scored_sentences[:3]
    lines = []
    seen = set()
    for _, page_num, sent in top_picks:
        if sent in seen:
            continue
        seen.add(sent)
        lines.append(f"- **[Page {page_num}]:** \"{sent}\"")

    return "**Extractive Evidence Identified:**\n\n" + "\n".join(lines)


def answer_question_rag(
    rag_index: LocalRAGIndex,
    query: str,
    top_k: int = 4,
    min_similarity: float = MIN_SIMILARITY_THRESHOLD,
    use_ollama_if_available: bool = True,
    preferred_ollama_model: Optional[str] = None
) -> Dict[str, Any]:
    """End-to-end RAG answer pipeline.

    Guarantees:
    - Never uses Gemini or requires API keys.
    - If retrieved evidence is below threshold, clearly declares insufficient evidence.
    - If Ollama is available, optionally generates a grounded answer strictly constrained to context.
    - If Ollama is unavailable, presents extractive evidence directly.
    - Always returns exact passages with source page numbers.
    """
    # 1. Semantic retrieval with FAISS
    results = rag_index.search(query=query, top_k=top_k, min_similarity=min_similarity)

    # 2. Check evidence sufficiency
    if not results or not any(r.is_sufficient for r in results):
        top_score = results[0].score if results else 0.0
        return {
            "answer": (
                "⚠️ **Insufficient Evidence in Document:**\n\n"
                f"The retrieved passages yielded low semantic similarity ({top_score:.2f} < threshold {min_similarity:.2f}). "
                "The uploaded court document does not contain clear or verifiable facts addressing this question. "
                "Per NyayaLens judicial reliability rules, no facts, citations, or outcomes are fabricated."
            ),
            "sources": results,
            "mode": "insufficient_evidence",
            "model_used": None,
            "evidence_sufficient": False,
            "top_score": top_score
        }

    # Filter to sufficient passages for context
    sufficient_passages = [r for r in results if r.is_sufficient]

    # 3. Check for Ollama local instruction model
    ollama_ok, available_models = check_ollama_availability(timeout=1.0)
    selected_ollama = None
    if use_ollama_if_available and ollama_ok and available_models:
        if preferred_ollama_model and preferred_ollama_model in available_models:
            selected_ollama = preferred_ollama_model
        else:
            selected_ollama = available_models[0]

    # 4. Attempt Ollama generation if available
    if selected_ollama:
        context_blocks = []
        for p in sufficient_passages:
            context_blocks.append(f"[Page {p.page_num}]:\n{p.text}")
        context_str = "\n\n---\n\n".join(context_blocks)

        prompt = f"""You are a legal document assistant for NyayaLens. Answer the user question based STRICTLY and EXCLUSIVELY on the retrieved court document passages below.

Context Passages:
{context_str}

Question: {query}

Instructions:
1. Answer using ONLY the facts explicitly stated in the context passages above.
2. Explicitly cite the page number for every assertion (e.g. [Page 2]).
3. If the context passages do not contain enough evidence to answer, state: "Insufficient evidence in the retrieved passages to answer this question."
4. NEVER fabricate, extrapolate, or invent legal provisions, facts, or final court outcomes.

Answer:"""

        ollama_response = query_ollama(prompt, model_name=selected_ollama, timeout=25.0)
        if ollama_response:
            return {
                "answer": ollama_response,
                "sources": results,
                "mode": "local_ollama",
                "model_used": selected_ollama,
                "evidence_sufficient": True,
                "top_score": results[0].score
            }

    # 5. Extractive Answer Fallback (Fast, deterministic, zero hallucination)
    extractive_ans = _synthesize_extractive_answer(query, sufficient_passages)
    return {
        "answer": extractive_ans,
        "sources": results,
        "mode": "extractive",
        "model_used": None,
        "evidence_sufficient": True,
        "top_score": results[0].score
    }
