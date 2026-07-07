"""Retrieval-augmented answering, deliberately constrained to reduce hallucination.

Two things do the heavy lifting here:
1. A strict prompt that forbids the model from using outside knowledge and
   gives it an explicit, easy "I don't know" escape hatch.
2. Returning the actual source chunks used, so the answer is auditable
   instead of a black box.
"""

from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL, RETRIEVER_K
from app.services.ingestion_service import load_vectorstore

from pydantic import SecretStr

GROUNDED_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a document assistant. Answer the question using ONLY the
context below, which was extracted from the user's uploaded document.

Rules:
- Do not use any knowledge from outside the context, even if you know the answer.
- If the context does not contain enough information to answer, respond exactly:
  "I couldn't find this in the document."
- Do not guess, speculate, or fill in gaps.
- Keep the answer concise and directly grounded in the context.

Context:
{context}

Question: {question}

Answer:""",
)


def _get_llm() -> ChatGroq:
    if not GROQ_API_KEY:
        raise RuntimeError("Missing GROQ_API_KEY. Set it in backend/.env before running.")
    return ChatGroq(model=GROQ_MODEL, api_key=SecretStr(GROQ_API_KEY), temperature=0)


def answer_question(doc_id: str, question: str) -> dict:
    """Run a grounded retrieval-QA pass over a document and return the result.

    Args:
        doc_id: Identifier of the previously ingested document.
        question: The user's question.

    Returns:
        A dict with "answer" (str) and "sources" (list of {page, snippet}).
    """
    vectorstore = load_vectorstore(doc_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})

    chain = RetrievalQA.from_chain_type(
        llm=_get_llm(),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": GROUNDED_PROMPT},
        return_source_documents=True,
    )

    result = chain.invoke({"query": question})

    sources = []
    for doc in result.get("source_documents", []):
        sources.append(
            {
                "page": doc.metadata.get("page"),
                "snippet": doc.page_content[:250].strip(),
            }
        )

    return {"answer": result["result"], "sources": sources}
