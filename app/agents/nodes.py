from app.agents.intent_classifier import classify_intent
from app.vector_store import search_documents
from app.llm.azure_client import chat_completion
from app.agents.state import AgentState
from app.models.document import Document
from app.database import SessionLocal


def intent_node(state: AgentState) -> AgentState:
    intent = classify_intent(state["question"])
    state["intent"] = intent
    return state


def retrieval_node(state: AgentState) -> AgentState:
    doc_ids = search_documents(state["question"], top_k=3)

    db = SessionLocal()
    docs = db.query(Document).filter(Document.id.in_(doc_ids)).all()
    db.close()

    state["documents"] = [doc.content for doc in docs]
    return state


def answer_node(state: AgentState) -> AgentState:
    context = "\n\n".join(state.get("documents", []))

    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{state['question']}
"""

    answer = chat_completion([prompt])
    state["answer"] = answer
    return state
