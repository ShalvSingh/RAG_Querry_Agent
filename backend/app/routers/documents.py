"""Endpoints for uploading and listing PDF documents."""

import json
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app.config import MAX_UPLOAD_MB, UPLOADS_DIR
from app.models.schemas import DocumentInfo, UploadResponse
from app.services.ingestion_service import ingest_pdf

router = APIRouter(prefix="/documents", tags=["documents"])

_REGISTRY_PATH = UPLOADS_DIR.parent / "documents.json"


def _load_registry() -> dict:
    if _REGISTRY_PATH.exists():
        return json.loads(_REGISTRY_PATH.read_text())
    return {}


def _save_registry(registry: dict) -> None:
    _REGISTRY_PATH.write_text(json.dumps(registry, indent=2))


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile) -> UploadResponse:
    """Accept a PDF upload, ingest it, and persist its vectorstore."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_UPLOAD_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f} MB). Max is {MAX_UPLOAD_MB} MB.",
        )

    doc_id = uuid.uuid4().hex[:12]
    saved_path: Path = UPLOADS_DIR / f"{doc_id}.pdf"
    saved_path.write_bytes(contents)

    try:
        num_chunks = ingest_pdf(saved_path, doc_id)
    except Exception as exc:
        saved_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {exc}")

    doc_info = DocumentInfo(doc_id=doc_id, filename=file.filename, num_chunks=num_chunks)

    registry = _load_registry()
    registry[doc_id] = doc_info.model_dump()
    _save_registry(registry)

    return UploadResponse(document=doc_info, message="Document processed successfully.")


@router.get("", response_model=list[DocumentInfo])
async def list_documents() -> list[DocumentInfo]:
    """Return all previously uploaded documents."""
    registry = _load_registry()
    return [DocumentInfo(**info) for info in registry.values()]
