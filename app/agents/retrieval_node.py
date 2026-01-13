from app.vector_store import search_similar_chunks
from app.agents.state import AgentState

def retrieval_node(state: AgentState) -> AgentState:
    chunks = search_similar_chunks(
        state["question"],
        state["owner_id"],
        top_k=5
    )
    
    state["retrieved_chunks"] = chunks
    print(f"Retrieved {len(chunks)} chunks for answer generation")
    return state
