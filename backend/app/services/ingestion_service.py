"""Handles turning an uploaded PDF into a persisted, queryable vectorstore.

Each document gets its own Chroma collection on disk, keyed by doc_id, so
multiple uploaded PDFs can coexist and be queried independently. This is the
piece the original app was missing entirely (it only ever read one hardcoded
ML.pdf).
"""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_OVERLAP, CHUNK_SIZE, EMBEDDING_MODEL, VECTORSTORES_DIR

_embeddings = None


def get_embeddings() -> HuggingFaceEmbeddings:
    """Lazily construct a single shared embeddings model instance."""
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def ingest_pdf(file_path: Path, doc_id: str) -> int:
    """Load a PDF, split it into chunks, embed it, and persist a Chroma store.

    Args:
        file_path: Path to the saved PDF file on disk.
        doc_id: Unique identifier for this document's vectorstore collection.

    Returns:
        The number of chunks created and stored.
    """
    loader = PyPDFLoader(str(file_path))
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(pages)

    persist_dir = str(VECTORSTORES_DIR / doc_id)
    Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=persist_dir,
        collection_name=doc_id,
    )
    return len(chunks)


def load_vectorstore(doc_id: str) -> Chroma:
    """Load a previously persisted vectorstore for a given document."""
    persist_dir = str(VECTORSTORES_DIR / doc_id)
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=get_embeddings(),
        collection_name=doc_id,
    )


def vectorstore_exists(doc_id: str) -> bool:
    """Check whether a persisted vectorstore exists for this doc_id."""
    return (VECTORSTORES_DIR / doc_id).exists()
