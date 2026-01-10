from app.llm.azure_client import chat_completion


def answer_node(state):
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
