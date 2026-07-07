# RAG Chatbot — FastAPI + React

A document Q&A app: upload a PDF, it gets chunked/embedded/stored, and questions
are answered strictly from the retrieved content using Groq's LLM — with source
page numbers returned so you can verify every answer.

## Project structure

```
rag-chatbot/
├── backend/            FastAPI app (ingestion, vectorstore, RAG, API)
└── frontend/            React (Vite) app
```

## 1. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and paste your real GROQ_API_KEY

uvicorn app.main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`. Check `http://localhost:8000/health`.

## 2. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## How it fixes the hallucination problem

- **Custom grounded prompt** (`backend/app/services/rag_service.py`): the model
  is instructed to answer only from retrieved context and to say
  *"I couldn't find this in the document"* when the answer isn't there,
  instead of guessing.
- **Per-document vectorstores**: every upload gets its own persisted Chroma
  collection (`backend/storage/vectorstores/<doc_id>`), so you're never
  accidentally querying stale or wrong data.
- **Larger chunk overlap** (150, up from 10): reduces facts getting cut off
  at chunk boundaries.
- **Source citations returned to the frontend**: every answer shows which
  page(s) and snippet it was grounded in, so hallucination is visible
  immediately instead of hidden.
- **No more double-invoke bug**: the old code called the chain twice and
  rendered the raw result dict instead of the answer string. This version
  returns a clean `{answer, sources}` JSON from a single call.

## Extending this

- Swap Chroma for a hosted vector DB (Pinecone, Qdrant) if you need this
  running across multiple machines/deployments.
- Add a `DELETE /documents/{doc_id}` endpoint plus a "remove file" button
  if you want document management.
- Add streaming responses (`ChatGroq(streaming=True)` + SSE) if you want
  the answer to type out live instead of arriving all at once.
