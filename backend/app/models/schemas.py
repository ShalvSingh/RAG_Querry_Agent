"""Request and response models for the API."""

from pydantic import BaseModel


class DocumentInfo(BaseModel):
    doc_id: str
    filename: str
    num_chunks: int


class UploadResponse(BaseModel):
    document: DocumentInfo
    message: str


class AskRequest(BaseModel):
    doc_id: str
    question: str


class SourceChunk(BaseModel):
    page: int | None = None
    snippet: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
