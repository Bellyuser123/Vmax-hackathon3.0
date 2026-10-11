"""Core package for NyayaLens."""

from .local_rag import (
    LocalRAGIndex,
    DocumentChunk,
    SearchResult,
    build_rag_index,
    answer_question_rag,
    extract_document_chunks,
    check_ollama_availability,
    get_embedding_model
)

__all__ = [
    "LocalRAGIndex",
    "DocumentChunk",
    "SearchResult",
    "build_rag_index",
    "answer_question_rag",
    "extract_document_chunks",
    "check_ollama_availability",
    "get_embedding_model"
]
