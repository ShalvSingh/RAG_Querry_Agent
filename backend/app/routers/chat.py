"""Endpoint for asking questions about an ingested document."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import AskRequest, AskResponse, SourceChunk
from app.services.ingestion_service import vectorstore_exists
from app.services.rag_service import answer_question

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    """Answer a question grounded in the specified document's content."""
    if not vectorstore_exists(request.doc_id):
        raise HTTPException(status_code=404, detail="Document not found. Upload it first.")

    try:
        result = answer_question(request.doc_id, request.question)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return AskResponse(
        answer=result["answer"],
        sources=[SourceChunk(**s) for s in result["sources"]],
    )
