from app.vector_store import search_documents


def retrieval_node(state):
    query = state["question"]

    results = search_documents(query, top_k=5)

    # Store ONLY chunk text
    state["documents"] = [chunk["text"] for chunk in results]

    return state
